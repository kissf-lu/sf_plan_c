# -*- coding: utf-8 -*-


from simpy import Environment
from random import seed, randint
seed(23)


class Env(Environment):
    def __init__(self):
        Environment.__init__(self)
        self.drive_proc = self.process(self.drive())
        self.bat_ctrl_proc = self.process(self.bat_ctrl())
        self.bat_ctrl_reactivate = self.event()

    def drive(self):
        while True:
            print('in_drive at ', self.now)
            # Drive for 20-40 min
            yield self.timeout(randint(20, 40))
            # Park for 1–6 hours
            print('Start parking at', self.now)
            self.bat_ctrl_reactivate.succeed()  # "reactivate"
            print('see bat_ctrl at ', self.now)
            self.bat_ctrl_reactivate = self.event()
            yield self.timeout(randint(60, 360))  # "parking deactivate after timeout"
            print('Stop parking at', self.now)
            print('out of drive at ', self.now)

    def bat_ctrl(self):
        while True:
            print('in bat at ', self.now)
            print('Bat. ctrl. passivating at', self.now)
            yield self.bat_ctrl_reactivate  # "passivate"
            print('Bat. ctrl. reactivated at', self.now)
            # Intelligent charging behavior here …
            yield self.timeout(randint(30, 90))
            print('out of bat at ', self.now)


def test_car_env():
    car_env = Env()
    car_env.run(until=310)

if __name__ == '__main__':

    test_car_env()
