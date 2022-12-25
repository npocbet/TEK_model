import datetime
import uuid

client_cargo = {'clients': {}, 'cargo': {}}
order_cargo = {'orders': {}, 'cargo': {}}
transport_cargo = {'transport': {}, 'cargo': {}}
transport_order = {'transport': {}, 'orders': {}}

DAY_DISTANCE = 500


class Client:
    clients = {}

    def __init__(self, name, phone_number):
        self.id = uuid.uuid4()
        self.name = name
        self.phone_number = phone_number
        Client.clients[self.id] = self

    @classmethod
    def find_client(self, name, phone_number):
        for id, link in Client.clients:
            if link.name == name and link.phone_number == phone_number:
                return link
        return None


class Transport:
    transport = {}

    def __init__(self, load_capacity, body_volume, usage_cost):
        self.id = uuid.uuid4()
        self.load_capacity = load_capacity
        self.body_volume = body_volume
        self.usage_cost = usage_cost
        Transport.transport[str(self.id)] = self

    def __repr__(self):
        return f'{self.load_capacity}\t\t{self.body_volume}\t\t{self.usage_cost}'

    def search_order(self):
        return 'свободен' if self.id not in transport_order['transport'] else \
            transport_order['transport'][self.id]

    def transport_can_take_cargo(self, size, weight, destination):
        temp_cargo = self.load_capacity - int(weight)
        temp_volume = self.body_volume - max([int(i) for i in size.split('x')]) ** 2
        cargo_array = [] if self.id not in transport_cargo['trincluded_cargoansport'] \
            else transport_cargo['transport'][self.id]
        if not cargo_array:
            included_weight = sum([cg.weight for cg in cargo_array])
            included_size = sum([cg.size for cg in cargo_array])
            if cargo_array[0].destination == destination:
                temp_cargo -= included_weight
                temp_volume -= included_size
            else:
                return False
        if temp_volume > 0 and temp_volume > 0:
            return True
        else:
            return False


class Cargo:
    cargo = {}

    def __init__(self, weight, destination, price, size):
        self.id = uuid.uuid4()
        self.weight = weight
        self.destination = destination
        self.price = price
        self.size = size
        Cargo.cargo[self.id] = self

    def __repr__(self):
        return f'{self.weight}\t\t{self.destination}\t\t{self.price}\t\t{self.size}'


class Order:
    orders = {}

    def __init__(self, date_of_creation, date_of_complition):
        self.id = uuid.uuid4()
        self.date_of_creation = date_of_creation
        self.date_of_complition = date_of_complition
        Order.orders = self


running = True
date = datetime.datetime.now()
while running:
    req = int(input(f'''Сегодня {date}.
                Перечень команд:
                1. расчет стоимости заказа
                2. поиск транспорта
                3. просмотр статуса транспорта
                4. поиск заказа
                5. просмотр статуса заказов
                6. добавить новое транспортное средство
                7. завершить день
                0. выход из программы. 
            '''))
    if req == 1:
        print('Введите размер, вес, пункт назначения и расстояние до этого пункта\n'
              'через пробел, например 30х40х50 5 Краснодар 236')
        size, weight, destination, distance = input().split()
        # список подходящего транспорта
        tr_lst = []
        for id, tr in Transport.transport:
            if tr.search_order() == 'свободен' and \
                    tr.transport_can_take_cargo(size, weight, destination):
                tr_lst.append(tr)
        price = min([tr.usage_cost for tr in tr_lst])
        print(f'Стоимость доставки составит {price * distance}\n'
              f'срок доставки - {int(distance) // DAY_DISTANCE + 1}\n'
              'оформляем? (y/n)')
        answer = input()
        if answer == 'y':
            print('необходимо указать ваше имя и телефон для обратной связи')
            name, phone = input().split()
            client = Client.find_client(name, phone)
            if not client:
                client = Client(name, phone)
                client_cargo['clients'][client.id] = []
            transport = list(filter(lambda x: x.usage_cost == price, tr_lst))
            cargo = Cargo(weight, destination, price, size)
            print(f'Номер груза {cargo.id}')
            order = Order(date + datetime.timedelta(days=1),
                          date + datetime.timedelta(days=1 + (int(distance)
                                                              // DAY_DISTANCE + 1) * 2))
            print(f'Номер вашего заказа {order.id}')
            client_cargo['clients'][client.id].append(cargo.id)
            client_cargo['cargo'][cargo.id].append(client.id)
            order_cargo['orders'][order.id].append(cargo.id)
            order_cargo['cargo'][cargo.id].append(order.id)
            transport_cargo['transport'][transport[0].id].append(cargo.id)
            transport_cargo['cargo'][cargo.id].append(transport[0].id)
            transport_order['transport'][transport[0].id].append(order.id)
            transport_order['orders'][order.id].append(transport[0].id)
        else:
            input('Приходите еще \n Press any key...')
    elif req == 2:
        print('введите часть id транспорта ...')
        search = input()
        print('id\t\tV\t\tM\t\tusage cost\t\tЗаказ')
        print('\n'.join([f'{id[-6:]}\t{tr}\t\t\t\t{tr.search_order()}'
                         for id, tr in Transport.transport.items()
                         if search in id]))
        print('-' * 56)
        input('Press any key ...')
    elif req == 3:
        print('Лист транспорта:')
        print('id\t\tV\t\tM\t\tusage cost\t\tЗаказ')
        print('\n'.join([f'{id[-6:]}\t{tr}\t\t\t\t{tr.search_order()}'
                         for id, tr in Transport.transport.items()]))

        print('-' * 56)
        input('Press any key ...')
    elif req == 4:
        print('введите часть id груза ...')
        search = input()
        print('id\t\tweight\t\tdestination\t\tprice\t\tsize')
        print('\n'.join([f'{id[-6:]}\t{cg}\t\t\t\t{cg.search_order()}'
                         for id, cg in Cargo.cargo.items()
                         if search in id]))
        print('-' * 56)
        input('Press any key ...')
    elif req == 5:
        print('Лист грузов:')
        print('id\t\tweight\t\tdestination\t\tprice\t\tsize')
        print('\n'.join([f'{id[-6:]}\t{cg}\t\t\t\t{cg.search_order()}'
                         for id, cg in Cargo.cargo.items()]))
        print('-' * 56)
        input('Press any key ...')
    elif req == 6:
        print('Введите через пробел характеристики нового транспорта:'
              'объем багажника, грузоподъемность и стоимость использования\n'
              'за единицу расстояния ...')
        load_capacity, body_volume, usage_cost = map(int, input().split())
        new_transport = Transport(load_capacity, body_volume, usage_cost)
    elif req == 7:
        date += datetime.timedelta(days=1)
        for id, order in Order.orders:
            if order.date_of_complition == date:
                transport_id = transport_order['orders'][id]
                del transport_order['orders'][id]
                del transport_order['transport'][transport_id]
                cargo_id_lst = transport_cargo['transport'][transport_id]
                del transport_cargo['transport'][transport_id]
                for cargo_id in cargo_id_lst:
                    del transport_cargo['cargo_id'][cargo_id]

    elif req == 0:
        running = False
        print('Завершение программы.')
