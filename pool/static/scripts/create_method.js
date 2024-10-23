
const openModalBtn = document.getElementById('openAddClientModal');
const addClientModal = document.getElementById('addClientModal');
const closeModal = document.querySelector('.close-btn');
const clientForm = document.querySelector('.add-client-form');
const clientSelect = document.getElementById('id_client');
const formQuestions = document.querySelectorAll('.question');
const materialTypeRadios = document.querySelectorAll('input[name="material_type"]');
const materialsDropdown = document.getElementById('materials-dropdown');
const equipmentHeatingsRadios = document.querySelectorAll('input[name="heating"]')
const heatingDropdown = document.getElementById('heatings-dropdown')
const lightingRadios = document.querySelectorAll('input[name="ligthing"]');
const lightQuantityInput = document.getElementById('ligth_quantity');
const desinfectionRadios = document.querySelectorAll('input[name="desinfection"]')
const desinfecionDropdown = document.getElementById('desinfection-dropdown')
const entranceRadios = document.querySelectorAll('input[name="entrance"]')
const entranceDropdown = document.getElementById('entrance-dropdown')
const MaterialZaclad = document.querySelectorAll('input[name=["type_materials"]')




const initializeModalAndForm = () => {


    if (openModalBtn && addClientModal && closeModal) {

        openModalBtn.addEventListener('click', () => {

            addClientModal.style.display = 'flex';
        });

        closeModal.addEventListener('click', () => {

            addClientModal.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target === addClientModal) {

                addClientModal.style.display = 'none';
            }
        });
    } else {
        console.warn('Элементы модального окна не найдены');
    }

    if (clientForm) {
        clientForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(clientForm);

            fetch('/calculation/create-client/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    clientForm.reset();
                    // Добавляем нового клиента в выпадающий список
                    const newOption = document.createElement('option');
                    newOption.value = data.client.id;
                    newOption.text = data.client.name;
                    newOption.selected = true;
                    clientSelect.appendChild(newOption);

                    // Закрываем модальное окно
                    addClientModal.style.display = 'none';
                } else {
                    console.error('Ошибка добавления клиента:', data.errors);
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке формы нового клиента:', error);
            });
        });
    } else {
        console.warn('Форма для добавления клиента не найдена');
    }

}

const helpTextVisible = () => {
    formQuestions.forEach(question => {
        question.addEventListener('mouseenter', () => {
            const helpText = question.nextElementSibling;
            if (helpText && helpText.classList.contains('help-text')) {

                helpText.style.display = 'flex';
             }
        });
        question.addEventListener('mouseleave', () => {
            const helpText = question.nextElementSibling;
            if (helpText && helpText.classList.contains('help-text')) {

                helpText.style.display = 'none';
            }
        });
    });
}

