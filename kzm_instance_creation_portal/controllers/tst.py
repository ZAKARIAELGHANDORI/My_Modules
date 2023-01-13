from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from markupsafe import Markup
from odoo.osv.expression import OR, AND
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


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

    def _prepare_instances_domain(self):
        return []

    def _prepare_my_instances_values(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all',
                                     search=None, groupby='none', search_in='content'):
        values = self._prepare_home_portal_values()
        domain = self._prepare_instances_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'name'},
            'client': {'label': _('Client'), 'order': 'partner_id'},
            'odoo version': {'label': _('Odoo Version'), 'order': 'odoo_id'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'draft': {'label': _('DRAFT'), 'domain': [('state', '=', 'brouillon')]},
            'submitted': {'label': _('SUBMITTED'), 'domain': [('state', '=', 'soumise')]},
            'processing': {'label': _('PROCESSING'), 'domain': [('state', '=', 'en traitment')]},
            'treaty': {'label': _('TREATY'), 'domain': [('state', '=', 'traite')]},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'url': {'input': 'url', 'label': _('Search in URL')},
            'limit date': {'input': 'limit_date', 'label': _('Search in Limit Date')},
            'cpu': {'input': 'cpu', 'label': _('Search in CPU')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'state', 'label': _('Stage')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'url':
                search_domain = OR([search_domain, [('url', 'ilike', search)]])
            if search_in == 'content':
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in == 'limit_date':
                search_domain = OR([search_domain, [('limit_date', 'ilike', search)]])
            if search_in == 'cpu':
                search_domain = OR([search_domain, [('cpu', 'ilike', search)]])
            domain = AND([domain, search_domain])

        # pager
        instances_count = request.env['kzm.instance.request'].search_count(domain)
        pager = portal_pager(
            url="/Create_instance",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in,
                      'search': search, 'groupby': groupby, 'filterby': filterby},
            total=instances_count,
            page=page,
            step=self._items_per_page
        )

        instances = request.env['kzm.instance.request'].search(domain, order=order, limit=self._items_per_page,
                                                               offset=pager['offset'])
        request.session['my_instances_history'] = instances.ids[:100]

        if groupby != 'none':
            grouped_instances = [request.env['kzm.instance.request'].concat(*g) for k, g in
                                 groupbyelem(instances, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_instances = [instances]

        values.update({
            'date': date_begin,
            'grouped_tickets': grouped_instances,
            'page_name': 'instances',
            'default_url': '/Create_instance',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return values


class InstanceCount(CustomerPortal):
    """def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        if values.get('name', False):
            values['title'] = _("Instances")
        return values """

    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCount, self)._prepare_home_portal_values(counters)
        if 'instance_count' in counters:
            # partner_id = http.request.env.user.partner_id
            instance_count = http.request.env['kzm.instance.request'].sudo().search_count([])
            values.update({
                'instance_count': instance_count,
            })
        return values
