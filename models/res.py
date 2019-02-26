	@api.onchange('metodo_pago')
	def calcular_carga(self):
		if self.metodo_pago.aplicar_cargos == True:
			if self.metodo_pago.fees_tipo == 'fixed':
				#raise UserError(self.amount_untaxed)
				self.carga = self.metodo_pago.fees_cantidad

			if self.metodo_pago.fees_tipo == 'percentage':
				base = self.amount_untaxed
				impuestos = self.amount_tax 
				cr = (base + impuestos) * (self.metodo_pago.fees_cantidad / 100)
				self.carga = cr
		else:
			self.carga = 0
	    self._amount_all()

	@api.depends('order_line.price_total')
	def _amount_all(self):
		"""
		Compute the total amounts of the SO.
		"""
		for order in self:
			car = 0
			if self.metodo_pago.aplicar_cargos == True:
				if self.metodo_pago.fees_tipo == 'fixed':
					car = self.metodo_pago.fees_cantidad
				if self.metodo_pago.fees_tipo == 'percentage':
					base = self.amount_untaxed
					impuestos = self.amount_tax 
					car = (base + impuestos) * (self.metodo_pago.fees_cantidad / 100)
			else:
				car = 0
			amount_untaxed = amount_tax = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax
			order.update({
				'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
				'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
				'amount_total': amount_untaxed + amount_tax + car,
			})