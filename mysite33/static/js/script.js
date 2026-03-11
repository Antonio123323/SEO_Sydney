    (function () {
    const nav = document.getElementById('mobile-nav');
    const burger = document.querySelector('.burger');

    if (!nav || !burger) return;

    // Вспомогательная функция — открыть
    function openNav() {
    // Ставим явную высоту = контенту
    nav.style.maxHeight = nav.scrollHeight + 'px';
    nav.classList.add('is-open');
    burger.classList.add('is-active');
    burger.setAttribute('aria-expanded', 'true');
    burger.setAttribute('aria-label', 'Закрыть меню');
}

    // Закрыть
    function closeNav() {
    // Перед закрытием ставим текущую высоту, чтобы анимация шла из неё
    nav.style.maxHeight = nav.scrollHeight + 'px';
    // Дальше в следующем тике уменьшаем до 0
    requestAnimationFrame(() => {
    nav.style.maxHeight = '0px';
    nav.classList.remove('is-open');
    burger.classList.remove('is-active');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Открыть меню');
});
}

    // Переключить
    function toggleNav() {
    const isOpen = nav.classList.contains('is-open');
    if (isOpen) {
    closeNav();
} else {
    openNav();
}
}

    // После окончания анимации, если открыто — фиксируем auto, чтобы адаптировалось к динамическим изменениям
    nav.addEventListener('transitionend', (e) => {
    if (e.propertyName !== 'max-height') return;
    if (nav.classList.contains('is-open')) {
    nav.style.maxHeight = 'none'; // позволяет контенту расти/схлопываться без повторной анимации
}
});

    // При открытии заново (если max-height была none) — вернуть числовое значение для плавности
    function prepareHeightForAnimation() {
    if (nav.classList.contains('is-open') && nav.style.maxHeight === 'none') {
    nav.style.maxHeight = nav.scrollHeight + 'px';
    // force reflow
    void nav.offsetHeight;
}
}

    burger.addEventListener('click', (e) => {
    e.stopPropagation();
    // если открыто и max-height none — подготовим к анимации
    prepareHeightForAnimation();
    toggleNav();
});

    // Клик снаружи — закрыть
    document.addEventListener('click', (e) => {
    if (!nav.classList.contains('is-open')) return;
    const clickInsideNav = nav.contains(e.target);
    const clickOnBurger = burger.contains(e.target);
    if (!clickInsideNav && !clickOnBurger) {
    closeNav();
}
});

    // Esc — закрыть
    document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
    closeNav();
}
});

    // Обновляем высоту при ресайзе (если меню открыто)
    window.addEventListener('resize', () => {
    if (nav.classList.contains('is-open')) {
    nav.style.maxHeight = 'none'; // пусть тянется под контент
}
});
})();