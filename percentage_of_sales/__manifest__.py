# -*- coding: utf-8 -*-
{
    'name': "Percentage of sales",

    'summary': """Commission with card payment.""",

    'description': """
        This module helps us to generate commissions when payments are made with a card.
    """,

    'author': "Xmarts",
    'website': "https://xmarts.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales.',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'web', 'point_of_sale','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/product.xml',
        'views/account_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
    'installable': True
}