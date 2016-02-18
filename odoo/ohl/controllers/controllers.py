# -*- coding: utf-8 -*-
from openerp import http

# class Ohl(http.Controller):
#     @http.route('/ohl/ohl/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ohl/ohl/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ohl.listing', {
#             'root': '/ohl/ohl',
#             'objects': http.request.env['ohl.ohl'].search([]),
#         })

#     @http.route('/ohl/ohl/objects/<model("ohl.ohl"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ohl.object', {
#             'object': obj
#         })