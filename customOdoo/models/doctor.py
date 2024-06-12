from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Doctor'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string="Image")
    appointment_count = fields.Integer(string='Number of appointments', compute='_compute_appointment_count')
    active = fields.Boolean(string='Active', default=True)
    experience = fields.Char(string='Years of expr')
    hospital_department_id = fields.Many2one(comodel_name='hospital.department', string='Department', required=True)

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)", self.doctor_name)
        return super(HospitalDoctor, self).copy(default)

    def _compute_appointment_count(self):

        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('hospital_doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_open_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'res_model': 'hospital.appointment',
            'domain': [('hospital_doctor_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
