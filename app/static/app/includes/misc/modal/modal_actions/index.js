const openModalActionsButton = document.querySelectorAll('[data-modal-actions-target]');

function openModalActions(modal) {
    if (modal == null) return;
    modal.classList.toggle('modal-actions--active');
}

openModalActionsButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalActionsTarget);

        openModalActions(modal);
    });
});
