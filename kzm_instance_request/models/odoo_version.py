from odoo import models, fields, api


class OdooVersion(models.Model):
     _name = 'odoo.version'
     _description = 'La version de odoo'

     name = fields.Char(string="Version")