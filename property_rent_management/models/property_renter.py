from odoo import fields, models


class PropertyRenter(models.Model):
    _name = 'property.renter'
    _description = 'Property Renter / Tenant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Renter Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Contact')
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    id_number = fields.Char(string='ID / Passport Number')
    address = fields.Char(string='Address')
    image = fields.Image(string='Photo')
    note = fields.Text(string='Notes')
    active = fields.Boolean(default=True)

    contract_ids = fields.One2many('property.contract', 'renter_id', string='Contracts')
    contract_count = fields.Integer(compute='_compute_contract_count', string='Contracts')
    payment_count = fields.Integer(compute='_compute_payment_count', string='Payments')

    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = len(rec.contract_ids)

    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = self.env['property.payment'].search_count(
                [('renter_id', '=', rec.id)]
            )

    def action_view_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'property.contract',
            'view_mode': 'list,form',
            'domain': [('renter_id', '=', self.id)],
        }

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'property.payment',
            'view_mode': 'list,form',
            'domain': [('renter_id', '=', self.id)],
        }
