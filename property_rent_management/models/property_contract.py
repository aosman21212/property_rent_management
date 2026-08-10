from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PropertyContract(models.Model):
    _name = 'property.contract'
    _description = 'Rental Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Contract Reference', copy=False, readonly=True, default='New')
    property_id = fields.Many2one('property.property', string='Property', required=True, tracking=True)
    owner_id = fields.Many2one('property.owner', string='Owner',
                               related='property_id.owner_id', store=True, readonly=True)
    renter_id = fields.Many2one('property.renter', string='Renter', required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)

    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)
    rent_amount = fields.Monetary(string='Monthly Rent', currency_field='currency_id', tracking=True)
    deposit_amount = fields.Monetary(string='Security Deposit', currency_field='currency_id')
    payment_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly (3 months)'),
        ('biannual', 'Bi-Annual (6 months)'),
        ('yearly', 'Yearly'),
    ], string='Payment Frequency', default='monthly', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    payment_ids = fields.One2many('property.payment', 'contract_id', string='Payments')
    payment_count = fields.Integer(compute='_compute_payment_count', string='Payments')
    total_paid = fields.Monetary(compute='_compute_financials', string='Total Paid',
                                 currency_field='currency_id')
    total_due = fields.Monetary(compute='_compute_financials', string='Total Due',
                                currency_field='currency_id')

    note = fields.Html(string='Terms & Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('property.contract') or 'New'
        return super().create(vals_list)

    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    def _compute_financials(self):
        for rec in self:
            paid = sum(rec.payment_ids.filtered(lambda p: p.state == 'paid').mapped('amount'))
            due = sum(rec.payment_ids.filtered(lambda p: p.state in ('pending', 'late')).mapped('amount'))
            rec.total_paid = paid
            rec.total_due = due

    def action_activate(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft contracts can be activated.'))
            rec.state = 'active'
            rec.property_id.status = 'rented'
            # Generate scheduled payments
            rec._generate_payments()

    def action_expire(self):
        for rec in self:
            rec.state = 'expired'
            if rec.property_id.status == 'rented':
                rec.property_id.status = 'available'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'
            if rec.property_id.status == 'rented':
                rec.property_id.status = 'available'

    def action_reset_draft(self):
        for rec in self:
            if rec.state == 'cancelled':
                rec.state = 'draft'

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'property.payment',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }

    def _generate_payments(self):
        """Auto-generate scheduled payment records based on frequency."""
        self.ensure_one()
        Payment = self.env['property.payment']
        # Remove any existing draft payments
        self.payment_ids.filtered(lambda p: p.state == 'pending').unlink()

        freq_map = {'monthly': 1, 'quarterly': 3, 'biannual': 6, 'yearly': 12}
        months_step = freq_map.get(self.payment_frequency, 1)

        current = self.start_date
        seq = 1
        while current <= self.end_date:
            Payment.create({
                'name': _('%(ref)s - Payment %(seq)s', ref=self.name, seq=seq),
                'contract_id': self.id,
                'property_id': self.property_id.id,
                'renter_id': self.renter_id.id,
                'due_date': current,
                'amount': self.rent_amount,
                'state': 'pending',
            })
            current = current + relativedelta(months=months_step)
            seq += 1
