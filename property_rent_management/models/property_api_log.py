from odoo import fields, models


class PropertyApiLog(models.Model):
    _name = 'property.api.log'
    _description = 'Mobile API Log'
    _rec_name = 'endpoint'
    _order = 'request_date desc'

    api_key_id = fields.Many2one('property.api.key', string='API Key', ondelete='cascade')
    endpoint = fields.Char(string='Endpoint', required=True)
    method = fields.Selection([
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ], string='Method', default='GET')
    request_date = fields.Datetime(string='Date / Time', default=fields.Datetime.now)
    response_code = fields.Integer(string='HTTP Status')
    ip_address = fields.Char(string='IP Address')
    request_data = fields.Text(string='Request Data')
    response_data = fields.Text(string='Response Data')
    duration_ms = fields.Integer(string='Duration (ms)')
