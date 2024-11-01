let intervals = [];
let timeouts = [];
let events = [];
function interval(func, timeout, autoClear = true)
{
    let _interval = setInterval(func, timeout);
    if (autoClear) {
        intervals.push({
            "interval": _interval,
        });
    }
}

function timeout(func, timeout, autoClear = true)
{
    let _timeout = setTimeout(func, timeout);
    if (autoClear)
    {
        timeouts.push({
            "timeout": _timeout,
        });
    }
}

function event(element, _event, func, autoClear = true)
{
    element.addEventListener(_event, func);
    if (autoClear)
    {
        events.push({
            "event": _event,
            "element": element
        });
    }
}

function clearIntervals()
{
    intervals.forEach(interval => {
        clearInterval(interval.interval);
    });
    intervals = [];
}

function clearTimeouts()
{
    timeouts.forEach(timeout => {
        clearTimeout(timeout.timeout);
    });
    timeouts = [];
}

function clearEvents()
{
    events.forEach(event => {
        event.element.removeEventListener(event.event);
    });
    events = [];
}

function clearAllProcesses()
{
    clearIntervals();
    clearTimeouts();
    clearEvents();
}

function notification(state, title, message, closeable = true)
{
    document.getElementById('alertModalLabel').textContent = title;
    document.getElementById('alertModalMessage').innerHTML = message;
    document.getElementById("alertModal").classList.add("show");
    document.getElementById("main").style.opacity = "0.2";
    document.getElementById("alertModal").style.zIndex = "9999";
    document.getElementsByClassName("modal-footer")[0].style.display = closeable ? "block" : "none";
}

function notificationTemplate(title, template, closeable = true)
{
    template = "pages/modals/" + template + ".html?v=250";
    document.getElementById('alertModalLabel').textContent = title;
    fetch(template).then(response => response.text()).then(data => {
        document.getElementById('alertModalMessage').innerHTML = data;
    });
    document.getElementById("alertModal").classList.add("show");
    document.getElementById("main").style.opacity = "0.2";
    document.getElementById("alertModal").style.zIndex = "9999";
    document.getElementsByClassName("modal-footer")[0].style.display = closeable ? "block" : "none";
}
// notificationTemplate("Verify Your Account", "2fa", false); || Verify Your Account
// notificationTemplate('Change Information', 'change-information', false) || Change Information
// notificationTemplate('42 Connect', '42-connect', false) || Change Password

function closeModal()
{
    document.getElementById("alertModal").classList.remove("show");
    document.getElementById("main").style.opacity = "1";
    document.getElementById("alertModal").style.zIndex = "-1";
}