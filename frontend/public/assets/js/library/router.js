var Router = {
    root: '#/',
    routes: [],
    urls: [],
    titles: [],
    currentCleanup: null,

    add: function(path, url, title) {
        this.routes.push(path);
        this.urls.push(url);
        this.titles.push(title);
    },

    navigate: function() {
        var routes = this.routes,
            urls = this.urls,
            root = this.root;

        async function loading() {
            var routeIndex = routes.indexOf(location.hash),
                template = urls[routeIndex];

            if (Router.currentCleanup) {
                Router.currentCleanup();
                Router.currentCleanup = null;
            }

            let preloader = document.createElement("div");
            preloader.classList.add("preloader");
            preloader.innerHTML = `<div class="pong-ball"></div>`;
            document.body.prepend(preloader);

            document.getElementById('main').style.display = 'none';

            if (routeIndex === -1) {
                location.hash = root;
                template = urls[0];
            }
            template = "pages/" + template;

            const existingCss = document.getElementById("css");
            if (existingCss) document.head.removeChild(existingCss);

            let css = document.createElement("link");
            css.rel = "stylesheet";
            css.href = "assets/css/" + template.split(".")[0] + ".css?v=250";
            css.id = "css";
            css.onerror = function() {
                console.warn('CSS file not found for template:', template);
            };
            document.head.appendChild(css);
            const existingJs = document.getElementById("js");
            if (existingJs) {
                document.body.removeChild(existingJs);
                clearAllProcesses();
            }

            try {
                const response = await fetch(template);
                if (!response.ok)
                    throw new Error('Network response was not ok ' + response.statusText);

                const html = await response.text();
                document.getElementById("main").innerHTML = html;

                const script = document.createElement("script");
                script.id = "js";
                script.src = "assets/js/" + template.split(".")[0] + ".js?v=250";
                script.defer = true;

                script.onload = function() {
                    console.log('JS file loaded successfully:', script.src);
                    if (window.cleanup) {
                        Router.currentCleanup = window.cleanup;
                    }
                };

                script.onerror = function() {
                    console.warn('JS file not found for template:', template);
                };
                document.body.appendChild(script);
            }
            catch (error) {
                console.error('Fetch error: ', error);
            }
            finally {
                if (preloader && preloader.parentNode)
                    document.body.removeChild(preloader);
                document.getElementById('main').style.display = 'block';
                const existingJS = document.getElementById("mainJS");
                if (existingJS)
                    existingJS.remove()
                const script = document.createElement("script");
                script.id = "mainJS";
                script.src = "assets/js/main.js?v=250";
                script.defer = true;
                script.onload = function() {
                    console.log('JS file loaded successfully:', script.src);
                };

                script.onerror = function() {
                    console.warn('JS main file not found');
                };
                document.body.appendChild(script);
            }
        }

        window.onload = loading;
        window.onhashchange = loading;
    }
};
