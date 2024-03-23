from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from controllers.schemas.item_schemas import ItemSchema, ItemUpdateSchema
from models import db, ItemModel

items_blp = Blueprint("items", __name__, description="Controller for items")


@items_blp.route("/items/<item_id>")
class ItemView(MethodView):
    @items_blp.response(200, ItemSchema)
    def get(self, item_id):
        item = db.get_or_404(ItemModel, item_id)
        return item

    @items_blp.response(204)
    def delete(self, item_id):
        item = db.session.get(ItemModel, item_id)
        db.session.delete(item)
        db.session.commit()

    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = db.session.get(ItemModel, item_id)
        if item:
            item.name = item_data.get("name", item.name)
            item.price = item_data.get("price", item.price)
        else:
            item = ItemModel(**item_data)
        db.session.add(item)
        db.session.commit()
        return item


@items_blp.route("/items")
class ItemsView(MethodView):
    @items_blp.response(200, ItemSchema(many=True))
    def get(self):
        return db.session.query(ItemModel).all()

    @items_blp.arguments(ItemSchema)
    @items_blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")
        return item
