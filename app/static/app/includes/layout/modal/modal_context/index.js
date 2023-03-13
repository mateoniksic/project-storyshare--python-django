const openContextMenuButton = document.querySelectorAll('[data-modal-actions-target]');

function openContextMenu(contextMenu) {
    if (contextMenu == null) return;
    contextMenu.classList.toggle('context-menu--is-active');
}

openContextMenuButton.forEach((button) => {
    button.addEventListener('click', () => {
        const contextMenu = document.querySelector(button.dataset.modalActionsTarget);

        openContextMenu(contextMenu);
    });
});
