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

class StaffUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/warehouse/'):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            elif not (request.user.is_staff or request.user.is_superuser):
                return redirect('products:product_list')

        if request.user.is_authenticated and (request.user.is_staff and not request.user.is_superuser):

            if (not request.path.startswith('/warehouse/') and
                    not request.path.startswith('/admin/') and
                    not request.path.startswith('/accounts/')):
                return redirect('warehouse:orders_manager')

        return self.get_response(request)