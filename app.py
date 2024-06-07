from flask import Flask
from flask_smorest import Api
from controllers.store_controller import stores_blp
from controllers.item_controller import items_blp
from controllers.tag_controller import tags_blp
from controllers.user_controller import users_blp
from config import config_option
from models import StoreModel, ItemModel, db, TagModel, UserModel
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from exceptions.jwt_handler import jwt_exceptions
import os


def create_app():
    app = Flask(__name__)
    load_config = config_option.get(os.getenv("FLASK_ENV", "Test"))
    app.config.from_object(load_config)

    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    api.register_blueprint(stores_blp)
    api.register_blueprint(items_blp)
    api.register_blueprint(tags_blp)
    api.register_blueprint(users_blp)

    jwt = JWTManager(app)
    jwt_exceptions(jwt)
    return app


App = create_app()

if __name__ == "__main__":
    App.run()
