# Development Guide

## Contributing to WorkoutTracker

This guide will help you set up a development environment and contribute to the WorkoutTracker project.

## Development Setup

### 1. Fork and Clone

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/WorkoutTracker.git
cd WorkoutTracker

# Add upstream remote
git remote add upstream https://github.com/ccarmody5/WorkoutTracker.git
```

### 2. Create Development Branch

```bash
# Update from upstream
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov flake8 black
```

### 4. Configure Development Database

```bash
# Use a separate dev database
psql -U postgres

CREATE DATABASE workout_tracker_dev;
CREATE USER workout_dev WITH PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE workout_tracker_dev TO workout_dev;
```

Set environment variables:
```bash
export DATABASE_URL="postgresql://workout_dev:dev_password@localhost:5432/workout_tracker_dev"
export FLASK_ENV="development"
```

---

## Project Structure

```
WorkoutTracker/
├── docs/                          # Documentation (this directory)
├── config/
│   ├── __init__.py
│   ├── app_log_config.py          # Terminal logging
│   ├── webapp_log_config.py       # Web logging
│   └── db_table_config.py         # SQLAlchemy models
├── helpers/
│   ├── __init__.py
│   ├── activity_lib.py            # Activity business logic
│   ├── user_lib.py                # User business logic
│   ├── workout_lib.py             # Workout business logic
│   ├── workout_detail_lib.py      # Set/detail business logic
│   └── dbHelper.py                # Database connection
├── templates/                     # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── select-activity.html
│   ├── workout-control.html
│   ├── set-control.html
│   ├── manage-users.html
│   └── user-edit.html
├── static/                        # CSS/JavaScript
│   ├── css/
│   └── js/
├── alembic/                       # Database migrations
│   ├── versions/                  # Migration files
│   └── env.py
├── tests/                         # Unit tests (to be created)
├── terminal_program.py            # Terminal entry point
├── webapp.py                      # Web server entry point
├── alembic.ini                    # Alembic configuration
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Code Style

### Follow PEP 8

Use `black` for formatting:
```bash
# Format entire project
black .

# Format specific file
black terminal_program.py
```

Use `flake8` for linting:
```bash
# Check entire project
flake8 .

# Check specific file
flake8 terminal_program.py

# Ignore certain errors
flake8 --ignore=E501,W503 .
```

---

## Key Components to Understand

### 1. Helper Libraries

Each helper library follows a consistent pattern:

```python
# Example: helpers/user_lib.py
from sqlalchemy.orm import sessionmaker
from config.db_table_config import User

class UserLib:
    def __init__(self, session):
        self.session = session()  # Create session from sessionmaker
    
    def create_user(self, first_name, last_name, created_by, updated_by):
        """Create and return new user"""
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            created_by=created_by,
            updated_by=updated_by
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user.user_id
    
    def get_pk(self, user_id):
        """Get user by primary key"""
        return self.session.query(User).filter(User.user_id == user_id).first()
```

**Pattern:**
1. Accept `session` parameter (sessionmaker)
2. Create instance session in `__init__`
3. Return primary key for create operations
4. Return object for retrieve operations
5. Always commit after modifications
6. Use filters for querying

---

### 2. Database Models

Located in `config/db_table_config.py`:

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    disabled = Column(String(1), default='N')
    created_by = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    updated_by = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = relationship('Workout', back_populates='user')
    
    def to_dict(self):
        """Convert to JSON-serializable dict"""
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'disabled': self.disabled
        }
```

**Model Guidelines:**
- Use `@declarative_base()` for inheritance
- Define relationships for ORM queries
- Include `to_dict()` for API serialization
- Use ForeignKey for relationships
- Include timestamps (created_at, updated_at)

---

## Adding New Features

### Example: Add Total Weight Calculation

**1. Update Model** (`config/db_table_config.py`):
```python
class Workout(Base):
    # ... existing columns ...
    total_weight = Column(Integer, default=0)  # New column
```

**2. Create Migration**:
```bash
alembic revision --autogenerate -m "Add total_weight to workout"
alembic upgrade head
```

**3. Update Business Logic** (`helpers/workout_lib.py`):
```python
def calculate_total_weight(self, workout_id):
    """Calculate total weight for all sets"""
    workout = self.session.query(Workout).filter(
        Workout.workout_id == workout_id
    ).first()
    
    total = self.session.query(
        func.sum(WorkoutDetail.rep_count * WorkoutDetail.weight)
    ).filter(
        WorkoutDetail.workout_id == workout_id
    ).scalar()
    
    workout.total_weight = total
    self.session.commit()
    return workout
