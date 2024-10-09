const formQuestion = document.querySelectorAll('.question');
const resetButton = document.querySelector('button[type="reset"]');
const clientForm = document.querySelector('.add-client-form');
const addClientModal = document.getElementById('addClientModal');
const closeModal = document.querySelector('.close-btn');
const openModalBtn = document.getElementById('openAddClientModal')


const openModalFunction = () => {
    openModalBtn.addEventListener('click', () => {
        addClientModal.style.display = 'flex'
    })

    closeModal.addEventListener('click', () => {
        addClientModal.style = 'none'
    })

    window.addEventListener('click', (event) => {
        if (event.target === addClientModal) {
            addClientModal.style.display = 'none'
        }
    })
}

const resetForm = () => {
    resetButton.addEventListener('click', () => {
        if (clientForm) {
            clientForm.reset(); // Сбрасываем форму
        }
    });
}

const helpTextVisible = () => {
    formQuestion.forEach((question) => {
        question.addEventListener('mouseenter', () => {
            const helpText = question.nextElementSibling; // Получаем следующий элемент (help-text)
            if (helpText && helpText.classList.contains('help-text')) {
                helpText.style.display = 'flex'; // Показываем help-text при наведении
            }
        });

        question.addEventListener('mouseleave', () => {
            const helpText = question.nextElementSibling; // Получаем следующий элемент (help-text)
            if (helpText && helpText.classList.contains('help-text')) {
                helpText.style.display = 'none'; // Скрываем help-text при уходе курсора
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    resetForm()
    helpTextVisible();
    openModalFunction()
});
