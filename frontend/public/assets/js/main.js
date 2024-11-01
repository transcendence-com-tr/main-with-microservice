(async function () {
    document.addEventListener('submit', function(event) {
        if (event.target.tagName === 'FORM') {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            let action = new URL(form.action).pathname;

            action = action[0] === '/' ? action.substring(1) : action;

            request(form.getAttribute("method"), action, formData);
        }
    }, true);
    let code = new URLSearchParams(window.location.search).get("code")
    if (code && code.length > 5)
        await get("auth/42/callback/?code=" + code);

    let response = await get("auth/me");

    if (response.status === 200 && Router.get() === "")
        window.location.href = "#/home";
    else if (response.status !== 200 && (Router.get() !== "" && Router.get() !== "login" && Router.get() !== "register"))
        window.location.href = "#/login";

    if (response.status === 200 && (response.payload.user.email === null || response.payload.username === null))
        notificationTemplate("Update your profile information", "42-register", response.payload.user);
})();