const initializeHeatingScript = () => {
    if (!equipmentHeatingsRadios.length || !heatingDropdown) {
        console.warn('Элементы для инициализации Подогрева не найдены');
        return;
    }

    const updateHeatingsEquipment = (equipmentHeatings) => {

        // Если выбран "Без подогрева", блокируем dropdown и очищаем его
        if (equipmentHeatings === "") {
            heatingDropdown.innerHTML = '<option value="">Без подогрева</option>';
            heatingDropdown.disabled = true;
        } else {
            heatingDropdown.disabled = false; // Активируем dropdown, если выбран другой вариант
            fetch(`/calculation/get-heating/?heating_type=${equipmentHeatings}`)
                .then(response => response.json())
                .then(data => {
                    heatingDropdown.innerHTML = '<option value="">Выберите Оборудование</option>';
                    data.heatings.forEach((heating) => {
                        let option = document.createElement('option');
                        option.value = heating.id;
                        option.text = heating.name;
                        heatingDropdown.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Ошибка при получении оборудования:', error);
                });
        }
    };

    equipmentHeatingsRadios.forEach(radio => {
        radio.addEventListener('change', (event) => {
            const selectedValue = event.target.value; // Получаем выбранное значение
            updateHeatingsEquipment(selectedValue); // Обновляем оборудование в зависимости от выбора
        });
    });

    const checkedRadio = document.querySelector('input[name="heating"]:checked');
    if (checkedRadio) {
        updateHeatingsEquipment(checkedRadio.value); // Используем выбранное значение по умолчанию
    }
}

const initialzeDesinfectionScript = () => {
    if (!desinfectionRadios.length || !desinfecionDropdown) {
        console.warn('Элементы для инициализации списка с оборудованием не найдены');
        return;
    }

    const updateDesinfrctionEquipment = (equipmentDesinfrctions) => {

        // Если выбран "Без подогрева", блокируем dropdown и очищаем его
        if (equipmentDesinfrctions === "") {
            desinfecionDropdown.innerHTML = '<option value="">Ручное добавление химии</option>';
            desinfecionDropdown.disabled = true;
        } else {
            desinfecionDropdown.disabled = false; 
            fetch(`/calculation/get_desinfection/?type_desinfection=${equipmentDesinfrctions}`)
                .then(response => response.json())
                .then(data => {
                    desinfecionDropdown.innerHTML = '<option value="">Выберите Оборудование</option>';
                    data.desinfections.forEach((desinfection) => {
                        let option = document.createElement('option');
                        option.value = `${desinfection.id}|${desinfection.model}`;
                        option.text = desinfection.name;
                        desinfecionDropdown.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Ошибка при получении оборудования:', error);
                });
        }
    };

    desinfectionRadios.forEach(radio => {
        radio.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
           updateDesinfrctionEquipment(selectedValue); // Обновляем оборудование в зависимости от выбора
        });
    });

    const checkedRadio = document.querySelector('input[name="desinfection"]:checked');
    if (checkedRadio) {
        updateDesinfrctionEquipment(checkedRadio.value); // Используем выбранное значение по умолчанию
    }
}

const lightingScript = () => {
    const updateLightQuantityState = () => {
        const selectedLighting = document.querySelector('input[name="ligthing"]:checked').value;
        
        if (selectedLighting === 'none') {
            lightQuantityInput.disabled = true;
            lightQuantityInput.value = 0;
        } else {
            lightQuantityInput.disabled = false;
            lightQuantityInput.value = ''; // Очищаем значение при выборе другого варианта
        }
    };

    updateLightQuantityState();

    lightingRadios.forEach(radio => {
        radio.addEventListener('change', updateLightQuantityState);
    });


}

const initializeMaterialScript = () => {
    if (!materialTypeRadios.length || !materialsDropdown) {
        console.warn('Элементы для инициализации материалов не найдены');
        return;
    }

    function updateMaterialsDropdown(materialType) {
        fetch(`/calculation/get-materials/?type=${materialType}`)
            .then(response => response.json())
            .then(data => {
                materialsDropdown.innerHTML = '<option value="">Выберите материал</option>';
                data.materials.forEach(material => {
                    let option = document.createElement('option');
                        option.value = material.id;
                        option.text = material.name;
                        materialsDropdown.appendChild(option);
                    });
                })
            .catch(error => {
                console.error('Ошибка при получении материалов:', error);
            });
        }

        materialTypeRadios.forEach(radio => {
            radio.addEventListener('change', function () {
                updateMaterialsDropdown(this.value);
            });
        });

        updateMaterialsDropdown(document.querySelector('input[name="material_type"]:checked').value);
    
}

const initializeEntranceScript = () => {

    if (!entranceRadios.length || !entranceDropdown) {
        console.warn('Элементы для инициализации входной группы не найдены');
        return;
    }

    function updateEntranceDropdown(entranceType) {
        fetch(`/calculation/get_entrance/?entrance_type=${entranceType}`)
            .then(response => response.json())
            .then(data => {
                entranceDropdown.innerHTML = '<option value="">Выберите элемент</option>';
                data.entrances.forEach(entrance => {
                    let option = document.createElement('option');
                        option.value = entrance.id;
                        option.text = entrance.name;
                        entranceDropdown.appendChild(option);
                    });
                })
            .catch(error => {
                console.error('Ошибка при получении входной группы:', error);
            });
        }

        entranceRadios.forEach(radio => {
            radio.addEventListener('change', function () {
                updateEntranceDropdown(this.value);
            });
        });

        updateEntranceDropdown(document.querySelector('input[name="entrance"]:checked').value);
    
}




document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM полностью загружен');
    initializeModalAndForm()
    helpTextVisible()
    initializeHeatingScript()
    initializeMaterialScript()
    lightingScript()
    initialzeDesinfectionScript()
    initializeEntranceScript()
    // initializePumpsScript()
})
