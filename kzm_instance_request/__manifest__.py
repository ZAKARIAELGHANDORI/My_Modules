# -*- coding: utf-8 -*-
{
    'name': "Karizma Instance",

    'summary': """
        Demande de création d’instance (machine de déploiement de Odoo).""",

    'description': """
        
    """,

    'author': "ZAKARIA ELGHANDORI",
    'website': "https://www.karizma.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'contacts', 'sale_management'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/activity.xml',
        'data/instancedata.xml',
        'data/odoo_version.xml',
        'data/sequence_instance.xml',
        'views/odoo_version.xml',
        'views/instances.xml',

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #   'demo/demo.xml',
    # ],
}
