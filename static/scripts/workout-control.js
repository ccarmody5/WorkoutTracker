window.onload = init;

function init() {
    updateDateTime();
    get_workout_detail();
    get_activity();
    get_workout();
}

var activity_status = "Stopped";
var current_activity = "";
var workout_start_time = null;
var set_start_time = new Date();
var refreshTimer = 100;

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
    controlButton.id = "btn_start_stop";
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
                activity_status = "Running"
                set_start_time = new Date(workout_detail.start_time)
            }

        })
        .catch(error => console.error('Error:', error));
}

function get_workout() {
    console.log('get_workout')
    fetch('/get_workout')
        .then(response => response.json())
        .then(workout => {
            console.log(workout)
            if (workout.workout_id !== null) {
                workout_start_time = new Date(workout.start_time);
            }

        })
        .catch(error => console.error('Error:', error));
}

// Function to update the timer text content
function updateWorkoutTimer() {
    var timeString = "Workout Time: ";

    //console.log(workout_start_time)

    if (workout_start_time !== null) {
        var now = new Date();
        var difference = now - workout_start_time;

        // Convert the difference to a more readable format (HH:MM:SS)
        var hours = Math.floor(difference / (1000 * 60 * 60));
        var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((difference % (1000 * 60)) / 1000);

        // Ensure double digits for minutes and seconds
        var timeString = timeString +
            (hours < 10 ? '0' : '') + hours + ":" +
            (minutes < 10 ? '0' : '') + minutes + ":" +
            (seconds < 10 ? '0' : '') + seconds;
    } else {
        timeString = timeString + " Resting"
    }

    document.querySelector('#workoutTimerText').textContent = timeString;
}

// Update the timer every second
setInterval(updateWorkoutTimer, refreshTimer);

// Function to update the timer text content
function updateSetTimer() {
    var timeString = "Set Time: "

    if (activity_status == "Running") {
        var now = new Date();
        var difference = now - set_start_time;

        // Convert the difference to a more readable format (HH:MM:SS)
        var hours = Math.floor(difference / (1000 * 60 * 60));
        var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((difference % (1000 * 60)) / 1000);

        // Ensure double digits for minutes and seconds
        timeString = timeString +
            (hours < 10 ? '0' : '') + hours + ":" +
            (minutes < 10 ? '0' : '') + minutes + ":" +
            (seconds < 10 ? '0' : '') + seconds;
    } else {
        timeString = timeString + " Resting"
    }

    document.querySelector('#setTimerText').textContent = timeString;
}

// Update the timer every second
setInterval(updateSetTimer, refreshTimer);