window.onload = init;
var current_user;
const user_data = JSON.parse(localStorage.getItem('userData'));

function init() {
    updateDateTime();
    get_current_user();
    load_page();
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

function load_page() {
    if (user_data.action == 'add') {
        action = "Add User"
    } else {
        action = "Update User"
        var first_name = document.getElementById('firstNameInput');
        var last_name = document.getElementById('lastNameInput');
        var disabled = document.getElementById('disabledCheckbox');
        first_name.value = user_data.first_name;
        last_name.value = user_data.last_name;
        if (user_data.disabled == 'Y') {
            document.getElementById('disabledCheckbox').checked = true;
        }
    }

    // Create dynamic text to display the activity
    const nameActionCont = document.getElementById('name-action-container');
    const nameActionText = document.createElement('p');
    nameActionText.textContent = action;
    nameActionText.className = "activityTitle";
    nameActionCont.appendChild(nameActionText);
}

function save_user(first_name, last_name, disabled) {
    if (disabled == true) {
        disabled = 'Y';
    } else {
        disabled = 'N';
    }

    const dataToSend = {
        user_id: user_data.user_id,
        first_name: first_name,
        last_name: last_name,
        disabled: disabled
    };

    fetch('/update_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    }).then(() => {
        window.location.href = '/manage-users';
    }).catch((error) => {
        console.error('Error:', error);
    });
}