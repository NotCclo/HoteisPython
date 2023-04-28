class ReservationModel:
    def __init__(self, hotel_id, data_ini, data_end, room_type, client_id):
        self.client_id = client_id
        self.hotel_id=hotel_id
        self.data_ini=data_ini
        self.data_end=data_end
        self.room_type=room_type