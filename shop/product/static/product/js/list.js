document.addEventListener('DOMContentLoaded', function() {
    // ===== ОБРАБОТКА КАТЕГОРИЙ =====
    const toggleButtons = document.querySelectorAll('.category-toggle');

    toggleButtons.forEach(toggle => {
        const listItem = toggle.closest('.category-item');
        const childrenList = listItem.querySelector('.children');

        // Обработчик клика по стрелке
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (childrenList.style.display === 'none' || !childrenList.style.display) {
                childrenList.style.display = 'block';
                toggle.innerHTML = '▼';
                toggle.classList.add('expanded');
            } else {
                childrenList.style.display = 'none';
                toggle.innerHTML = '▶';
                toggle.classList.remove('expanded');
            }
        });
    });

    // Автоматически раскрываем путь до текущей категории
    function expandPathToCurrentCategory() {
        const currentCategoryItem = document.querySelector('#sidebar li.selected');
        if (currentCategoryItem) {
            let parent = currentCategoryItem.parentElement;
            while (parent && parent.classList.contains('children')) {
                const parentItem = parent.parentElement;
                const toggle = parentItem.querySelector('.category-toggle');
                const childrenList = parentItem.querySelector('.children');
                if (toggle && childrenList) {
                    childrenList.style.display = 'block';
                    toggle.innerHTML = '▼';
                    toggle.classList.add('expanded');
                }
                parent = parentItem.parentElement;
            }
        }
    }

    expandPathToCurrentCategory();

    // Автоматически раскрываем родительские категории если выбрана дочерняя (дополнительная проверка)
    const currentPath = window.location.pathname;
    const activeLinks = document.querySelectorAll('.category-link');

    activeLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');

            // Раскрываем родительские категории
            let parentList = link.closest('.children');
            while (parentList) {
                parentList.style.display = 'block';
                const prevToggle = parentList.previousElementSibling?.querySelector('.category-toggle');
                if (prevToggle) {
                    prevToggle.innerHTML = '▼';
                    prevToggle.classList.add('expanded');
                }
                parentList = parentList.parentElement.closest('.children');
            }
        }
    });

    // Плавная анимация появления товаров
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // ===== ОБРАБОТКА ИЗБРАННОГО =====
    const favoriteBtns = document.querySelectorAll('.favorite-btn');

    if (favoriteBtns.length > 0) {
        favoriteBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                const productId = this.getAttribute('data-product-id');
                const icon = this.querySelector('.favorite-icon');

                // Переключаем состояние
                const isActive = icon.classList.contains('favorite-active');

                if (isActive) {
                    // Удаляем из избранного
                    removeFromWishlist(productId, icon);
                } else {
                    // Добавляем в избранное
                    addToWishlist(productId, icon);
                }
            });
        });
    }

    function addToWishlist(productId, icon) {
        fetch(`/wishlist/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded', // Измените тип контента
            },
            body: `csrfmiddlewaretoken=${getCSRFToken()}` // Добавьте токен в тело запроса
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                icon.classList.add('favorite-active');
                showNotification('Товар добавлен в избранное', 'success');
            } else {
                showNotification(data.error || 'Ошибка добавления', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка соединения', 'error');
        });
    }

    function removeFromWishlist(productId, icon) {
        fetch(`/wishlist/remove/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `csrfmiddlewaretoken=${getCSRFToken()}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                icon.classList.remove('favorite-active');
                showNotification('Товар удален из избранного', 'success');
            } else {
                showNotification(data.error || 'Ошибка удаления', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка соединения', 'error');
        });
    }

    // Правильная функция получения CSRF токена
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            return csrfToken.value;
        }

        // Альтернативный способ получения CSRF токена из cookies
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showNotification(message, type) {
        // Простая реализация уведомления
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#28a745' : '#dc3545'};
            color: white;
            border-radius: 5px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
});