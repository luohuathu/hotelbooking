#!/usr/bin/python
""" This simple hotel booking application is tested with Python 2.7 """
import csv
import argparse
from datetime import datetime

class Hotel:       
    def __init__(self, name, num_room): 
        self.__occupancy = {}          # __occupancy stores the number of reserved rooms for each date(converted to proleptic Gregorian ordinal) 
        self.__name = name
        self.__num_rooms = num_room

    def reserve(self, checkin, checkout):
        if checkin.toordinal() >= checkout.toordinal():
            raise ValueError("Checkout date earlier than checkin date!")
        for i in range(checkin.toordinal(), checkout.toordinal()):
            if i not in self.__occupancy:
                self.__occupancy[i] = 1
            elif self.__occupancy[i] < self.__num_rooms:
                self.__occupancy[i] += 1
            else:
                raise ValueError("Reservation fails!") 
                
    def is_available(self, checkin, checkout):
        if checkin.toordinal() >= checkout.toordinal():
            raise ValueError("Checkout date earlier than checkin date!")
        for i in range(checkin.toordinal(), checkout.toordinal()):
            if i in self.__occupancy and self.__occupancy[i] == self.__num_rooms:
                return False
        return True

    def get_name(self):
        return self.__name


class HotelSystem:
    def __init__(self):
        self.__hotels = {}           # A dictionary of hotels, indexed by their names.

    def add_hotel(self, name, num_rooms):
        if name in self.__hotels:
            raise ValueError("Hotel already exists.")
        self.__hotels[name] = Hotel(name, num_rooms)
 
    def make_reservation(self, name, checkin, checkout):
        if name not in self.__hotels:
            raise ValueError("Hotel does not exist.")
        self.__hotels[name].reserve(checkin, checkout)
        
    def check_availability(self, checkin, checkout):
        results = []
        for hotel in self.__hotels.values():
            if hotel.is_available(checkin, checkout):
                results.append(hotel.get_name())
        return '\n'.join(results)


parser = argparse.ArgumentParser(description='A simple hotel booking app')
parser.add_argument('--hotels', dest = 'hotels_file', required = True, help = 'name of the file containing a list of hotels')
parser.add_argument('--bookings', dest = 'bookings_file', required = True, help = 'name of the file containing a list of bookings')
parser.add_argument('--checkin', dest = 'checkin', required = True, help = 'checkin date')
parser.add_argument('--checkout', dest = 'checkout', required = True, help = 'checkout date')
args = parser.parse_args()

S = HotelSystem()

with open(args.hotels_file, 'r') as csvfile:
    hotel_data = csv.reader(csvfile, delimiter = ',')
    for row in hotel_data:
        if row[0][0] == '#':
            continue
        S.add_hotel(row[0], int(row[1]))

with open(args.bookings_file, 'r') as csvfile:
    booking_data = csv.reader(csvfile, delimiter = ',')
    for row in booking_data:
        if row[0][0] == '#':
            continue
        checkin = datetime.strptime(row[1], ' %Y-%m-%d')
        checkout = datetime.strptime(row[2], ' %Y-%m-%d')
        S.make_reservation(row[0], checkin, checkout)

checkin = datetime.strptime(args.checkin,'%Y-%m-%d')
checkout = datetime.strptime(args.checkout,'%Y-%m-%d')
print S.check_availability(checkin, checkout)      
