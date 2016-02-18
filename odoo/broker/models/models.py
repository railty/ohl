# -*- coding: utf-8 -*-

from openerp import models, fields, api

class broker(models.Model):
    _name = 'broker.broker'

    name = fields.Char()

class agent(models.Model):
    _name = 'broker.agent'

    name = fields.Char()
