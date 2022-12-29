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

     def action_scheduled_day():
          t1 = daten=datetime.datetime.now()
          t1 = datetime.strptime(t1, '%a %d %b %Y %H:%M:%S %z')
          t2 = limit_date
          t2 = datetime.strptime(t2, '%a %d %b %Y %H:%M:%S %z')
          days = int(abs(t1 - t2).total_seconds())
          if days >= 432000 :
               self.state="treaty"






