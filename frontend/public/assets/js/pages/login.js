(async function ()
{
    let code = new URLSearchParams(window.location.search).get("code")
    if (code && code.length > 5)
        await request("GET", "auth/42/callback/?code=" + code);
})();