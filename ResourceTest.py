# -*- coding: utf-8 -*-

from simpy import Resource, Environment, Container

# gas station global params
GAS_STATION_ALARM_LEVEL = 100  # 加油站预警油位
GAS_STATION_CAPACITY = 1000  # 加油站总计油量
GAS_RESOURCE_DISPENSER_CAPACITY = 2  # 加油站加油点数
GAS_TANKER_MONITOR_TIME = 15  # 加油站预警油位扫描间隔
GAS_TANKER_ARRIVE_USE_TIME = 10  # 加油车到达耗时

# =================================================
# monitor global params

# =================================================


class GasStation:
    def __init__(self, env_station):
        self.fuel_dispensers = Resource(env_station, capacity=GAS_RESOURCE_DISPENSER_CAPACITY)
        self.gas_tank = Container(env_station, init=GAS_STATION_ALARM_LEVEL, capacity=GAS_STATION_CAPACITY)
        self.mon_proc = env_station.process(self.monitor_tank(env_station))

    def monitor_tank(self, env_station):
        """
        每 15秒 检查 if level < 100 触发加油事件: tanker
        """
        while True:
            if self.gas_tank.level < GAS_STATION_ALARM_LEVEL:
                print('Calling tanker at %s' % env_station.now)
                env_station.process(self.tanker(env_station))
            yield env_station.timeout(GAS_TANKER_MONITOR_TIME)

    def tanker(self, env_station):
        """
        加油车进程单元： 10s后加油车到达，触发加油事件
        """
        yield env_station.timeout(GAS_TANKER_ARRIVE_USE_TIME)  # Need 10 Minutes to arrive
        print('Tanker arriving at %s' % env_station.now)
        amount = self.gas_tank.capacity - self.gas_tank.level
        yield self.gas_tank.put(amount)
        print('Tanker leaving at %s' % env_station.now)

    def car_generator(self, env_car):
        for i in range(10):
            env_car.process(self.car(i, env_car))
            yield env_car.timeout(5)

    def car(self, name, env_car):
        print('Car %s arriving at %s' % (name, env_car.now))
        with self.fuel_dispensers.request() as req:
            yield req
            print('Car %s starts refueling at %s' % (name, env_car.now))
            yield self.gas_tank.get(40)
            yield env_car.timeout(5)
            print('Car %s done refueling at %s' % (name, env_car.now))


if __name__ == '__main__':
    env = Environment()
    gas_station = GasStation(env)
    car_gen = env.process(gas_station.car_generator(env))
    env.run(70)
