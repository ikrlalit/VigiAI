from django.http import JsonResponse
from apis.jwt_utility import decode_token

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            try:
                payload = decode_token(auth.split(" ")[1])
                request.user_id = payload["user_id"]
                request.role = payload["role"]
            except Exception:
                return JsonResponse({"error": "Invalid token"}, status=401)
        else:
            request.user_id = None
            request.role = None

        return self.get_response(request)
