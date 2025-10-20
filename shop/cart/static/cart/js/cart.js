document.addEventListener('DOMContentLoaded', function() {
  const quantityForms = document.querySelectorAll('.quantity-form');
  const removeForms = document.querySelectorAll('.remove-form');

  // Функция для обновления шапки корзины
  function updateCartHeader(cartTotal, cartLength) {
    const cartItemsCount = document.getElementById('cart-items-count');
    const cartTotalHeader = document.getElementById('cart-total-header');
    const cartItemsText = document.getElementById('cart-items-text');
    const cartHeader = document.getElementById('cart-header');

    if (cartItemsCount && cartTotalHeader && cartItemsText) {
      // Обновляем числа, текст склонения и добавляем Р
      cartItemsCount.textContent = cartLength;
      cartItemsText.textContent = getRussianPlural(cartLength);
      cartTotalHeader.textContent = parseFloat(cartTotal).toFixed(2) + ' Р';
    } else if (cartItemsCount && cartTotalHeader) {
      // Fallback - если нет cartItemsText, обновляем только числа
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
  }

  function updateCartItem(productId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('override', 'true');
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    const itemRow = document.getElementById(`item-${productId}`);
    if (itemRow) itemRow.classList.add('updating');

    fetch(`/cart/add/${productId}/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        updatePrices(productId, data.item_total, data.cart_total, data.cart_length);
      } else {
        console.error('Error updating cart:', data.error);
        const input = document.querySelector(`#item-${productId} .quantity-input`);
        if (input) input.value = quantity;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
    .finally(() => {
      if (itemRow) itemRow.classList.remove('updating');
    });
  }

  function removeCartItem(productId) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    const itemRow = document.getElementById(`item-${productId}`);
    if (itemRow) itemRow.classList.add('updating');

    fetch(`/cart/remove/${productId}/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        itemRow.remove();

        // Обновляем общую сумму в корзине
        const cartTotalElement = document.getElementById('cart-total');
        if (cartTotalElement) {
          cartTotalElement.textContent = parseFloat(data.cart_total).toFixed(2) + ' Р';
        }

        // Обновляем шапку корзины
        updateCartHeader(data.cart_total, data.cart_length);

        // Если корзина пуста
        if (data.cart_length === 0) {
          const cartItemsElement = document.getElementById('cart-items');
          if (cartItemsElement) {
            cartItemsElement.innerHTML = '<tr><td colspan="6" style="text-align: center;">Ваша корзина пуста</td></tr>';
          }

          const textRightElement = document.querySelector('.text-right');
          if (textRightElement) {
            textRightElement.style.display = 'none';
          }
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  function updatePrices(productId, itemTotal, cartTotal, cartLength) {
    // Обновляем сумму для конкретного товара
    const itemTotalElement = document.querySelector(`#item-${productId} .total-price`);
    if (itemTotalElement) {
      itemTotalElement.textContent = parseFloat(itemTotal).toFixed(2) + ' Р';
    }

    // Обновляем общую сумму корзины
    const cartTotalElement = document.getElementById('cart-total');
    if (cartTotalElement) {
      cartTotalElement.textContent = parseFloat(cartTotal).toFixed(2) + ' Р';
    }

    // Обновляем шапку корзины
    updateCartHeader(cartTotal, cartLength);
  }

  // Обработчики для изменения количества
  quantityForms.forEach(form => {
    const quantityInput = form.querySelector('.quantity-input');
    const minusBtn = form.querySelector('.quantity-btn.minus');
    const plusBtn = form.querySelector('.quantity-btn.plus');
    const productId = form.action.split('/').filter(Boolean).pop();

    if (minusBtn && plusBtn && quantityInput) {
      minusBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
          updateCartItem(productId, currentValue - 1);
        }
      });

      plusBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        const maxQuantity = parseInt(quantityInput.getAttribute('max')) || 999;
        if (currentValue < maxQuantity) {
          quantityInput.value = currentValue + 1;
          updateCartItem(productId, currentValue + 1);
        }
      });

      quantityInput.addEventListener('change', function() {
        let value = parseInt(this.value);
        const maxQuantity = parseInt(this.getAttribute('max')) || 999;

        if (isNaN(value) || value < 1) {
          this.value = 1;
          value = 1;
        } else if (value > maxQuantity) {
          this.value = maxQuantity;
          value = maxQuantity;
        }

        updateCartItem(productId, value);
      });

      quantityInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          let value = parseInt(this.value);
          const maxQuantity = parseInt(this.getAttribute('max')) || 999;

          if (isNaN(value) || value < 1) {
            this.value = 1;
            value = 1;
          } else if (value > maxQuantity) {
            this.value = maxQuantity;
            value = maxQuantity;
          }

          updateCartItem(productId, value);
        }
      });
    }
  });

  // Обработчики для удаления товаров
  removeForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const productId = form.action.split('/').filter(Boolean).pop();
      removeCartItem(productId);
    });
  });
});