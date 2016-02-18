# -*- coding: utf-8 -*-
from openerp import http

class Broker(http.Controller):
     @http.route('/broker/broker/', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/broker/broker/objects/', auth='public')
     def list(self, **kw):
         return http.request.render('broker.listing', {
             'root': '/broker/broker',
             'objects': http.request.env['broker.broker'].search([]),
         })

     @http.route('/broker/broker/objects/<model("broker.broker"):obj>/', auth='public')
     def object(self, obj, **kw):
         return http.request.render('broker.object', {
             'object': obj
         })
