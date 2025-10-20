from decimal import Decimal
from django.conf import settings
from product.models import Product
from .models import CartItem, Cart


class CartService:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        # Загружаем корзину из БД для авторизованных пользователей
        if request.user.is_authenticated:
            self.cart = self._load_from_db()
            # Сохраняем в сессию для консистентности
            self.session['cart'] = self.cart
            self.session.modified = True
        else:
            # Для анонимных - из сессии
            cart = self.session.get('cart', {})
            self.cart = cart
            self.session['cart'] = cart

    def __iter__(self):
        return self._iter_cart()

    def _iter_cart(self):
        """Универсальный итератор для работы с корзиной"""
        if self.request.user.is_authenticated:
            # Работа с базой данных для авторизованных пользователей
            try:
                cart = Cart.objects.get(user=self.request.user)
                cart_items = CartItem.objects.filter(cart=cart).select_related('product')
                for item in cart_items:
                    yield {
                        'product': item.product,
                        'quantity': item.quantity,
                        'price': item.product.price,
                        'total_price': item.product.price * item.quantity,
                        'id': item.id,
                        'max_quantity': item.product.quantity
                    }
            except Cart.DoesNotExist:
                return
        else:
            # Работа с сессией для анонимных пользователей
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            product_dict = {str(product.id): product for product in products}

            for product_id, item_data in self.cart.items():
                product = product_dict.get(product_id)
                if product:
                    yield {
                        'product': product,
                        'quantity': item_data['quantity'],
                        'price': Decimal(str(item_data['price'])),
                        'total_price': Decimal(str(item_data['price'])) * item_data['quantity'],
                        'id': product_id,
                        'max_quantity': product.quantity
                    }
    def _get_cart_data(self):
        """Получаем данные корзины из сессии или БД"""
        if self.user.is_authenticated:
            return self._load_from_db()
        else:
            return self.session.get(settings.CART_SESSION_ID, {})

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()



    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """Сохраняем в сессию и БД"""
        self.session.modified = True
        if self.request.user.is_authenticated:
            self._save_to_db()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

            # Удаляем из БД если пользователь авторизован
            if self.request.user.is_authenticated:  # ← исправлено на request.user
                try:
                    cart = Cart.objects.get(user=self.request.user)  # ← исправлено
                    CartItem.objects.filter(cart=cart, product=product).delete()
                except Cart.DoesNotExist:
                    pass

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищаем корзину полностью"""
        self.cart = {}
        if self.request.user.is_authenticated:  # ← исправлено
            try:
                cart = Cart.objects.get(user=self.request.user)  # ← исправлено
                CartItem.objects.filter(cart=cart).delete()
            except Cart.DoesNotExist:
                pass
        else:
            del self.session[settings.CART_SESSION_ID]
        self.save()

    def _load_from_db(self):
        """Загружаем корзину из БД через модель Cart"""
        cart_data = {}
        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
                cart_items = CartItem.objects.filter(cart=cart)
                for item in cart_items:
                    cart_data[str(item.product.id)] = {
                        'quantity': item.quantity,
                        'price': str(item.product.price)
                    }
            except Cart.DoesNotExist:
                pass
        return cart_data

    def _save_to_db(self):
        """Сохраняем корзину в БД через модель Cart"""
        if not self.request.user.is_authenticated:
            return

        # Получаем или создаем корзину для пользователя
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                # Фильтруем через cart
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,  # Используем cart вместо user
                    product=product,
                    defaults={'quantity': item_data['quantity']}
                )
                if not created:
                    cart_item.quantity = item_data['quantity']
                    cart_item.save()
            except Product.DoesNotExist:
                # Если товар удален, пропускаем
                continue

    def merge_carts(self, session_cart):
        """Переносим корзину из сессии в БД при логине"""
        if not self.request.user.is_authenticated:
            return

        # Получаем или создаем корзину для пользователя
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        for product_id, item_data in session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
                # Фильтруем через cart
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,  # Используем cart вместо user
                    product=product,
                    defaults={'quantity': item_data['quantity']}
                )
                if not created:
                    # Если товар уже есть в БД, заменяем количество
                    cart_item.quantity = item_data['quantity']
                    cart_item.save()
            except Product.DoesNotExist:
                continue

        # Обновляем данные корзины из БД
        self.cart = self._load_from_db()
        self.save()

    def get_total_price_float(self):
        """Возвращает общую сумму как float для JSON"""
        return float(self.get_total_price())

    def get_item_total_float(self, product):
        """Возвращает сумму по конкретному товару как float для JSON"""
        product_id = str(product.id)
        if product_id in self.cart:
            item = self.cart[product_id]
            return float(Decimal(item['price']) * item['quantity'])
        return 0.0



#    def get_cart(self):
#        """Итератор для работы с базой данных"""
#        if self.request.user.is_authenticated():
#            cart = Cart.objects.get(user=self.request.user)
#            cart_items = CartItem.objects.filter(cart=cart).select_related('product')
#        else:
#            cart = self.session.get(settings.CART_SESSION_ID, {})