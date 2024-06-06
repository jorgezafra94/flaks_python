from flask import jsonify

BLOCKLIST = set()


def jwt_validation(jwt):
    @jwt.token_in_blocklist_loader
    def check_jwt_validation(header, payload):
        return payload.get("jti") in BLOCKLIST


def jwt_exceptions(jwt):
    @jwt.revoked_token_loader
    def revoked_token_loader(header, payload):
        return (
            jsonify({"message": "the token has been revoked", "error": "token revoked"}),
            401
        )

    @jwt.expired_token_loader
    def expired_token_loader(header, payload):
        return (
            jsonify({"message": "the token has expired", "error": "token expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_loader(error):
        return (
            jsonify({"message": "signature verification failed", "error": "invalid token"}),
            401
        )

    @jwt.unauthorized_loader
    def missing_token(error):
        return (
            jsonify({"message": "unauthorized token", "error": "authorization missed"}),
            401
        )
