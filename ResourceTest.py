# -*- coding: utf-8 -*-

from simpy import Resource, Environment, Container


class GasStation:
    def __init__(self, env_car):
        self.fuel_dispensers = Resource(env_car, capacity=2)
        self.gas_tank = Container(env_car, init=100, capacity=1000)
        self.mon_proc = env_car.process(self.monitor_tank(env_car))

    def monitor_tank(self, env_car):
        while True:
            if self.gas_tank.level < 100:
                print('Calling tanker at %s' % env_car.now)
                env_car.process(self.tanker(env_car, self))
            yield env_car.timeout(15)

    def tanker(self, env_car):
        yield env_car.timeout(10)  # Need 10 Minutes to arrive
        print('Tanker arriving at %s' % env_car.now)
        amount = self.gas_tank.capacity - self.gas_tank.level
        yield self.gas_tank.put(amount)



def car(name, env_car, g_station):
    print('Car %s arriving at %s' % (name, env_car.now))
    with g_station.fuel_dispensers.request() as req:
        yield req
        print('Car %s starts refueling at %s' % (name, env_car.now))
        yield g_station.gas_tank.get(40)
        yield env_car.timeout(5)
        print('Car %s done refueling at %s' % (name, env_car.now))


def car_generator(env_car, g_station):
    for i in range(4):
        env_car.process(car(i, env_car, g_station))
        yield env_car.timeout(5)


if __name__ == '__main__':
    env = Environment()
    gas_station = GasStation(env)
    car_gen = env.process(car_generator(env))
    env.run(35)
