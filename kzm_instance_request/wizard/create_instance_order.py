from odoo import models, fields, api, _, exceptions


class CreateInstanceOrder(models.Model):
    _name = 'create.instance'

    cpu = fields.Char(string='CPU')
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    limit_date = fields.Date(string='Processing deadline', tracking=True)
    tl = fields.Many2one(comodel_name='hr.employee', string="Employees")
    name = fields.Char(string='Designation', tracking=True)

    def default_purchase(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    purchase_orders = fields.Many2many(comodel_name='sale.order', string="Purchase Order", default=default_purchase)

    def create_instance(self):
        domain = [('tl_id', '=', self.tl.id)]
        if self.cpu == 0 or self.disk == 0 or self.ram == 0:
            raise exceptions.ValidationError(_("You cannot request instances with zero performance"))
        for x in range(len(self.purchase_orders)):
            self.env['kzm.instance.request'].create({
                'name': self.name,
                'cpu': self.cpu,
                'disk': self.disk,
                'limit_date': self.limit_date,
                'tl_id': self.tl.id,
                'purchase_orders': self.purchase_orders
            })

        return {
            'name': _('list of instance created'),
            'res_model': 'kzm.instance.request',
            'view_mode': 'tree, form',
            'context': {},
            'domain': domain,
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('kzm_instance_request.list_view').id, 'tree')]
        }
