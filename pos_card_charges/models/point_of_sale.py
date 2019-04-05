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

from openerp import models, fields, api, _


class pos_config(models.Model):
    _inherit = "pos.config"

    enable_card_charges = fields.Boolean("Enable Card Charges")
    payment_product_id = fields.Many2one('product.product',"Payment Charge Product")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
