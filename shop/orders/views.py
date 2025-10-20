from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from .forms import OrderCreationForm
from cart.cart import CartService
from .tasks import order_created
from product.models import Product
from django.http import Http404

def order_create(request):

    cart = CartService(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.save()
            order_created.delay(order.id)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
                product = item['product'] # добавил 3 строчки для уменьшения количества при заказе
                product.quantity -= item['quantity'] #
                product.save() #
            cart.clear()
            return render(request, 'orders/created.html', {'orders': order})

    else:
        form = OrderCreationForm()


    return render(request, 'orders/create.html', {
        'cart': cart, 'form': form})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    order_detail = {
        'order': order,
        'order_accessible': True,
    }

    return render(request, 'orders/order_detail.html', order_detail)


def imitation_payment(request,order_id):
    try:
        order = get_object_or_404(Order, id= order_id)
    except Http404:
        return redirect('product:product_list')

    if not order.paid:
        order.paid = True
        order.save()
        order_created(order_id)

    return render(request, 'orders/successful_payment.html',{'order':order})

