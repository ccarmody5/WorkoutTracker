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
import helpers.dbHelper as db_helper
import helpers.activity_lib as activity_lib


logger = log_config.webapp_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX webapp.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

'''
'   Set-up Flask application
'''
webapp = Flask(__name__)

webapp.config['SECRET_KEY'] = 'GDtfDCFYjD'
webapp.config['ENV'] = 'dev'

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
    return render_template('index.html')

'''
' Stats page
'''
@webapp.route('/get_all_activities', methods=['GET'])
def get_all_activities():
    logger.debug(request.method)

    activities = activity_lib.ActivityLib(session=Session()).get_all_activities()

    activities_dict = [activity.to_dict() for activity in activities]

    return jsonify(activities_dict)

if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')
