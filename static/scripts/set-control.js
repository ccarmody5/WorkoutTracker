window.onload = init;
var current_user;

function init() {
    updateDateTime();
    get_activity();
    get_current_user();
}

var activity_status = "Stopped"

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleTimeString();

    document.querySelector('#currentTime').textContent = currentDateTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 500);

function loadPage(activity) {
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

    // Load default weight
    const weightInput = document.getElementById('weightInput');
    weightInput.value = activity.default_weight;

    // Only show the weight input options if the activity_type = strength
    const weightInputContainer = document.getElementById('weight-input-container');
    const bodyWeightContainer = document.getElementById('body-weight-container');

    if (activity.activity_type !== 'strength') {
        weightInputContainer.classList.add('hidden');
        bodyWeightContainer.classList.remove('hidden');
    } else {
        weightInputContainer.classList.remove('hidden');
        bodyWeightContainer.classList.add('hidden');
    }

}

function get_activity() {
    fetch('/get_activity')
        .then(response => response.json())
        .then(activity => {
            current_activity = activity.activity_desc
            loadPage(activity)
        })
        .catch(error => console.error('Error:', error));
}

function increaseReps() {
    var input = document.getElementById('repsInput');
    var newValue = parseInt(input.value) + 1;
    if (newValue <= input.max) {
        input.value = newValue;
    }
}

function decreaseReps() {
    var input = document.getElementById('repsInput');
    var newValue = parseInt(input.value) - 1;
    if (newValue >= input.min) {
        input.value = newValue;
    }
}

function increaseWeight() {
    var input = document.getElementById('weightInput');
    var newValue = parseInt(input.value) + 5;
    if (newValue <= input.max) {
        input.value = newValue;
    }
}

function decreaseWeight() {
    var input = document.getElementById('weightInput');
    var newValue = parseInt(input.value) - 5;
    if (newValue >= input.min) {
        input.value = newValue;
    }
}


function complete_set(completeWorkout, repsInput, weightInput) {
    var destination
    if (completeWorkout == 'N') {
        destination = '/workout-control'
    } else {
        destination = '/select-activity'
    }

    const dataToSend = { command: "complete", reps: repsInput, weight: weightInput, completeWorkout: completeWorkout };

    fetch('/set_workout_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    }).then(() => {
        window.location.href = destination;
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function get_current_user() {
    fetch('/get_user')
        .then(response => response.json())
        .then(user => {
            current_user = user.fullname
            document.getElementById("currentUser").textContent = current_user;
        })
        .catch(error => console.error('Error:', error));
}