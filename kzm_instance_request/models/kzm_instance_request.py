# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KzmInstanceRequest(models.Model):
     _name = 'kzm.instance.request'
     _description = "demande d'instance"

     name = fields.Char('Designation')
     #user = create_uid('Crée par')
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


