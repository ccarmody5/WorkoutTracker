#!/usr/bin/env python3
"""
' Workout Tracker
' 10/12/2024 - Chris Carmody
'
' Flask Server Set-up
'
"""
from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import sessionmaker

import config.webapp_log_config as log_config
import helpers.activity_lib as activity_lib
import helpers.dbHelper as dbHelper
import helpers.workout_detail_lib as workout_detail_lib
import helpers.workout_lib as workout_lib
from config.db_table_config import Activity, Workout, WorkoutDetail, User
from helpers import user_lib

logger = log_config.webapp_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX webapp.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

'''
'   Set-up Flask application
'''
webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'GDtfDCFYjD'
webapp.config['ENV'] = 'dev'

'''
' Global Variables
'''
current_activity = Activity()
current_workout = Workout()
current_workout_detail = WorkoutDetail()
continue_workout = False
current_user = User()

'''
' Start DB Engine
'''
# Create DB Engine
engine = dbHelper.create_db_engine()
Session = sessionmaker(bind=engine)

''' ***********************************************************************************************************************'''
''' **************************************************** ROUTER CALLS *****************************************************'''
''' ***********************************************************************************************************************'''
'''
' index function
'''

@webapp.route('/')
def index():
    return render_template(get_template_based_on_login_status('index.html'))

'''
' login function
'''

@webapp.route('/login')
def login():
    return render_template('login.html')

'''
' select-activity function
'''

@webapp.route('/select-activity')
def select_activity():
    return render_template(get_template_based_on_login_status('select-activity.html'))

'''
' workout-control function
'''

@webapp.route('/workout-control')
def workout_control():
    return render_template(get_template_based_on_login_status('workout-control.html'))

'''
' set-control function
'''

@webapp.route('/set-control')
def set_control():
    return render_template(get_template_based_on_login_status('set-control.html'))

'''
' manage_users function
'''

@webapp.route('/manage-users')
def manage_users():
    return render_template(get_template_based_on_login_status('manage-users.html'))

'''
' manage_activities function
'''

@webapp.route('/manage-activities')
def manage_activities():
    return render_template(get_template_based_on_login_status('manage-activities.html'))

'''
' user_edit function
'''

@webapp.route('/user-edit')
def user_edit():
    return render_template(get_template_based_on_login_status('user-edit.html'))

'''
' activity_edit function
'''

@webapp.route('/activity-edit')
def activity_edit():
    return render_template(get_template_based_on_login_status('activity-edit.html'))

''' ***********************************************************************************************************************'''
''' *************************************************** FUNCTION CALLS ****************************************************'''
''' ***********************************************************************************************************************'''

def get_template_based_on_login_status(template):  # name this function
    """
    :param template: The template to be returned if the user is logged in
    :return: 'login.html' if the user is not logged in, otherwise the given template
    """
    if current_user.user_id is None:
        return 'login.html'
    else:
        return template

@webapp.route('/get_all_activities', methods=['GET'])
def get_all_activities():
    """
    Retrieve a list of all activities, including disabled ones.

    :return: A JSON response containing a list of dictionaries, each representing an activity.
    """
    activities = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='Y')

    activities_dict = [activity.to_dict() for activity in activities]

    return jsonify(activities_dict)

@webapp.route('/get_enabled_activities', methods=['GET'])
def get_enabled_activities():
    """
    Handles the GET request to retrieve all enabled activities.

    Returns a JSON response containing the list of all enabled activities in dictionary format.

    :return: JSON response with a list of enabled activities.
    """
    activities = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='N')

    activities_dict = [activity.to_dict() for activity in activities]

    return jsonify(activities_dict)

@webapp.route('/get_all_users', methods=['GET'])
def get_all_users():
    """
    Handles the HTTP GET request to retrieve all users from the database.

    :return: A JSON response containing a list of all users.
    """
    users = user_lib.UserLib(session=Session()).get_all_users(include_disabled='Y')

    users_dict = [user.to_dict() for user in users]

    return jsonify(users_dict)

