import datetime
import uuid

client_cargo = {}
order_cargo = {}
transport_cargo = {}
transport_order = {}


class Client:
    clients = {}

    def __init__(self, name, phone_number):
        self.id = uuid.UUID
        self.name = name
        self.phone_number = phone_number
        Client.clients[self.id] = self

    def preorder(self, size, weight, destination):
        pass


class Transport:
    transport = {}

    @classmethod
    def search_transport_to_the_same_destinition(cls, destinition):
        pass

    def __init__(self, load_capacity, body_volume, usage_cost):
        self.id = uuid.UUID
        self.load_capacity = load_capacity
        self.body_volume = body_volume
        self.usage_cost = usage_cost
        Transport.transport[self.id] = self

    def transport_can_take_cargo(self, cargo):
        pass

    def put_order_into_transport(self, order):
        pass


class Cargo:
    cargo = {}

    def __init__(self, weight, destination, price, size):
        self.id = uuid.UUID
        self.weight = weight
        self.destination = destination
        self.price = price
        self.size = size
        Cargo.cargo[self.id] = self


class Order:
    orders = {}

    def __init__(self, date_of_creation, date_of_complition):
        self.id = uuid.UUID
        self.date_of_creation = date_of_creation
        self.date_of_complition = date_of_complition
        Order.orders = self


running = True
date = datetime.datetime.now()
while running:
    req = int(input(f'''Сегодня {date}.
                Перечень команд:
                1. расчет стоимости заказа
                2. принять заказ
                3. поиск автомобиля
                4. просмотр статуса автомобиля
                5. поиск заказа
                6. добавить новое транспортное средство
                7. завершить день
                0. выход из программы. 
            '''))
    if req == 1:
        pass
    elif req == 2:
        pass
    elif req == 3:
        pass
    elif req == 4:
        pass
    elif req == 5:
        pass
    elif req == 6:
        pass
    elif req == 7:
        pass
    elif req == 0:
        running = False
        print('Завершение программы.')
