document.addEventListener('DOMContentLoaded', function() {
    // Галерея изображений
    const thumbnails = document.querySelectorAll('.gallery-thumbnail');
    const mainImage = document.getElementById('main-product-image');

    // Обработчик клика на миниатюры
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-image');

            // Обновляем основное изображение
            mainImage.src = imageUrl;

            // Убираем активный класс у всех миниатюр
            thumbnails.forEach(t => t.classList.remove('active'));

            // Добавляем активный класс к текущей миниатюре
            this.classList.add('active');
        });
    });

    // Увеличение при наведении на основное изображение
    if (mainImage) {
        mainImage.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
        });

        mainImage.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // Управление количеством товара
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.plus');
    const quantityInput = document.querySelector('.quantity-input');

    if (minusBtn && plusBtn && quantityInput) {
        minusBtn.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
            }
        });

        plusBtn.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            const max = parseInt(quantityInput.getAttribute('max'));
            if (value < max) {
                quantityInput.value = value + 1;
            }
        });

        // Валидация ввода
        quantityInput.addEventListener('change', function() {
            let value = parseInt(this.value);
            const max = parseInt(this.getAttribute('max'));
            const min = parseInt(this.getAttribute('min'));

            if (isNaN(value) || value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    }

    // ===== ОБРАБОТКА ИЗБРАННОГО НА ДЕТАЛЬНОЙ СТРАНИЦЕ =====
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
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `csrfmiddlewaretoken=${getCSRFToken()}`
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

    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    function showNotification(message, type) {
        // Удаляем предыдущие уведомления
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());

        // Создаем новое уведомление
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
            z-index: 10000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Анимации для уведомлений
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});