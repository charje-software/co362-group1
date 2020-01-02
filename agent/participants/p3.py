import pandas as pd
import sys

from agents.ar_retrain_decision_agent import ArRetrainDecisionAgent
from agents.random_agent_controller import RandomAgentController

if __name__ == "__main__":
    controller = RandomAgentController(ArRetrainDecisionAgent(
            '0x768848539fc4AA09435797773456d114ea83bcE1'))
    if len(sys.argv) == 3:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]),
                       time_delta=pd.Timedelta(sys.argv[3]))
