$(document).ready(function() {
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
    let isContentLoaded = false;
    let constansflag = false;
    let constandEditModal = false;
    let isDetailContentLoaded = false;

    let closeModalDetail,
        modalRecordDetail,
        recordDataDetail, 
        deleteClientDone, 
        deleteClientCancel,
        deleteModalChevron,
        deleteClientBtn,
        deleteModal,
        deleteModalDone,
        deleteModalDoneMessageText,
        deleteModalDoneOk;

    $('.load-content').click(function() {
        const url = $(this).data('url');

        $.ajax({
            url: url,
            method: 'GET',
            success: function(response) {
                $('#client-list').html(response);
                isContentLoaded = true;
                loadConstants();
                if (constansflag) {
                    loadClients();
                    closeModalDetail.addEventListener('click', () => {
                        recordModalVisible();
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке данных:', error);
                $('#client-list').html('<p>Не удалось загрузить данные.</p>');
            }
        });
    });

    const loadConstants = () => {
        closeModalDetail = document.querySelector('.close-modal-detail');
        modalRecordDetail = document.querySelector('.record-detail');
        recordDataDetail = document.getElementById('client-detail');
        clientList = document.getElementById('dashbord-body');

        if (closeModalDetail && modalRecordDetail && recordDataDetail && clientList) {
            constansflag = true;
        }
    };

    function loadClients() {
        if (constansflag) {
            $.ajax({
                url: '/clients/get-clients',
                method: 'GET',
                success: function(response) {
                    let clientsData = response.clients;
                    let tableHtml = `
                        <div class="dashbord-body-table">
                            <div class="dashbord-body-table-cell title"><p>Имя</p></div>
                            <div class="dashbord-body-table-cell title"><p>Город</p></div>
                            <div class="dashbord-body-table-cell title"><p>Телефон</p></div>
                            <div class="dashbord-body-table-cell title"><p>Электронная почта</p></div>
                            <div class="dashbord-body-table-cell title"><p>Ответственный</p></div>
                            <div class="dashbord-body-table-cell title"><p>Заметка</p></div>
                        </div>`;

                    $.each(clientsData, function(index, client) {
                        tableHtml += `
                            <div class="dashbord-body-table client-row" data-client-id="${client.id}">
                                <div class="dashbord-body-table-cell"><p>${client.name}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.city}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.phone}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.email}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.manager}</p></div>
                                <div class="dashbord-body-table-cell"><p>${client.note}</p></div>
                            </div>`;
                    });

                    clientList.innerHTML = tableHtml;

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

    function loadClientDetails(clientId) {
        $.ajax({
            url: `/clients/client/${clientId}`,
            method: 'GET',
            success: function(response) {
                $(recordDataDetail).html(response);
                showRecordModal();
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

    function showRecordModal() {
        modalRecordDetail.style.display = 'block';
        modalRecordDetail.style.width = 'calc(100% - 25px)';
        modalRecordDetail.style.transform = 'translateX(0)';
    }

    function recordModalVisible() {
        recordDataDetail.innerHTML = '';
        modalRecordDetail.style.width = '0';
        modalRecordDetail.style.transform = 'translateX(100%)';
        modalRecordDetail.style.display = 'none';
    }

    const inicializeConstansEditModal = () => {
        deleteClientDone = document.getElementById('delete-client-done');
        deleteClientCancel = document.getElementById('delete-client-cancel');
        deleteModalChevron = document.querySelector('.delete-modal-chevron');
        deleteClientBtn = document.getElementById('delete-client-btn');
        deleteModal = document.querySelector('.delete-modal');
        deleteModalDone = document.querySelector('.delete-modal-done');
        deleteModalDoneMessageText = document.querySelector('.delete-modal-done-message-text');
        deleteModalDoneOk = document.getElementById('delete-client-done-ok');

        if (deleteClientDone && deleteClientCancel && deleteModalChevron && deleteClientBtn &&
            deleteModal && deleteModalDone && deleteModalDoneMessageText && deleteModalDoneOk) {
            constandEditModal = true;
            console.log('Переменные инициализированы', deleteClientDone, 
                deleteClientCancel,
                deleteModalChevron,
                deleteClientBtn,
                deleteModal,
                deleteModalDone,
                deleteModalDoneMessageText,
                deleteModalDoneOk);
        }
    };


    function runAfterInitialization() {

        const closeModalWindowDeleteRecord = () => {
            deleteModal.style.display = 'none';
        };

        const openModalWindowDeleteRecord = () => {
            deleteModal.style.display = 'flex';
        };
    
        // Открыть окно с подтверждением удаления
        const openModalWindowDeleteDone = () => {
            deleteModalDone.style.display = 'flex';
        };
    
        // Закрыть окно с подтверждением удаления
        const closeModalWindowDeleteDone = () => {
            deleteModalDone.style.display = 'none';
        };
    
        // Открытие окна при нажатии на кнопку удаления
        deleteClientBtn.addEventListener('click', () => {
            openModalWindowDeleteRecord();
        });
    
        // Закрытие окна при нажатии на Chevron или отмену
        deleteModalChevron.addEventListener('click', closeModalWindowDeleteRecord);
        deleteClientCancel.addEventListener('click', closeModalWindowDeleteRecord);
    
        // Закрытие окна с подтверждением удаления
        deleteModalDoneOk.addEventListener('click', () => {
            closeModalWindowDeleteRecord();
            setTimeout(closeModalWindowDeleteDone, 150);
        });
        console.log("Константы инициализированы, запускаем дополнительные действия...");
        
        $(deleteClientDone).click(function() {
                    const clientId = $(this).data('client-id');
        
                    if (!clientId) {
                        console.error("Client ID is not available.");
                        return;
                    }
        
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

    }
            

});

            
            


        
     
