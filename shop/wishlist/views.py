from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from product.models import Product, Category
from django.http import Http404, JsonResponse


@login_required
def wishlist_view(request):
    try:
        wishlist = get_object_or_404(Wishlist,user=request.user)
        wishlist_products = wishlist.products.all()
    except Http404:
        return redirect('product:product_list')


    return render(request, 'wishlist/wishlist.html', {
        'wishlist_products': wishlist_products,
        'wishlist': wishlist
    })


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        return JsonResponse({'success': False, 'error': 'Товар уже в избранном'})

    wishlist.products.add(product)
    return JsonResponse({'success': True})


def remove_from_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Товар не найден в избранном'})


