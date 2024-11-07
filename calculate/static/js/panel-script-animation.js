const panelHeaderAccountLink = document.querySelector('.panel-header-account-link')
const panelHeaderLogout = document.querySelector('.panel-header-logout')
const panelHeaderLogoutBtn = document.querySelectorAll('.panel-header-logout-btn')
const userChevron = document.getElementById('user-chevron')

const animationLogounPanel = () => {
let clicked = false

    panelHeaderAccountLink.addEventListener('click', () => {
        userChevron.style.rotateZ = '180deg'
        if(!clicked) {
            panelHeaderLogout.style.height = '300px'
            userChevron.style.transform = 'rotateZ(180deg)'
            
            setTimeout(() =>{   
                panelHeaderLogoutBtn.forEach((e, index) => {
                    e.style.display = 'flex'
                    setTimeout(() => {   
                        e.style.opacity = 1
                        e.style.transform = 'translateX(0)';
                    }, 100 * index)
                })
            }, 500)
        } else{
            panelHeaderLogoutBtn.forEach((e, index) => {
                setTimeout(() => {
                    e.style.transform = 'translateX(20px)';
                    e.style.opacity = 0
                    setTimeout(() => {   
                        e.style.display = 'none'
                    }, 100 * index)
                }, 100 * index)
            })
            setTimeout(() => {
                panelHeaderLogout.style.height = 0
                userChevron.style.transform = 'rotateZ(0)'
            }, 500)
            
        }
        clicked = !clicked
    })
    
}

document.addEventListener("DOMContentLoaded", () => {
    animationLogounPanel()
});