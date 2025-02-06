import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from models import db, User, init_db  # Replace 'your_module' with your actual module name


# Test app setup for an in-memory SQLite database
@pytest.fixture(scope='module')
def test_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        init_db()  # Initialize the database
        yield app


# Test case for database initialization
def test_init_db(test_app):
    with test_app.app_context():
        # Test that the 'user' table exists after db.create_all()
        inspector = inspect(db.engine)
        assert inspector.has_table('user')  # Check if 'user' table exists


# Test case for creating a user
def test_create_user(test_app):
    with test_app.app_context():
        # Create a user instance
        user = User(name="John Doe", email="john@example.com", password="password123")

        # Add and commit the user to the database
        db.session.add(user)
        db.session.commit()

        # Query the user by email to verify it's inserted
        queried_user = User.query.filter_by(email="john@example.com").first()
        assert queried_user is not None
        assert queried_user.name == "John Doe"
        assert queried_user.email == "john@example.com"


# Test case for unique email constraint
def test_unique_email(test_app):
    with test_app.app_context():
        # Add a user with a specific email
        user1 = User(name="Jane Doe", email="jane@example.com", password="password456")
        db.session.add(user1)
        db.session.commit()

        # Try to add another user with the same email, it should raise an IntegrityError
        user2 = User(name="Bob Smith", email="jane@example.com", password="password789")
        db.session.add(user2)

        # Commit to the session and expect an error
        with pytest.raises(Exception):
            db.session.commit()


# Test case for password length
def test_password_length(test_app):
    with test_app.app_context():
        # Create a user with a password of valid length
        user = User(name="Alice", email="alice@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Check if the user has been created
        queried_user = User.query.filter_by(email="alice@example.com").first()
        assert queried_user.password == "password"


# Test case for querying users
def test_query_users(test_app):
    with test_app.app_context():
        # Clear any existing data
        db.session.query(User).delete()
        db.session.commit()

        # Add multiple users to the database
        user1 = User(name="Eve", email="eve@example.com", password="mypassword")
        user2 = User(name="Charlie", email="charlie@example.com", password="password123")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Query for all users
        users = User.query.all()
        assert len(users) == 2  # Should only be 2 users


# Test case for deleting a user
def test_delete_user(test_app):
    with test_app.app_context():
        # Create a user
        user = User(name="David", email="david@example.com", password="davidpass")
        db.session.add(user)
        db.session.commit()

        # Query for the user
        queried_user = User.query.filter_by(email="david@example.com").first()
        assert queried_user is not None

        # Delete the user
        db.session.delete(queried_user)
        db.session.commit()

        # Verify the user is deleted
        deleted_user = User.query.filter_by(email="david@example.com").first()
        assert deleted_user is None


# Test case for updating user details
def test_update_user(test_app):
    with test_app.app_context():
        # Create a user
        user = User(name="Michael", email="michael@example.com", password="michaelpass")
        db.session.add(user)
        db.session.commit()

        # Query for the user and update their details
        queried_user = User.query.filter_by(email="michael@example.com").first()
        queried_user.name = "Michael Jordan"
        db.session.commit()

        # Verify the name has been updated
        updated_user = User.query.filter_by(email="michael@example.com").first()
        assert updated_user.name == "Michael Jordan"
