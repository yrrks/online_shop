from django.shortcuts import redirect


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/activation-required/',  

        ]
        if (request.user.is_authenticated and
                not request.user.is_confirmed and
                request.path not in allowed_paths):
            return redirect('accounts:activation-required')

        return self.get_response(request)