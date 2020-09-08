# -*- coding: utf-8 -*-

from odoo import api, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    
    def button_confirm(self):
        for order in self:
            res = super(PurchaseOrder, self).button_confirm()
            for record in model:
                partner_ids = env['res.company'].search([]).mapped('partner_id')
                if record.state == 'purchase' and record.partner_id in partner_ids.ids:
                    company = env['res.company'].search([('partner_id', '=', record.partner_id.id)])
                    sale_id = env['sale.order'].create({'partner_id': record.partner_id.id, 'company_id': company.id})
                    for line in record.order_line:
                        vals = {
                            'order_id': sale_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_qty,
                            'price_unit': line.product_id.lst_price,
                            'company_id': company.id
                        }
                        lines = env['sale.order.line'].create(vals)
        return res
           