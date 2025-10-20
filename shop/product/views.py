from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from wishlist.models import Wishlist
from cart.forms import CartAddProductForm
from django.http import Http404

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            favorite_product_ids = wishlist.products.values_list('id', flat=True)
        except Wishlist.DoesNotExist:
            favorite_product_ids = []
    else:
        favorite_product_ids = []

    if category_slug:
        try:
            category = get_object_or_404(Category,slug=category_slug)
        except Http404:
            return redirect('product:product_list')
        descendants = category.get_descendants(include_self=True)
        products = products.filter(category__in=descendants)

    return render(request,'product/list.html',{'category': category,
                                                    'categories': categories, 'products': products,
                                               'favorite_product_ids': favorite_product_ids})

def product_detail(request, id, slug):
    try:
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
    except Http404:
        return redirect('product:product_list')

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            favorite_product_ids = wishlist.products.values_list('id', flat=True)
        except Wishlist.DoesNotExist:
            favorite_product_ids = []
    else:
        favorite_product_ids = []

    cart_product_form = CartAddProductForm()
    max_quantity = product.quantity
    additional_images = product.images.all()

    return render(request, 'product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form,
                                                        'max_quantity': max_quantity,
                                                        'additional_images':additional_images,
                                                   'favorite_product_ids': favorite_product_ids})

