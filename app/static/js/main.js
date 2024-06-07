document.addEventListener("DOMContentLoaded", function() {
    var userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    fetch('/timezone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Timezone': userTimezone
        },
    });
});