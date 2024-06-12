from odoo import models, fields, api, _


class CrmLeadSyncMailingList(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = ''

    hospital_patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', required=True)

    def action_search_appointment(self):
        # method1
        action = self.env.ref('om_hospital.action_appointment').read()[0]
        action['domain'] = [('hospital_patient_id', '=', self.hospital_patient_id.id)]
        return action
        # #method2
        # action = self.env['ir.action.actions']._for_xml_id('om_hospital.action_appointment')
        # action['domain'] = [('hospital_patient_id', '=', self.hospital_patient_id.id)]
        # return action
        # method 3
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Appointments',
        #     'res_model': 'hospital.appointment',
        #     'domain': [('hospital_patient_id', '=', self.hospital_patient_id.id)],
        #     'view_mode': 'tree, form',
        #     'target': 'current'
        # }
