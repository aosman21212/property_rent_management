from odoo import api, fields, models


class PropertyMaintenance(models.Model):
    _name = 'property.maintenance'
    _description = 'Property Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'request_date desc'

    name = fields.Char(string='Maintenance Reference', copy=False, readonly=True, default='New')
    property_id = fields.Many2one('property.property', string='Property', required=True, tracking=True)
    owner_id = fields.Many2one('property.owner', string='Owner',
                               related='property_id.owner_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)

    maintenance_type = fields.Selection([
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('hvac', 'HVAC / Air Conditioning'),
        ('painting', 'Painting'),
        ('structural', 'Structural'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other'),
    ], string='Type', required=True, default='other', tracking=True)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
        ('2', 'Critical'),
    ], string='Priority', default='0', tracking=True)

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='new', tracking=True)

    request_date = fields.Date(string='Request Date', default=fields.Date.today, tracking=True)
    completion_date = fields.Date(string='Completion Date', tracking=True)
    responsible_id = fields.Many2one('res.users', string='Assigned To',
                                     default=lambda self: self.env.user, tracking=True)
    cost = fields.Monetary(string='Estimated Cost', currency_field='currency_id')
    actual_cost = fields.Monetary(string='Actual Cost', currency_field='currency_id')
    description = fields.Text(string='Description', required=True)
    note = fields.Html(string='Work Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('property.maintenance') or 'New'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'
            rec.property_id.status = 'maintenance'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.completion_date = fields.Date.today()
            # Only reset to available if no active contract
            active_contracts = self.env['property.contract'].search_count([
                ('property_id', '=', rec.property_id.id),
                ('state', '=', 'active'),
            ])
            if not active_contracts:
                rec.property_id.status = 'available'
            else:
                rec.property_id.status = 'rented'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset(self):
        self.state = 'new'
        self.completion_date = False
