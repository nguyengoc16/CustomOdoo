from odoo import models, fields, api, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = ''

    date_appointment = fields.Date(string="Date", required=False)
    hospital_patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', required=True)
    hospital_doctor_id = fields.Many2one(comodel_name='hospital.doctor', string='Doctor', required=True)

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['hospital_patient_id'] = self._context.get('active_id')
            return res

    def action_create_appointment(self):
        vals = {
            'hospital_patient_id': self.hospital_patient_id.id,
            'hospital_doctor_id': self.hospital_doctor_id.id,
            'date_appointment': self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print('Appointment', appointment_rec.id)
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
        }

    def action_view_appointment(self):
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
