document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.collection-checkbox');
    const completeBtn = document.getElementById('completeBtn');
    const completionText = document.getElementById('completionText');
    const collectedCountEl = document.getElementById('collectedCount');
    const totalItems = parseInt(document.getElementById('totalItems').textContent);

    // Обновляем статус завершения
    function updateCompletionStatus() {
        const collectedCount = document.querySelectorAll('.collection-checkbox:checked').length;
        collectedCountEl.textContent = collectedCount;

        if (collectedCount === totalItems) {
            completeBtn.disabled = false;
            completeBtn.classList.remove('disabled');
            completionText.innerHTML = '<span class="text-success">✓ Все позиции собраны</span>';
        } else {
            completeBtn.disabled = true;
            completeBtn.classList.add('disabled');
            completionText.innerHTML = `⚠ Собрано <span id="collectedCount">${collectedCount}</span> из <span id="totalItems">${totalItems}</span> позиций`;
        }
    }

    // Обработчик для чекбоксов
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const itemElement = document.getElementById(`item-${itemId}`);
            const toggleText = this.parentNode.querySelector('.toggle-text');

            if (this.checked) {
                itemElement.classList.add('collected');
                toggleText.textContent = '✅ Собрано';
            } else {
                itemElement.classList.remove('collected');
                toggleText.textContent = '⏳ Собрать';
            }

            updateCompletionStatus();
        });
    });

    // Предотвращаем отправку формы, если не все собрано
    document.getElementById('completeForm').addEventListener('submit', function(e) {
        const collectedCount = document.querySelectorAll('.collection-checkbox:checked').length;
        if (collectedCount !== totalItems) {
            e.preventDefault();
            alert('Не все позиции собраны!');
        }
    });

    // Инициализируем счетчик
    updateCompletionStatus();
});