from flask import Flask
from flask_smorest import Api
from controllers.store_controller import stores_blp
from controllers.item_controller import items_blp
from controllers.tag_controller import tags_blp
from config import config_option
from models import StoreModel, ItemModel, db, TagModel, UserModel
import os

app = Flask(__name__)
load_config = config_option.get(os.getenv("FLASK_ENV", "Test"))
app.config.from_object(load_config)

db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)
api.register_blueprint(stores_blp)
api.register_blueprint(items_blp)
api.register_blueprint(tags_blp)

if __name__ == "__main__":
    app.run()
