from odoo import models, fields, api, _, exceptions


class CreateInstanceOrder(models.Model):
    _name = 'create.instance'

    cpu = fields.Char(string='CPU')
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    limit_date = fields.Date(string='Processing deadline')
    tl = fields.Many2one(comodel_name='hr.employee', string="Employees")
    instance_id = fields.Many2one(comodel_name='kzm.instance.request', string="Instance id", invisible=True)

    def default_sales(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    sale_order_ids = fields.Many2many(comodel_name='sale.order', string="Sale Order", default=default_sales)

    def create_instance(self):
        ids_rec = []
        if self.cpu == 0 or self.disk == 0 or self.ram == 0:
            raise exceptions.ValidationError(_("You cannot request instances with zero performance"))
        for x in self.sale_order_ids:
            val = self.env['kzm.instance.request'].create({
                'cpu': self.cpu,
                'ram': self.ram,
                'disk': self.disk,
                'limit_date': self.limit_date,
                'tl_id': self.tl.id,
                'sale_order_id': x.id
            })
            ids_rec.append(val.id)
        domain = [('id', '=', ids_rec)]
        return {
            'name': _('list of instance created'),
            'res_model': 'kzm.instance.request',
            'view_mode': 'tree, form',
            'context': {},
            'domain': domain,
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('kzm_instance_request.list_view').id, 'tree')]
        }
