from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CreateInstancePortal(http.Controller):
    @http.route('/Create_instance', auth='public', website=True)
    def my_instances(self, **kw):
        create_id = request.env.context.get('uid')
        instances = http.request.env['kzm.instance.request'].search([('create_uid', '=', create_id)])
        return http.request.render('kzm_instance_creation_portal.portal_my_instance_request', {
            'instances': instances,
            'page_name': 'instance'

        })

    @http.route('/Create_Instance', auth='public', website=True)
    def create_instances1(self, **kw):
        return http.request.render('kzm_instance_creation_portal.create_instance', {})

    @http.route('/Create_request', auth='public', website=True)
    def create_request(self, **kw):
        request.env['kzm.instance.request'].sudo().create(kw)
        create_id = request.env.context.get('uid')
        instances = http.request.env['kzm.instance.request'].search([('create_uid', '=', create_id)])
        return http.request.render('kzm_instance_creation_portal.portal_my_instance_request', {
            'instances': instances,

        })


class InstanceCount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCount, self)._prepare_home_portal_values(counters)
        if 'instance_count' in counters:
            # partner_id = http.request.env.user.partner_id
            instance_count = http.request.env['kzm.instance.request'].sudo().search_count([])
            values.update({
                'instance_count': instance_count,
            })
        return values
