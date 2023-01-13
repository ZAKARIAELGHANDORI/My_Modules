from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from markupsafe import Markup
from odoo.osv.expression import OR, AND
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers import portal
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


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

    def _prepare_portal_layout_values(self):
        print("ttt")

    def _instance_get_groupby_mapping(self):
        return {
            'state': 'state'
        }

    def _get_portal_default_domain(self):
        my_user = request.env.context.get('uid')
        return [
            ('create_uid', '=', my_user),
        ]

    def _get_instance_search_domain(self, search_in, search):
        search_domain = []
        if search_in == 'url':
            search_domain = OR([search_domain, [('url', 'ilike', search)]])
        if search_in == 'limit_date':
            search_domain = OR([search_domain, [('limit_date', 'ilike', search)]])
        if search_in == 'cpu':
            search_domain = OR([search_domain, [('cpu', 'ilike', search)]])
        return search_domain

    @http.route('/Create_instance', auth='public', website=True)
    def display_instances(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None,
                          groupby='none', search_in='content'):
        values = self._prepare_portal_layout_values()
        insts = request.env['kzm.instance.request'].sudo()
        domain = self._get_portal_default_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'name'},
            'client': {'label': _('Client'), 'order': 'partner_id'},
            'odoo version': {'label': _('Odoo Version'), 'order': 'odoo_id'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'brouillon': {'label': _('DRAFT'), 'domain': [('state', '=', 'brouillon')]},
            'soumise': {'label': _('SUBMITTED'), 'domain': [('state', '=', 'soumise')]},
            'en traitment': {'label': _('PROCESSING'), 'domain': [('state', '=', 'en traitment')]},
            'traite': {'label': _('TREATY'), 'domain': [('state', '=', 'traite')]},
        }

        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'url': {'input': 'url', 'label': _('Search in URL')},
            'limit date': {'input': 'limit_date', 'label': _('Search in Limit Date')},
            'cpu': {'input': 'cpu', 'label': _('Search in CPU')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'state': {'input': 'state', 'label': _('state')},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        groupby_mapping = self._instance_get_groupby_mapping()
        groupby_field = groupby_mapping.get(groupby, None)
        if groupby_field is not None and groupby_field not in insts._fields:
            raise ValueError(_("The field '%s' does not exist in the targeted model", groupby_field))
        order = '%s, %s' % (groupby_field, order) if groupby_field else order

        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain = AND([domain, self._get_instance_search_domain(search_in, search)])

        # if groupby == 'state':
        #   order = 'state, %s' % order

        # inst = http.request.env['kzm.instance.request'].search(domain, order=order)

        instances = http.request.env['kzm.instance.request'].search(domain, order=order)

        grouped_appointments = False
        if groupby_field:
            grouped_appointments = [(g, instances.concat(*events)) for g, events in
                                    groupbyelem(instances, itemgetter(groupby_field))]

        # instance_count = insts.search_count(domain)

        return http.request.render('kzm_instance_creation_portal.portal_my_instance_request', {
            'instances': instances,
            # 'inst': inst,
            # 'pager': pager,
            # 'grouped_signatures': grouped_signatures,
            #'grouped_tickets': grouped_tickets,
            'grouped_appointments': grouped_appointments,
            'page_name': 'instance',
            'default_url': '/Create_instance',
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'search_in': search_in,
            'search': search,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,

        })
