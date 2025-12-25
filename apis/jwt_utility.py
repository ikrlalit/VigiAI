import jwt, datetime
from django.conf import settings

def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
