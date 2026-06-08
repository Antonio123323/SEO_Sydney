(function () {
    var config = window.TRACKING_CONFIG || {};

    function loadScript(src, attrs) {
        if (!src) return;

        var existingScripts = document.getElementsByTagName('script');
        for (var i = 0; i < existingScripts.length; i++) {
            if (existingScripts[i].src === src) return;
        }

        var script = document.createElement('script');
        script.src = src;
        script.async = true;

        if (attrs) {
            for (var key in attrs) {
                if (Object.prototype.hasOwnProperty.call(attrs, key)) {
                    script.setAttribute(key, attrs[key]);
                }
            }
        }

        var firstScript = document.getElementsByTagName('script')[0];
        if (firstScript && firstScript.parentNode) {
            firstScript.parentNode.insertBefore(script, firstScript);
        } else {
            document.head.appendChild(script);
        }
    }

    function initYandexMetrika() {
        var ymConfig = config.yandexMetrika;

        if (!ymConfig || !ymConfig.enabled || !ymConfig.id) return;

        (function (m, e, t, r, i, k, a) {
            m[i] = m[i] || function () {
                (m[i].a = m[i].a || []).push(arguments);
            };
            m[i].l = 1 * new Date();

            for (var j = 0; j < document.scripts.length; j++) {
                if (document.scripts[j].src === r) return;
            }

            k = e.createElement(t);
            a = e.getElementsByTagName(t)[0];
            k.async = 1;
            k.src = r;

            if (a && a.parentNode) {
                a.parentNode.insertBefore(k, a);
            } else {
                e.head.appendChild(k);
            }
        })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');

        window.ym(Number(ymConfig.id), 'init', ymConfig.initOptions || {});

        var noscript = document.createElement('noscript');
        var wrapper = document.createElement('div');
        var img = document.createElement('img');

        img.src = 'https://mc.yandex.ru/watch/' + ymConfig.id;
        img.style.position = 'absolute';
        img.style.left = '-9999px';
        img.alt = '';

        wrapper.appendChild(img);
        noscript.appendChild(wrapper);
        document.body.appendChild(noscript);
    }

    function initGoogleAnalytics() {
        var gaConfig = config.googleAnalytics;

        if (!gaConfig || !gaConfig.enabled || !gaConfig.id) return;

        loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaConfig.id));

        window.dataLayer = window.dataLayer || [];
        window.gtag = window.gtag || function () {
            window.dataLayer.push(arguments);
        };

        window.gtag('js', new Date());
        window.gtag('config', gaConfig.id);
    }

    function startTracking() {
        initYandexMetrika();
        initGoogleAnalytics();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startTracking);
    } else {
        startTracking();
    }
})();