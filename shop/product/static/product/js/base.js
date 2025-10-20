function updateCartHeader(cartTotal, cartLength) {
        const cartItemsCount = document.getElementById('cart-items-count');
        const cartTotalHeader = document.getElementById('cart-total-header');
        const cartItemsText = document.getElementById('cart-items-text');  // Добавлено
        const cartHeader = document.getElementById('cart-header');

        if (cartItemsCount && cartTotalHeader && cartItemsText) {
            // Обновляем числа и текст склонения
            cartItemsCount.textContent = cartLength;
            cartTotalHeader.textContent = parseFloat(cartTotal).toFixed(2);
            cartItemsText.textContent = getRussianPlural(cartLength);  // Обновляем склонение
        } else if (cartItemsCount && cartTotalHeader) {
            // Fallback если нет cartItemsText
            cartItemsCount.textContent = cartLength;
            cartTotalHeader.textContent = parseFloat(cartTotal).toFixed(2);
        }

        // Обработка пустой корзины
        if (cartLength === 0 && cartHeader) {
            cartHeader.innerHTML = 'Корзина пуста';
        }
    }

    // Функция для русского склонения
function getRussianPlural(count) {
    if (count === 0) return 'товаров';

    const lastDigit = count % 10;
    const lastTwoDigits = count % 100;

    if (11 <= lastTwoDigits && lastTwoDigits <= 14) return 'товаров';
    if (lastDigit === 1) return 'товар';
    if (lastDigit >= 2 && lastDigit <= 4) return 'товара';
    return 'товаров';


document.addEventListener('DOMContentLoaded', function() {
    // Помечаем текущую страницу как активную в навигации
    const currentUrl = window.location.pathname;

    // Для категорий
    const categoryLinks = document.querySelectorAll('.category-list a, .sidebar-categories a');
    categoryLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });

    // Убираем стили посещенных ссылок
    const allLinks = document.querySelectorAll('a');
    allLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Сохраняем состояние активной ссылки
            localStorage.setItem('activeLink', this.getAttribute('href'));
        });
    });
});