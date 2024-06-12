from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _order = 'hospital_patient_id desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    hospital_patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', required=True)
    age = fields.Integer(string='Age', related='hospital_patient_id.age', tracking=True)
    hospital_doctor_id = fields.Many2one(comodel_name='hospital.doctor', string='Doctor', required=True)
    appointment_count = fields.Integer(string='Number of appointments', compute='_compute_appointment_count')
    hello = fields.Integer()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], string='Gender', tracking=True)
    prescription = fields.Text(string='Prescription')
    # appointment_prescription_lines_ids = fields.One2many('appointment.prescription.lines',
    #                                                      'hospital_appointment_id',
    #                                                      # regard to the col FK in that model
    #                                                      string="Prescription Lines")
    hospital_appointment_line_ids = fields.One2many(
        comodel_name='hospital.appointment.line',
        inverse_name='hospital_appointment_id',
        string="Appointment Lines")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check up time")
    total = fields.Monetary(string="Total", compute='_compute_total_appointment', store=True)
    tax = fields.Monetary(string="Tax", compute='_compute_tax_appointment', store=True)
    subtotal = fields.Monetary(string="Before Tax", compute='_compute_subtotal_appointment', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.ref('base.VND'))

    @api.depends('hospital_appointment_line_ids.subtotal')
    def _compute_total_appointment(self):
        for rec in self:
            total = 0.0
            for line in rec.hospital_appointment_line_ids:
                total += line.subtotal
            rec.total = total

    @api.depends('hospital_appointment_line_ids.tax_amount')
    def _compute_tax_appointment(self):
        for rec in self:
            tax = 0.0
            for line in rec.hospital_appointment_line_ids:
                tax += line.tax_amount
            rec.tax = tax

    @api.depends('total', 'tax')
    def _compute_subtotal_appointment(self):
        for rec in self:
            rec.subtotal = rec.total - rec.tax

    @api.depends('hospital_patient_id')
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count(
                [('hospital_patient_id', '=', rec.hospital_patient_id.id)])
            rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        }

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New appointment"
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')

        return super(HospitalAppointment, self).create(vals)

    @api.onchange('hospital_patient_id')
    def onchange_hospital_patient_id(self):
        if self.hospital_patient_id:
            self.gender = self.hospital_patient_id.gender
            self.note = self.hospital_patient_id.note
        else:
            self.gender = ''
            self.note = ''

    def unlink(self):
        if any(rec.state == 'done' for rec in self):
            raise ValidationError(_("You cannot delete a record in 'Done' state"))
        return super(HospitalAppointment, self).unlink()


class AppointmentPrescriptionLines(models.Model):
    _name = 'appointment.prescription.lines'
    _description = "Appointment Prescription Line"

    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
    hospital_appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
