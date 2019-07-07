# Author: Teshan Liyanage <teshanl@zone24x7.com>

from env.server import ModularServer, canvas_element, chart_element
from env.model import MallModel

if __name__ == "__main__":
    params = dict(num_security=12,
                  num_gates=5,
                  active_guards=True,
                  guard_follow_time=1)
    server = ModularServer(MallModel, [canvas_element, chart_element],
                           "Finding The Thief", model_params=params)
    server.launch()
