# Author: Teshan Liyanage <teshanl@zone24x7.com>

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from env.agents import ThiefAgent, GateAgent, SecurityAgent
from env.scheduler import MallActivation


class MallModel(Model):
    def __init__(self,
                 height=20,
                 width=20,
                 num_security=15,
                 num_gates=5,
                 active_guards=False,
                 guard_follow_time=2):
        # Set parameters
        self.height = height
        self.width = width
        self.num_security = num_security
        self.num_gates = num_gates

        self.schedule = MallActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({"Escape Distance": lambda m: m.schedule.get_thief_escape_dist()})
        # {"Gates": lambda m: m.schedule.get_breed_count(GateAgent),
        #  "Guards": lambda m: m.schedule.get_breed_count(SecurityAgent)})
        self.thief_gate_ = None
        self.active_guards = active_guards
        self.guard_follow_time = guard_follow_time

        object_locs = [(self.width // 2, self.height // 2)]
        i = 0
        # for i in range(self.initial_security):
        while i < self.num_security:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) not in object_locs:
                object_locs.append((x, y))
                guard = SecurityAgent((x, y), self,
                                      guard_id=i,
                                      active=self.active_guards,
                                      follow_time=self.guard_follow_time)
                self.grid.place_agent(guard, (x, y))
                self.schedule.add(guard)
                i += 1

        i = 0
        while i < self.num_gates // 2:
            x = random.randrange(self.width)
            y = random.choice([0, self.height - 1])
            if (x, y) not in object_locs:
                object_locs.append((x, y))
                gate = GateAgent((x, y), self, gate_id=i)
                self.grid.place_agent(gate, (x, y))
                self.schedule.add(gate)
                i += 1
        while i < self.num_gates:
            x = random.choice([0, self.width - 1])
            y = random.randrange(self.height)
            if (x, y) not in object_locs:
                object_locs.append((x, y))
                gate = GateAgent((x, y), self, gate_id=i)
                self.grid.place_agent(gate, (x, y))
                self.schedule.add(gate)
                i += 1

        thief = ThiefAgent((self.width // 2, self.height // 2), self)

        self.grid.place_agent(thief, thief.pos)
        self.schedule.add(thief)

        self.running = True

    def step(self):
        if self.schedule.thief_fleeing:
            self.schedule.step()
            self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()
            # print("Step {}".format(i))

    def thief_found(self, direction):
        self.thief_gate_ = direction

    def if_thief_found(self):
        return self.thief_gate_ is not None
