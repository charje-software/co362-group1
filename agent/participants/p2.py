import pandas as pd
import sys

from agents.ar_retrain_agent import ArRetrainAgent
from agents.random_agent_controller import RandomAgentController

if __name__ == "__main__":
    controller = RandomAgentController(ArRetrainAgent(
            '0x4B516E6c8c3a5Ea97Ff7377d81Ea2238C46C5882'))
    if len(sys.argv) == 3:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]),
                       time_delta=pd.Timedelta(sys.argv[3]))
