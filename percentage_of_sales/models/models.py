# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, pycompat

class InheritCampo(models.Model):

	_inherit = 'sale.order'

	metodo_pago = fields.Many2one('account.journal', string = 'Formas de pago')

	carga = fields.Float(string="Carga agregada: ", compute="_amount_all")

	@api.multi
	def _prepare_invoice(self):
		self.ensure_one()
		journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
		if not journal_id:
			raise UserError(_('Please define an accounting sales journal for this company.'))
		invoice_vals = {
			'name': self.client_order_ref or '',
			'origin': self.name,
			'type': 'out_invoice',
			'account_id': self.partner_invoice_id.property_account_receivable_id.id,
			'partner_id': self.partner_invoice_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'journal_id': journal_id,
			'currency_id': self.pricelist_id.currency_id.id,
			'comment': self.note,
			'payment_term_id': self.payment_term_id.id,
			'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
			'company_id': self.company_id.id,
			'user_id': self.user_id and self.user_id.id,
			'carg_ret' : self.carga,
			'team_id': self.team_id.id
		}
		return invoice_vals

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

class AddCampCarg(models.Model):

	_inherit = 'account.invoice'

	carg_ret = fields.Float( string = 'Carga agregada')

	@api.one
	@api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding','currency_id', 'company_id', 'date_invoice', 'type')
	def _compute_amount(self):
		round_curr = self.currency_id.round
		self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
		self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
		self.amount_total = self.amount_untaxed + self.amount_tax + self.carg_ret
		amount_total_company_signed = self.amount_total
		amount_untaxed_signed = self.amount_untaxed
		if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
			currency_id = self.currency_id.with_context(date=self.date_invoice)
			amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
			amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
		sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
		self.amount_total_company_signed = amount_total_company_signed * sign
		self.amount_total_signed = self.amount_total * sign
		self.amount_untaxed_signed = amount_untaxed_signed * sign

	@api.one
	@api.depends(
		'state', 'currency_id', 'invoice_line_ids.price_subtotal',
		'move_id.line_ids.amount_residual',
		'move_id.line_ids.currency_id')
	def _compute_residual(self):
		residual = 0.0
		residual_company_signed = 0.0
		sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
		for line in self.sudo().move_id.line_ids:
			if line.account_id == self.account_id:
				residual_company_signed += line.amount_residual
				if line.currency_id == self.currency_id:
					residual += line.amount_residual_currency if line.currency_id else line.amount_residual
				else:
					from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
					residual += from_currency.compute(line.amount_residual, self.currency_id) 
		self.residual_company_signed = abs(residual_company_signed) * sign
		self.residual_signed = abs(residual) * sign
		self.residual_signed += self.carg_ret
		self.residual = abs(residual + self.carg_ret)
		digits_rounding_precision = self.currency_id.rounding
		if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
			self.reconciled = True
		else:
			self.reconciled = False

class AccountPay(models.Model):

	_inherit = 'account.payment'

	@api.one
	@api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id')
	def _compute_payment_difference(self):
		if len(self.invoice_ids) == 0:
			return
		if self.invoice_ids[0].type in ['in_invoice', 'out_refund']:
			self.payment_difference = self.amount - self._compute_total_invoices_amount()
		else:
			self.payment_difference = self._compute_total_invoices_amount() - self.amount

	@api.model
	def _compute_total_invoices_amount(self):
		payment_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id or self.env.user.company_id.currency_id
		total = 0
		for inv in self.invoice_ids:
			if inv.currency_id == payment_currency:
				total += inv.residual_signed
			else:
				total += inv.company_currency_id.with_context(date=self.payment_date).compute(inv.residual_company_signed, payment_currency)
		return abs(total)
		
		