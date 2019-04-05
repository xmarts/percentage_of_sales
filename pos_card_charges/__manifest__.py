# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'POS Card Charges',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'POS Card Charges',
    'description': """
POS Card Charges
""",
    'price': 19.00,
    'currency': 'EUR',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "http://www.acespritech.com",
    'depends': ['web', 'point_of_sale', 'base'],
    'data': [
        'data/product.xml',
        'views/pos_card_charges.xml',
        'views/account_view.xml',
        'views/point_of_sale_view.xml',
    ],
    'demo': [],
    'test': [],
    'images': ['static/description/main_screenshot.png'],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: