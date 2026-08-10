from odoo import api, fields, models, _


class PropertyPayment(models.Model):
    _name = 'property.payment'
    _description = 'Rent Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'due_date asc'

    name = fields.Char(string='Payment Reference', required=True, tracking=True)
    contract_id = fields.Many2one('property.contract', string='Contract', required=True, tracking=True)
    property_id = fields.Many2one('property.property', string='Property',
                                  related='contract_id.property_id', store=True)
    owner_id = fields.Many2one('property.owner', string='Owner',
                               related='contract_id.owner_id', store=True)
    renter_id = fields.Many2one('property.renter', string='Renter',
                                related='contract_id.renter_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='contract_id.currency_id', store=True)

    due_date = fields.Date(string='Due Date', required=True, tracking=True)
    payment_date = fields.Date(string='Payment Date', tracking=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', tracking=True)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('late', 'Late'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', tracking=True)

    move_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    note = fields.Text(string='Notes')

    def action_mark_paid(self):
        for rec in self:
            rec.state = 'paid'
            rec.payment_date = fields.Date.today()

    def action_mark_late(self):
        for rec in self:
            if rec.state == 'pending':
                rec.state = 'late'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset_pending(self):
        for rec in self:
            if rec.state in ('cancelled', 'late'):
                rec.state = 'pending'
                rec.payment_date = False

    def action_create_invoice(self):
        """Create an Odoo invoice for this payment."""
        self.ensure_one()
        if self.move_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.move_id.id,
                'view_mode': 'form',
            }

        partner = self.renter_id.partner_id or self.env['res.partner'].search(
            [('name', '=', self.renter_id.name)], limit=1
        )
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id if partner else False,
            'invoice_date': fields.Date.today(),
            'invoice_date_due': self.due_date,
            'invoice_line_ids': [(0, 0, {
                'name': _('Rent — %(prop)s (%(ref)s)', prop=self.property_id.name, ref=self.name),
                'quantity': 1,
                'price_unit': self.amount,
            })],
        })
        self.move_id = move
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
        }

    @api.model
    def _cron_mark_late_payments(self):
        """Cron: mark overdue payments as Late."""
        today = fields.Date.today()
        overdue = self.search([('state', '=', 'pending'), ('due_date', '<', today)])
        overdue.write({'state': 'late'})
