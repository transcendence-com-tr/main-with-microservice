var Router = {
    root: '#/',
    routes: [],
    urls: [],
    titles: [],
    funcs: [],
    currentCleanup: null,

    add: function(path, url, title, func) {
        this.routes.push(path);
        this.urls.push(url);
        this.titles.push(title);
        this.funcs.push(func);
    },

    navigate: function() {
        var routes = this.routes,
            urls = this.urls,
            funcs = this.funcs,
            root = this.root;

        async function loading() {
            var routeIndex = routes.indexOf(location.hash),
                template = urls[routeIndex], func = funcs[routeIndex];

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
            css.href = "assets/css/" + template.split(".")[0] + ".css?v=350";
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

                var html = await response.text();

                if (func)
                {
                    const data = await func();
                    console.log(data);
                    Object.entries(data).forEach(([key, value]) => {
                        Object.entries(value).forEach(([key2, value2]) => {
                            html = html.replaceAll("{" + key + "." + key2 + "}", value2);
                        });
                    });
                }
                document.getElementById("main").innerHTML = html;

                const script = document.createElement("script");
                script.id = "js";
                script.src = "assets/js/" + template.split(".")[0] + ".js?v=350";
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
                script.src = "assets/js/main.js?v=350";
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
    },

    get: function() {
        return location.hash.slice(2);
    },
};
