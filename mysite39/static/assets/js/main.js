(function () {
  "use strict";

  function initLatestNewsSlider() {
    var section = document.querySelector(".echo-latest-news-area");
    if (!section || typeof Swiper === "undefined") return;

    var swiperEl = section.querySelector(".mySwiper");
    if (!swiperEl) return;

    new Swiper(swiperEl, {
      slidesPerView: 1,
      spaceBetween: 20,
      grabCursor: true,
      navigation: {
        nextEl: section.querySelector(".swiper-button-next"),
        prevEl: section.querySelector(".swiper-button-prev"),
      },
      breakpoints: {
        576: { slidesPerView: 2, spaceBetween: 25 },
        992: { slidesPerView: 3, spaceBetween: 30 },
        1200: { slidesPerView: 4, spaceBetween: 30 },
      },
    });
  }

  function initMobileMenu() {
    var sidebar = document.getElementById("side-bar");
    var menuBtn = document.querySelector(".menu-btn");
    if (!sidebar || !menuBtn) return;

    var overlay = document.getElementById("anywhere-home");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "anywhere-home";
      document.body.appendChild(overlay);
    }

    var closeBtn = sidebar.querySelector(".close-icon-menu");

    function openMenu(e) {
      if (e) e.preventDefault();
      sidebar.classList.add("show");
      overlay.classList.add("bgshow");
      document.body.style.overflow = "hidden";
    }

    function closeMenu(e) {
      if (e) e.preventDefault();
      sidebar.classList.remove("show");
      overlay.classList.remove("bgshow");
      document.body.style.overflow = "";
    }

    menuBtn.addEventListener("click", openMenu);
    menuBtn.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openMenu();
      }
    });
    if (closeBtn) closeBtn.addEventListener("click", closeMenu);
    overlay.addEventListener("click", closeMenu);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && sidebar.classList.contains("show")) {
        closeMenu();
      }
    });

    sidebar.querySelectorAll("li.has-droupdown").forEach(function (item) {
      var trigger = item.querySelector(":scope > a");
      var submenu = item.querySelector(":scope > .submenu");
      if (!trigger || !submenu) return;

      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        item.classList.toggle("mm-active");
      });
    });
  }

  function initScrollTopButton() {
    var btn = document.querySelector(".scroll-top-btn");
    if (!btn) return;

    btn.removeAttribute("style");

    var threshold = 300;

    function toggleVisibility() {
      btn.classList.toggle("is-visible", window.scrollY > threshold);
    }

    window.addEventListener("scroll", toggleVisibility, { passive: true });
    toggleVisibility();

    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initLatestNewsSlider();
      initMobileMenu();
      initScrollTopButton();
    });
  } else {
    initLatestNewsSlider();
    initMobileMenu();
    initScrollTopButton();
  }
})();