@webapp.route('/get_enabled_users', methods=['GET'])
def get_enabled_users():
    """
    A Flask route that retrieves all enabled users from the database and returns them as a JSON response.

    :return: A JSON list of all enabled users.
    """
    users = user_lib.UserLib(session=Session()).get_all_users(include_disabled='N')

    users_dict = [user.to_dict() for user in users]

    return jsonify(users_dict)

@webapp.route('/update_user', methods=['POST'])
def update_user():
    """
    Handles user updates and creation based on the JSON payload received in a POST request.

    :return: JSON response indicating the success status.
    """
    logger.info(request.method)

    if request.method == 'POST':
        data = request.json
        logger.info(data)
        print(data)
        global current_user

        if 'user_id' in data:
            # Update User
            user_id = data['user_id']
            first_name = data['first_name']
            last_name = data['last_name']
            disabled = data['disabled']

            user = user_lib.UserLib(session=Session()).update_user(user_id=user_id,
                                                                   first_name=first_name,
                                                                   last_name=last_name,
                                                                   disabled=disabled,
                                                                   updated_by=current_user.user_id)

            logger.info(user.to_dict())
            return jsonify({'status': 'success'})

        else:
            # Add User
            first_name = data['first_name']
            last_name = data['last_name']
            disabled = data['disabled']

            user_lib.UserLib(session=Session()).create_user(first_name=first_name,
                                                            last_name=last_name,
                                                            disabled=disabled,
                                                            created_by=current_user.user_id,
                                                            updated_by=current_user.user_id)
            # logger.info(user.to_dict())
            return jsonify({'status': 'success'})

@webapp.route('/update_activity', methods=['POST'])
def update_activity():
    """
    Handles the updating or creation of an activity.

    The route listens for POST requests and expects a JSON payload. If the payload contains an
    'activity_id', it updates the existing activity; otherwise, it creates a new activity.

    The `activity_id`, `activity_desc`, and `disabled` fields are extracted from the payload,
    and the `current_user`'s `user_id` is used to mark who made the changes.

    :return: A JSON response indicating the status of the operation.
    """
    logger.info(request.method)

    if request.method == 'POST':
        data = request.json
        logger.info(data)
        print(data)
        global current_user

        activity_desc = data['activity_desc']
        activity_type = data['activity_type']
        default_weight = data['default_weight']
        disabled = data['disabled']

        if 'activity_id' in data:
            # Update User
            activity_id = data['activity_id']

            activity = activity_lib.ActivityLib(session=Session()).update_activity(activity_id=activity_id,
                                                                                   activity_desc=activity_desc,
                                                                                   activity_type=activity_type,
                                                                                   default_weight=default_weight,
                                                                                   disabled=disabled,
                                                                                   updated_by=current_user.user_id)

            logger.info(activity.to_dict())
            return jsonify({'status': 'success'})

        else:
            # Add User
            activity = activity_lib.ActivityLib(session=Session()).create_activity(activity_desc=activity_desc,
                                                                                   activity_type=activity_type,
                                                                                   default_weight=default_weight,
                                                                                   disabled=disabled,
                                                                                   created_by=current_user.user_id,
                                                                                   updated_by=current_user.user_id)

            logger.info(activity.to_dict())
            return jsonify({'status': 'success'})

@webapp.route('/set_user', methods=['POST'])
def set_user():
    """
    Sets the global current user based on the POST request data.

    This endpoint expects a JSON payload that contains a `user_id` field.
    If `user_id` is None, a new User instance is assigned to the global `current_user`.
    Otherwise, it retrieves the user from the user library and assigns it to `current_user`.

    :return: A JSON response indicating the status of the operation.
    """
    logger.info(request.method)

    global current_user

    if request.method == 'POST':
        process = request.json
        logger.info(process)

        if 'user_id' in process:
            user_id = process['user_id']

            if user_id is None:
                current_user = User()
                logger.info('Change User')
            else:
                current_user = user_lib.UserLib(session=Session()).get_pk(
                    user_id=user_id)
                logger.info(current_user.to_dict())

            return jsonify({'status': 'success'})

