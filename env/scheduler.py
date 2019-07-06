# Author: Teshan Liyanage <teshanl@zone24x7.com>

from mesa.time import RandomActivation

from env.agents import ThiefAgent, GateAgent


class MallActivation(RandomActivation):
    def __init__(self, model):
        super().__init__(model)

    def get_thief_escape_dist(self):
        thief = self.get_agent_of_type(ThiefAgent)
        assert len(thief) == 1, "Thief not found by scheduler"
        return thief[0].closest_gate_dist

    def thief_escape_gate(self):
        thief = self.get_agent_of_type(ThiefAgent)
        assert len(thief) == 1, "Thief not found by scheduler"
        gates = self.get_agent_of_type(GateAgent)
        for gate in gates:
            if gate.gate_id == thief[0].direction:
                return gate

    @property
    def thief_fleeing(self):
        thief = self.get_agent_of_type(ThiefAgent)
        assert len(thief) == 1, "Thief not found by scheduler"
        return thief[0].status == "FLEEING"

    def get_agent_of_type(self, agent_type):
        return [agent for agent in self.agents if isinstance(agent, agent_type)]
