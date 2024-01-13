from odoo import fields, models

class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate description"
    _order = "id desc"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('description')
    postcode = fields.Integer('Postcode')
    date_availability = fields.Date('Data Availability')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'), ])

