from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Hospital Patient'

    sale_description = fields.Char(string='Sale Description')
