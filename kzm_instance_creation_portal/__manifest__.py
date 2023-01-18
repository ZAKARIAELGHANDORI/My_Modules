# -*- coding: utf-8 -*-
{
    'name': "KARIZMA Instance portal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ZAKARIA ELGHANDORI",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16',

    # any module necessary for this one to work correctly
    'depends': ['base', 'kzm_instance_request', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/Website_instances.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
}
