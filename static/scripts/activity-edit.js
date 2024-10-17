window.onload = init;
var current_user;
const activity_data = JSON.parse(localStorage.getItem('activityData'));

function init() {
    updateDateTime();
    get_current_user();
    load_page();

    // Add listener to disable Default Weight input and set to 0 if Activity Type <> Strength
    document.getElementById('activityTypeOptions').addEventListener('change', function () {
    var defaultWeightInput = document.getElementById('defaultWeightInput');
    var defaultWeightIncBtn = document.getElementById('default-increase-btn');
    var defaultWeightDecBtn = document.getElementById('default-decrease-btn');
        if (this.value !== 'strength') {
            defaultWeightInput.disabled = true;
            defaultWeightInput.value = "0";
            defaultWeightIncBtn.disabled = true;
            defaultWeightDecBtn.disabled = true;
        } else {
            defaultWeightInput.disabled = false;
            defaultWeightIncBtn.disabled = false;
            defaultWeightDecBtn.disabled = false;
        }
    });

    // Initialize the state
    document.getElementById('activityTypeOptions').dispatchEvent(new Event('change'));
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

function load_page() {
    console.log(activity_data)

    if (activity_data.action == 'add') {
        action = "Add Activity"
    } else {
        action = "Update Activity"
        var activity_desc = document.getElementById('activityDescInput');
        var disabled = document.getElementById('disabledCheckbox');
        var activity_type = document.getElementById('activityTypeOptions');
        var default_weight = document.getElementById('defaultWeightInput');

        activity_desc.value = activity_data.activity_desc;
        activity_type.value = activity_data.activity_type;
        default_weight.value = activity_data.default_weight;
        if (activity_data.disabled == 'Y') {
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

function save_activity() {
    const activity_desc = document.getElementById('activityDescInput').value;
    const activity_type = document.getElementById('activityTypeOptions').value;
    const default_weight = document.getElementById('defaultWeightInput').value;
    const disabled_checkbox = document.getElementById('disabledCheckbox').checked;
    var disabled;

    if (disabled_checkbox == true) {
        disabled = 'Y';
    } else {
        disabled = 'N';
    }

    const dataToSend = {
        activity_id: activity_data.activity_id,
        activity_desc: activity_desc,
        activity_type: activity_type,
        default_weight: default_weight,
        disabled: disabled
    };

    fetch('/update_activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    }).then(() => {
        window.location.href = '/manage-activities';
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function increaseWeight() {
    var input = document.getElementById('defaultWeightInput');
    var newValue = parseInt(input.value) + 5;
    if (newValue <= input.max) {
        input.value = newValue;
    }
}

function decreaseWeight() {
    var input = document.getElementById('defaultWeightInput');
    var newValue = parseInt(input.value) - 5;
    if (newValue >= input.min) {
        input.value = newValue;
    }
}