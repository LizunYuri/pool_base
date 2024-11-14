$(document).ready(function() {
    // Функция для получения CSRF-токена из мета-тега
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    let dashbordBody,
        supplierDetail,
        loadListConstantFlag 

    $('#load-suppliers-list').click(function() {

        $('#client-list').html('');

        const url = $(this).data('url')

        console.log(url)

        $.ajax({
            url : url,
            method: 'GET',
            success: function(response) {

                $('#client-list').html(response);

                loadListConstants()

                if(loadListConstantFlag){
                    loadSuppliers();
                    console.log('Данные получены')
                    console.log(dashbordBody)
                    
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


        loadListConstantFlag = false


        if (dashbordBody){
            loadListConstantFlag = true
        }
    }

    const loadDetailConstans = () =>{
        supplierDetail = document.getElementById('supplier-detail');
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

    const loadSupplierDetails = (supplierId) => {
        if (!supplierId) {
            console.error("Ошибка: supplierId не задан");
            return;
        }
    console.log(supplierDetail)
        console.log(supplierId);  // Лог для проверки значения
        
        $.ajax({
            url: `/suppliers/supplier/${supplierId}`,
            method: 'GET',
            success: function(response) {
                console.log(supplierDetail)
                $(supplierDetail).html(response);
                console.log(supplierDetail)
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке данных клиента:', error);
                $(supplierDetail).html('<p>Не удалось загрузить данные о клиенте.</p>');
            }
        });
    };
    

})