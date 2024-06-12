from odoo import api, fields, models, _


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Department'

    name = fields.Char(string='Department', required=True, tracking=True)
    note = fields.Text(string='Description')


