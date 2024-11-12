const panelHeaderAccountLink = document.querySelector('.panel-header-account-link')
const panelHeaderLogout = document.querySelector('.panel-header-logout')
const panelHeaderLogoutBtn = document.querySelectorAll('.panel-header-logout-btn')
const userChevron = document.getElementById('user-chevron')
const visibleEquipmentSubnavigation = document.getElementById('visibleEquipmentSubnavigation')
const visibleEquipmentChevron = document.getElementById('visibleEquipmentChevron')
const visibleEquipment = document.getElementById('visibleEquipment')
const equipmentList = document.querySelectorAll('.equipment-list')
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


const navAnimationList = (element, block, list, chevron) =>{
    let clicked = false
    console.log('click')

    element.addEventListener('click', () => {

        
        console.log('click')
        if(!clicked){
            block.style.display = 'flex';
            chevron.style.transform = 'rotateZ(180deg)'
            setTimeout(() => {
                block.style.opacity = 1
                block.style.height = '200px'
            }, 100)
            setTimeout(() => {
                list.forEach((e, index) =>{
                    e.style.display = 'flex';
                    setTimeout(() => {
                        e.style.opacity = 1
                        e.style.transform = 'translateX(0px)'
                    }, 50 * index)
                })
            }, 250)
            clicked = true
        } else {
            list.forEach((e, index) =>{
                setTimeout(() => {
                    e.style.transform = 'translateX(-20px)'
                    setTimeout(() =>{
                        e.style.opacity = 0
                        e.style.display = 'flex';
                    }, 50)
                }, 50 * index)
            })
            setTimeout(() => {
                block.style.height = 0
                block.style.opacity = 0
               chevron.style.transform = 'rotateZ(0)'
            }, 200)
            setTimeout(() => {
                block.style.display = 'none';
            }, 700)
            clicked = false
        }
    }) 
}

document.addEventListener("DOMContentLoaded", () => {
    animationLogounPanel()
    navAnimationList(
                    visibleEquipment,
                    visibleEquipmentSubnavigation,
                    equipmentList,
                    visibleEquipmentChevron
                    )
});