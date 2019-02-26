# -*- coding: utf-8 -*-
from odoo import http

# class Porcentaje(http.Controller):
#     @http.route('/porcentaje/porcentaje/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/porcentaje/porcentaje/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('porcentaje.listing', {
#             'root': '/porcentaje/porcentaje',
#             'objects': http.request.env['porcentaje.porcentaje'].search([]),
#         })

#     @http.route('/porcentaje/porcentaje/objects/<model("porcentaje.porcentaje"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('porcentaje.object', {
#             'object': obj
#         })