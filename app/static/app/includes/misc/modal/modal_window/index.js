const openModalWindowButton = document.querySelectorAll('[data-modal-window-target]');
const closeModalWindowButton = document.querySelectorAll('[data-button-close]');
const modalOverlayEl = document.getElementById('modal-overlay');

function openModalWindow(modal) {
    if (modal == null) return;
    modal.classList.add('modal-window--is-active');
    modalOverlayEl.classList.add('modal-overlay--is-active');
}

openModalWindowButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalWindowTarget);

        openModalWindow(modal);
    });
});

function closeModalWindow(modal) {
    if (modal == null) return;
    modal.classList.remove('modal-window--is-active');
    modalOverlayEl.classList.remove('modal-overlay--is-active');
}

closeModalWindowButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal-window');

        closeModalWindow(modal);
    });
});

modalOverlayEl.addEventListener('click', () => {
    const modal = document.querySelector('.modal-window--is-active');

    closeModalWindow(modal)
})