
$(document).ready(function() {
    // Функция для получения CSRF-токена из мета-тега
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

   const clientList = document.getElementById('client-list')

    $('#load-pumps-list').click(function() {
        $('#client-list').html('');
            $.ajax({
                url: '/equipment/get-equipment/',
                method: 'GET',
                success: function(response) {
                    let pumpsData = response.pumps;

                    console.log(pumpsData)
                    let tableHtml = `
                        <div class="dashbord-body-table border-bottom-table">
                            <div class="dashbord-body-table-cell title"><p>Артикул</p></div>
                            <div class="dashbord-body-table-cell title"><p>Наименование</p></div>
                            <div class="dashbord-body-table-cell title"><p>Мощность</p></div>
                            <div class="dashbord-body-table-cell title"><p>РРЦ</p></div>
                            <div class="dashbord-body-table-cell title"><p>Поставщик</p></div>
                        </div>`;
                        $.each(pumpsData, function(index, client) {
                            tableHtml += `
                                <div class="dashbord-body-table client-row" data-client-id="${client.id}">
                                    <div class="dashbord-body-table-cell"><p>${client.article || ''}</p></div>
                                    <div class="dashbord-body-table-cell"><p>${client.name || ''}</p></div>
                                    <div class="dashbord-body-table-cell"><p>${client.power || ''} м3/ч</p></div>
                                    <div class="dashbord-body-table-cell"><p>${client.price || ''} руб</p></div>
                                    <div class="dashbord-body-table-cell"><p>${client.supplier || ''}</p></div>
                                 </div>`;
                        });
    
                        clientList.innerHTML = tableHtml;
    
                    
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при загрузке списка клиентов:', error);
                    clientList.innerHTML = '<p>Не удалось загрузить данные клиентов.</p>';
                }
            });
    });


});