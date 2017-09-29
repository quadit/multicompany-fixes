# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import ValidationError


class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        res = []
        names = super(StockLocationRoute, self).name_get()
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
        self.pull_ids = False
        self.supplied_wh_id = False
        self.supplier_wh_id = False
        self.warehouse_ids = False

    @api.multi
    @api.constrains('pull_ids', 'company_id')
    def _check_company_pull_ids(self):
        for location_route in self.sudo():
            for procurement_rule in location_route.pull_ids:
                if location_route.company_id and \
                        location_route.company_id != procurement_rule.\
                        company_id:
                    raise ValidationError(
                        _('The Company in the Location Route and in '
                          'Procurement Rule must be the same.'))
        return True

    @api.multi
    @api.constrains('supplied_wh_id', 'company_id')
    def _check_company_supplied_wh_id(self):
        for location_route in self.sudo():
            if location_route.company_id and location_route.supplied_wh_id and\
                    location_route.company_id != location_route.\
                    supplied_wh_id.company_id:
                raise ValidationError(
                    _('The Company in the Location Route and in '
                      'Supplied Warehouse must be the same.'))
        return True

    @api.multi
    @api.constrains('supplier_wh_id', 'company_id')
    def _check_company_supplier_wh_id(self):
        for location_route in self.sudo():
            if location_route.company_id and location_route.supplier_wh_id and\
                    location_route.company_id != location_route.\
                    supplier_wh_id.company_id:
                raise ValidationError(
                    _('The Company in the Location Route and in '
                      'Supplying Warehouse must be the same.'))
        return True

    @api.multi
    @api.constrains('warehouse_ids', 'company_id')
    def _check_company_warehouse_ids(self):
        for location_route in self.sudo():
            for stock_warehouse in location_route.warehouse_ids:
                if location_route.company_id and \
                        location_route.company_id != stock_warehouse.\
                        company_id:
                    raise ValidationError(
                        _('The Company in the Location Route and in '
                          'Warehouse must be the same.'))
        return True

    @api.constrains('company_id')
    def _check_company_id(self):
        for rec in self:
            rule = self.env['procurement.rule'].search(
                [('route_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if rule:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location Route is assigned to Procurement Rule '
                      '%s.' % rule.name))
            warehouse = self.env['stock.warehouse'].search(
                [('route_ids', 'in', [rec.id]),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location Route is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('crossdock_route_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Crossdock Route is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('reception_route_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Reception Route is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('delivery_route_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Delivery Route is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('resupply_route_ids', 'in', [rec.id]),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Resupply Route is assigned to Warehouse '
                      '%s.' % warehouse.name))


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        res = []
        names = super(StockLocation, self).name_get()
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
        self.location_id = False
        self.child_ids = False

    @api.multi
    @api.constrains('location_id', 'company_id')
    def _check_company_location_id(self):
        for location in self.sudo():
            if location.company_id and location.location_id and \
                    location.company_id != location.location_id.company_id:
                raise ValidationError(_('The Company in both Locations '
                                        'must be the same.'))
        return True

    @api.multi
    @api.constrains('child_ids', 'company_id')
    def _check_company_child_ids(self):
        for location in self.sudo():
            for stock_location in location.child_ids:
                if location.company_id and \
                        location.company_id != stock_location.company_id:
                    raise ValidationError(
                        _('The Company in both Locations '
                          'must be the same.'))
        return True

    @api.constrains('company_id')
    def _check_company_id(self):
        for rec in self:
            rule = self.env['procurement.rule'].search(
                [('location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if rule:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Procurement Rule '
                      '%s.' % rule.name))
            rule = self.env['procurement.rule'].search(
                [('location_src_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if rule:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Procurement Rule '
                      '%s.' % rule.name))
            inventory = self.env['stock.inventory'].search(
                [('location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if inventory:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Inventory '
                      '%s.' % inventory.name))
            quant = self.env['stock.quant'].search(
                [('location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if quant:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Quant '
                      '%s.' % quant.name))
            quant = self.env['stock.quant'].search(
                [('negative_dest_location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if quant:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned as Negative Destination to Quant '
                      '%s.' % quant.name))
            location = self.search(
                [('location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if location:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Location '
                      '%s.' % location.name))
            location = self.search(
                [('child_ids', 'in', [rec.id]),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if location:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned as child to Location '
                      '%s.' % location.name))
            warehouse = self.env['stock.warehouse'].search(
                [('view_location_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('lot_stock_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('wh_input_stock_loc_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('wh_qc_stock_loc_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('wh_output_stock_loc_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))
            warehouse = self.env['stock.warehouse'].search(
                [('wh_pack_stock_loc_id', '=', rec.id),
                 ('company_id', '!=', rec.company_id.id)], limit=1)
            if warehouse:
                raise ValidationError(
                    _('You cannot change the company, as this '
                      'Location is assigned to Warehouse '
                      '%s.' % warehouse.name))