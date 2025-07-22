from flask_security import SQLAlchemySessionUserDatastore
from controllers.database import db, User, Role

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)