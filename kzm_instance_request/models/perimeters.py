from odoo import models, fields, api


class Perimeters(models.Model):
     _name = 'perimeters'

     name = fields.Char(string="Name")