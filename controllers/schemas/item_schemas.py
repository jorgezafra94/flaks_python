from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Integer(required=True)


class ItemUpdateSchema(Schema):
    price = fields.Float()
    name = fields.Str()
