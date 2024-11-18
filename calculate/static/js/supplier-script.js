$(document).ready(function() {

    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    let dashbordBody,
        supplierDetail,
        supplierDetailCloseModal,
        supplierDetailBody,
        deleteSupplierBtn,
        loadListConstantFlag,
        supplierDeleteModal,
        deleteModalSupplierChevron,
        deleteSupplierDone,
        deleteSupplierCancel,
        supplierDeleteModalMessage,
        supplierDeleteModalMessageCompleted,
        supplierDeleteModalMessageText,
        supplierCreate,
        supplierCreateModalChevron,
        supplierCreateModal,
        supplierCreateMessage,
        supplierCreateMessageText,
        supplierCreateMessageCompleted,
        updateSupplierModalFormComplete,
        updateSupplierModalFormCancel,
        editSupplierBtn,
        updateSupplierModalFormMessage,
        updateSupplierModalFormMessageText,
        updateSupplierSodalFormMessageComplete,
        loadCardEditFlag,
        supplierSearchResetChevron,
        supplierSearch,
        supplierEquipmentList,
        loadUpdateElementsFlag 

    $('#load-suppliers-list').click(function() {

        $('#client-list').html('');

        const url = $(this).data('url')

        $.ajax({
            url : url,
            method: 'GET',
            success: function(response) {

                $('#client-list').html(response);

                loadListConstants()

                if(loadListConstantFlag){
                    loadSuppliers(); 
                    addSupplierFunction()
                    searchSupplierFunction()
                } 
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке списка клиентов:', error);
                dashbordBody.innerHTML = '<p>Не удалось загрузить данные клиентов.</p>';
            }
        })

    })

    const loadListConstants = () =>{
        dashbordBody = document.getElementById('dashbord-body-supplier');
        supplierCreate  = document.getElementById('add-supplier')
        supplierCreateModal = document.getElementById('supplier-create-modal')
        supplierCreateModalChevron = document.getElementById('supplier-create-modal-chevron')
        supplierCreateMessage = document.getElementById('supplier-create-message')
        supplierCreateMessageText = document.getElementById('supplier-create-message-text')
        supplierCreateMessageCompleted = document.getElementById('supplier-create-message-completed')
        supplierSearchResetChevron = document.getElementById('supplier-search-reset-chevron')
        supplierSearch = document.getElementById('supplier-search')
        loadListConstantFlag = false
        if (dashbordBody){
            loadListConstantFlag = true
        }
    }
    
    const loadDetailConstans = () =>{
        supplierDetail = document.getElementById('supplier-detail');
        supplierDetailCloseModal = document.getElementById('supplier-detail-close-modal')
        supplierDetailBody = document.getElementById('supplier-detail-body')
       
    }

    const loadCardEdit = () => {
        deleteSupplierBtn = document.getElementById('delete-supplier-btn')
        editSupplierBtn = document.getElementById('edit-supplier-btn')
        supplierDeleteModal = document.getElementById('supplier-delete-modal')
        deleteModalSupplierChevron = document.getElementById('delete-modal-supplier-chevron')
        deleteSupplierDone = document.getElementById('delete-supplier-done')
        deleteSupplierCancel = document.getElementById('delete-supplier-cancel')
        supplierDeleteModalMessage = document.getElementById('suplier-delete-modal-message')
        supplierDeleteModalMessageCompleted = document.getElementById('supplier-delete-modal-message-completed')
        supplierDeleteModalMessageText = document.getElementById('suplier-delete-modal-message-text')
        updateSupplierRecordModal = document.getElementById('update-supplier-record-modal')
        updateSupplierRecordModalChevron = document.getElementById('update-supplier-record-modal-chevron')
        supplierEquipmentList = document.getElementById('supplier-equipment-list')
        loadCardEditFlag = false
        if (deleteSupplierBtn) {
            loadCardEditFlag = true
        }
    }

    const loadUpdateElements = () =>{
        updateSupplierModalFormComplete = document.getElementById('update-supplier-modal-form-complete')
        updateSupplierModalFormCancel = document.getElementById('update-supplier-modal-form-cancel')
        updateSupplierModalFormMessage = document.getElementById('update-supplier-modal-form-message')
        updateSupplierModalFormMessageText = document.getElementById('update-supplier-modal-form-message-text')
        updateSupplierSodalFormMessageComplete = document.getElementById('update-supplier-modal-form-message-complete')
        loadUpdateElementsFlag = false

        if(updateSupplierModalFormComplete && updateSupplierModalFormCancel){
            loadUpdateElementsFlag = true
        }
        
    }

    function loadSuppliers() {
        if (loadListConstantFlag) {
            $.ajax({
                url: '/suppliers/get-supplier',
                method: 'GET',
                success: function(response) {
                    let suppliersData = response.suppliers
                    
                    loadDetailConstans()

                    let tableHtml = `
                        <div class="dashbord-body-table border-bottom-table">
                            <div class="dashbord-body-table-cell title"><p>Поставщик</p></div>
                            <div class="dashbord-body-table-cell title"><p>Менеджер</p></div>
                            <div class="dashbord-body-table-cell title"><p>Номер телефона</p></div>
                            <div class="dashbord-body-table-cell title"><p>Юридическое наименование</p></div>
                        </div>`;
                        $.each(suppliersData, function(index, supplier) {
                        tableHtml += `
                            <div class="dashbord-body-table supplier-row" data-supplier-id="${supplier.id}">
                                <div class="dashbord-body-table-cell"><p>${supplier.name || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${supplier.manager || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${supplier.phone || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${supplier.legal_name || ''}</p></div>
                            </div>`;
                        });
    
                        dashbordBody.innerHTML = tableHtml;

                    $('.supplier-row').click(function() {
                        const supplierId = $(this).data('supplier-id');
                        
                        loadSupplierDetails(supplierId);
                        
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при загрузке списка поставщиков:', error);
                    clientList.innerHTML = '<p>Не удалось загрузить данные клиентов.</p>';
                }
            });
        }
    }

    const closeModalWindow = (button, modal) =>{
        button.addEventListener('click', () => {
            modal.style.display = 'none';

        })
    }

    const loadSupplierDetails = (supplierId) => {
        if (!supplierId) {
            console.error("Ошибка: supplierId не задан");
            return;
        }
        supplierDetail.style.display = 'flex'
        
        
        closeModalWindow(
            supplierDetailCloseModal,
            supplierDetail,
            )
            supplierDetailBody.innerHTML = ''

        $.ajax({
            url: `/suppliers/supplier/${supplierId}`,
            method: 'GET',
            success: function(response) {
                $(supplierDetailBody).html(response);
                loadCardEdit()
                if(loadCardEditFlag) {
                    deleteSupplierFunction()
                    editSupplierFunction()
                    getEquipmentForSupplier(supplierId)
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке данных клиента:', error);
                $(supplierDetail).html('<p>Не удалось загрузить данные о клиенте.</p>');
            }
        });
    };

    const deleteSupplierFunction = () =>{

        closeModalWindow(
            deleteModalSupplierChevron,
            supplierDeleteModal
        )

        closeModalWindow(
            deleteSupplierCancel,
            supplierDeleteModal
        )

        deleteSupplierBtn.addEventListener('click', () =>{
            supplierDeleteModal.style.display = 'flex'
        })


        


        $(deleteSupplierDone).click(function(){

            const supplierId = $(this).data('supplier-id')

            fetch(`/suppliers/supplier/${supplierId}/delete/`, {
                method : 'DELETE',
                headers : {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    supplierDeleteModalMessage.style.display = 'flex'
                    supplierDeleteModalMessageText.textContent = data.error
                    supplierDeleteModalMessageCompleted.addEventListener('click', () =>{
                        supplierDeleteModal.style.display = 'none'
                        setTimeout(() =>{
                            supplierDeleteModalMessage.style.display = 'none'
                        }, 100)
                    })
                } else {
                    supplierDeleteModalMessage.style.display = 'flex'
                    supplierDeleteModalMessageText.textContent = data.success
                    supplierDeleteModalMessageCompleted.addEventListener('click', () =>{
                        supplierDeleteModal.style.display = 'none'
                        supplierDetailBody.innerHTML = ''
                        setTimeout(() =>{
                            supplierDeleteModalMessage.style.display = 'none'
                            supplierDetail.style.display = 'none'
                            loadSuppliers()
                        }, 100)

                    })
                }
            })
            .catch(error => console.error('Error' , error))

        })
        
    }

    const addSupplierFunction = () => {

        closeModalWindow(
            supplierCreateModalChevron,
            supplierCreateModal
        )

        supplierCreateModalChevron.addEventListener('click', () =>{
            $('#create-supplier-form')[0].reset();
        })

        supplierCreateMessageCompleted.addEventListener('click', () => {
            supplierCreateMessage.style.display = 'none'
            setTimeout(() =>{
                supplierCreateModal.style.display = 'none'
            }, 100)
        })


        $(supplierCreate).click(function(e) {
            e.preventDefault();

            $.ajax({
                url : '/suppliers/create/',
                method : 'GET',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                success : function(response) {
                    supplierCreateModal.style.display = 'flex'
                    $('#create-supplier-form').html(response);

                    const supplierCreateCancel = document.getElementById('supplier-create-cancel')
                    const supplierCreateCompleted = document.getElementById('supplier-create-completed')

                    $(supplierCreateCompleted).click(function(e) {
                        e.preventDefault()
                        var form = $('#create-supplier-form')[0];
                        if(form.checkValidity()){
                            console.log("Форма прошла валидацию");

                            // Сериализация данных формы
                            var formData = $('#create-supplier-form').serialize();
                            console.log("Сериализованные данные формы:", formData);

                            $.ajax({
                                url: '/suppliers/create/',
                                method: 'POST',
                                data: formData,  // Отправляем данные формы
                                headers: {
                                    'X-CSRFToken': getCSRFToken(),
                                },
                                success: function(response) {
                                    if (response.success) {
                                        supplierCreateMessage.style.display = 'flex'
                                        supplierCreateMessageText.textContent = 'Поставщик добавлен'
                                        $('#create-supplier-form')[0].reset();
                                        loadSuppliers()
                                    } else {
                                        supplierCreateMessage.style.display = 'flex'
                                        supplierCreateMessageText.textContent = 'Ошибка при сохранении данных'
                                        console.error("Ошибка при сохранении данных:", response.errors); 
                                    }
                                },
                                error: function(xhr, status, error) {
                                    console.error("Ошибка запроса при сохранении данных:", error);
                                }
                            });
                        } else {
                            // Если форма невалидна
                            console.log("Форма не прошла валидацию");
                            alert('Заполните все обязательные поля');
                        }
                    })
                    if (supplierCreateCancel) {
                        $(supplierCreateCancel).click(function(e) {
                            e.preventDefault();  // Останавливаем стандартное поведение
                            console.log("Форма отменена");
                            $('#create-supplier-form')[0].reset();
                            supplierCreateModal.style.display = 'none';  // Закрытие модального окна
                        });
                    }
                }
            })
        })
    }

    const editSupplierFunction = () => {
        // console.log("Функция editSupplierFunction вызвана");
        // console.log("CSRF Token:", getCSRFToken());

        closeModalWindow(
            updateSupplierRecordModalChevron,
            updateSupplierRecordModal
        )

        const cancelEditForm = () =>{
            updateSupplierModalFormCancel.addEventListener('click', function(e) {
                e.preventDefault()
                updateSupplierRecordModal.style.display = 'none'
            })
        }

        // updateSupplierSodalFormMessageComplete.addEventListener('click', () =>{
        //     updateSupplierRecordModal.style.display = 'none'
        //     setTimeout(() => {
        //         updateSupplierModalFormMessage.style.display = 'none'
        //     }, 100)
        // })

        editSupplierBtn.addEventListener('click', function (e) {
            e.preventDefault();
        
            const supplierId = $(this).data('supplier-id');
        
            $.ajax({
                url: `/suppliers/supplier/${supplierId}/edit/`,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function (response) {
                    updateSupplierRecordModal.style.display = 'flex';
                    $('#update-supplier-record-modal-body').html(response);
        
                    // Привязка обработчика для кнопки "Сохранить"
                    $(document).off('click', '#update-supplier-modal-form-complete').on('click', '#update-supplier-modal-form-complete', function (e) {
                        e.preventDefault();
        
                        $.ajax({
                            url: `/suppliers/supplier/${supplierId}/edit/`,
                            method: 'POST',
                            data: $('#update-supplier-record-modal-body form').serialize(),
                            headers: {
                                'X-CSRFToken': getCSRFToken()
                            },
                            success: function (response) {
                                $('#update-supplier-modal-form-message').css('display', 'flex');
                                $('#update-supplier-modal-form-message-text').text('Данные изменены');
                                loadSupplierDetails(supplierId);
                                loadSuppliers();
                                console.log("Успешный ответ сервера:", response);
                            },
                            error: function (xhr, status, error) {
                                $('#update-supplier-modal-form-message').css('display', 'flex');
                                $('#update-supplier-modal-form-message-text').text('Не удалось сохранить данные клиента.');
                                console.error('Ошибка при сохранении данных клиента:', error);
                                console.error("Ошибка AJAX-запроса:", xhr.responseText, status, error);
                            }
                        });
                    });
        
                    // Привязка обработчика для кнопки "Отмена"
                    $(document).off('click', '#update-supplier-modal-form-cancel').on('click', '#update-supplier-modal-form-cancel', function (e) {
                        e.preventDefault();
                        updateSupplierRecordModal.style.display = 'none';
                    });
                },
                error: function (xhr, status, error) {
                    console.error("Ошибка загрузки формы редактирования:", error);
                    console.error("Ошибка AJAX-запроса:", xhr.responseText, status, error);
                }
            });
        });
    } 
    
    const searchSupplierFunction = () =>{

        supplierSearchResetChevron.addEventListener('click', () =>{
            supplierSearch.value = ''
            loadSuppliers()
        })

        $(supplierSearch).on('input', function() {
            dashbordBody.innerHTML = ''
            const query = $(this).val()

            fetch('/suppliers/search/', {
                method : 'POST',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    "input_data": query,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if(data.suppliers) {
                  dashbordBody.innerHTML = '' 
                    let tableHtml = `
                    <div class="dashbord-body-table border-bottom-table">
                        <div class="dashbord-body-table-cell title"><p>Поставщик</p></div>
                        <div class="dashbord-body-table-cell title"><p>Менеджер</p></div>
                        <div class="dashbord-body-table-cell title"><p>Номер телефона</p></div>
                        <div class="dashbord-body-table-cell title"><p>Юридическое наименование</p></div>
                    </div>`;
                    $.each(data.suppliers, function(index, supplier) {
                    tableHtml += `
                        <div class="dashbord-body-table supplier-row" data-supplier-id="${supplier.id}">
                            <div class="dashbord-body-table-cell"><p>${supplier.name || ''}</p></div>
                            <div class="dashbord-body-table-cell"><p>${supplier.manager || ''}</p></div>
                            <div class="dashbord-body-table-cell"><p>${supplier.phone || ''}</p></div>
                            <div class="dashbord-body-table-cell"><p>${supplier.legal_name || ''}</p></div>
                        </div>`;
                    });

                    dashbordBody.innerHTML = tableHtml;

                    $('.supplier-row').click(function() {
                        const supplierId = $(this).data('supplier-id');
                        
                        loadSupplierDetails(supplierId);
                        
                    });
                } else{
                    alert('Error send data')
                }
            })
            .catch(error => {
                console.error('Ошибка запроса :', error)
            })
            })

        console.log(supplierSearchResetChevron, supplierSearch)
        console.log("функция searchSupplierFunction вызвана")
    }

    const getEquipmentForSupplier = (supplierId) =>{

        fetch(`/equipment/equipment-list/${supplierId}/filter/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => response.json())
            .then(data => {
                const records = data.records;        
                let htmlContent = ``
                for (const [category, items] of Object.entries(records)) {

                    htmlContent += '<div class="supplier-equipment-list-card">'
                    htmlContent += `<h3>${category}</h3>`; // Заголовок категории
                    htmlContent += `
                        <div class="supplier-equipment-list-card-body">
                            <div class="supplier-equipment-list-card-body-item card-title">Артикул</div>
                            <div class="supplier-equipment-list-card-body-item card-title">Номенклатура</div>
                            <div class="supplier-equipment-list-card-body-item card-title">Дата актуальности</div>
                            <div class="supplier-equipment-list-card-body-item card-title">стоимость</div>
                        </div>
                    `
                    if (items.length === 0) {
                        htmlContent += `<p>Нет записей в этой категории.</p>`;
                        continue;
                    }
                    items.forEach(item => {
                        htmlContent += `
                        <div data-equipment-id='${item.id}' class="supplier-equipment-list-card-body hover">
                            <div class="supplier-equipment-list-card-body-item">${item.article}</div>
                            <div class="supplier-equipment-list-card-body-item">${item.name}</div>                            
                            <div class="supplier-equipment-list-card-body-item">${item.date}</div>
                            <div class="supplier-equipment-list-card-body-item">${item.price}руб.</div>
                        </div>
                        `;
                    });
                    htmlContent += '</div>';
                }
        
                supplierEquipmentList.innerHTML = htmlContent;
            })
            .catch(error => console.error('Ошибка при получении данных:', error));
    }
})
