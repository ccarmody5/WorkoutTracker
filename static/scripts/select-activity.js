window.onload = init;
var workout_type;
var current_user;

function init() {
    updateDateTime();
    getActivities();
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

function getActivities() {
    fetch('/get_all_activities')
        .then(response => response.json())
        .then(activities => {
            // Create the activity buttons dynamically
            const container = document.getElementById('activity-buttons-container');
            activities.forEach(function (activity) {
                const button = document.createElement("button");
                button.textContent = activity.activity_desc;
                button.id = "btn_" + activity.activity_desc;
                button.className = "btnActivity";
                button.onclick = () => select_workout(activity.activity_desc)
                container.appendChild(button);
            })

            // Create a Home button
            const homeContainer = document.getElementById('home-button-container');
            const homeButton = document.createElement("button");
            homeButton.textContent = "Home";
            homeButton.id = "btn_home";
            homeButton.className = "btnActivity";
            homeButton.onclick = function () {
                window.location.href = '/'
            };
            homeContainer.appendChild(homeButton);
        })
        .catch(error => console.error('Error:', error));
}

function select_workout(activity) {
    console.log(activity)
    const dataToSend = { activity: activity };

    fetch('/set_activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
        .then(response => response.json())
        .then(data => {
            window.location.href = '/workout-control';
        })
        .catch((error) => {
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