$(document).ready(function() {

    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    let loadUpdateUserFormFlag = false
    let isError = false

    let profileSubtitle,
        profileNavPersonalData,
        profileFormInput, //класс инпута изменения профиля
        passwordVisible, //класс инпута для изменения видимости пароля
        updatePersonalDataChevron, // кнопка закрытия модального окна
        updatePersonalData, // модальное окно
        updatePersonalBody, // тело модального окна
        openModalWindowUpdateProfile,
        updateProfileForm,
        changePasswordForm,
        messageProfileBtn,
        messageProfileText,
        messageProfileCard,
        passwordVisibleChevron
        



    const addActiveStyle = () => {
        const navChecked = document.querySelectorAll('.nav-checked'); // Находим все элементы
        
        navChecked.forEach(el => {
            el.addEventListener("click", () => {
                
                navChecked.forEach(nav => nav.classList.remove('is-active'));
    
                el.classList.add('is-active');
            });
        });
    };

    const loadElementsModalUpdateUser = () => {
        
        passwordVisible = document.querySelectorAll('.password-visible')
        updateProfileForm = document.getElementById('update-profile-form')
        changePasswordForm = document.getElementById('change-password-form')
        passwordVisibleChevron = document.querySelectorAll('.password-visible-chevron')
        passwordVisible = document.querySelectorAll('.password-visible')
        if(passwordVisible && passwordVisible){
            loadUpdateUserFormFlag = true
        }
    }

    const updateUserProfile = () => {

        openModalWindowUpdateProfile = document.getElementById('open-modal-window-update-profile')
        updatePersonalData = document.getElementById('update-personal-data')
        updatePersonalDataChevron = document.getElementById('update-personal-data-chevron')
        updatePersonalBody = document.getElementById('update-personal-body')
        messageProfileBtn = document.getElementById('message-profile-btn')
        messageProfileText = document.getElementById('message-profile-text')
        messageProfileCard = document.getElementById('message-profile-card')

        updatePersonalDataChevron.addEventListener('click', () => {
            updatePersonalData.style.display = 'none'
        })

        openModalWindowUpdateProfile.addEventListener('click', () => {
            updatePersonalData.style.display = 'flex'
            updatePersonalData.style.filter = 'blur(0px)'
            loadUpdateUserForm()
        })

        const openProfileMessage = () => {
            messageProfileCard.style.display = 'flex'
            updatePersonalData.style.filter = 'blur(2px)'
        }

        const closeProfileMessage = () => {

            if(isError) {
                messageProfileCard.style.display = 'none'
                messageProfileText.innerHTML = ''
                updatePersonalData.style.filter = 'blur(0px)'
                isError = false
            } else {
                updatePersonalData.style.display = 'none'
                setTimeout(() => {
                    messageProfileCard.style.display = 'none'
                    messageProfileText.innerHTML = ''
                },150)
            }
        }

        const errorListForMessage = (errors) =>{
            messageProfileText.innerHTML = ''


            const ul = document.createElement('ul')

            for (const field in errors) {
                const li = document.createElement('li')
                li.innerHTML = `${errors[field].join(',</br>')}`
                ul.appendChild(li)
            }

            messageProfileText.appendChild(ul)
        }

        messageProfileBtn.addEventListener('click', () => {
            closeProfileMessage()
        })


        const visiblePassword = () =>{

            let isLeftMouseButtonDown = false

            passwordVisibleChevron.forEach(el => {
                el.addEventListener('mousedown', (e) =>{
                    if (e.button === 0){
                        isLeftMouseButtonDown = true

                        passwordVisible.forEach(e =>{
                            e.type = 'text'
                        })
                    }
                })

            })

            passwordVisibleChevron.forEach(el => {
                el.addEventListener('mouseup', (e) =>{
                    if (e.button === 0){
                        isLeftMouseButtonDown = false

                        passwordVisible.forEach(e =>{
                            e.type = 'password'
                        })
                    }
                })

            })
            
        }

        

        const loadUpdateUserForm = () =>{
            fetch('/login/update-profile/',{
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(response => response.text())
                .then(html => {

                    updatePersonalBody.innerHTML = html
                    loadElementsModalUpdateUser()
                    setupFormHandlers()
                    visiblePassword()
                })
        }

        const setupFormHandlers = () => {

            if (loadUpdateUserFormFlag) {
                updateProfileForm.addEventListener('submit', (e) => {
                    e.preventDefault();

                    const formData = new FormData(updateProfileForm);

                    formData.append('update_profile', 'true');

                    fetch('/login/update-profile-save/', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'X-Requested-With': 'XMLHttpRequest',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("полученные данные:", data);
                        if (data.success) {
                            openProfileMessage()
                            messageProfileText.innerHTML = data.message
                        } else {
                            isError = true
                            openProfileMessage()
                            errorListForMessage(data.errors)
                        }
                    })
                    .catch(error => {
                        console.log('Error send form', error);
                        isError = true
                        openProfileMessage()
                        errorListForMessage(data.errors)
                    })
                })


                changePasswordForm.addEventListener('submit', (e) => {
                    e.preventDefault();

                    const formData = new FormData(changePasswordForm);

                    formData.append('change_password', 'true');

                        fetch('/login/update-profile-save/', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'X-Requested-With': 'XMLHttpRequest',
                        }
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                openProfileMessage()
                                messageProfileText.innerHTML = data.message
                            } else {
                                isError = true
                                messageProfileText.innerHTML = ''
                                openProfileMessage()
                                errorListForMessage(data.errors)
                            }
                        })
                        .catch(error => {
                            console.log('Error send form', error);
                            isError = true
                            openProfileMessage()
                            errorListForMessage(data.errors)
                        });
                })
            }
        }        
    }
    
   addActiveStyle()
   updateUserProfile() 
})
