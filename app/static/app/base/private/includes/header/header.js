function setActiveLink() {
    const links = document.getElementsByClassName('link-list__link');
    const current_link_href = window.location.href.split(/[/?#]/)[3];

    for (let i = 0; i < links.length; i++) {
        let link = links[i];
        let link_href = link.href.split(/[/?#]/)[3];

        if (link_href === current_link_href) {
            link.classList.toggle('link-list__link--active');

            const hasIcon = link.querySelector('.icon use');

            if (hasIcon) {
                const linkIconFilled = hasIcon.attributes['xlink:href'].value.concat('-filled');
                hasIcon.setAttribute('xlink:href', linkIconFilled);
            }
        }
    }
}

setActiveLink();
