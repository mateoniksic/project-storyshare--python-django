function swapForms() {
    const currentFormContainer = document.getElementsByClassName('container__item-2')[0];
    const currentForm = currentFormContainer.getElementsByClassName('form__container')[0];

    const newFormContainer = document.getElementsByTagName('template')[0];
    const newForm = newFormContainer.content.cloneNode(true);

    newFormContainer.content.replaceChildren(currentForm);
    currentFormContainer.append(newForm);
}