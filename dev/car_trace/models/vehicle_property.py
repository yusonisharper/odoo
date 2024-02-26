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
    year = fields.Date(string="manufacture year", copy=False)
    color = fields.Selection(string="color", selection=[('black', 'Black'), ('gray', 'Gray'), ('white', 'White'), ('blue', 'Blue'), ('green', 'Green')])
    body_type = fields.Selection(string="body type", selection=[('sedan', 'Sedan'), ('suv', "SUV"), ('truck', 'Truck'), ('rv', 'RV')])
    VIN = fields.Char("VIN")
    name = fields.Char('vehicle', readonly=True, default="", compute="_compute_name")
    description = fields.Text('description')
    last_seen = fields.Date(string="last seen", copy=False, compute='_compute_last_seen_time')
    user_id = fields.Many2one('res.users', string='Handler', default=lambda self: self.env.user)
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'),
                                                         ('confirm', 'Confirm'),
                                                         ('vehicle_discovered', 'Vehicle Discovered'),
                                                         ('finished', 'Finished'),
                                                         ('canceled', 'Canceled')],
                             required=True, copy=False, default='draft', readonly=True)
    suspects = fields.Many2many("vehicle.suspect", string="suspects")
    curr_location = fields.One2many("vehicle.location", "vehicle_id", string="vehicle's latest location")

    @api.onchange('year', 'make', 'model', 'body_type', 'color')
    def _compute_name(self):
        for record in self:
            result = ""
            if record.year:
                result = result + str(record.year.year)
            if record.make:
                result = result + " " + record.make
            if record.model:
                result = result + " " + record.model
            if record.body_type:
                result = result + " " + record.body_type
            if record.color:
                result = result + ", " + record.color
            record.name = result

    @api.onchange('curr_location.create_date')
    def _compute_last_seen_time(self):
        for record in self:
            record.last_seen = max(record.curr_location.mapped('create_date'), default=0)
    def cancel(self):
        for record in self:
            if record.state == 'finished':
                raise UserError("Finished record cannot be canceled.")
                continue
            record.state = 'canceled'
        return True

    def confirm(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled record cannot be confirm.")
                continue
            record.state = 'confirm'
        return True

    def finish(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled record cannot be finish.")
                continue
            record.state = 'finished'
        return True