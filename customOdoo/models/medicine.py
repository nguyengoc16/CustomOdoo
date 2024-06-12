from odoo import api, fields, models, _


class HospitalMedicine(models.Model):
    _name = 'hospital.medicine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Medicine'

    name = fields.Char(string='Name', required=True, tracking=True)
    price = fields.Monetary(string='Unit Price', required=True, tracking=True)
    tax = fields.Many2one(comodel_name='hospital.tax',string='Tax(%)', default=0)
    note = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.ref('base.VND'))
