from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from controllers.schemas import PlainTagSchema, TagSchema
from models import db, TagModel, StoreModel

tags_blp = Blueprint("tags", __name__, description="controller for tags")


@tags_blp.route("/stores/<store_id>/tags")
class TagView(MethodView):

    @tags_blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store.tags.all()

    @tags_blp.arguments(PlainTagSchema)
    @tags_blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        store = db.get_or_404(StoreModel, store_id)
        tag = TagModel(**tag_data)
        tag.store_id = store.id
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred creating tag")
        return tag
