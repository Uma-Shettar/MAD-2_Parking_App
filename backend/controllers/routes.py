from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, utils, roles_required
from controllers.database import db, ParkingLot, ParkingSpot, Reservation, User

from controllers.userdatastore import user_datastore

class Add_Lot(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            spots = []
            for spot in lot.parking_spots:
                spots.append({
                    'id': spot.id,
                    'status': spot.status
                })
            result.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price_per_hour': lot.price_per_hour,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'total_spots': lot.total_spots,
                'spots': spots
            })

        return make_response(jsonify(result), 201)
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        prime_location_name = data.get('prime_location_name')
        price_per_hour = float(data.get('price_per_hour'))
        address = data.get('address')
        pin_code = data.get('pin_code')
        total_spots = int(data.get('total_spots'))

        if not data:
            return make_response(jsonify({'message': 'Lot data is required'}), 400)
        
        if not prime_location_name:
            return make_response(jsonify({'message': 'Prime location name is required'}), 400)
        
        if not price_per_hour:
            return make_response(jsonify({'message': 'Price per hour is required'}), 400)
        
        if not address:
            return make_response(jsonify({'message': 'Address is required'}), 400)
        
        if not pin_code:
            return make_response(jsonify({'message': 'Pin code is required'}), 400)
        
        if not total_spots:
            return make_response(jsonify({'message': 'Total spots is required'}), 400)
        
        if ParkingLot.query.filter_by(prime_location_name=prime_location_name).first():
            return make_response(jsonify({'message': 'Lot already exists'}), 409)


        new_lot = ParkingLot(prime_location_name=prime_location_name, price_per_hour=price_per_hour, address=address, pin_code=pin_code, total_spots=total_spots)
        db.session.add(new_lot)
        db.session.commit()

        for _ in range(total_spots):
            new_spot = ParkingSpot(lot_id=new_lot.id, status='A')
            db.session.add(new_spot)
        db.session.commit()

        return make_response(jsonify({'message': 'Lot added successfully'}), 200)
    
class Lot_Management(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self, lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        
        if lot is None:
            return make_response(jsonify({'message': 'Lot not found'}), 404)
        

        result = {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'price_per_hour': lot.price_per_hour,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'total_spots': lot.total_spots,
        }
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self, lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        
        if lot is None:
            return make_response(jsonify({'message': 'Lot not found'}), 404)
        
        db.session.delete(lot)
        db.session.commit()

        return make_response(jsonify({'message': 'Lot deleted successfully'}), 200)
    

    @auth_token_required
    @roles_required('admin')
    def put(self, lot_id):
        data = request.get_json()
        lot = ParkingLot.query.get_or_404(lot_id)
        
        if lot is None:
            return make_response(jsonify({'message': 'Lot not found'}), 404)
        
        if not data:
            return make_response(jsonify({'message': 'Lot data is required'}), 400)
        
        prime_location_name = data.get('prime_location_name')
        price_per_hour = data.get('price_per_hour')
        address = data.get('address')
        pin_code = data.get('pin_code')
        total_spots = data.get('total_spots')

        if not prime_location_name:
            return make_response(jsonify({'message': 'Prime location name is required'}), 400)
        
        if not price_per_hour:
            return make_response(jsonify({'message': 'Price per hour is required'}), 400)
        
        if not address:
            return make_response(jsonify({'message': 'Address is required'}), 400)
        
        if not pin_code:
            return make_response(jsonify({'message': 'Pin code is required'}), 400)
        
        if not total_spots:
            return make_response(jsonify({'message': 'Total spots is required'}), 400)
        
        if total_spots < ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count():
            return make_response(jsonify({'message': 'Not enough available spots'}), 400)
        
        elif total_spots < lot.total_spots:
            for _ in range(lot.total_spots - total_spots):
                delete_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').order_by(ParkingSpot.id.desc()).first()
                db.session.delete(delete_spot)

        elif total_spots > lot.total_spots:
            for _ in range(total_spots - lot.total_spots):
                new_spot = ParkingSpot(lot_id=lot_id, status='A')
                db.session.add(new_spot)
        
        lot.prime_location_name = prime_location_name
        lot.price_per_hour = price_per_hour
        lot.address = address
        lot.pin_code = pin_code
        lot.total_spots = total_spots

        
        db.session.add(lot)

        db.session.commit()

        return make_response(jsonify({'message': 'Lot updated successfully'}), 200)
    
class viewspots(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self,spot_id):
        spot = ParkingSpot.query.get_or_404(spot_id)
        if spot is None:
            return make_response(jsonify({'message': 'Spot not found'}), 404)
        result = {
            'id': spot.id,
            'lot_id': spot.lot_id,
            'status': spot.status,
        }
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self,spot_id):
        spot = ParkingSpot.query.get_or_404(spot_id)
        if spot is None:
            return make_response(jsonify({'message': 'Spot not found'}), 404)
        if spot.status != 'A':
            return make_response(jsonify({'message': 'Spot is not available'}), 400)
        db.session.delete(spot)
        db.session.commit()
        return make_response(jsonify({'message': 'Spot deleted successfully'}), 200)
    
class viewspotdetails(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self,spot_id):
        spot = ParkingSpot.query.get_or_404(spot_id)

        if spot is None:
            return make_response(jsonify({'message': 'Spot not found'}), 404)
        result = {
            'id': spot.id,
            'status': spot.status,
            'reservations': [reservation.to_dict() for reservation in spot.reservations],
        }
        return make_response(jsonify(result), 200)
    
class users(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        users = User.query.filter(User.email != 'admin@gmail.com').all()
        result = []
        for user in users:

            frequency = Reservation.query.filter_by(user_id=user.id).count()
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'frequency': frequency
            })
        return make_response(jsonify(result), 200)
        