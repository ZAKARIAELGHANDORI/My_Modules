# -*- coding: utf-8 -*-
# from odoo import http


# class KzmInstance(http.Controller):
#     @http.route('/kzm_instance/kzm_instance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kzm_instance/kzm_instance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kzm_instance.listing', {
#             'root': '/kzm_instance/kzm_instance',
#             'objects': http.request.env['kzm_instance.kzm_instance'].search([]),
#         })

#     @http.route('/kzm_instance/kzm_instance/objects/<model("kzm_instance.kzm_instance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kzm_instance.object', {
#             'object': obj
#         })
