from flask_restful import Resource
from flask import request, jsonify, make_response, g
from flask_security import auth_token_required, utils, roles_required, current_user
from controllers.database import db, ParkingLot, ParkingSpot, Reservation, User
from pytz import timezone
from datetime import datetime
import pytz

from controllers.userdatastore import user_datastore

def get_time():
    return datetime.now(timezone('Asia/Kolkata'))

class Add_Lot(Resource):
    @auth_token_required
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
                'spots_count':ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count(),
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

class Reservationdata(Resource):
    @auth_token_required
    @roles_required('user')
    def get(self):
        user_id = current_user.id
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        result = []
        for reservation in reservations:
            result.append({
                'id': reservation.id,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'user_id': reservation.user_id,
                'spot_id': reservation.spot_id,
                'parking_timestamp': reservation.parking_timestamp,
                'leaving_timestamp': reservation.leaving_timestamp,
                'vehicle_number': reservation.vehicle_number,
                'cost_per_hour': reservation.cost_per_hour
            })
        return make_response(jsonify(result), 200)

class user_search(Resource):
    @auth_token_required
    @roles_required('user')
    def get(self, search,search_type):
        if search_type == 'location':
            lots = ParkingLot.query.filter_by(address=search).all()
        elif search_type == 'pincode':
            lots = ParkingLot.query.filter_by(pin_code=search).all()
        else:
            lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            result.append({
                'id': lot.id,
                'address': lot.address,
                'spots_count': ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
                
            })
        return make_response(jsonify(result), 200)

    
class release(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self,reservation_id):
        reservation = Reservation.query.get_or_404(reservation_id)
        if reservation is None:
            return make_response(jsonify({'message': 'Reservation not found'}), 404)
        if reservation.leaving_timestamp is not None:
            return make_response(jsonify({'message': 'Spot is not reserved'}), 400)
        spot = ParkingSpot.query.get_or_404(reservation.spot_id)
        if spot is None:
            return make_response(jsonify({'message': 'Spot not found'}), 404)
        reservation.leaving_timestamp = get_time()
        spot.status = 'A'
        db.session.commit()
        return make_response(jsonify({'message': 'Spot released successfully'}), 200)
    
    @auth_token_required
    @roles_required('user')
    def get(self,reservation_id):
        ist = pytz.timezone('Asia/Kolkata')
        reservation = Reservation.query.get_or_404(reservation_id)
        if reservation is None:
            return make_response(jsonify({'message': 'Reservation not found'}), 404)
        duration = (get_time() - ist.localize(reservation.parking_timestamp)).total_seconds()/3600
        total_cost = round(reservation.cost_per_hour * duration,2)
        result = {
            'id': reservation.id,
            'user_id': reservation.user_id,
            'spot_id': reservation.spot_id,
            'parking_timestamp': reservation.parking_timestamp,
            'vehicle_number': reservation.vehicle_number,
            'cost_per_hour': reservation.cost_per_hour,
            'duration': duration,
            'total_cost': total_cost
        }
        return make_response(jsonify(result), 200)

        
class book(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self,lot_id):

        lot = ParkingLot.query.get_or_404(lot_id)
        if lot is None:
            return make_response(jsonify({'message': 'Lot not found'}), 404)
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if spot is None:
            return make_response(jsonify({'message': 'No available spots'}), 400)
        data = request.get_json()

        reservation = Reservation(
            user_id = current_user.id,
            spot_id=spot.id,
            parking_timestamp=get_time(),
            vehicle_number=request.json.get('vehicle_number'), 
            cost_per_hour=lot.price_per_hour
            )
        db.session.add(reservation)
        spot.status = 'O'
        db.session.commit()
        return make_response(jsonify({'message': 'Spot reserved successfully'}), 200)
    
class spotbook(Resource):
    @auth_token_required
    @roles_required('user')
    def get(self,lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if spot is None:
            return make_response(jsonify({'message': 'No available spots'}), 400)
        result = {
            'spot_id': spot.id,
            'status': spot.status,
            'user_id': current_user.id
        }
        return make_response(jsonify(result), 200)
    
class records(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        ist = pytz.timezone('Asia/Kolkata')
        reservations = Reservation.query.all()
        result = []
        for reservation in reservations:
            if not reservation.leaving_timestamp:
                status = 'Active'
            else:
                duration = round((ist.localize(reservation.leaving_timestamp) - ist.localize(reservation.parking_timestamp)).total_seconds()/3600,2)
                total_cost = round(reservation.cost_per_hour * duration,2)
                status = 'Completed'
            result.append({
                'id': reservation.id,
                'user_id': reservation.user_id,
                'spot_id': reservation.spot_id,
                'parking_timestamp': reservation.parking_timestamp,
                'leaving_timestamp': reservation.leaving_timestamp,
                'duration': duration,
                'total_cost': total_cost,
                'vehicle_number': reservation.vehicle_number,
                'cost_per_hour': reservation.cost_per_hour,
                'name': reservation.user.name,
                'prime_location_name': reservation.parking_spot.parking_lot.prime_location_name,
                'status': status
            })
            duration = None
            total_cost = None
        return make_response(jsonify(result), 200)