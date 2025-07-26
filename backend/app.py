from flask import Flask
from flask_security import Security

from flask_restful import Api

from controllers.database import db
from controllers.config import Config
from controllers.userdatastore import user_datastore
from flask_cors import CORS
from controllers.authentication import Login, Logout, Register
from controllers.routes import Add_Lot, Lot_Management, viewspots, viewspotdetails, users, Reservationdata, user_search, book, spotbook, release

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)

    api = Api(app, prefix='/api')

    api.add_resource(Add_Lot, '/lots')
    api.add_resource(Lot_Management, '/lots/<int:lot_id>')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Register, '/register')
    api.add_resource(viewspots, '/spots/<int:spot_id>')
    api.add_resource(viewspotdetails, '/spotdetails/<int:spot_id>')
    api.add_resource(users, '/users')
    api.add_resource(Reservationdata, '/reservations')
    api.add_resource(user_search, '/search/<string:search>/<string:search_type>')
    api.add_resource(book, '/bookspot/<int:lot_id>')
    api.add_resource(spotbook, '/book/<int:lot_id>')
    api.add_resource(release, '/release/<int:reservation_id>')

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
        user_role = user_datastore.find_or_create_role(name='user', description='User role')

        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(email='admin@gmail.com', name='admin', password='admin@123', roles=[admin_role])

        db.session.commit()

    return app, api

app, api = create_app()
CORS(app, origins=["http://localhost:5173"], supports_credentials=True, allow_headers=['Content-Type', 'Authentication-Token'])




if __name__ == '__main__':
    app.run(debug=True)