# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritCampo(models.Model):

	_inherit = 'sale.order'

	metodo_pago = fields.Many2one('account.journal', string = 'formas de pago')

	carga = fields.Float(string="cargar agregada: ", compute="_amount_all")


	@api.depends('order_line.price_total', 'metodo_pago')
	def _amount_all(self):
		"""
		Compute the total amounts of the SO.
		"""
		for order in self:
			amount_untaxed = amount_tax = car = 0.0
			
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax

			if order.metodo_pago.aplicar_cargos == True:
				if order.metodo_pago.fees_tipo == 'fixed':
					car = order.metodo_pago.fees_cantidad
				else :
					base = amount_untaxed
					impuestos = amount_tax 
					car = (base + impuestos) * (order.metodo_pago.fees_cantidad / 100)
			else:
				car = 0.0

			order.update({
				'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
				'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
				'carga': order.pricelist_id.currency_id.round(car),
				'amount_total': amount_untaxed + amount_tax + car,
			})
			