@webapp.route('/get_user', methods=['GET'])
def get_user():
    """
    This endpoint retrieves information about the current user.

    :return: JSON representation of the current user's information.
    """
    global current_user

    return jsonify(current_user.to_dict())

@webapp.route('/set_activity', methods=['POST'])
def set_activity():
    """
    Handles the POST request to set a new activity.

    Logs the request method, processes the JSON request payload, and
    sets the current activity if 'activity' is present in the payload.
    Then, it returns a JSON response indicating success.

    :return: JSON response with status 'success'
    """
    logger.info(request.method)

    if request.method == 'POST':
        process = request.json
        logger.info(process)

        if 'activity' in process:
            activity = process['activity']

            global current_activity
            current_activity = activity_lib.ActivityLib(session=Session()).get_activity_by_desc(
                activity_desc=activity)

    return jsonify({'status': 'success'})

@webapp.route('/get_activity', methods=['GET'])
def get_activity():
    """
    Handles GET requests to fetch current activity data.

    :return: A JSON representation of the current activity.
    """
    global current_activity

    return jsonify(current_activity.to_dict())

@webapp.route('/get_workout', methods=['GET'])
def get_workout():
    """
    Handles HTTP GET requests to retrieve the current workout.

    :return: A JSON representation of the current workout
    """
    global current_workout

    return jsonify(current_workout.to_dict())

@webapp.route('/get_workout_detail', methods=['GET'])
def get_workout_detail():
    """
        Endpoint to get the details of the current workout.

        :return: A JSON response with the current workout details.
    """
    global current_workout_detail

    return jsonify(current_workout_detail.to_dict())

@webapp.route('/set_workout_status', methods=['POST'])
def set_workout_status():
    """
    Handles the status of a workout session based on the incoming command.

    The function listens for POST requests at the '/set_workout_status' endpoint. Depending on the 'command' in the JSON payload, the function performs the following operations:

    - 'start': Initiates a new workout or continues the current one if it has not been marked as continued already.
    - 'stop': Stops the current workout detail.
    - 'complete': Completes the current workout detail and optionally the entire workout session based on the 'completeWorkout' flag in the JSON payload.

    :return: JSON response of the current workout detail status after performing the operation
    """
    logger.info(request.method)

    if request.is_json:
        content = request.get_json()
        logger.info(content)

        command = content.get('command')

        reps, weight, complete_workout = 0, 0, ''

        if 'reps' in content:
            reps = content['reps']
            weight = content['weight']
            complete_workout = content['completeWorkout']
        global current_workout_detail
        global current_workout
        global continue_workout

        if command == 'start':
            if not continue_workout:
                current_workout = workout_lib.WorkoutLib(session=Session()).create_workout(
                    activity_id=current_activity.activity_id,
                    user_id=current_user.user_id, created_by=current_user.user_id, updated_by=current_user.user_id)
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).create_workout_detail(
                workout_id=current_workout.workout_id, created_by=current_user.user_id, updated_by=current_user.user_id
            )  # Expected type 'int', got 'Mapped' instead
            return jsonify(current_workout_detail.to_dict())

        elif command == 'stop':
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).stop_workout_detail(
                workout_detail_id=current_workout_detail.workout_detail_id, updated_by=current_user.user_id)
            return jsonify(current_workout_detail.to_dict())

        elif command == 'complete':
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).complete_workout_detail(
                workout_detail_id=current_workout_detail.workout_detail_id,
                rep_count=reps,
                weight=weight,
                updated_by=current_user.user_id
            )

            current_workout_detail = WorkoutDetail()

            if complete_workout == 'N':
                continue_workout = True
            else:
                current_workout = workout_lib.WorkoutLib(session=Session()).complete_workout(
                    workout_id=current_workout.workout_id, updated_by=current_user.user_id)
                continue_workout = False
                current_workout = Workout()

            return jsonify(current_workout_detail.to_dict())

if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')