```

**4. Expose via API** (`webapp.py`):
```python
@webapp.route('/get_workout_summary', methods=['GET'])
def get_workout_summary():
    workout = workout_lib.WorkoutLib(session=Session()).get_workout(
        current_workout.workout_id
    )
    return jsonify({
        'workout_id': workout.workout_id,
        'total_weight': workout.total_weight
    })
```

---

## Testing

### Write Unit Tests

Create `tests/test_user_lib.py`:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_table_config import Base, User
from helpers.user_lib import UserLib


@pytest.fixture
def test_db():
    """Create in-memory SQLite database for testing"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


def test_create_user(test_db):
    """Test user creation"""
    user_lib = UserLib(session=test_db)
    user_id = user_lib.create_user(
        first_name="John",
        last_name="Doe",
        created_by=1,
        updated_by=1
    )
    
    assert user_id is not None
    user = user_lib.get_pk(user_id)
    assert user.first_name == "John"
    assert user.last_name == "Doe"


def test_get_all_users(test_db):
    """Test retrieving all users"""
    user_lib = UserLib(session=test_db)
    
    # Create users
    user_lib.create_user("User1", "Test1", 1, 1)
    user_lib.create_user("User2", "Test2", 1, 1)
    
    users = user_lib.get_all_users()
    assert len(users) == 2
```

**Run tests:**
```bash
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov  # With coverage
```

---

## Database Migrations

### Create Migration for New Feature

```bash
# Auto-generate based on model changes
alembic revision --autogenerate -m "Add feature description"

# Edit migration file in alembic/versions/
# Then apply
alembic upgrade head
```

### Migration File Example

```python
# alembic/versions/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'user',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
    )

def downgrade():
    op.drop_table('user')
```

---

## Debugging

### Enable Debug Mode

```python
# In terminal_program.py
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# In webapp.py
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
```

### Use Python Debugger

```python
# Insert breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint (Python 3.7+)
breakpoint()

# Commands:
# n - next line
# c - continue
# p variable - print variable
# l - list code
# s - step into function
```

---

## Git Workflow

### Commit Guidelines

**Use descriptive commit messages:**
```bash
# Good
git commit -m "Add total_weight calculation to workout tracking"

# Bad
git commit -m "fix bug"
git commit -m "updates"
```

### Push Changes

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Link any related issues
# Add description of changes
```

---

## Performance Optimization

### Query Optimization

```python
# Bad: N+1 query problem
workouts = session.query(Workout).all()
for workout in workouts:
    print(workout.user.first_name)  # New query per workout!

# Good: Use eager loading
workouts = session.query(Workout).options(
    joinedload(Workout.user)
).all()
```

### Caching

```python
# Simple caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_activity_by_id(activity_id):
    # Cache queries
    return session.query(Activity).filter(...).first()
```

---

## Deployment Considerations

### Environment Variables

```python
# Use environment variables for configuration
import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://localhost/workout_tracker'
)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-not-for-production')
```

### Security

- [ ] Change hard-coded `SECRET_KEY`
- [ ] Add input validation
- [ ] Implement SQL injection prevention (use parameterized queries)
- [ ] Add user authentication
- [ ] Use HTTPS in production
- [ ] Sanitize file uploads
- [ ] Add rate limiting

### Scaling

- [ ] Implement database connection pooling
- [ ] Add caching layer (Redis)
- [ ] Use CDN for static files
- [ ] Monitor database performance
- [ ] Plan for horizontal scaling

---

## Resources

- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Flask:** https://flask.palletsprojects.com/
- **Alembic:** https://alembic.sqlalchemy.org/
- **PEP 8 Style Guide:** https://pep8.org/
- **Git Workflow:** https://git-scm.com/book/

---

## Getting Help

- Check existing issues on GitHub
- Review the [Troubleshooting](Troubleshooting) guide
- Comment on related issues
- Start a discussion in GitHub Discussions

---

## Future Enhancement Ideas

- [ ] Add user authentication/passwords
- [ ] Implement workout templates
- [ ] Add progress tracking/graphs
- [ ] Create mobile app version
- [ ] Add import/export functionality
- [ ] Implement user roles/permissions
- [ ] Add social features (sharing)
- [ ] Create API documentation (Swagger/OpenAPI)
- [ ] Add automated testing (CI/CD)
- [ ] Implement data backup/restore
