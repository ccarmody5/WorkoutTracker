#!/usr/bin/env python3
"""
' Workout Tracker
' 10/6/2024 - Chris Carmody
'
' Utilizing a Flask front-end and a Postgres db this application
' will accept workout activities and record them in the database
'
"""
import sys

from sqlalchemy.orm import sessionmaker

import config.app_log_config as log_config
import helpers.activity_lib as activity_lib
import helpers.dbHelper as db_helper
import helpers.user_lib as user_lib
import helpers.workout_detail_lib as workout_detail_lib
import helpers.workout_lib as workout_lib

logger = log_config.app_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX terminal_program.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# Create DB Engine
engine = db_helper.create_db_engine()
Session = sessionmaker(bind=engine)

active_user = 0

def get_activity():
    logger.info("")
    activity_list = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='N')
    print("\nSelect an Activity from the list below (q to Quit):")
    # if not activity:
    for activity in activity_list:
        print(activity.activity_desc)

    activity_entered = input()

    if activity_entered.lower() == "q":
        get_menu()
        return

    while activity_entered.lower() not in [activity.activity_desc.lower() for activity in activity_list]:
        logger.error(f"{activity_entered} is not valid")
        """print(f"{activity_entered} is not a valid option")
        activity_entered = input()"""
        get_menu()

    logger.info(f"{activity_entered} was selected")
    # else:
    #    activity_entered = activity

    activity_id = activity_lib.ActivityLib(session=Session()).get_activity_by_desc(
        activity_desc=activity_entered).activity_id

    workout_id = workout_lib.WorkoutLib(session=Session()).create_workout(activity_id=activity_id, user_id=active_user,
                                                                          created_by=active_user,
                                                                          updated_by=active_user)

    workout_detail_id = workout_detail_lib.WorkoutDetailLib(session=Session()).create_workout_detail(
        workout_id=workout_id, created_by=active_user, updated_by=active_user)

    get_reps(workout_detail_id=workout_detail_id)

    return activity_entered

def get_reps(workout_detail_id):
    logger.info(f"workout_detail_id: {workout_detail_id}")
    print(f"Enter number of reps:")
    reps_entered = input()

    while not reps_entered.isnumeric():
        logger.error(f"{reps_entered} is not valid")
        print(f"{reps_entered} is not a valid number, try again")
        reps_entered = input()

    logger.info(f"{reps_entered} reps were entered")
    get_weight(workout_detail_id=workout_detail_id, reps=reps_entered)

def get_weight(workout_detail_id, reps):
    logger.info(f"workout_detail_id: {workout_detail_id}, reps: {reps}")
    print(f"Enter weight in lbs:")
    weight_entered = input()

    while not weight_entered.isnumeric():
        logger.error(f"{weight_entered} is not valid")
        print(f"{weight_entered} is not a valid number, try again")
        weight_entered = input()

    logger.info(f"{weight_entered} lbs was entered")

    workout_detail = workout_detail_lib.WorkoutDetailLib(session=Session()).complete_workout_detail(
        workout_detail_id=workout_detail_id,
        rep_count=reps,
        weight=weight_entered,
        updated_by=active_user)

    activity = activity_lib.ActivityLib(session=Session()).get_activity_by_workout_id(
        workout_id=workout_detail.workout_id)

    workout_length = workout_detail.end_time - workout_detail.start_time

    print(
        f"You performed {workout_detail.rep_count} reps of {workout_detail.weight} lbs ({float(workout_detail.rep_count) * float(workout_detail.weight)}lbs) "
        f"during your {activity.activity_desc} workout; \nWorkout length: {workout_length}")

    print(f"\nPress any key to start next set (q to Quit current workout).")

    choice = input()
    if choice.lower() == "q":
        current_workout = workout_lib.WorkoutLib(session=Session()).complete_workout(workout_detail.workout_id,
                                                                                     updated_by=active_user)
        workout_time = current_workout.end_time - current_workout.start_time

        print(f"\nWorkout Complete! \nWorkout length: {workout_time}")
        get_menu()
        return
    else:
        workout_detail_id = workout_detail_lib.WorkoutDetailLib(session=Session()).create_workout_detail(
            workout_id=workout_detail.workout_id, created_by=active_user, updated_by=active_user)
        get_reps(workout_detail_id=workout_detail_id)

