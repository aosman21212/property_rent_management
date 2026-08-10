import uuid
from odoo import api, fields, models


class PropertyApiKey(models.Model):
    _name = 'property.api.key'
    _description = 'Mobile API Key'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string='Name / Label', required=True, tracking=True)
    key = fields.Char(string='API Key', copy=False, readonly=True)
    user_id = fields.Many2one('res.users', string='Assigned User',
                               default=lambda self: self.env.user, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    last_used = fields.Datetime(string='Last Used', readonly=True)
    description = fields.Text(string='Description')

    log_ids = fields.One2many('property.api.log', 'api_key_id', string='Logs')
    log_count = fields.Integer(compute='_compute_log_count', string='Calls')

    def _compute_log_count(self):
        for rec in self:
            rec.log_count = len(rec.log_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('key'):
                vals['key'] = str(uuid.uuid4()).replace('-', '').upper()
        return super().create(vals_list)

    def action_regenerate_key(self):
        for rec in self:
            rec.key = str(uuid.uuid4()).replace('-', '').upper()

    def action_view_logs(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'API Logs',
            'res_model': 'property.api.log',
            'view_mode': 'list,form',
            'domain': [('api_key_id', '=', self.id)],
        }
