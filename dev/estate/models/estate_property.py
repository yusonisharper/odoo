from odoo import fields, models
from dateutil import relativedelta

class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate description"
    _order = "id desc"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('description')
    postcode = fields.Integer('Postcode')
    date_availability = fields.Date('Available from', copy=False, default=fields.date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'), ])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('received', 'Offer Received'),
                                                  ('Accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True, copy=False, default='new')
    active = fields.Boolean('Active', default=True)
