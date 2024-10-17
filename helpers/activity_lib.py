from typing import Sequence

from sqlalchemy import insert, select, func, update
from sqlalchemy.orm import Session

import config.db_log_config as log_config
from config.db_table_config import Activity, Workout

# from helpers.dbHelper import create_db_engine

logger = log_config.db_logger

class ActivityLib:
    def __init__(self, session: Session = None):
        self.session = session

    def create_activity(self, activity_desc: str, disabled='N', activity_type: str = None, default_weight: float = None,
                        created_by: int = -1, updated_by: int = -1):
        logger.info(f"activity_desc: {activity_desc}, activity_type: {activity_type}, default_weight: {default_weight} "
                    f"created_by: {created_by}, updated_by: {updated_by}")

        stmt = insert(Activity).values(
            activity_desc=activity_desc,
            disabled=disabled,
            activity_type=activity_type,
            default_weight=default_weight,
            created_by=created_by,
            updated_by=updated_by
        ).returning(Activity)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            new_activity = result.scalar()
            return new_activity
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def update_activity(self, activity_id: int, activity_desc: str = None, disabled: str = None,
                        activity_type: str = None, default_weight: float = None, updated_by: int = -1):
        logger.info(
            f"activity_id: {activity_id}, activity_desc: {activity_desc}, activity_type: {activity_type}, "
            f"default_weight: {default_weight},disabled: {disabled}, updated_by: {updated_by}")

        stmt = update(Activity).where(Activity.activity_id == activity_id)

        values_dict = {
            'activity_desc': activity_desc,
            'activity_type': activity_type,
            'default_weight': default_weight,
            'disabled': disabled,
            'updated_by': updated_by,
            'update_date': func.now()
        }

        stmt = stmt.values(**values_dict).returning(Activity)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            new_activity = result.scalar()
            return new_activity
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def get_pk(self, activity_id: int) -> Activity:
        logger.info(f"activity_id: {activity_id}")
        stmt = select(Activity).where(Activity.activity_id == activity_id)

        try:
            result = self.session.execute(stmt).scalar()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_activity_by_desc(self, activity_desc: str) -> Activity:
        logger.info(f"activity_desc: {activity_desc}")
        stmt = select(Activity).where(activity_desc.lower() == func.lower(Activity.activity_desc))

        try:
            result = self.session.execute(stmt).scalars().first()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_activity_by_workout_id(self, workout_id: int):
        logger.info(f"workout_id: {workout_id}")

        # Join workout with activity on activity_id
        stmt = (select(Activity)
                .join(Workout, Activity.activity_id == Workout.activity_id)
                .where(Workout.workout_id == workout_id))

        try:
            result = self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_all_activities(self, include_disabled: str = 'N') -> Sequence[Activity]:
        logger.info(f"getting all activities")

        if include_disabled == 'Y':
            stmt = select(Activity).order_by(Activity.activity_desc.asc())
        else:
            stmt = select(Activity).where(Activity.disabled == 'N').order_by(Activity.activity_desc.asc())

        try:
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()
