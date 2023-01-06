from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    instance_ids = fields.One2many(comodel_name='kzm.instance.request', inverse_name='tl_id', string='Instance ID', tracking=True)

    num_instance = fields.Integer(string='Number of instances', compute='comp_instance')

    def comp_instance(self):
        self.num_instance = len(self.instance_ids)

    def open_tree_view(self, context=None):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kzm.instance.request',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'views_id': 'kzm_instance_request.list_view',
            'target': 'current',
            'domain': [('tl_id', '=', self.name)]

        }




