const userLenght = document.getElementById('user-lenght')
const pumpsDropdown = document.getElementById('pumps-dropdown')
const filtersDropdown = document.getElementById('filters-dropdown')
const valveGroup = document.getElementById('valve-group')
const lightingsDropdown = document.getElementById('lighting-dropdown')

const initializePumpsScript = () => {

    if ( !pumpsDropdown) {
        pumpsDropdown.innerHTML = '<option value="">Нет оборудования соотвествующего заданным параметрам</option>';
        console.warn('Элементы для инициализации входной группы не найдены');
        return;
    }

    function updateEntranceDropdown() {
        fetch(`/calculation/get_filtred_pumps/`)
            .then(response => response.json())
            .then(data => {
                pumpsDropdown.innerHTML = '<option value="">Выберите насос</option>';
                data.pumps.forEach(pumps => {
                    let option = document.createElement('option');
                        const formattedPrice = pumps.price.toLocaleString('ru-RU', {
                            style: 'decimal',
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        })
                        option.text = `${pumps.name} | цена: ${formattedPrice} ₽/шт.`;
                        option.value = pumps.id;
                        pumpsDropdown.appendChild(option);
                    });
                })
            .catch(error => {
                console.error('Ошибка при перечня насосов', error);
            });
        }

        updateEntranceDropdown();
    
}


const initializeFiltersScript = () => {

    if (!filtersDropdown) {
        filtersDropdown.innerHTML = '<option value="">Нет оборудования, соответствующего заданным параметрам</option>';
        console.warn('Элементы для инициализации выпадающего списка не найдены');
        return;
    }

    function updateFiltersDropdown() {
        fetch(`/calculation/get_filtred_filter/`)
            .then(response => response.json())
            .then(data => {
                filtersDropdown.innerHTML = '<option value="">Выберите фильтр</option>';
                data.filters.forEach(filter => {  
                    let option = document.createElement('option');
                    const formattedPrice = filter.price.toLocaleString('ru-RU', {
                        style: 'decimal',
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })
                    option.value = filter.id;  
                    option.text = `${filter.name} | цена: ${formattedPrice} ₽/шт.`;
                    filtersDropdown.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Ошибка при получении списка фильтров', error);
            });
    }

    updateFiltersDropdown(); 
}


const initializeValveFilterScript = () => {

    if (!valveGroup) {
        valveGroup.innerHTML = '<option value="">Нет оборудования, соответствующего заданным параметрам</option>';
        console.warn('Элементы для инициализации выпадающего списка не найдены');
        return;
    }

    function updateValveDropdown() {
        fetch(`/calculation/get_filter_valve/`)
            .then(response => response.json())
            .then(data => {
                valveGroup.innerHTML = '<option value="">Выберите фильтр</option>';
                data.valves.forEach(valve => {  
                    let option = document.createElement('option');
                    const formattedPrice = valve.price.toLocaleString('ru-RU', {
                        style: 'decimal',
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })
                    option.value = valve.id;  
                    option.text = `${valve.connection_type} | ${valve.name} | цена: ${formattedPrice} ₽/шт.`;
                    valveGroup.appendChild(option); 
                });
            })
            .catch(error => {
                console.error('Ошибка при получении списка фильтров', error);
            });
    }

    updateValveDropdown(); 
}
   

$(document).ready(function() {
    $('.ajax-response input, .ajax-response select').on('input change', function() {
        console.log($(this).val());
        let formData = {
            length: $('#{{ form.length.id_for_label }}').val(),
            width: $('#{{ form.width.id_for_label }}').val(),
            depth_from: $('#{{ form.depth_from.id_for_label }}').val(),
            depth_to: $('#{{ form.depth_to.id_for_label }}').val(),
            water_exchange_time: $('#{{ form.water_exchange_time.id_for_label }}').val(),
            filtration_speed: $('#{{ form.filtration_speed.id_for_label }}').val(),
            
            //    {% comment %} csrfmiddlewaretoken: '{{ csrf_token }}',  для защиты от CSRF {% endcomment %}
        };

        $.ajax({
            url: "{% url 'accept_size' %}",  
            type: "POST",
            data: formData,
            success: function(response) {
                console.log("Данные отправлены успешно:", response);
                initializePumpsScript()
                initializeFiltersScript()
                
            },
            error: function(response) {
                console.log("Ошибка при отправке данных:", response);
            }
        });
    });

    $('.ajax-filters input, .ajax-filters select').on('input change', function() {
        console.log($(this).val());
        let formFiltersData = {
            filters_materials: $('#filters-dropdown').val(),
        };

        $.ajax({
            url: "{% url 'accept_filter' %}",  
            type: "POST",
            data: formFiltersData,
            success: function(response) {
                console.log("Данные отправлены успешно:", response);
                initializeValveFilterScript (); 
            },
            error: function(response) {
                console.log("Ошибка при отправке данных:", response);
            }
        });
    });

    // {% comment %} $('.lighting-ajax input, .lighting-ajax select').on('input change', function() {
    //     console.log($(this).val());
    //     let formlightingData = {
    //         lighting-data: $('#lighting-dropdown').val(),
    //     };

    //     $.ajax({
    //         url: "{% url 'accept_filter' %}",  
    //         type: "POST",
    //         data: formFiltersData,
    //         success: function(response) {
    //             console.log("Данные отправлены успешно:", response);
                
    //         },
    //         error: function(response) {
    //             console.log("Ошибка при отправке данных:", response);
    //         }
    //     });
    // }); {% endcomment %}
        
});