from django import template

register = template.Library()


@register.filter
def product_plural(value):
    """
    Возвращает правильную форму слова 'товар' в зависимости от количества
    1 товар, 2 товара, 5 товаров и т.д.
    """
    try:
        count = int(value)
    except (ValueError, TypeError):
        return "товаров"

    if count == 0:
        return "товаров"

    last_digit = count % 10
    last_two_digits = count % 100

    # Исключения для чисел 11-14
    if 11 <= last_two_digits <= 14:
        return "товаров"

    if last_digit == 1:
        return "товар"
    elif 2 <= last_digit <= 4:
        return "товара"
    else:
        return "товаров"


@register.filter
def cart_items_plural(cart):
    """
    Специальный фильтр для корзины, который возвращает количество и правильную форму
    Использование: {{ cart|cart_items_plural }}
    """
    try:
        count = len(cart)
    except (TypeError, AttributeError):
        return "0 товаров"

    return f"{count} {product_plural(count)}"