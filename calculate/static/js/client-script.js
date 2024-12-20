$(document).ready(function() {
    // Функция для получения CSRF-токена из мета-тега
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    // Инициализация переменных для отслеживания состояния загрузки и модальных окон
    let isContentLoaded = false;
    let constansflag = false;
    let constandEditModal = false;
    let isDetailContentLoaded = false;
    let loadSearchFlag = false;

    

    // Переменные для элементов модальных окон
    let closeModalDetail,
        modalRecordDetail,
        recordDataDetail, 
        deleteClientDone, 
        deleteClientCancel,
        deleteModalChevron,
        deleteClientBtn,
        editClientBtn,
        deleteModal,
        deleteModalDone,
        deleteModalDoneMessageText,
        deleteModalDoneOk,
        closeClientList,
        editModalWindowChevron,
        cancelEditForm,
        editConstantFlag,
        doneEditForm,
        messageModalDone,
        messageModalDoneMessageText,
        clientSearch,
        searchInputReset,
        addClient,
        createModalWindowChevron,
        createModalWindow,
        cancelCreateForm,
        doneCreateForm,
        createMessageModalDone,
        createMessageModalDoneMessageText,
        createMessageClientDoneOk



    // Обработчик события при нажатии на кнопку для загрузки контента

    $('.load-content').click(function() {
        $('#client-list').html('');
        
            const url = $(this).data('url');  // URL для запроса данных

            // AJAX-запрос для загрузки содержимого
            $.ajax({
                url: url,
                method: 'GET',
                success: function(response) {
                    // Добавление загруженного контента в HTML и установка флага загрузки
                    $('#client-list').html(response);
                    isContentLoaded = true;

                    // Загрузка необходимых констант для работы с модальными окнами
                    loadConstants();
                    if (constansflag) {
                        // Загрузка списка клиентов, если константы загружены
                        loadClients();
                        closeClientList = document.querySelector('.close-client-list');

                        // Добавление события для закрытия модального окна при клике
                        closeModalDetail.addEventListener('click', () => {
                            recordModalVisible();
                        });

                        closeClientList.addEventListener('click', () => {
                            closeClientsListFunction();
                            document.getElementById('client-list').innerHTML = '';
                            console.log('Функция клика сработала');
                        });

                        loadSearchFlag = true;

                        if (loadSearchFlag) {
                            loadSearchConstant();

                            if (loadSearchConstant) {
                                searchClientAffter();
                                addClientAffter()
                                console.log(clientSearch, loadSearchFlag, addClient);
                            }
                        }
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при загрузке данных:', error);
                    $('#client-list').html('<p>Не удалось загрузить данные.</p>');
                }
            });
        
    });

    // Функция для инициализации элементов модальных окон
    const loadConstants = () => {
        closeModalDetail = document.querySelector('.close-modal-detail');
        modalRecordDetail = document.querySelector('.record-detail');
        recordDataDetail = document.getElementById('client-detail');
        clientList = document.getElementById('dashbord-body');
        closeClientList = document.querySelector('.close-client-list')
        addClient = document.getElementById('add-client')
        createModalWindow = document.querySelector('.create-modal-window')
        createModalWindowChevron = document.querySelector('.create-modal-window-chevron')
        cancelCreateForm = document.getElementById('cancel-create-form')
        createMessageModalDone = document.querySelector('.create-message-modal-done')
        createMessageModalDoneMessageText = document.querySelector('.create-message-modal-done-message-text')
        createMessageClientDoneOk = document.getElementById('create-message-client-done-ok')

        // Установка флага при успешной инициализации всех необходимых элементов
        if (addClient && closeModalDetail && modalRecordDetail && recordDataDetail && clientList) {
            constansflag = true;
        }
    };

    const loadSearchConstant = () =>{
        clientSearch = document.getElementById('client-search')
        searchInputReset = document.querySelector('.search-input-reset')
    }

    // Функция для загрузки списка клиентов
    function loadClients() {
        if (constansflag) {
            $.ajax({
                url: '/clients/get-clients',
                method: 'GET',
                success: function(response) {
                    let clientsData = response.clients;

                    // Формирование HTML для отображения данных клиентов
                    let tableHtml = `
                        <div class="dashbord-body-table border-bottom-table">
                            <div class="dashbord-body-table-cell title"><p>Имя</p></div>
                            <div class="dashbord-body-table-cell title"><p>Город</p></div>
                            <div class="dashbord-body-table-cell title"><p>Телефон</p></div>
                            <div class="dashbord-body-table-cell title"><p>Электронная почта</p></div>
                            <div class="dashbord-body-table-cell title"><p>Ответственный</p></div>
                            <div class="dashbord-body-table-cell title"><p>Заметка</p></div>
                        </div>`;

                    // Добавление информации о каждом клиенте в таблицу
                    $.each(clientsData, function(index, client) {
                        tableHtml += `
                            <div class="dashbord-body-table client-row" data-client-id="${client.id}">
                                <div class="dashbord-body-table-cell"><p>${client.name || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.city || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.phone || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.email || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.manager || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.note || ''}</p></div>
                            </div>`;
                    });

                    clientList.innerHTML = tableHtml;


                    // Добавление обработчика клика для загрузки деталей клиента
                    $('.client-row').click(function() {
                        const clientId = $(this).data('client-id');
                        loadClientDetails(clientId);
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при загрузке списка клиентов:', error);
                    clientList.innerHTML = '<p>Не удалось загрузить данные клиентов.</p>';
                }
            });
        }
    }

    function searchClientAffter() {

        searchInputReset.addEventListener('click', () =>{
            clientSearch.value = ''
            loadClients()
        })

        $(clientSearch).on('input', function() {
            clientList.innerHTML = '';
            const query = $(this).val();
            
            
    
            fetch('/clients/search/', {
                method: "POST",
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
                if (data.clients) {
                    clientList.innerHTML = '';
    
                    let tableHtml = `
                        <div class="dashbord-body-table border-bottom-table">
                            <div class="dashbord-body-table-cell title"><p>Имя</p></div>
                            <div class="dashbord-body-table-cell title"><p>Город</p></div>
                            <div class="dashbord-body-table-cell title"><p>Телефон</p></div>
                            <div class="dashbord-body-table-cell title"><p>Электронная почта</p></div>
                            <div class="dashbord-body-table-cell title"><p>Ответственный</p></div>
                            <div class="dashbord-body-table-cell title"><p>Заметка</p></div>
                        </div>`;
    
                    $.each(data.clients, function(index, client) {  // изменяем clients на data.clients
                        tableHtml += `
                            <div class="dashbord-body-table client-row" data-client-id="${client.id}">
                                <div class="dashbord-body-table-cell"><p>${client.name || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.city || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.phone || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.email || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.manager || ''}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.note || ''}</p></div>
                            </div>`;
                    });
    
                    clientList.innerHTML = tableHtml;
                    
                    $('.client-row').click(function() {
                        const clientId = $(this).data('client-id');
                        loadClientDetails(clientId);
                    });
                } else {
                    alert("Ошибка при отправке данных");
                }
            })
            .catch(error => {
                console.error("Ошибка запроса:", error);
            });
        });
    }

    function addClientAffter() {

        createMessageClientDoneOk.addEventListener('click', () => {
            createModalWindow.style.display = 'none'
            setTimeout(() =>{
                createMessageModalDone.style.display = 'none'
                loadClients()
            }, 100)
        })

        createModalWindowChevron.addEventListener('click', () =>{
            createModalWindow.style.display = 'none'
            $('#create-client-form')[0].reset();
        })

        $(addClient).click(function(e) {
            e.preventDefault();
        
            $.ajax({
                url: '/clients/create/',
                method: 'GET',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                success: function(response) {
                    createModalWindow.style.display = 'flex';  // Открытие модального окна
                    $('#create-client-form').html(response); 

                    const cancelCreateForm = document.getElementById('cancel-create-form');
                    const doneCreateForm = document.getElementById('done-create-form');

        
                    // Привязка событий
                    $(doneCreateForm).click(function(e) {
                        e.preventDefault();  // Останавливаем стандартное поведение формы
                        var form = $('#create-client-form')[0];
                            if (form.checkValidity()) {  // Проверяем форму на валидность
                                console.log("Форма прошла валидацию");

                                // Сериализация данных формы
                                var formData = $('#create-client-form').serialize();
                                console.log("Сериализованные данные формы:", formData);

                                $.ajax({
                                    url: '/clients/create/',
                                    method: 'POST',
                                    data: formData,  // Отправляем данные формы
                                    headers: {
                                        'X-CSRFToken': getCSRFToken(),
                                    },
                                    success: function(response) {
                                        if (response.success) {
                                            createMessageModalDone.style.display = 'block'
                                            createMessageModalDoneMessageText.textContent = 'Запись успешно сохранена'
                                            $('#create-client-form')[0].reset();
                                            loadClients()
                                        } else {
                                            
                                            console.error("Ошибка при сохранении данных:", response.errors);
                                            alert('Ошибка при сохранении данных');
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
                    });
        
                    // Если кнопка отмены существует, назначаем обработчик
                    if (cancelCreateForm) {
                        $(cancelCreateForm).click(function(e) {
                            e.preventDefault();  // Останавливаем стандартное поведение
                            console.log("Форма отменена");
                            $('#create-client-form')[0].reset();
                            createModalWindow.style.display = 'none';  // Закрытие модального окна
                        });
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Ошибка запроса при открытии формы:", error);
                }
            });
        });
        
    }

    const closeClientsListFunction = () => {
        clientList.innerHTML = '';
    }

    // Функция для загрузки деталей конкретного клиента
    function loadClientDetails(clientId) {
        $.ajax({
            url: `/clients/client/${clientId}`,
            method: 'GET',
            success: function(response) {
                $(recordDataDetail).html(response);
                showRecordModal();  // Отображение модального окна
                isDetailContentLoaded = true;

                if (isDetailContentLoaded) {
                    inicializeConstansEditModal();

                    if (constandEditModal) {
                        runAfterInitialization();
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке данных клиента:', error);
                $('#client-detail').html('<p>Не удалось загрузить данные о клиенте.</p>');
            }
        });
    }

    // Функция для отображения модального окна с деталями клиента
    function showRecordModal() {
        modalRecordDetail.style.display = 'block';
        modalRecordDetail.style.width = 'calc(100% - 25px)';
        modalRecordDetail.style.transform = 'translateX(0)';
    }

    // Функция для скрытия модального окна с деталями клиента
    function recordModalVisible() {
        recordDataDetail.innerHTML = '';
        modalRecordDetail.style.width = '0';
        modalRecordDetail.style.transform = 'translateX(100%)';
        modalRecordDetail.style.display = 'none';
    }

    // Функция для инициализации элементов модального окна удаления
    const inicializeConstansEditModal = () => {
        deleteClientDone = document.getElementById('delete-client-done');
        deleteClientCancel = document.getElementById('delete-client-cancel');
        deleteModalChevron = document.querySelector('.delete-modal-chevron');
        deleteClientBtn = document.getElementById('delete-client-btn');
        deleteModal = document.querySelector('.delete-modal');
        deleteModalDone = document.querySelector('.delete-modal-done');
        deleteModalDoneMessageText = document.querySelector('.delete-modal-done-message-text');
        deleteModalDoneOk = document.getElementById('delete-client-done-ok');
        editClientBtn = document.getElementById('edit-client-btn');

        
        editModalWindowChevron = document.querySelector('.edit-modal-window-chevron')

        if (deleteClientDone && deleteClientCancel && deleteModalChevron && deleteClientBtn &&
            deleteModal && deleteModalDone && deleteModalDoneMessageText && deleteModalDoneOk) {
            constandEditModal = true;
        }
    };


    const inicializeEditModalConstans = () =>{
        cancelEditForm = document.getElementById('cancel-edit-form')
        doneEditForm = document.getElementById('done-edit-form')
        messageModalDone = document.getElementById('message-client-done-ok')
        messageModalDoneMessageText = document.querySelector('.message-modal-done-message-text')
        editConstantFlag = true
    }

    // Функция для выполнения действий после инициализации
    function runAfterInitialization() {

        // Закрытие окна подтверждения удаления
        const closeModalWindowDeleteRecord = () => {
            deleteModal.style.display = 'none';
        };

        // Открытие окна подтверждения удаления
        const openModalWindowDeleteRecord = () => {
            deleteModal.style.display = 'flex';
        };

        // Открытие окна с сообщением об успешном удалении
        const openModalWindowDeleteDone = () => {
            deleteModalDone.style.display = 'flex';
        };

        // Закрытие окна с сообщением об успешном удалении
        const closeModalWindowDeleteDone = () => {
            deleteModalDone.style.display = 'none';
        };

        // Открытие окна при нажатии на кнопку удаления
        deleteClientBtn.addEventListener('click', () => {
            openModalWindowDeleteRecord();
        });

        const openEditModalWindow = () =>{
            document.querySelector('.edit-modal-window').style.display = 'flex'
        }

        const closeEditModalWindow = () =>{
            document.querySelector('.edit-modal-window').style.display = 'none'
        }

        // Закрытие окна при нажатии на Chevron или кнопку отмены
        deleteModalChevron.addEventListener('click', closeModalWindowDeleteRecord);
        deleteClientCancel.addEventListener('click', closeModalWindowDeleteRecord);
        editModalWindowChevron.addEventListener('click', closeEditModalWindow)


        // Закрытие окна с сообщением об удалении при подтверждении
        deleteModalDoneOk.addEventListener('click', () => {
            closeModalWindowDeleteRecord();
            recordModalVisible();
            loadClients()
            setTimeout(closeModalWindowDeleteDone, 150);
           
        });

        // Обработчик для удаления клиента
        $(deleteClientDone).click(function() {
            const clientId = $(this).data('client-id');

            if (!clientId) {
                console.error("Client ID is not available.");
                return;
            }

            // AJAX-запрос для удаления клиента
            $.ajax({
                url: `/clients/client/${clientId}/delete/`,
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken()  // Передача CSRF-токена
                },
                success: function(response) {
                    openModalWindowDeleteDone();
                    deleteModalDoneMessageText.textContent = 'Клиент успешно удален.';
                    console.log('Клиент успешно удален');
                },
                error: function(xhr, status, error) {
                    deleteModalDoneMessageText.textContent = 'Не удалось удалить клиента.';
                    console.error('Ошибка при удалении клиента:', error);
                }
            });
        });

        const afterEditRecord = () => {
            cancelEditForm.addEventListener('click', function(event) {
                event.preventDefault();  // Отменяет стандартное поведение отправки формы
                closeEditModalWindow();  // Закрывает модальное окно
            });

            messageModalDone.addEventListener('click', function(event) {
                event.preventDefault();  // Отменяет стандартное поведение отправки формы
                closeEditModalWindow();  // Закрывает модальное окно

            });

        }

        $(editClientBtn).click(function(event) {
            event.preventDefault();
    
            const clientId = $(this).data('client-id');
    
            if (!clientId) {
                console.error("Client ID is not available.");
                return;
            }
            $.ajax({
                url: `/clients/client/${clientId}/edit/`,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function(response) {
                    openEditModalWindow();
                    $('#edit-modal-window').html(response);
    
                    isDetailContentLoaded = true;
    
                    if (isDetailContentLoaded) {
                        inicializeEditModalConstans();
    
                        if (editConstantFlag) {
                            afterEditRecord();
                        }
    
                        // Добавляем обработчик для кнопки "Сохранить"
                        $('#done-edit-form').click(function(event) {
                            event.preventDefault();  // Предотвращаем стандартную отправку формы
    
                            $.ajax({
                                url: `/clients/client/${clientId}/edit/`,
                                method: 'POST',
                                data: $('#edit-client-form').serialize(),  // Отправка данных формы
                                headers: {
                                    'X-CSRFToken': getCSRFToken()
                                },
                                success: function(response) {
                                    document.querySelector('.message-modal-done').style.display = 'flex'
                                    messageModalDoneMessageText.textContent = 'Данные клиента успешно сохранены!'
                                    loadClientDetails(clientId);
                                    loadClients()
                                },
                                error: function(xhr, status, error) {
                                    document.querySelector('.message-modal-done').style.display = 'flex'
                                    messageModalDoneMessageText.textContent = 'Не удалось сохранить данные клиента.'
                                    console.error('Ошибка при сохранении данных клиента:', error);
                                }
                            });
                        });
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error loading edit form:", error);
                }
            });
        });
    }
});