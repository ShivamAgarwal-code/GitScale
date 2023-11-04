from models import User
from mongoengine.errors import NotUniqueError
import jwt
from flask import make_response, jsonify

def signup_user(user_name, password, full_name, product_offering):
    try:
        user = User(
            username=user_name,
            password=password,
            full_name=full_name,
            company_product_offering=product_offering
        )
        user.save()
        token = jwt.encode(
            {"username": user_name, "full_name": full_name},
            "efgiul211uif13r321342fhruedslrih3lfch3ruic3re",
            "HS256"
        )
        return make_response(jsonify({"auth_creds": token}), 200)
    
    except NotUniqueError:
        token = jwt.encode(
            {"username": user_name, "full_name": full_name},
            "efgiul211uif13r321342fhruedslrih3lfch3ruic3re",
            "HS256"
        )
        return make_response(jsonify({"auth_creds": token}), 200)
    

def validate_user(token:str, is_admin:bool=False):
    unauthorizedResponse = make_response(
        jsonify({"message": "Invalid or Expired User token"}), 401
    )
    try:
        user_name = jwt.decode(
            token, "efgiul211uif13r321342fhruedslrih3lfch3ruic3re", ["HS256"]
        )["username"]
        user = User.objects(username=user_name).first()
        if user is not None:
            return True, user
        return False, unauthorizedResponse
    except Exception:
        return False, unauthorizedResponse