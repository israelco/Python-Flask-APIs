from flask_restful import Resource,reqparse
from models.hotel import HotelModel

hoteis = [
    { 'hotel_id': 1,
      'nome': 'Alpha Hotel',
      'estrelas': 4.3,
      'diaria': 420.34,
      'cidade': 'Torres'
    },
    {'hotel_id': 2,
     'nome': 'Bravo Hotel',
     'estrelas': 4.4,
     'diaria': 430.34,
     'cidade': "Nova Veneza"
    },
    {'hotel_id': 3,
     'nome': 'Charlie Hotel',
     'estrelas': 4.9,
     'diaria': 480.34,
     'cidade': 'Florianopolis'
     }

]



class Hoteis(Resource):

    def get(self):

        return{'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field ")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #not found

    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists." .format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()

        return hotel.json()

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 #ok

        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()

        return hotel.json(),201 #hotel criado

    def delete(self, hotel_id):
       hotel = HotelModel.find_hotel(hotel_id)
       if hotel:
            hotel.delete_hotel()
            return {'message':'Hotel deleted.'}

       return {'message': 'Hotel not found.'},404
