# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import ValidationError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    @api.constrains('company_id')
    def _check_company_id(self):
        super(PaymentAcquirer, self)._check_company_id()
        for rec in self:
            order = self.env['sale.order'].search(
                [('payment_acquirer_id', '=', rec.id),
                 ('company_id', '!=', False),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if order:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Payment Acquirer is assigned to Sales Order '
                      '%s.' % order.name))
