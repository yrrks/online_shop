from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from product.models import Product
from .cart import CartService
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'item_total': cart.get_item_total_float(product),
                'cart_total': cart.get_total_price_float(),
                'cart_length': len(cart)
            })

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid form'})

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.get_total_price_float(),
            'cart_length': len(cart)
        })

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = CartService(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html', {'cart': cart})