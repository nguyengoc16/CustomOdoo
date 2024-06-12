from odoo import api, fields, models, _


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'

    note = fields.Text(string='Description')
    hospital_appointment_id = fields.Many2one(
        comodel_name='hospital.appointment',
        string="Appointment Reference",
        required=True, ondelete='cascade', index=True, copy=False)
    hospital_medicine_id = fields.Many2one(
        comodel_name='hospital.medicine',
        string="Medicine",
    )
    qty = fields.Integer(string="Quantity")
    tax = fields.Float(string="Tax(%)", compute='_compute_tax')
    tax_amount = fields.Monetary(string="Tax amount", compute='_compute_tax_amount')
    unit_price = fields.Monetary(string="Unit Price", compute='_compute_unit_price')
    subtotal = fields.Monetary(string="Subtotal", compute='_compute_subtotal')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.ref('base.VND'))

    @api.depends('hospital_medicine_id')
    def _compute_unit_price(self):
        for line in self:
            if line.hospital_medicine_id:
                line.unit_price = line.hospital_medicine_id.price
            else:
                line.unit_price = 0

    @api.depends('hospital_medicine_id')
    def _compute_tax(self):
        for line in self:
            if line.hospital_medicine_id:
                line.tax = line.hospital_medicine_id.tax.value
            else:
                line.tax = 0

    @api.depends('tax', 'unit_price')
    def _compute_tax_amount(self):
        for line in self:
            if line.unit_price and line.tax:
                line.tax_amount = line.unit_price * line.tax * line.qty / 100
            else:
                line.tax_amount = 0

    @api.depends('qty', 'unit_price', 'tax')
    def _compute_subtotal(self):
        for line in self:
            if line.qty and line.unit_price:
                line.subtotal = (line.qty * line.unit_price) * (1 + line.tax / 100)
            else:
                line.subtotal = 0
