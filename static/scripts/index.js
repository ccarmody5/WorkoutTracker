window.onload = init;

function init() {
    updateDateTime();
    //create_activity_buttons();
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
    fetch('/get_all_activities')
        .then(response => response.json())
        .then(activities => {
            console.log(activities);

            activities.forEach(function (activity) {
                console.log(activity.activity_desc)
                const button = document.createElement("button");
                button.textContent = activity.activity_desc;
                button.id = "btn_" + activity.activity_desc;
                button.className = "btnActivity";

                container.appendChild(button); //add to specific div
            })
        })
        .catch(error => console.error('Error:', error));


}