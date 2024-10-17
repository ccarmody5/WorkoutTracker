window.onload = init;
var current_user;

function init() {
    updateDateTime();
    get_current_user();

    document.getElementById('workout-button').focus()
}

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleTimeString();

    document.querySelector('#currentTime').textContent = currentDateTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 500);

function get_current_user() {
    fetch('/get_user')
        .then(response => response.json())
        .then(user => {
            current_user = user.fullname
            document.getElementById("currentUser").textContent = current_user;
        })
        .catch(error => console.error('Error:', error));
}

function change_user() {
    const dataToSend = { user_id: null };

    fetch('/set_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
        .then(response => response.json())
        .then(data => {
            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}