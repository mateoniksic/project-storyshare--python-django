function setActiveLink() {
    const links = document.querySelectorAll('.link-list__item > a');
    const current_link_href = window.location.href.split(/[/?#]/)[3];

    for (let i = 1; i < links.length; i++) {
        const link = links[i];
        const link_href = link.href.split(/[/?#]/)[3];
        
        if (link_href === current_link_href) {         
            link.parentElement.classList.toggle('link-list__item--active');

            const hasIcon = link.querySelector('.icon use');

            if (hasIcon) {
                const linkIconFilled = hasIcon.attributes['xlink:href'].value.concat('-filled');
                hasIcon.setAttribute('xlink:href', linkIconFilled);
            }
        }
    }
}

setActiveLink();
