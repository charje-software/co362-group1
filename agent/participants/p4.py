import pandas as pd
import sys

from agents.lstm_agent import LstmAgent
from agents.random_agent_controller import RandomAgentController

if __name__ == "__main__":
    controller = RandomAgentController(LstmAgent(
            '0xfcC640fB2629943aaaA35c4D0A79000e0bfc8870'))
    if len(sys.argv) == 3:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]),
                       time_delta=pd.Timedelta(sys.argv[3]))
