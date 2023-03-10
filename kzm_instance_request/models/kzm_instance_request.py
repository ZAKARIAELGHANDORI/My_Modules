# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
from odoo import models, exceptions, fields, api, _


class KzmInstanceRequest(models.Model):
    _name = 'kzm.instance.request'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = "demande d'instance"

    name = fields.Char(string="Designation", required=True, copy=False, readonly=True, default="New")

    address = fields.Char('Address IP')
    actif = fields.Boolean(string="Actif by default", default=True)
    cpu = fields.Char(string='CPU')
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    url = fields.Char(string='URL')
    company_id = fields.Char(string='invisible')

    state = fields.Selection([('brouillon', 'Draft'), ('soumise', 'Submitted'),
                              ('en traitment', 'Processing'), ('traite', 'Treaty')], default='brouillon', tracking=True)
    limit_date = fields.Date(string='Processing deadline', tracking=True)
    treat_date = fields.Datetime(string='Processing date')
    treat_duration = fields.Float(string='Processing time', compute="_compute_treat_duration", store=True)

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner")
    tl_id = fields.Many2one(comodel_name='hr.employee', string="Employees")
    tl_user_id = fields.Many2one(related='tl_id.user_id', string="Employee")
    odoo_id = fields.Many2one(comodel_name='odoo.version', string="Odoo version")
    perimeters_ids = fields.Many2many(comodel_name='perimeters', string="Perimeters")
    address_employee = fields.Many2one(related='tl_id.address_id', string="Employee address", readonly=False)
    num_peri = fields.Integer(string='Number of Perimeters', compute='comp_perimeters', store=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order")

    # compter le nombre de perimeters choisi
    @api.depends('perimeters_ids')
    def comp_perimeters(self):
        self.num_peri = len(self.perimeters_ids)

    # compute le champ treat_date
    @api.depends('treat_date')
    def _compute_treat_duration(self):
        for rec in self:
            if rec.treat_date:
                treat = rec.treat_date.date()
                today = date.today()
                rec.treat_duration = (treat - today).days
        # for rec in self:
        #   if rec.treat_date:
        #       duration = abs((datetime.now() - rec.treat_date).days)
        # self.treat_duration = duration
        # print(rec.treat_duration)

    # pour ne pas avoir deux address IP identiques
    _sql_constraints = [
        ("address_unique", "unique(address)", "The address IP Already Exists")
    ]

    def action_draft(self):
        for x in self:
            x.state = "brouillon"

    def action_submitted(self):
        for x in self:
            x.state = "soumise"

    def action_processing(self):
        for x in self:
            x.state = "en traitment"

    def action_treaty(self):
        for x in self:
            x.state = "traite"
            x.treat_date = datetime.now()

    def action_scheduled_day(self):
        day = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for x in day:
            x.action_submitted()

    # override the creation methode
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('kzm.instance.request') or 'New'
        res = super(KzmInstanceRequest, self).create(vals)
        return res

    # override the unlink methode
    def unlink(self):
        for state in self:
            if state.state != "brouillon":
                raise exceptions.ValidationError(_("Cannot delete an instance which is in a state different to draft"))
            # print('success')
        return super().unlink()

    # override the update methode
    def write(self, vals):
        if vals.get('limit_date'):
            users = self.env.ref('kzm_instance_request.manager_group').users
            for user in users:
                self.activity_schedule('kzm_instance_request.activity_mail_a_traite', user_id=user.id,
                                       note=f" veuillez soumettre l'instance {self.name} avant {self.limit_date}")
            t2 = vals['limit_date']
            t2 = datetime.strptime(str(t2), '%Y-%m-%d')
            # print("----->", datetime.now(), "----->", t2)
            if t2 < datetime.now():
                raise exceptions.UserError(_("You cannot set a deadline later than today"))
            # cette fonction ca sera pas possible si on deplace l'instance sur la view gantt seulment si on change le type de champ
            # limit_date ?? Datetime

        return super(KzmInstanceRequest, self).write(vals)

    # @api.onchange('state')
    # def print_msg(self):
    #   print(f'Done the two actions are triggered (actions : print_msg , action_{self.state})')
    # lorsque l'etat est changer ?? cause d'un clic sur un button (treat , draft.. : ??a veut dire on change le state) la fonction print_msg se declenche pas
    # on doit changer directement le champ pour que la fonction se declenche


""" def action_scheduled_day5(self):
          limit_date = self.env['kzm.instance.request'].search([])
          date_l = limit_date.mapped('limit_date')

          for date in date_l:
             t1 =datetime.now()
             t1 = datetime.strptime(str(t1), '%Y-%m-%d %H:%M:%S.%f')
             t2 = date
             t2 = datetime.strptime(str(t2), '%Y-%m-%d')
             days = int(abs(t1 - t2).total_seconds())
             print(days
             if days >= 432000 :

                # make sure 'state' is up-to-date in database
                # self.env['kzm.instance.request'].flush_model(['state'])
                # self.env.cr.execute("UPDATE kzm_instance_request SET state=%s WHERE limit_date=%s", ['soumise', date])

                # invalidate 'state' from the cache
                # self.env['kzm.instance.request'].invalidate_model(['state'])

                #print("action scheduled done") """
