import pandas as pd
import sys

from agents.ar_agent import ArAgent
from agents.random_agent_controller import RandomAgentController

if __name__ == "__main__":
    controller = RandomAgentController(ArAgent(
            '0xEA43d7cE5224683B1D83D19327699756504fB489'))
    if len(sys.argv) == 3:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]),
                       time_delta=pd.Timedelta(sys.argv[3]))
