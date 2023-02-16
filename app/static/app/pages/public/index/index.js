const SECTION_HERO_HEIGHT = document.body.querySelector('.section__hero').offsetHeight;
const HEADER_HEIGHT = document.body.querySelector('.header').offsetHeight;

function changeHeaderStyle(css) {
    const headerEl = document.body.querySelector('.header');
    for (const [property, value] of Object.entries(css)) {
        headerEl.style[property] = value;
    }
}

window.addEventListener('scroll', () => {
    let css = {};

    if (window.pageYOffset <= SECTION_HERO_HEIGHT - HEADER_HEIGHT) {
        css = {
            color: 'var(--color-light)',
            backgroundColor: 'rgba(255, 255, 255, 0)',
        };
    } else {
        css = {
            color: 'var(--color-primary)',
            backgroundColor: 'rgba(255, 255, 255, 0.5)',
        };
    }

    changeHeaderStyle(css);
});
