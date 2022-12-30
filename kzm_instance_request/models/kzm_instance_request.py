# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class KzmInstanceRequest(models.Model):
     _name = 'kzm.instance.request'
     _description = "demande d'instance"

     name = fields.Char('Designation')

     address = fields.Char('Address IP')
     actif = fields.Boolean(string="Actif by default", default=True)
     cpu = fields.Char('CPU')
     ram = fields.Char('RAM')
     disk = fields.Char('DISK')
     url = fields.Char('URL')
     state = fields.Selection([('brouillon','Draft'),('soumise','Submitted'),('en traitment','Processing'),('traite','Treaty')],default='brouillon')
     limit_date = fields.Date('Processing deadline')
     treat_date = fields.Datetime('Processing date')
     treat_duration = fields.Float('Processing time')

     def action_draft(self):
        self.state="brouillon"
     def action_submitted(self):
          self.state ="soumise"
     def action_processing(self):
          self.state="en traitment"
     def action_treaty(self):
          self.state="traite"


     def action_scheduled_day(self):
          limit_date = self.env['kzm.instance.request'].search([])
          date_l = limit_date.mapped('limit_date')

          for date in date_l:
             t1 =datetime.now()
             t1 = datetime.strptime(str(t1), '%Y-%m-%d %H:%M:%S.%f')
             t2 = date
             t2 = datetime.strptime(str(t2), '%Y-%m-%d')
             days = int(abs(t1 - t2).total_seconds())
             print(days)
             if days >= 432000 :

                # make sure 'state' is up-to-date in database
                self.env['kzm.instance.request'].flush_model(['state'])

                self.env.cr.execute("UPDATE kzm_instance_request SET state=%s WHERE limit_date=%s", ['soumise', date])

                # invalidate 'state' from the cache
                self.env['kzm.instance.request'].invalidate_model(['state'])









