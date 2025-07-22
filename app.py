from flask import Flask
from flask_security import Security

from flask_restful import Api

from controllers.database import db
from controllers.config import Config
from controllers.userdatastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)

    api = Api(app)

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
        user_role = user_datastore.find_or_create_role(name='user', description='User role')

        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(email='admin@gmail.com', password='admin', roles=[admin_role])

        db.session.commit()

    return app, api

app, api = create_app()

if __name__ == '__main__':
    app.run(debug=True)