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
    'depends': ['base', 'mail', 'contacts', 'sale_management', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/activity.xml',
        'data/odoo_version.xml',
        'data/perimeters_data.xml',
        'data/sequence_instance.xml',
        'views/perimeters.xml',
        'views/odoo_version.xml',
        'views/instances.xml',
        'views/employee.xml',
        'views/odoo_version_instance.xml',
        'views/devis_odoo_version.xml',
        'report/sale_order_inherit_report.xml',
        'report/kzm_instance_request_report.xml',
        'report/instance_document.xml',
        'wizard/order_instance_wizard.xml',

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #   'demo/demo.xml',
    # ],
}
