from flask import Flask
from flask_restful import Resource, Api, request
from authentication import signup_user
from integrations import integrations_master
import mongoengine


mongoengine.connect("ProductCopilot")

app = Flask(__name__)
api = Api(app)


class Signup(Resource):
    def post(self):
        return signup_user(
            request.get_json()["user_name"],
            request.get_json()["pwd"],
            request.get_json()["full_name"],
            request.get_json()["company_product_offering"]
        )


class Integrations(Resource):
    def post(self):
        return integrations_master(
            request.headers.get("Authorization"),
            request.get_json()
        )


api.add_resource(Signup, "/signup")
api.add_resource(Integrations, "/integrations")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
