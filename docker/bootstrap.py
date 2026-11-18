"""Create the starter profile and activity when the database is empty."""

from sqlalchemy import func, insert, select
from sqlalchemy.orm import Session

from config.db_table_config import Activity, User
from helpers.dbHelper import create_db_engine


def main():
    engine = create_db_engine()
    with Session(engine) as session, session.begin():
        session.connection().exec_driver_sql('LOCK TABLE "user" IN SHARE ROW EXCLUSIVE MODE')
        if session.scalar(select(User.user_id).limit(1)) is not None:
            return

        user_id = session.scalar(select(func.nextval(func.pg_get_serial_sequence('"user"', 'user_id'))))
        session.execute(insert(User).values(
            user_id=user_id,
            first_name="Workout",
            last_name="User",
            created_by=user_id,
            updated_by=user_id,
        ))
        session.add(Activity(activity_desc="Weight Training", created_by=user_id, updated_by=user_id))


if __name__ == "__main__":
    main()
