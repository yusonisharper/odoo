from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta


class vehicle_location(models.Model):
    _name = "vehicle.location"
    _description = "vehicle current location"
    _order = "id desc"

    name = fields.Char('suspect name', required=True, translate=True)
    description = fields.Text('description')
    longitude = fields.Float("longitude")
    latitude = fields.Float("latitude")
    vehicle_id = fields.Many2one("vehicle.property")