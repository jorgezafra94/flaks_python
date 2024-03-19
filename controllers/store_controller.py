import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from controllers.schemas.store_schemas import StoreSchema

stores_blp = Blueprint("stores", __name__, description="Controller for stores")


@stores_blp.route("/stores/<store_id>")
class StoreView(MethodView):

    @stores_blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted successfully."}
        except KeyError:
            abort(404, message="Store not found.")


@stores_blp.route("/stores")
class StoresView(MethodView):

    @stores_blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @stores_blp.arguments(StoreSchema)
    @stores_blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
