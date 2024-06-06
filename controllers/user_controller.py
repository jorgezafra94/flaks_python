from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from controllers.schemas import UserSchema
from models import db, UserModel

users_blp = Blueprint("users", __name__, description="Controller for users")


@users_blp.route("/user/registration")
class RegistrationView(MethodView):
    @users_blp.arguments(UserSchema)
    @users_blp.response(200, UserSchema)
    def post(self, user_data):
        if db.session.query(UserModel).filter(UserModel.username == user_data.get("username")).first():
            abort(409, message="User already exist")

        user = UserModel(
            username=user_data.get("username"),
            password=pbkdf2_sha256.hash(user_data.get("password"))
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred creating user")
        return user


@users_blp.route("/user/login")
class LoginView(MethodView):
    @users_blp.arguments(UserSchema)
    def post(self, user_data):
        user = db.session.query(UserModel).filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid credentials")


@users_blp.route("/user/logout")
class LogoutView(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt_identity()
        [].add(jti)
        return {"message": "successfully logged out"}


@users_blp.route("/user/<user_id>")
class UserView(MethodView):
    @users_blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = db.get_or_404(UserModel, user_id)
        return user

    @users_blp.response(204)
    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = db.session.get(UserModel, user_id)
        db.session.delete(user)
        db.session.commit()
