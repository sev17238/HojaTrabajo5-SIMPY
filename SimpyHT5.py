# -*- coding: cp1252 -*-
#Algoritmos y Estructuras de Datos
#Josue Lopez - 17081
#Diego Sevilla - -17238
#Fecha: 2/03/18
#Este programa simula la ejecucion de procesos en un sistema operativo

import random
import simpy
import math

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


def Process(env, name, counter, time_in_bank):
    #Customer arrives, is served and leaves.
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive"""
operation_time = 1
processes_time = []

cpu_speed = 1

INTERVAL_PROCESSES = 1
CPU_INSTRUCCIONS = 3

#CAPACIDAD_CPU = 1
MEMORIA_RAM = 100

NUM_OF_PROCESSES = 10
NUM_CPUS = 1

class System:
    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity=NUM_CPUS)
        self.RAM = simpy.Container(env, init=MEMORIA_RAM, capacity=MEMORIA_RAM)
        #self.mon_ram = env.process(self.monitor_memory(env))

    """def monitor_memory(self, env):
        while True:
            if self.RAM.level < 100:
                print('Calling tanker at %s' % env.now)
                env.process(CPUprocesses(env, self))
            yield env.timeout(15)
    def monitor_cpu(self,env):"""


def process_gen(env,system):
    iterator=0
    while(iterator<NUM_OF_PROCESSES):
        Process(env,"Process "+str(iterator), iterator, system)
        yield env.timeout( random.expovariate(1.0/INTERVAL_PROCESSES))  # Tiempo que tardara en crearse cada proceso
        iterator=iterator+1


class Process:
    
    def __init__(self,env,name,num,system): #constructor del proceso
        process_memory = random.randint(1,10)
        num_instructions = random.randint(1,10)
        self.createTime = 0
        self.env = env
        self.name = name
        self.instructions = num_instructions;
        self.requiredMemory = process_memory;
        self.num = num
        self.system = system
        self.PROCESS = env.process(self.processing(env,system))
        self.TERMINATED = False        
        self.TOTALTime = 0


    def processing(self,env,system): #Funcion que define el procesamiento

        self.createTime = env.now
        print(str(self.name) + ": Created at " + str(env.now))
    
        with (system.RAM.get(self.requiredMemory)) as ram:
            yield ram


            print(str(self.name)+": State=WAIT, gets RAM at "+str(env.now))
            Next = 0
            while(self.TERMINATED==False):
                with (system.CPU.request()) as req:
                    print(str(self.name)+": State=WAIT, wait for the CPU at "+str(env.now))
                    yield req

                    print(str(self.name)+": State=RUNNING, gets CPU at "+str(env.now))
                    
                    iterator=0
                    while(iterator<CPU_INSTRUCCIONS):
                        if (self.instructions > 0):
                            self.instructions = self.instructions - 1
                            waiting_or_ready = random.randint(1,2)
                            Next = waiting_or_ready  
                        iterator=iterator+1
                        
                    yield env.timeout(cpu_speed) 

                    if(self.instructions==0):
                        self.TERMINATED=True

                    if(Next==1):
                        print(str(self.name)+": State=I/O Operation, wait for I/O operation at "+str(env.now))
                        yield env.timeout(operation_time)
                
            print(str(self.name)+": State=Terminated, finished at "+str(env.now))
            system.RAM.put(self.requiredMemory)  # Regresa la RAM que se utilizo

        self.totalTime = int(env.now - self.createTime)
        processes_time.insert(self.num, self.totalTime)


random.seed(15)
env = simpy.Environment() #ambiente de la simulacion
system = System(env)
env.process(process_gen(env,system))
env.run()


def average(s): return sum(s) * 1.0 / len(s)
totaltime_variance = map(lambda x: (x - average(processes_time)) ** 2, processes_time)
totaltime_standardev = math.sqrt(average(totaltime_variance)) 

print "The average time that each process is on the computer is: ", average(processes_time), ", and its standar deviation is: ", \
      totaltime_standardev



