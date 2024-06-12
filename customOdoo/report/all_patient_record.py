from odoo import api, fields, models


class SaleOrder(models.AbstractModel):
    _name = 'report.om_hospital.report_all_patients_template'  #report.module_name.template_name

    @api.model
    def _get_report_values(self, docids, data=None):  #data is data getting from wizarddddd automatically
        domain = []
        gender = data.get('form').get('gender')
        age = data.get('form').get('age')

        if gender:
            domain.append(('gender', '=', gender))
        if age != 0:
            domain.append(('age', '=', age))
        docs = self.env['hospital.patient'].search(domain)
        return {
            'docs': docs,
        }