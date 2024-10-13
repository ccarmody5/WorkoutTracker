window.onload = init;

function init() {
    updateDateTime();
    get_activity()
}

function updateDateTime() {
    // create a new `Date` object
    const now = new Date();
    const currentDateTime = now.toLocaleString();

    document.querySelector('#currentTime').textContent = currentDateTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 500);

function loadPage(activity) {
    if (activity == "Pec Fly") {
        textContent = "Start Set"
    } else {
        textContent = "Stop Set"
    }

    // Create dynamic text to display the activity
    const activityNameCont = document.getElementById('activity-name-container');
    const activityNameText = document.createElement('p');
    activityNameText.textContent = "Workout: " + activity;
    activityNameText.className = "activityTitle";
    activityNameCont.appendChild(activityNameText);

    // Create the start or stop button dynamically
    const controlContainer = document.getElementById('control-button-container');
    const controlButton = document.createElement("button");
    controlButton.textContent = "Start";
    controlButton.id = "btn_home";
    controlButton.className = "btnActivity";
    /*homeButton.onclick = function () {
        window.location.href = '/'
    };*/
    controlContainer.appendChild(controlButton);

}

function get_activity() {
    fetch('/get_activity')
        .then(response => response.json())
        .then(activity => {
            console.log(activity.activity)
            loadPage(activity.activity)
        })
        .catch(error => console.error('Error:', error));
}