# -*- coding: utf-8 -*-

from openerp import models, fields, api

class broker(models.Model):
    _name = 'ohl.broker'

    name = fields.Char()

class agent(models.Model):
    _name = 'ohl.agent'

    name = fields.Char()
    broker_id = fields.Many2one('ohl.broker', string="Broker")
