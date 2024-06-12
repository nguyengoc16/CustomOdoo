from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'
    _order = 'name desc,age asc'

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)
    responsible_id = fields.Many2one(comodel_name='res.partner', string="Responsible")
    image = fields.Binary(string="Image")
    hospital_appointment_ids = fields.One2many('hospital.appointment', 'hospital_patient_id', string="Appointment")
    appointment_count = fields.Integer(string='Number of appointments', compute='_compute_appointment_count')
    active = fields.Boolean(string="Active", default=True)

    def _compute_appointment_count(self):

        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('hospital_patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count
        # self.appointment_count = appointment_count

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    def action_open_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'res_model': 'hospital.appointment',
            'domain': [('hospital_patient_id', '=', self.id)],
            'context': {'default_hospital_patient_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }

    @api.model
    def create(self, vals):

        if not vals.get('note'):
            vals['note'] = "New patient"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _(
                'New')  #next_by_code('<field name="code">hospital.patient</field>')
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        result = super(HospitalPatient, self).default_get(fields)
        return result

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(
                    _("You cannot create this, as %s is already exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError(
                    _("You cannot create this, as %s's age is less than 0" % rec.name))

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + ']' + ' ' + rec.name
            result.append((rec.id, name))
        return result
