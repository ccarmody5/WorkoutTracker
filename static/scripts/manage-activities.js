window.onload = init;
var current_user;

function init() {
    updateDateTime();
    get_activities();
    get_current_user();
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

function get_activities() {
    fetch('/get_all_activities')
        .then(response => response.json())
        .then(activities => {
            // Create the activity buttons dynamically
            const container = document.getElementById('activities-buttons-container');

            activities.forEach(function (activity) {
                if (activity.disabled == 'Y') {
                    var className = "btnActivity disabledButton"
                } else {
                    var className = "btnActivity"
                }
                const button = document.createElement("button");
                button.textContent = activity.activity_desc
                button.id = "btn_" + activity.activity_id;
                button.className = className;
                button.onclick = () => select_activity(activity)
                container.appendChild(button);
            })
        })
        .catch(error => console.error('Error:', error));
}

function select_activity(activity) {

    if (!activity || activity.activity_id === null || activity.activity_id === undefined) {
        action = 'add'
        data = {action: action}

    } else {
        action = 'update'
        data = {
            action: action,
            activity_id: activity.activity_id,
            activity_desc: activity.activity_desc,
            activity_type: activity.activity_type,
            default_weight: activity.default_weight,
            disabled: activity.disabled
        };
    }

//    data = {
//        action: action,
//        activity_id: activity.activity_id,
//        activity_desc: activity.activity_desc,
//        activity_type: activity.activity_type,
//        default_weight: activity.default_weight,
//        disabled: activity.disabled
//    };

    console.log(data)

    localStorage.setItem('activityData', JSON.stringify(data));
    window.location.href = '/activity-edit';
}