from odoo import api, fields, models


class PropertyProperty(models.Model):
    _name = 'property.property'
    _description = 'Rental Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Property Name', required=True, tracking=True)
    code = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('warehouse', 'Warehouse'),
        ('land', 'Land'),
    ], string='Type', required=True, default='apartment', tracking=True)

    owner_id = fields.Many2one('property.owner', string='Owner', required=True, tracking=True)
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')

    area = fields.Float(string='Area (m²)')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    floor = fields.Integer(string='Floor')
    furnished = fields.Boolean(string='Furnished', default=False)

    rent_amount = fields.Monetary(string='Rent Amount', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)

    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ], string='Status', default='available', tracking=True)

    image = fields.Image(string='Property Image')
    description = fields.Html(string='Description')
    note = fields.Text(string='Internal Notes')
    active = fields.Boolean(default=True)

    contract_ids = fields.One2many('property.contract', 'property_id', string='Contracts')
    maintenance_ids = fields.One2many('property.maintenance', 'property_id', string='Maintenance')
    payment_ids = fields.One2many('property.payment', 'property_id', string='Payments')

    contract_count = fields.Integer(compute='_compute_counts', string='Contracts')
    maintenance_count = fields.Integer(compute='_compute_counts', string='Maintenance')
    payment_count = fields.Integer(compute='_compute_counts', string='Payments')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('property.property') or 'New'
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.contract_count = len(rec.contract_ids)
            rec.maintenance_count = len(rec.maintenance_ids)
            rec.payment_count = len(rec.payment_ids)

    def action_view_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'property.contract',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_view_maintenance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance',
            'res_model': 'property.maintenance',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'property.payment',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_set_available(self):
        self.status = 'available'

    def action_set_maintenance(self):
        self.status = 'maintenance'
