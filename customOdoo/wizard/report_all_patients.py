from odoo import models, fields, api, _


class ReportAllPatientsWizard(models.TransientModel):
    _name = "report.all.patients.wizard"
    _description = ''

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    age = fields.Integer(string='Age')

    def action_print_report(self):

        data = {
            'form': self.read()[0],

        }
        return self.env.ref('om_hospital.report_all_patients').report_action(self, data=data)
