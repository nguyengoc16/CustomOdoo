from odoo import api, fields, models, _


class HospitalTax(models.Model):
    _name = 'hospital.tax'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Tax'

    name = fields.Char(string='Name', required=True, tracking=True)
    value = fields.Float(string='Percentage', required=True,)

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name + ' [' + str(rec.value) + '%]'
            result.append((rec.id, name))
        return result
