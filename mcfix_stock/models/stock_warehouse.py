# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        res = []
        names = super(StockWarehouse, self).name_get()
        multicompany_group = self.env.ref('base.group_multi_company')
        if multicompany_group not in self.env.user.groups_id:
            return names
        for name in names:
            rec = self.browse(name[0])
            name = '%s [%s]' % (name[1], name.company_id.name) if \
                name.company_id else name[1]
            res += [(rec.id, name)]
        return res

    @api.onchange('company_id')
    def onchange_company_id(self):
        self.view_location_id = False
        self.lot_stock_id = False
        self.route_ids = False
        self.wh_input_stock_loc_id = False
        self.wh_qc_stock_loc_id = False
        self.wh_output_stock_loc_id = False
        self.wh_pack_stock_loc_id = False
        self.mto_pull_id = False
        self.crossdock_route_id = False
        self.reception_route_id = False
        self.delivery_route_id = False
        self.resupply_wh_ids = False
        self.resupply_route_ids = False
        self.default_resupply_wh_id = False

    @api.multi
    @api.constrains('view_location_id', 'company_id')
    def _check_company_view_location_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.view_location_id and \
                    warehouse.company_id != warehouse.view_location_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'View Location must be the same.'))
        return True

    @api.multi
    @api.constrains('lot_stock_id', 'company_id')
    def _check_company_lot_stock_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.lot_stock_id and \
                    warehouse.company_id != warehouse.lot_stock_id.company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Location Stock must be the same.'))
        return True

    @api.multi
    @api.constrains('route_ids', 'company_id')
    def _check_company_route_ids(self):
        for warehouse in self.sudo():
            for stock_location_route in warehouse.route_ids:
                if warehouse.company_id and \
                        warehouse.company_id != stock_location_route.\
                        company_id:
                    raise ValidationError(
                        _('The Company in the Warehouse and in '
                          'Location Route must be the same.'))
        return True

    @api.multi
    @api.constrains('wh_input_stock_loc_id', 'company_id')
    def _check_company_wh_input_stock_loc_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.wh_input_stock_loc_id and \
                    warehouse.company_id != warehouse.wh_input_stock_loc_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Input Location must be the same.'))
        return True

    @api.multi
    @api.constrains('wh_qc_stock_loc_id', 'company_id')
    def _check_company_wh_qc_stock_loc_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.wh_qc_stock_loc_id and \
                    warehouse.company_id != warehouse.wh_qc_stock_loc_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Quality Control Location must '
                                        'be the same.'))
        return True

    @api.multi
    @api.constrains('wh_output_stock_loc_id', 'company_id')
    def _check_company_wh_output_stock_loc_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.wh_output_stock_loc_id and \
                    warehouse.company_id != warehouse.wh_output_stock_loc_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Output Location must be the same.'))
        return True

    @api.multi
    @api.constrains('wh_pack_stock_loc_id', 'company_id')
    def _check_company_wh_pack_stock_loc_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.wh_pack_stock_loc_id and \
                    warehouse.company_id != warehouse.wh_pack_stock_loc_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Packing Location must be the same.'))
        return True

    @api.multi
    @api.constrains('mto_pull_id', 'company_id')
    def _check_company_mto_pull_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.mto_pull_id and \
                    warehouse.company_id != warehouse.mto_pull_id.company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'MTO Rule must be the same.'))
        return True

    @api.multi
    @api.constrains('crossdock_route_id', 'company_id')
    def _check_company_crossdock_route_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.crossdock_route_id and \
                    warehouse.company_id != warehouse.crossdock_route_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Crossdock Rule must be the same.'))
        return True

    @api.multi
    @api.constrains('reception_route_id', 'company_id')
    def _check_company_reception_route_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.reception_route_id and \
                    warehouse.company_id != warehouse.reception_route_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Reception Route must be the same.'))
        return True

    @api.multi
    @api.constrains('delivery_route_id', 'company_id')
    def _check_company_delivery_route_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.delivery_route_id and \
                    warehouse.company_id != warehouse.delivery_route_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Delivery Route must be the same.'))
        return True

    @api.multi
    @api.constrains('resupply_wh_ids', 'company_id')
    def _check_company_resupply_wh_ids(self):
        for warehouse in self.sudo():
            for stock_warehouse in warehouse.resupply_wh_ids:
                if warehouse.company_id and \
                        warehouse.company_id != stock_warehouse.company_id:
                    raise ValidationError(
                        _('The Company in the Warehouse and in '
                          'Resupply Warehouse must be the same.'))
        return True

    @api.multi
    @api.constrains('resupply_route_ids', 'company_id')
    def _check_company_resupply_route_ids(self):
        for warehouse in self.sudo():
            for stock_location_route in warehouse.resupply_route_ids:
                if warehouse.company_id and \
                        warehouse.company_id != stock_location_route.\
                        company_id:
                    raise ValidationError(
                        _('The Company in the Warehouse and in '
                          'Resupply Route must be the same.'))
        return True

    @api.multi
    @api.constrains('default_resupply_wh_id', 'company_id')
    def _check_company_default_resupply_wh_id(self):
        for warehouse in self.sudo():
            if warehouse.company_id and warehouse.default_resupply_wh_id and \
                    warehouse.company_id != warehouse.default_resupply_wh_id.\
                    company_id:
                raise ValidationError(_('The Company in the Warehouse and in '
                                        'Default Resupply Warehouse must '
                                        'be the same.'))
        return True

    @api.constrains('company_id')
    def _check_company_id(self):
        for rec in self:
            rule = self.env['procurement.rule'].search(
                [('warehouse_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if rule:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Warehouse is assigned to Procurement Rule '
                      '%s.' % rule.name))
            rule = self.env['procurement.rule'].search(
                [('propagate_warehouse_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if rule:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Warehouse is assigned to Procurement Rule '
                      '%s.' % rule.name))
            location_route = self.env['stock.location.route'].search(
                [('supplied_wh_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if location_route:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Warehouse is assigned to Location Route '
                      '%s.' % location_route.name))
            location_route = self.env['stock.location.route'].search(
                [('supplier_wh_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if location_route:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Warehouse is assigned to Location Route '
                      '%s.' % location_route.name))
            location_route = self.env['stock.location.route'].search(
                [('warehouse_ids', 'in', [rec.id]),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if location_route:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Warehouse is assigned to Location Route '
                      '%s.' % location_route.name))
            warehouse = self.search(
                [('resupply_wh_ids', 'in', [rec.id]),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as it '
                      'is assigned as Resupply Warehouse in Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.search(
                [('default_resupply_wh_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as it '
                      'is assigned Default Resupply Warehouse in Warehouse '
                      '%s.' % warehouse.name))
