from odoo import models, fields, api


class DevisOdooVersion(models.Model):
    _inherit = 'sale.order'

    version_odoo_id = fields.Char(string="Odoo Version")
