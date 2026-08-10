from odoo import fields, models


class PropertyOwner(models.Model):
    _name = 'property.owner'
    _description = 'Property Owner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Owner Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Contact')
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    id_number = fields.Char(string='ID / Passport Number')
    address = fields.Char(string='Address')
    image = fields.Image(string='Photo')
    note = fields.Text(string='Notes')
    active = fields.Boolean(default=True)

    property_ids = fields.One2many('property.property', 'owner_id', string='Properties')
    property_count = fields.Integer(compute='_compute_property_count', string='Properties')
    contract_count = fields.Integer(compute='_compute_contract_count', string='Contracts')

    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = self.env['property.contract'].search_count(
                [('owner_id', '=', rec.id)]
            )

    def action_view_properties(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'property.property',
            'view_mode': 'list,form',
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }

    def action_view_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'property.contract',
            'view_mode': 'list,form',
            'domain': [('owner_id', '=', self.id)],
        }
