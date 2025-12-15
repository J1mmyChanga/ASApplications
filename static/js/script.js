document.addEventListener('DOMContentLoaded', function() {
    // === 1. ЭЛЕМЕНТЫ ФОРМЫ ===
    const fileInput = document.getElementById('photos');
    const filePreview = document.getElementById('filePreview');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const descriptionTextarea = document.getElementById('issueDescription');
    const charCounter = document.getElementById('charCount');
    const resetBtn = document.getElementById('resetBtn');
    const form = document.getElementById('repairForm');
    const formPreview = document.getElementById('previewContent');
    
    // === 2. КОНСТАНТЫ ===
    const maxFiles = 5;
    const maxSize = 5 * 1024 * 1024; // 5 MB
    const maxChars = 1000;
    
    // === 3. ПРЕВЬЮ ИЗОБРАЖЕНИЙ ===
    
    // Инициализация превью
    function initFilePreview() {
        // Обработчик выбора файлов через диалог
        fileInput.addEventListener('change', function(e) {
            handleFiles(e.target.files);
        });

        // Drag & Drop функционал
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#2980b9';
            this.style.background = '#e3f2fd';
        });

        fileUploadArea.addEventListener('dragleave', function() {
            this.style.borderColor = '#3498db';
            this.style.background = '#f8fafc';
        });

        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#3498db';
            this.style.background = '#f8fafc';
            
            if (e.dataTransfer.files.length) {
                handleFiles(e.dataTransfer.files);
            }
        });
    }

    // Обработка файлов
    function handleFiles(files) {
        const currentFiles = filePreview.children.length;
        const filesArray = Array.from(files);
        
        // Проверка количества файлов
        if (currentFiles + filesArray.length > maxFiles) {
            alert(`Максимальное количество файлов: ${maxFiles}`);
            return;
        }

        filesArray.forEach(file => {
            // Проверка размера файла
            if (file.size > maxSize) {
                alert(`Файл "${file.name}" слишком большой. Максимум 5 МБ`);
                return;
            }

            // Проверка типа файла
            if (!file.type.startsWith('image/')) {
                alert(`Файл "${file.name}" не является изображением`);
                return;
            }

            const reader = new FileReader();
            
            reader.onload = function(e) {
                const previewItem = document.createElement('div');
                previewItem.className = 'file-preview-item';
                
                previewItem.innerHTML = `
                    <img src="${e.target.result}" alt="${file.name}">
                    <div class="file-info-overlay">
                        <span class="file-name">${truncateFileName(file.name, 15)}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    </div>
                    <button type="button" class="remove-file" title="Удалить">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                
                // Удаление файла из превью
                previewItem.querySelector('.remove-file').addEventListener('click', function() {
                    previewItem.remove();
                    updateFileCount();
                    updateFormPreview();
                });
                
                filePreview.appendChild(previewItem);
                updateFileCount();
                updateFormPreview();
            };
            
            reader.readAsDataURL(file);
        });
    }

    // Обрезка длинного имени файла
    function truncateFileName(filename, maxLength) {
        if (filename.length <= maxLength) return filename;
        return filename.substring(0, maxLength - 3) + '...';
    }

    // Форматирование размера файла
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    // Обновление счетчика файлов
    function updateFileCount() {
        const count = filePreview.children.length;
        
        // Удаляем старый счетчик если есть
        const oldCounter = fileUploadArea.querySelector('.file-counter');
        if (oldCounter) oldCounter.remove();
        
        if (count > 0) {
            const counter = document.createElement('div');
            counter.className = 'file-counter';
            counter.textContent = `Выбрано файлов: ${count}/${maxFiles}`;
            fileUploadArea.appendChild(counter);
        }
    }

    // === 4. СЧЕТЧИК СИМВОЛОВ ДЛЯ ОПИСАНИЯ ===
    
    function initCharCounter() {
        // Инициализация при загрузке
        updateCharCounter();
        
        // Обновление при вводе
        descriptionTextarea.addEventListener('input', function() {
            updateCharCounter();
            updateFormPreview();
        });
    }
    
    function updateCharCounter() {
        const currentLength = descriptionTextarea.value.length;
        charCounter.textContent = currentLength;
        
        // Подсветка при превышении лимита
        if (currentLength > maxChars) {
            charCounter.style.color = '#e74c3c';
            descriptionTextarea.value = descriptionTextarea.value.substring(0, maxChars);
            charCounter.textContent = maxChars;
        } else if (currentLength > maxChars * 0.9) {
            charCounter.style.color = '#f39c12'; // Оранжевый при 90%
        } else {
            charCounter.style.color = '#7f8c8d';
        }
    }
    
    // === 5. КНОПКА СБРОСА ФОРМЫ ===
    
    function initResetButton() {
        resetBtn.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите очистить всю форму? Все введенные данные будут потеряны.')) {
                form.reset();
                filePreview.innerHTML = '';
                updateFileCount();
                updateCharCounter();
                updateFormPreview();
            }
        });
    }
    
    // === 6. ПРЕДПРОСМОТР ФОРМЫ ===
    
    function initFormPreview() {
        // Обновление предпросмотра при изменении формы
        const formElements = form.querySelectorAll('input, textarea, select');
        formElements.forEach(element => {
            element.addEventListener('input', updateFormPreview);
            element.addEventListener('change', updateFormPreview);
        });
        
        // Инициализация при загрузке
        updateFormPreview();
    }
    
    function updateFormPreview() {
        const formData = {
            fullName: document.getElementById('fullName').value || 'Не указано',
            phoneNumber: document.getElementById('phoneNumber').value || 'Не указано',
            roomNumber: document.getElementById('roomNumber').value || 'Не указано',
            issueDescription: document.getElementById('issueDescription').value || 'Не указано',
            notify: document.getElementById('notify').checked ? 'Да' : 'Нет',
            filesCount: filePreview.children.length
        };
        
        let previewHTML = `
            <div class="preview-section">
                <h4><i class="fas fa-user"></i> Информация о заявителе</h4>
                <div class="preview-item">
                    <strong>ФИО:</strong> ${formData.fullName}
                </div>
                <div class="preview-item">
                    <strong>Телефон:</strong> ${formData.phoneNumber}
                </div>
            </div>
            
            <div class="preview-section">
                <h4><i class="fas fa-map-marker-alt"></i> Местоположение</h4>
                <div class="preview-item">
                    <strong>Помещение:</strong> ${formData.roomNumber}
                </div>
            </div>
            
            <div class="preview-section">
                <h4><i class="fas fa-exclamation-triangle"></i> Описание проблемы</h4>
                <div class="preview-item">
                    <strong>Описание:</strong><br>
                    <div class="description-preview">${truncateText(formData.issueDescription, 150)}</div>
                </div>
            </div>
            
            <div class="preview-section">
                <h4><i class="fas fa-camera"></i> Фотографии</h4>
                <div class="preview-item">
                    <strong>Количество файлов:</strong> ${formData.filesCount} из ${maxFiles}
                </div>
                ${getFilesPreviewHTML()}
            </div>
            
            <div class="preview-section">
                <h4><i class="fas fa-clipboard-check"></i> Дополнительно</h4>
                <div class="preview-item">
                    <strong>Уведомления:</strong> ${formData.notify}
                </div>
                <div class="preview-item">
                    <strong>Статус:</strong> <span class="status-badge preview">Новая</span>
                </div>
            </div>
        `;
        
        formPreview.innerHTML = previewHTML;
    }
    
    function truncateText(text, maxLength) {
        if (!text || text === 'Не указано') return text;
        if (text.length <= maxLength) return text.replace(/\n/g, '<br>');
        return text.substring(0, maxLength).replace(/\n/g, '<br>') + '...';
    }
    
    function getFilesPreviewHTML() {
        const items = filePreview.querySelectorAll('.file-preview-item');
        if (items.length === 0) return '<div class="preview-item">Файлы не выбраны</div>';
        
        let html = '<div class="files-preview-grid">';
        items.forEach(item => {
            const img = item.querySelector('img').src;
            const name = item.querySelector('.file-name').textContent;
            html += `
                <div class="file-preview-mini">
                    <img src="${img}" alt="${name}">
                    <span>${name}</span>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }
    
    // === 7. ВАЛИДАЦИЯ ПРИ ОТПРАВКЕ ===
    
    function initFormValidation() {
        form.addEventListener('submit', function(e) {
            // Проверка обязательных полей
            const requiredFields = [
                { id: 'fullName', name: 'ФИО' },
                { id: 'phoneNumber', name: 'Номер телефона' },
                { id: 'roomNumber', name: 'Номер помещения' },
                { id: 'issueDescription', name: 'Описание проблемы' }
            ];
            
            let isValid = true;
            let errorMessage = '';
            
            requiredFields.forEach(field => {
                const element = document.getElementById(field.id);
                if (!element.value.trim()) {
                    element.style.borderColor = '#e74c3c';
                    isValid = false;
                    errorMessage += `• ${field.name} - обязательное поле\n`;
                } else {
                    element.style.borderColor = '';
                }
            });
            
            // Проверка телефона (базовая)
            const phone = document.getElementById('phoneNumber').value;
            const phoneRegex = /^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;
            if (phone && !phoneRegex.test(phone.replace(/\s+/g, ''))) {
                document.getElementById('phoneNumber').style.borderColor = '#e74c3c';
                isValid = false;
                errorMessage += '• Номер телефона указан некорректно\n';
            }
            
            // Проверка количества файлов
            if (filePreview.children.length > maxFiles) {
                isValid = false;
                errorMessage += `• Максимальное количество файлов: ${maxFiles}\n`;
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, исправьте следующие ошибки:\n\n' + errorMessage);
                return false;
            }
            
            // Показать индикатор отправки
            const submitBtn = form.querySelector('.btn-submit');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправка...';
            submitBtn.disabled = true;
            
            // Автоматически включить кнопку через 5 секунд (на случай ошибки)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 5000);
        });
    }
    
    // === 8. ИНИЦИАЛИЗАЦИЯ ВСЕГО ===
    
    function initAll() {
        initFilePreview();
        initCharCounter();
        initResetButton();
        initFormPreview();
        initFormValidation();
        updateFileCount();
    }
    
    // Запуск инициализации
    initAll();
});