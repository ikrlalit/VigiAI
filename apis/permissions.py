from django.http import JsonResponse

def admin_only(view):
    def wrapper(request, *args, **kwargs):
        if request.role != "admin":
            return JsonResponse({"error": "Admin only"}, status=403)
        return view(request, *args, **kwargs)
    return wrapper

def admin_or_analyst(view):
    def wrapper(request, *args, **kwargs):
        if request.role in ("admin", "analyst"):
            return view(request, *args, **kwargs)
        return JsonResponse({"error": "Forbidden"}, status=403)
    return wrapper