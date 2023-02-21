const page = document.querySelector('.app__content');
const main_header = document.querySelector('.main__header');

page.addEventListener('scroll', (event) => {
    if (event.target.scrollTop >= 48) {
        main_header.classList.remove('main__header--border-radius');
    } else {
        main_header.classList.add('main__header--border-radius');
    }
});
