# -*- coding: utf8 -*-

from simpy import Environment


def fab(max_f):
    n, a, b = 0, 0, 1
    while n < max_f:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


def gene_simpy(env_gen, num):
    print('enter ')
    for i in range(num):
        env_gen.process(simpy_test(env_gen, i))
        yield env_gen.timeout(5)


def simpy_test(env_sim_test, num):
    print('sim of %s begin at %s' % (num, env_sim_test.now))
    yield env_sim_test.timeout(10)
    print('sim of %s end at %s' % (num, env_sim_test.now))


if __name__ == '__main__':
    env = Environment()
    sim_gen = env.process(gene_simpy(env, 5))
    env.run(50)
