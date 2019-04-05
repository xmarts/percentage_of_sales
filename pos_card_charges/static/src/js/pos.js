odoo.define('pos_card_charges.pos', function (require) {
	"use strict";
    var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var PopupWidget = require('point_of_sale.popups');
	var DB = require('point_of_sale.DB');

    var QWeb = core.qweb;
    var _t = core._t;

	models.load_fields("account.journal", ['apply_charges','fees_amount','fees_type','optional']);

	screens.PaymentScreenWidget.include({
		render_paymentlines: function() {
            var self  = this;
            var order = this.pos.get_order();
            if (!order) {
                return;
            }

            var lines = order.get_paymentlines();
            var due   = order.get_due();
            var extradue = 0;
            var charge = 0;
            if (due && lines.length  && due !== order.get_due(lines[lines.length-1])) {
                extradue = due;
            }

            if(self.pos.config.enable_card_charges){
		        if (order.selected_paymentline && order.selected_paymentline.cashregister.journal.apply_charges) {
		        	if(order.selected_paymentline.cashregister.journal.optional){
		        	}else{
			        	if(order.selected_paymentline.cashregister.journal.fees_type === _t('percentage')){
			        		charge = (order.selected_paymentline.get_amount() * order.selected_paymentline.cashregister.journal.fees_amount) / 100;
			        	} else if(order.selected_paymentline.cashregister.journal.fees_type === _t('fixed')){
			        		charge = order.selected_paymentline.cashregister.journal.fees_amount;
			        	}
		        	}
		        	order.selected_paymentline.set_payment_charge(charge.toFixed(2));
		        }
	        }

            this.$('.paymentlines-container').empty();
            var lines = $(QWeb.render('PaymentScreen-Paymentlines', {
                widget: this,
                order: order,
                paymentlines: lines,
                extradue: extradue,
            }));
            lines.on('click','.delete-button',function(){
                self.click_delete_paymentline($(this).data('cid'));
            });

            lines.on('click','.paymentline',function(){
                self.click_paymentline($(this).data('cid'));
            });

            lines.on('input','.payment_charge_input',function(){
	        	order.selected_paymentline.set_payment_charge($(this).val());
	        });

            if(self.pos.config.enable_card_charges) {
		        lines.on('focus','.payment_charge_input',function(){
		        	window.document.body.removeEventListener('keypress',self.keyboard_handler);
	                window.document.body.removeEventListener('keydown',self.keyboard_keydown_handler);
		        });
		        lines.on('focusout','.payment_charge_input',function(){
		        	window.document.body.addEventListener('keypress',self.keyboard_handler);
	                window.document.body.addEventListener('keydown',self.keyboard_keydown_handler);
		        });
	        }

            lines.appendTo(this.$('.paymentlines-container'));
        },
        validate_order: function(force_validation) {
            var self = this;
            if (this.order_is_valid(force_validation)) {
                if(self.pos.config.enable_card_charges){
                    this.add_charge_product();
                }
                this.finalize_validation();
            }
        },
        add_charge_product: function(){
        	var self = this;
        	var selectedOrder = self.pos.get_order();
            var paylines = selectedOrder.get_paymentlines();
            var charge_exist = false;
            var total_charges = 0;
            if(paylines){
            	paylines.map(function(payline){
            		if(payline.cashregister.journal.apply_charges){
	            		var paycharge = Number(payline.get_payment_charge());
	            		total_charges += paycharge;
	            		payline.set_amount(payline.get_amount() + paycharge);
            		}
            	});
            	if(total_charges > 0){
	 				var product = self.pos.db.get_product_by_id(self.pos.config.payment_product_id[0]);
	 				if(product){
    					selectedOrder.add_product(product, {
    						quantity: 1,
    						price: total_charges,
    					})
    				}
            	}
            }
        },
	});

    var _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        set_payment_charge: function(val){
        	this.set('payment_charge',val);
        },
        get_payment_charge: function(val){
        	return this.get('payment_charge');
        },
    });
});