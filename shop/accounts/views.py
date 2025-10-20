from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, settings
from .forms import CustomUserCreationForm, CustomAuthenticatedForm, CodeConfirmForm
from django.contrib.auth.decorators import login_required
from cart.cart import CartService
from .tasks import get_confirm_code
from .models import ActivationCode


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product:product_list')
    else:
        form = CustomUserCreationForm()

    return render(request,'accounts/register.html',{'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product:product_list')

    if request.method == 'POST':
        form = CustomAuthenticatedForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #
            session_cart = request.session.get(settings.CART_SESSION_ID, {})
            #
            login(request, user)
            #
            cart = CartService(request)
            if session_cart:
                cart.merge_carts(session_cart)
            #
            # Очищаем сессионную корзину
            if settings.CART_SESSION_ID in request.session:
                del request.session[settings.CART_SESSION_ID]
                #
            return redirect('product:product_list')
    else:
        form = CustomAuthenticatedForm()

    return render(request,'accounts/login.html',{'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('product:product_list')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def activation_required(request):
    return render(request, 'accounts/activation_required.html')

@login_required
def get_confirm_code(request):
    code = ActivationCode.objects.get(user=request.user)
    code.generate_code()
    get_confirm_code.delay(request.user.id)

    return redirect('accounts:activation_required')


@login_required
def activate_account(request):
    user = request.user

    if request.method == 'POST':
        form = CodeConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            confirm_code = ActivationCode.objects.get(user=user).code
            if code == confirm_code:
                user.is_confirmed = True
                user.save()
                ActivationCode.objects.filter(user=user).delete()

                return redirect('product:product_list')

            else:
                form.add_error('code', 'Неверный код')
    else:
        form = CodeConfirmForm()

    return render(request, 'accounts/activation_required.html', {'form': form})


