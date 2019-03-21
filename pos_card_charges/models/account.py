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


class account_journal(models.Model):
    _inherit = "account.journal"

    apply_charges = fields.Boolean("Apply Charges");
    fees_amount = fields.Float("Fees Amount");
    fees_type = fields.Selection(selection=[('fixed','Fixed'),('percentage','Percentage')],string="Fees type", default="fixed")
    optional = fields.Boolean("Optional")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
