
# -*- coding: cp1252 -*-

import simpy
import random



"""def source_CPU(env, number, interval, counter):
    for i in range(number):
        p = Proceso(env, 'Proceso%02d' % i, counter, time_in_bank=12.0)
        env.process(p)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def resource_CPU(env, resource):
     with resource.request() as req:  # Generate a request event
         yield req                    # Wait for access
         yield env.timeout(1)         # Do something


def Proceso(env, name, counter, time_in_bank):
    #Customer arrives, is served and leaves.
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))"""

memoria_proceso = random.randint(1,10)
cantidad_instrucciones = random.randint(1,10)

INTERVAL_PROCESSES = 10
RANDOM_SEED = 10
MIN_INSTRUCCIONS = 3

CAPACIDAD_CPU = 1
MEMORIA_RAM = 100

class System:
    def __init__(self, env, capacidadCPU, memoriaRAM):
        self.CPU = simpy.Resource(env, capacity=capacidadCPU)
        self.RAM = simpy.Container(env, init=memoriaRAM, capacity=memoriaRAM)
        #self.mon_ram = env.process(self.monitor_memory(env))

    """def monitor_memory(self, env):
        while True:
            if self.RAM.level < 100:
                print('Calling tanker at %s' % env.now)
                env.process(tanker(env, self))
            yield env.timeout(15)
    def monitor_cpu(self,env):"""

def tanker(env, gas_station):
     yield env.timeout(10)  # Need 10 Minutes to arrive
     print('Tanker arriving at %s' % env.now)
     amount = gas_station.gas_tank.capacity - gas_station.gas_tank.level
     yield gas_station.gas_tank.put(amount)
        
    
def Proceso(name,env,System):
     print('Proceso %s arriving at %s' % (name, env.now))
     with System.RAM.request() as req:
         mem = memoria_proceso
         if System.RAM.level < mem:
            print('No hay suficiente memoria para el proceso %' % (env.now, name, wait))
         else:
             yield req
             print('Proceso %s presta memoria RAM %f' % (name, env.now))
             yield System.RAM.get(mem)
             yield env.timeout(5)
             print('Proceso %s ha prestado %s memoria %s' % (name, mem,env.now))


def proceso_generator(env, System):
     for i in range(4):
         env.process(Proceso(i, env, System))
         yield env.timeout(5)


env = simpy.Environment() #ambiente de la simulacion
system = System(env,CAPACIDAD_CPU,MEMORIA_RAM)
proceso_gen = env.process(proceso_generator(env , System))
env.run()
