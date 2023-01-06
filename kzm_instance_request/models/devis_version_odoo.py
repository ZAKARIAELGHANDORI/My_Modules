from odoo import models, fields, api


class DevisOdooVersion(models.Model):
    _inherit = 'sale.order'

    odoo_version = fields.Char(string="Odoo Version")
