window.onload = init;

function init() {
    updateDateTime();
    get_workout_detail();
    get_activity();
}

var activity_status = "Stopped"
var current_activity = ""

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleString();

    document.querySelector('#currentTime').textContent = currentDateTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 500);

function loadPage() {
    if (activity_status == "Stopped") {
        textContent = "Start Set"
    } else {
        textContent = "Stop Set"
    }

    // Create dynamic text to display the activity
    const activityNameCont = document.getElementById('activity-name-container');
    const activityNameText = document.createElement('p');
    activityNameText.textContent = "Workout: " + current_activity;
    activityNameText.className = "activityTitle";
    activityNameCont.appendChild(activityNameText);

    // Create the start or stop button dynamically
    const controlContainer = document.getElementById('control-button-container');
    const controlButton = document.createElement("button");
    controlButton.textContent = textContent;
    controlButton.id = "btn_home";
    controlButton.className = "btnActivity";
    controlButton.onclick = () => control_workout(textContent);
    controlContainer.appendChild(controlButton);

}

function get_activity() {
    fetch('/get_activity')
        .then(response => response.json())
        .then(activity => {
            current_activity = activity.activity_desc
            loadPage()
        })
        .catch(error => console.error('Error:', error));
}

function start_set() {
    const dataToSend = { command: "start" };

    fetch('/set_workout_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    }).then(() => {
        window.location.href = '/workout-control';
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function end_set() {
    const dataToSend = { command: "stop" };

    fetch('/set_workout_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    }).then(() => {
        window.location.href = '/set-control';
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function control_workout(command) {
    if (command == "Start Set") {
        start_set()
    } else {
        end_set()
    }
}

function get_workout_detail() {
    fetch('/get_workout_detail')
        .then(response => response.json())
        .then(workout_detail => {
            if (workout_detail.workout_detail_id !== null) {
                console.log(workout_detail)
                activity_status = "Running"
            }

        })
        .catch(error => console.error('Error:', error));
}