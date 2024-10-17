from sqlalchemy import insert, select, update, func
from sqlalchemy.orm import Session

import config.db_log_config as log_config
from config.db_table_config import User

logger = log_config.db_logger

class UserLib:
    def __init__(self, session: Session = None):
        self.session = session

    def create_user(self, first_name: str, last_name: str, disabled: str = 'N', created_by: int = -1,
                    updated_by: int = -1):
        logger.info(f"first_name: {first_name}, last_name: {last_name}")

        stmt = insert(User).values(
            first_name=first_name,
            last_name=last_name,
            disabled=disabled,
            created_by=created_by,
            updated_by=updated_by
        ).returning(User)
        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            updated_user = result.scalar()
            return updated_user
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def update_user(self, user_id: int, first_name: str = None, last_name: str = None, disabled: str = 'N',
                    updated_by: int = -1):
        logger.info(
            f"first_name: {first_name}, last_name: {last_name}, user_id: {user_id}, disabled: {disabled}, updated_by: {updated_by}")

        stmt = update(User).where(User.user_id == user_id)

        values_dict = {
            'updated_by': updated_by,
            'update_date': func.now()
        }

        if first_name:
            values_dict['first_name'] = first_name
            values_dict['last_name'] = last_name

        if disabled:
            values_dict['disabled'] = disabled

        stmt = stmt.values(**values_dict).returning(User)

        logger.info(stmt)

        try:
            result = self.session.execute(stmt)
            self.session.commit()
            new_user = result.scalar()
            return new_user
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            self.session.close()

    def get_pk(self, user_id: int) -> User:
        logger.info(f"user_id: {user_id}")
        stmt = select(User).where(User.user_id == user_id)

        try:
            result = self.session.execute(stmt).scalar()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()

    def get_all_users(self, include_disabled: str = "N"):
        logger.info(f"include_disabled: {include_disabled}")

        if include_disabled == "N":
            stmt = select(User).where(User.last_name != "system", User.disabled == "N").order_by(User.last_name.asc())
        else:
            stmt = select(User).where(User.last_name != "system").order_by(User.last_name.asc())

        try:
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            self.session.close()
