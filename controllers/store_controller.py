from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from controllers.schemas.store_schemas import StoreSchema
from models import db, StoreModel

stores_blp = Blueprint("stores", __name__, description="Controller for stores")


@stores_blp.route("/stores/<store_id>")
class StoreView(MethodView):

    @stores_blp.response(200, StoreSchema)
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store

    @stores_blp.response(204)
    def delete(self, store_id):
        store = db.session.get(StoreModel, store_id)
        db.session.delete(store)
        db.session.commit()

    @stores_blp.arguments(StoreSchema)
    @stores_blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = db.session.get(StoreModel, store_id)
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(**store_data)
        db.session.add(store)
        db.session.commit()
        return store


@stores_blp.route("/stores")
class StoresView(MethodView):

    @stores_blp.response(200, StoreSchema(many=True))
    def get(self):
        return db.session.query(StoreModel).all()

    @stores_blp.arguments(StoreSchema)
    @stores_blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")
        return store
