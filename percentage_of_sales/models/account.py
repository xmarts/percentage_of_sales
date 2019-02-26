from odoo import models, fields, api, _

class account_journal(models.Model):
    _inherit = "account.journal"

    aplicar_cargos = fields.Boolean("Aplicar Cargos")
    fees_cantidad = fields.Float("Cantidad")
    fees_tipo = fields.Selection(selection=[('fixed','Fixed'),('percentage','Porcentage')],string="Tipo tarifa", default="fixed")
    