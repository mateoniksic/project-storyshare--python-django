const openModalContextButton = document.querySelectorAll('[data-modal-actions-target]');

function openContextMenu(modal) {
    if (modal == null) return;
    modal.classList.toggle('is-active');
}

openModalContextButton.forEach((button) => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalActionsTarget);

        openContextMenu(modal);
    });
});
