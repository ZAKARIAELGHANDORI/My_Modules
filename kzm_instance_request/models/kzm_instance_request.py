# -*- coding: utf-8 -*-
from datetime import date, timedelta , datetime
from odoo import models, fields, api


class KzmInstanceRequest(models.Model):
     _name = 'kzm.instance.request'
     _description = "demande d'instance"

     name = fields.Char(string='Designation')

     address = fields.Char('Address IP')
     actif = fields.Boolean(string="Actif by default", default=True)
     cpu = fields.Char(string='CPU')
     ram = fields.Char(string='RAM')
     disk = fields.Char(string='DISK')
     url = fields.Char(string='URL')
     state = fields.Selection([('brouillon','Draft'),('soumise','Submitted'),('en traitment','Processing'),('traite','Treaty')],default='brouillon')
     limit_date = fields.Date(string='Processing deadline')
     treat_date = fields.Datetime(string='Processing date')
     treat_duration = fields.Float(string='Processing time')

     def action_draft(self):
         for x in self:
            x.state="brouillon"

     def action_submitted(self):
         for x in self:
            x.state ="soumise"
     def action_processing(self):
         for x in self:
            x.state="en traitment"

     def action_treaty(self):
         for x in self:
            x.state="traite"


     def action_scheduled_day(self):
         day = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
         for x in day:
             x.state = 'soumise'

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










