window.onload = init;

function init() {
    updateDateTime();
    get_activity()
}

var activity_status = "Stopped"

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