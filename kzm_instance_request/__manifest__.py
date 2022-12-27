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
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_version.xml',
        'views/instances.xml',
        'data/instancedata.xml',
        'data/odoo_version.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
    #],
}
