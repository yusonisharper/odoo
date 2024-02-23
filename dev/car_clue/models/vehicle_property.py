from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta


class vehicle_property(models.Model):
    _name = "vehicle.property"
    _description = "vehicle description"
    _order = "id desc"

    license_plate = fields.Char("license plate", index=True, required=True, copy=False)
    license_plate_state = fields.Char("license plate state", required=True, copy=False)
    make = fields.Char(string='vehicle brand')
    model = fields.Char(string="vehicle model")
    year = fields.Integer(string="manufacture year")
    color = fields.Selection(string="color", selection=[('black', 'Black'), ('gray', 'Gray'), ('white', 'White'), ('blue', 'Blue'), ('green', 'Green')])
    body_type = fields.Selection(string="body type", selection=[('sedan', 'Sedan'), ('suv', "SUV"), ('truck', 'Truck'), ('rv', 'RV')])
    VIN = fields.Char("vehicle identification number")
    name = fields.Char('vehicle', required=True, readonly=True, compute="_compute_name")
    description = fields.Text('description')
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'),
                                                         ('confirm', 'Confirm'),
                                                         ('vehicle_discovered', 'Vehicle Discovered'),
                                                         ('finished', 'Finished'),
                                                         ('canceled', 'Canceled')],
                             required=True, copy=False, default='draft', readonly=True)
    suspects = fields.Many2many("vehicle.suspect", string="suspects")
    curr_location = fields.One2Many("vehicle.location", "vehicle_id", string="vehicle's latest location")

    @api.onchange('year', 'make', 'model', 'color')
    def _compute_name(self):
        for record in self:
            record.name = record.year + record.make + record.model + record.color