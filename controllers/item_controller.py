import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from controllers.schemas.item_schemas import ItemSchema, ItemUpdateSchema

items_blp = Blueprint("items", __name__, description="Controller for items")


@items_blp.route("/items/<item_id>")
class ItemView(MethodView):
    @items_blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted successfully."}
        except KeyError:
            abort(404, message="Item not found.")

    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found")


@items_blp.route("/items")
class StoresView(MethodView):
    @items_blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @items_blp.arguments(ItemSchema)
    @items_blp.response(200, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(400, message="Store already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item
