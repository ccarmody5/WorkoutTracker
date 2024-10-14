window.onload = init;

function init() {
    updateDateTime();
    get_users();
}

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleString();

    document.querySelector('#currentTime').textContent = currentDateTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 500);

function get_users() {
    fetch('/get_enabled_users')
        .then(response => response.json())
        .then(users => {
            // Create the activity buttons dynamically
            const container = document.getElementById('user-buttons-container');

            users.forEach(function (user) {
                const button = document.createElement("button");
                button.textContent = user.fullname
                button.id = "btn_" + user.user_id;
                button.className = "btnActivity";
                button.onclick = () => select_user(user.user_id)
                container.appendChild(button);
            })
        })
        .catch(error => console.error('Error:', error));
}

function select_user(user_id) {
    const dataToSend = { user_id: user_id };

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