# Author: Teshan Liyanage <teshanl@zone24x7.com>

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from env.agents import SecurityAgent, GateAgent, ThiefAgent
from env.model import MallModel

GATE_OPEN_COLOR = "Green"
GATE_CLOSE_COLOR = "Red"
GUARD_COLOR = "SlateBlue"
THIEF_COLOR = "Orange"

def mall_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if type(agent) is GateAgent:
        portrayal["Color"] = GATE_OPEN_COLOR if agent.gate_open else GATE_CLOSE_COLOR
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = agent.gate_id
        portrayal["text_color"] = "White"

    elif type(agent) is SecurityAgent:
        portrayal["Color"] = GUARD_COLOR if not agent.saw_thief else "Red"
        portrayal["r"] = 0.6
        portrayal["Layer"] = 2
        portrayal["text"] = agent.guard_id
        portrayal["text_color"] = "Black"

    elif type(agent) is ThiefAgent:
        portrayal["Color"] = THIEF_COLOR
        portrayal["Layer"] = 0
        portrayal["r"] = 0.8

        if agent.direction is not None:
            portrayal["text"] = agent.direction
            portrayal["text_color"] = "Black"

    return portrayal


canvas_element = CanvasGrid(mall_portrayal, 20, 20, 500, 500)

chart_element = ChartModule([{"Label":"Escape Distance", "Color": "#AA0000"}])


