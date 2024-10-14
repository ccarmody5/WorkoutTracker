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
from config.db_table_config import Activity, Workout, WorkoutDetail

logger = log_config.webapp_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX webapp.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

'''
'   Set-up Flask application
'''
webapp = Flask(__name__)

webapp.config['SECRET_KEY'] = 'GDtfDCFYjD'
webapp.config['ENV'] = 'dev'

current_activity = Activity()
current_workout = Workout()
current_workout_detail = WorkoutDetail()
continue_workout = False

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
    logger.info(request.method)
    return render_template('index.html')


'''
' select-activity function
'''


@webapp.route('/select-activity')
def select_activity():
    logger.info(request.method)

    return render_template('select-activity.html')


'''
' workout-control function
'''


@webapp.route('/workout-control')
def workout_control():
    logger.info(request.method)

    return render_template('workout-control.html')


'''
' set-control function
'''


@webapp.route('/set-control')
def set_control():
    logger.info(request.method)

    return render_template('set-control.html')


''' ***********************************************************************************************************************'''
''' *************************************************** FUNCTION CALLS ****************************************************'''
''' ***********************************************************************************************************************'''
'''
' get_all_activities
'''


@webapp.route('/get_all_activities', methods=['GET'])
def get_all_activities():
    logger.info(request.method)

    activities = activity_lib.ActivityLib(session=Session()).get_all_activities()

    activities_dict = [activity.to_dict() for activity in activities]

    return jsonify(activities_dict)


'''
' set_workout
'''


@webapp.route('/set_activity', methods=['POST'])
def set_activity():
    logger.info(request.method)

    if request.method == 'POST':
        process = request.json
        logger.info(process)

        if 'activity' in process:
            activity = process['activity']

            global current_activity
            current_activity = activity_lib.ActivityLib(session=Session()).get_activity_by_desc(
                activity_desc=activity)

    # NEED TO CHANGE PAGES
    return jsonify({'status': 'success'})


'''
' get_activity
'''


@webapp.route('/get_activity', methods=['GET'])
def get_activity():
    logger.info(request.method)

    global current_activity
    return jsonify(current_activity.to_dict())


'''
' get_workout_detail
'''


@webapp.route('/get_workout_detail', methods=['GET'])
def get_workout_detail():
    logger.info(request.method)

    global current_workout_detail
    return jsonify(current_workout_detail.to_dict())


'''
' set_workout_status
'''


@webapp.route('/set_workout_status', methods=['POST'])
def set_workout_status():
    if request.is_json:
        content = request.get_json()
        command = content.get('command')

        reps, weight, complete_workout = 0, 0, ''

        if 'reps' in content:
            reps = content['reps']
            weight = content['weight']
            complete_workout = content['completeWorkout']
            print(reps + weight)

        global current_workout_detail
        global current_workout
        global continue_workout

        if command == 'start':
            print('creating workout')
            if not continue_workout:
                current_workout = workout_lib.WorkoutLib(session=Session()).create_workout(
                    activity_id=current_activity.activity_id,
                    user_id=1, created_by=1, updated_by=1)
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).create_workout_detail(
                workout_id=current_workout.workout_id, created_by=1, updated_by=1
            )
            return jsonify(current_workout_detail.to_dict())

        elif command == 'stop':
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).stop_workout_detail(
                workout_detail_id=current_workout_detail.workout_detail_id, updated_by=1)
            return jsonify(current_workout_detail.to_dict())

        elif command == 'complete':
            current_workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).complete_workout_detail(
                workout_detail_id=current_workout_detail.workout_detail_id,
                rep_count=reps,
                weight=weight,
                updated_by=1
            )

            current_workout_detail = WorkoutDetail()

            if complete_workout == 'N':
                continue_workout = True
            else:
                current_workout = workout_lib.WorkoutLib(session=Session()).complete_workout(
                    workout_id=current_workout.workout_id, updated_by=1)
                continue_workout = False
                current_workout = Workout()

            return jsonify(current_workout_detail.to_dict())


if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')
