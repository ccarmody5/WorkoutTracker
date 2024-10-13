from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

import config.db_log_config as log_config
from config.db_table_config import User, Activity, Workout

logger = log_config.db_logger


class WorkoutLib:
    def __init__(self, session: Session = None):
        self.session = session

    def create_workout(self, activity_id: Activity.activity_id, user_id: User.user_id, created_by: int = -1,
                       updated_by: int = -1):
        logger.info(
            f"activity_id: {activity_id}, user_id: {user_id}, created_by: {created_by}, updated_by: {updated_by}")

        stmt = insert(Workout).values(
            activity_id=activity_id,
            user_id=user_id,
            start_time=datetime.now(),
            created_by=created_by,
            updated_by=updated_by
        ).returning(Workout.workout_id)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            new_workout_id = result.scalar()
            return new_workout_id
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def complete_workout(self, workout_id: int, updated_by: int = -1):
        logger.info(f"updated_by: {updated_by}")
        stmt = update(Workout).where(Workout.workout_id == workout_id).values(
            end_time=datetime.now(),
            updated_by=updated_by
        ).returning(Workout)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            workout = result.scalar()
            return workout
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def get_pk(self, workout_id: int) -> Workout:
        logger.info(f"workout_id: {workout_id}")
        stmt = select(Workout).where(Workout.workout_id == workout_id)

        try:
            result = self.session.execute(stmt).scalar()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_all_workouts(self):
        logger.info(f"getting all workouts")
        stmt = select(Workout).order_by(Workout.workout_id.asc())
        try:
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()
