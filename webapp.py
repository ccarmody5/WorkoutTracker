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
import helpers.dbHelper as db_helper

logger = log_config.webapp_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX webapp.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

'''
'   Set-up Flask application
'''
webapp = Flask(__name__)

webapp.config['SECRET_KEY'] = 'GDtfDCFYjD'
webapp.config['ENV'] = 'dev'

global activity
'''
' Start DB Engine
'''
# Create DB Engine
engine = db_helper.create_db_engine()
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


@webapp.route('/set_workout', methods=['POST'])
def set_workout():
    logger.info(request.method)

    if request.method == 'POST':
        process = request.json

        if 'activity' in process:
            workout_activity = process['activity']
            logger.info(f"Workout Activity: {workout_activity}")
            global activity
            activity = workout_activity

    # NEED TO CHANGE PAGES
    return jsonify({'status': 'success'})


'''
' get_activity
'''


@webapp.route('/get_activity', methods=['GET'])
def get_activity():
    logger.info(request.method)

    global activity
    return jsonify({'activity': activity})


if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')
