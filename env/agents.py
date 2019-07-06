# Author: Teshan Liyanage <teshanl@zone24x7.com>

import random

from mesa import Agent


class SecurityAgent(Agent):
    def __init__(self, pos, model, guard_id, moore=True, active=False, follow_time=2):
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore
        self.saw_thief = False
        self.guard_id = guard_id
        self.active = active
        self.following_time = 0
        self.follow_timeout = follow_time
        self.follow_gate = None

    def step(self):
        if self.model.if_thief_found() and self.active:
            self.following_time = self.follow_timeout
            self.follow_gate = self.model.schedule.thief_escape_gate()

        if self.following_time != 0:
            self.move_to_gate(self.follow_gate)
            self.following_time -= 1
        else:
            self.random_move()

        neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)

        if self.saw_thief:
            self.saw_thief = False

        for neighbour in neighbours:
            if isinstance(neighbour, ThiefAgent) and neighbour.status != "FREE":
                print("Guard {} found the thief moving to gate {}".format(self.guard_id, neighbour.direction))
                self.model.thief_found(neighbour.direction)
                self.saw_thief = True

    def random_move(self):
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def move_to_gate(self, gate):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        closest_move = self.closest_move_to_gate(next_moves, gate)
        self.model.grid.move_agent(self, closest_move)

    def closest_move_to_gate(self, moves, gate):
        dist = 10000
        closest_move = None
        for move in moves:
            if self.dist(move, gate.pos) < dist:
                dist = self.dist(move, gate.pos)
                closest_move = move
        return closest_move

    def dist(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5


class GateAgent(Agent):
    def __init__(self, pos, model, gate_id):
        super().__init__(pos, model)
        self.gate_id = gate_id
        self.gate_open = True
        self.pos = pos

    def step(self):
        if self.model.thief_found:
            for agent in self.model.schedule.agents:
                if isinstance(agent, ThiefAgent) and self.model.thief_gate_ == self.gate_id and self.gate_open:
                    print("Gate {}: Closing".format(self.gate_id))
                    self.gate_open = False
                    break


class ThiefAgent(Agent):
    def __init__(self, pos, model, moore=True):
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore
        self.direction = None
        self.status = "FLEEING"
        self.closest_gate_dist = 0.

    def step(self):
        gates = [agent for agent in self.model.schedule.agents if isinstance(agent, GateAgent) and agent.gate_open]
        if not gates and self.status != "CAUGHT":
            self.status = "CAUGHT"
            print("THIEF IS CAUGHT")
        elif self.status == "FLEEING":
            if self.linear_move(gates):
                self.status = "FREE"
                print("THIEF IS FREE")

    def linear_move(self, gates):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        closest_gate = self.closest_gate(gates)
        self.direction = closest_gate.gate_id

        closest_move = self.closest_move_to_gate(next_moves, closest_gate)
        self.model.grid.move_agent(self, closest_move)

        return closest_move == closest_gate.pos

    def closest_gate(self, gates):
        dist = 10000
        closest_gate = None
        for gate in gates:
            if self.dist(self.pos, gate.pos) < dist:
                dist = self.dist(self.pos, gate.pos)
                closest_gate = gate
        return closest_gate

    def dist(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5

    def closest_move_to_gate(self, moves, gate):
        dist = 10000
        closest_move = None
        for move in moves:
            if self.dist(move, gate.pos) < dist:
                dist = self.dist(move, gate.pos)
                closest_move = move
        self.closest_gate_dist = dist
        return closest_move
