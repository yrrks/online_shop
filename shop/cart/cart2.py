from decimal import Decimal
from django.conf import settings
from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price_float(self):
        """Возвращает общую сумму как float"""
        return float(self.get_total_price())

    def get_item_total_float(self, product):
        """Возвращает сумму за товар как float"""
        product_id = str(product.id)
        if product_id in self.cart:
            price = Decimal(self.cart[product_id]['price'])
            quantity = self.cart[product_id]['quantity']
            return float(price * quantity)
        return 0.0

    # Добавляем метод для получения данных корзины без Decimal
    def get_cart_data(self):
        """Возвращает данные корзины в сериализуемом формате"""
        cart_data = {
            'total_price': self.get_total_price_float(),
            'items_count': len(self),
            'items': []
        }

        for product_id, item_data in self.cart.items():
            product = Product.objects.get(id=product_id)
            price = Decimal(item_data['price'])
            quantity = item_data['quantity']
            total_price = price * quantity

            cart_data['items'].append({
                'product_id': int(product_id),
                'product_name': product.name,
                'quantity': quantity,
                'price': float(price),
                'total_price': float(total_price)
            })

        return cart_data

