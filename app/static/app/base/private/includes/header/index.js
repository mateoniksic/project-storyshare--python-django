(function setLinkIsActive() {
    const links = Array.from(document.querySelectorAll('header .nav__item a')).slice(1);

    links.forEach((link) => {
        if (link.pathname === window.location.pathname) {
            link.closest('.nav__item').classList.add('nav__item--isActive');

            const hasIcon = link.querySelector('.icon > use');
            if (hasIcon) {
                iconFilledPath = hasIcon.attributes['xlink:href'].value.concat('-filled');
                hasIcon.setAttribute('xlink:href', iconFilledPath);
            }
        }
    });
})();
