window.onload = init;
var current_user;

function init() {
    updateDateTime();
    get_users();
    get_current_user();
}

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleString();

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

function get_users() {
    fetch('/get_all_users')
        .then(response => response.json())
        .then(users => {
            // Create the activity buttons dynamically
            const container = document.getElementById('user-buttons-container');

            users.forEach(function (user) {
                if (user.disabled == 'Y') {
                    var className = "btnActivity disabledButton"
                } else {
                    var className = "btnActivity"
                }
                const button = document.createElement("button");
                button.textContent = user.fullname
                button.id = "btn_" + user.user_id;
                button.className = className;
                button.onclick = () => select_user(user.user_id, user.first_name, user.last_name, user.disabled)
                container.appendChild(button);
            })
        })
        .catch(error => console.error('Error:', error));
}

function select_user(user_id, first_name, last_name, disabled) {

    if (user_id == null){
        action = 'add'
    } else {
        action = 'update'
    }

    data = {action: action,
            user_id: user_id,
            first_name: first_name,
            last_name: last_name,
            disabled: disabled};

    localStorage.setItem('userData', JSON.stringify(data));
    window.location.href = '/user-edit';
}