def get_activities_menu():
    menu_list = ["1 - Add Activity",
                 "2 - Update Activity",
                 "3 - View Activities"]

    print(f"\nChoose an option from the menu below:")

    for menu_item in menu_list:
        print(menu_item)

    menu_choice = input()

    # Add Activity
    if menu_choice == "1":
        add_activity()
    # Update Activity
    elif menu_choice == "2":
        manage_activities()
    elif menu_choice == "3":
        activity_list = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='N')
        print(f"\nCurrent enabled activites: ")
        for activity in activity_list:
            print(activity.activity_desc)
        print(f"\nPress any key to continue.")
        input()
    else:
        print("Invalid menu choice")

def add_activity():
    logger.info("")
    activity_list = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='Y')

    print(f"Current activites: ")
    for activity in activity_list:
        print(activity.activity_desc)

    print(f"\nEnter the new activity description:")

    activity_desc = input()

    if activity_desc.lower() in ("exit", "quit", "cancel"):
        get_menu()
        return

    activity_lib.ActivityLib(session=Session()).create_activity(activity_desc=activity_desc, created_by=active_user
                                                                , updated_by=active_user)

def update_activity(activity_id: int, activity_desc: str = None, disabled: str = None):
    logger.info(f"activity_id: {activity_id}, activity_desc: {activity_desc}, disabled: {disabled}")
    if activity_desc:
        activity_lib.ActivityLib(session=Session()).update_activity(activity_id=activity_id,
                                                                    activity_desc=activity_desc,
                                                                    updated_by=active_user)
    elif disabled:
        activity_lib.ActivityLib(session=Session()).update_activity(activity_id=activity_id, disabled=disabled,
                                                                    updated_by=active_user)

def manage_activities():
    activity_list = activity_lib.ActivityLib(session=Session()).get_all_activities(include_disabled='Y')
    print(f"\nSelect an Activity from the list below:")

    for activity in activity_list:
        print(f"{activity.activity_id} - {activity.activity_desc} - Disabled: {activity.disabled}")

    choice = input()

    if choice not in [str(activity.activity_id) for activity in activity_list]:
        print("Invalid menu choice")
        get_menu()
        return

    update_activity_pk = activity_lib.ActivityLib(session=Session()).get_pk(activity_id=choice)

    menu_list = ["1 - Rename", "2 - Disable", "3 - Enable"]
    print(f"\nSelect an option for the Activity '{update_activity_pk.activity_desc}':")

    for menu_item in menu_list:
        print(menu_item)

    choice = input()

    if choice == "1":
        print(f"\nEnter the new activity description:")
        activity_desc = input()
        update_activity(update_activity_pk.activity_id, activity_desc=activity_desc)
    elif choice == "2":
        update_activity(update_activity_pk.activity_id, disabled="Y")
    elif choice == "3":
        update_activity(update_activity_pk.activity_id, disabled="N")
    else:
        print("Invalid menu choice")

def get_user_menu():
    menu_list = ["1 - Add User",
                 "2 - Update User",
                 "3 - View Users"]

    print(f"\nChoose an option from the menu below:")

    for menu_item in menu_list:
        print(menu_item)

    menu_choice = input()

    # Add User
    if menu_choice == "1":
        add_user()
    # Update User
    elif menu_choice == "2":
        manage_users()
    # View Users
    elif menu_choice == "3":
        user_list = user_lib.UserLib(session=Session()).get_all_users()
        print(f"\nCurrent enabled users: ")
        for user in user_list:
            print(f"{user.first_name} {user.last_name}")
        print(f"\nPress any key to continue.")
        input()
    else:
        print("Invalid menu choice")

