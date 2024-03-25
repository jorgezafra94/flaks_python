from marshmallow import Schema
from marshmallow.fields import Str, Float, Nested, Int, List


class PlainStoreSchema(Schema):
    id = Int(dump_only=True)
    name = Str(required=True)


class PlainItemSchema(Schema):
    id = Int(dump_only=True)
    name = Str(required=True)
    price = Float(required=True)


class ItemUpdateSchema(Schema):
    price = Float()
    name = Str()


class ItemSchema(PlainItemSchema):
    store_id = Int(required=True, load_only=True)
    store = Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = List(Nested(PlainItemSchema(), dump_only=True))
