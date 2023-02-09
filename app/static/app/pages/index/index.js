const SECTION_HERO_HEIGHT = document.body.querySelector('.section__hero').offsetHeight;
const HEADER_HEIGHT = document.body.querySelector('.header').offsetHeight;

function changeHeaderStyle(css) {
    const headerEl = document.body.querySelector('.header');
    headerEl.style.color = css.color;
    headerEl.style.backgroundColor = css.backgroundColor;
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
