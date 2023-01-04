from odoo import models, fields, api


class OdooVersionTwo(models.Model):
    _name = 'odoo.version.instance'
    _inherit = ['odoo.version']

    instance_ids = fields.One2many(comodel='kzm.instance.request', string='Instance ID', tracking=True)

    num_instance = fields.Integer(string='Number of instances', compute='comp_instance')

    def comp_instance(self):
        self.num_instance = len(self.instance_ids)




