from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

import config.db_log_config as log_config
from config.db_table_config import WorkoutDetail, Workout, User, Activity

logger = log_config.db_logger

class WorkoutDetailLib:
    def __init__(self, session: Session = None):
        self.session = session

    def create_workout_detail(self, workout_id: int, rep_count: str = None, weight: float = None,
                              created_by: int = -1, updated_by: int = -1) -> WorkoutDetail:
        logger.info(
            f"workout_id: {workout_id}, rep_count: {rep_count}, weight: {weight}, created_by: {created_by}, updated_by: {updated_by}")

        stmt = insert(WorkoutDetail).values(
            workout_id=workout_id,
            rep_count=rep_count,
            weight=weight,
            start_time=datetime.now(),
            created_by=created_by,
            updated_by=updated_by
        ).returning(WorkoutDetail)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            new_workout_detail = result.scalar()
            return new_workout_detail
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def stop_workout_detail(self, workout_detail_id: int, updated_by: int = -1):
        logger.info(f"workout_detail_id: {workout_detail_id}, updated_by: {updated_by}")

        stmt = update(WorkoutDetail).where(WorkoutDetail.workout_detail_id == workout_detail_id).values(
            end_time=datetime.now(),
            updated_by=updated_by,
            update_date=datetime.now()
        ).returning(WorkoutDetail)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            workout_detail = result.scalar()
            return workout_detail
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def complete_workout_detail(self, workout_detail_id: int, rep_count: int = None, weight: float = None,
                                updated_by: int = -1):
        logger.info(
            f"workout_detail_id: {workout_detail_id}, rep_count: {rep_count}, weight: {weight}, updated_by: {updated_by}")

        stmt = update(WorkoutDetail).where(WorkoutDetail.workout_detail_id == workout_detail_id).values(
            rep_count=rep_count,
            weight=weight,
            updated_by=updated_by,
            update_date=datetime.now()
        ).returning(WorkoutDetail)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            workout_detail = result.scalar()
            return workout_detail
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def get_pk(self, workout_detail_id: int) -> WorkoutDetail:
        logger.info(f"workout_detail_id: {workout_detail_id}")
        stmt = select(WorkoutDetail).where(WorkoutDetail.workout_detail_id == workout_detail_id)

        try:
            result = self.session.execute(stmt).scalar()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_workout_details(self, workout_id: int):
        logger.info(f"getting workout details for workout_id {workout_id}")
        '''
        stmt = select(Workout, User, Activity).select_from(Workout).join(User, User.user_id == Workout.user_id).join(
            Activity, Activity.activity_id == Workout.activity_id).where(User.user_id == user_id)
        '''
        stmt = select(Workout, User, Activity, WorkoutDetail).select_from(WorkoutDetail).join(
            Workout, Workout.workout_id == WorkoutDetail.workout_id).join(
            Activity, Activity.activity_id == Workout.activity_id).join(
            User, User.user_id == Workout.user_id
        ).where(Workout.workout_id == workout_id)

        try:
            result = self.session.execute(stmt).all()
            return result
        except Exception as e:
            logger.error(e)
            print(e)
        finally:
            self.session.close()