def add_user():
    logger.info("")
    user_list = user_lib.UserLib(session=Session()).get_all_users()

    print(f"Current users: ")
    for user in user_list:
        print(f"{user.first_name} {user.last_name}")

    print(f"\nEnter the new users first name:")
    first_name = input()

    print(f"\nEnter the new users last name:")
    last_name = input()

    if first_name.lower() in ("exit", "quit", "cancel") or last_name.lower() in ("exit", "quit", "cancel"):
        get_menu()
        return

    user_lib.UserLib(session=Session()).create_user(first_name=first_name, last_name=last_name, created_by=active_user
                                                    , updated_by=active_user)

def manage_users():
    user_list = user_lib.UserLib(session=Session()).get_all_users(include_disabled='Y')
    print(f"\nSelect a User from the list below:")

    for user in user_list:
        print(f"{user.user_id} - {user.first_name} {user.last_name}- Disabled: {user.disabled}")

    choice = input()

    if choice not in [str(user.user_id) for user in user_list]:
        print("Invalid menu choice")
        get_menu()
        return

    update_user_pk = user_lib.UserLib(session=Session()).get_pk(user_id=choice)

    menu_list = ["1 - Rename", "2 - Disable", "3 - Enable"]
    print(f"\nSelect an option for the User '{update_user_pk.first_name} {update_user_pk.last_name}':")

    for menu_item in menu_list:
        print(menu_item)

    choice = input()

    if choice == "1":
        print(f"\nEnter the users first name:")
        first_name = input()
        print(f"\nEnter the users last name:")
        last_name = input()
        update_user(update_user_pk.user_id, first_name=first_name, last_name=last_name)
    elif choice == "2":
        update_user(update_user_pk.user_id, disabled="Y", )
    elif choice == "3":
        update_user(update_user_pk.user_id, disabled="N")
    else:
        print("Invalid menu choice")

def update_user(user_id: int, first_name: str = None, last_name: str = None, disabled: str = None):
    logger.info(f"user_id: {user_id}, first_name: {first_name}, last_name: {last_name}, disabled: {disabled}")
    if first_name:
        user_lib.UserLib(session=Session()).update_user(user_id=user_id, first_name=first_name, last_name=last_name,
                                                        updated_by=active_user)
    elif disabled:
        user_lib.UserLib(session=Session()).update_user(user_id=user_id, disabled=disabled, updated_by=active_user)

def login():
    user_list = user_lib.UserLib(session=Session()).get_all_users(include_disabled='Y')
    print(f"\nSelect a User from the list below to login:")

    for user in user_list:
        print(f"{user.user_id} - {user.first_name} {user.last_name}")
    print(f"Q - Quit")

    user_selected = input()

    if user_selected.lower() == "q":
        print("Shutting down")
        sys.exit(0)

    if user_selected not in [str(user.user_id) for user in user_list]:
        print("Invalid menu choice")
        get_menu()
        return

    global active_user
    active_user = int(user_selected)

def logout():
    global active_user
    active_user = 0

def get_menu():
    if active_user == 0:
        login()
        return

    menu_list = ["1 - Start Activity",
                 "2 - Manage Activities",
                 "3 - Manage Users",
                 "4 - Logout",
                 "Q - Quit"]

    print("\nChoose an option from the menu below:")

    for menu_item in menu_list:
        print(menu_item)

    menu_choice = input()

    # Start Activity
    if menu_choice == "1":
        get_activity()
    # Manage Activities
    elif menu_choice == "2":
        get_activities_menu()
    # Manage Users
    elif menu_choice == "3":
        get_user_menu()
    elif menu_choice == "4" and active_user > 0:
        logout()
    elif menu_choice == "4" and active_user == 0:
        login()
    elif menu_choice.lower() == "q":
        print(f"Shutting down")
        sys.exit(0)
    else:
        print("Invalid menu choice")

def main():
    logger.info("In main loop")

    while True:
        get_menu()

# Call main()
__name__ == '__main__' and main()
