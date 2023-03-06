const openModalWindowButton = document.querySelectorAll('[data-modal-window-target]');
const closeModalWindowButton = document.querySelectorAll('[data-button-close]');
const modalOverlayEl = document.getElementById('modal-overlay');

function openModalWindow(modal) {
    if (modal == null) return;
    modal.classList.add('modal-window--isActive');
    modalOverlayEl.classList.add('modal-overlay--isActive');
}

openModalWindowButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalWindowTarget);

        openModalWindow(modal);
    });
});

function closeModalWindow(modal) {
    if (modal == null) return;
    modal.classList.remove('modal-window--isActive');
    modalOverlayEl.classList.remove('modal-overlay--isActive');
}

closeModalWindowButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal-window');

        closeModalWindow(modal);
    });
});
