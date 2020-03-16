class IllegalCarError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

rep_procedure = 'Repair procedure for {} loaded.'

class Car:
    average_weight = 70  # average person weight in kg

    def __init__(self, pax_count, car_mass, gear_count):

        self.pax_count = pax_count
        self.car_mass = car_mass
        self.gear_count = gear_count
        self.total_mass = self.car_mass + self.pax_count * self.average_weight

    @property
    def pax_count(self):
        return self.__pax_count

    @property
    def car_mass(self):
        return self.__car_mass

    @pax_count.setter
    def pax_count(self, pax_count):
        if isinstance(pax_count, int) and pax_count > 0 and pax_count <= 5:
            self.__pax_count = pax_count
        else:
            raise IllegalCarError('Not appropriate amount of seats.')

    @car_mass.setter
    def car_mass(self, car_mass):
        if isinstance(car_mass, int) and car_mass <= 2000:
            self.__car_mass = car_mass
        else:
            raise IllegalCarError("Car mass of vehicle shouldn't exceed 2000kg")

    def repair(self):
        print(rep_procedure.format('Car'))


class Workshop:


    def accept(self, vehicle):
        vehicle.repair()


class Bicycle:
    def repair(self):
        print(rep_procedure.format('Bicycle'))


class Truck:
    def repair(self):
        print(rep_procedure.format('Truck'))


c = Car(3, 1600, 5)
try:
    wrong_car_1 = Car(3, 2001, 5)
except Exception as e:
    print(f'{type(e)}:{e}')

b = Bicycle()
t = Truck()
w = Workshop()
w.accept(b)
w.accept(c)
w.accept(t)
