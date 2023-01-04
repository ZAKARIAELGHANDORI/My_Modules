from odoo import models, fields, api


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee']

    instance_ids = fields.One2many(comodel='kzm.instance.request', string='Instance ID', tracking=True)

    num_instance = fields.Integer(string='Number of instances', compute='comp_instance')

    def comp_instance(self):
        self.num_instance = len(self.instance_ids)




