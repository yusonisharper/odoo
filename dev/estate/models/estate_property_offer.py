from odoo import api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, readonly=True, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer("Validity", default=7, store=True)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer_price is strictly a positive number.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def accept(self):
        for offer in self:
            if offer.status != 'accepted' and offer.property_id.offer_accepted == True:
                raise UserError("Only one offer can be accepted!")
                continue
            offer.status = 'accepted'
            offer.property_id.offer_accepted = True
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def refuse(self):
        for offer in self:
            if offer.property_id.offer_accepted == True and offer.status == 'accepted':
                offer.property_id.offer_accepted = False
                offer.property_id.selling_price = 0
                offer.property_id.buyer_id = ''
            offer.status = 'refused'

    @api.model
    def create(self, vals):
        prop = self.env['estate.property'].browse(vals['property_id'])
        prop.state = 'offer_received'
        for offer in prop.offer_ids:
            if vals['price'] < offer.price:
                raise UserError("Offer price must be higher than %.2f" % vals['price'])
        return super(estate_property_offer, self).create(vals)
