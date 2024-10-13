window.onload = init;
var workout_type;

function init() {
    updateDateTime();
    getActivities()
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
    const container = document.getElementById('activity-buttons-container');
    const homeContainer = document.getElementById('home-button-container');
    fetch('/get_all_activities')
        .then(response => response.json())
        .then(activities => {
            console.log(activities);

            // Create the activity buttons dynamically
            activities.forEach(function (activity) {
                const button = document.createElement("button");
                button.textContent = activity.activity_desc;
                button.id = "btn_" + activity.activity_desc;
                button.className = "btnActivity";
                button.onclick = () => select_workout(activity.activity_desc)
                container.appendChild(button);
            })

            // Create a Home button
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

    fetch('/set_workout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Redirect to homepage after successful data sending
            window.location.href = '/workout-control';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

/*
        function performActivity(activity) {
            fetch('http://127.0.0.1:5000/perform_activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ activity: activity })
            }).catch(error => console.error('Error:', error));
        }
*/

/**
 *  EXAMPLE TO SEND DATA BACK TO PYTHON
 *                                  button.onclick = function () {
                    const dataToSend = { activity: activity.activity_desc };

                    fetch('/select_workout', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(dataToSend)
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Success:', data);
                            // Redirect to homepage after successful data sending
                            window.location.href = '/';
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                }
 */