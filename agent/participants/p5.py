import pandas as pd
import sys

from agents.lstm_multi_agent import LstmMultiAgent
from agents.random_agent_controller import RandomAgentController

if __name__ == "__main__":
    household_2_normalise_values = [1.16123236e+03, 4.24041018e+02, 2.47572234e-01, 2.41049693e-01]
    controller = RandomAgentController(LstmMultiAgent(
            account='0x80Fb53cb93F0e23b7698E6475498d3395806B2c9',
            model_file_name='./models/LSTMmultivariate.h5',
            household_name='MAC000002',
            normalise_values=household_2_normalise_values))
    if len(sys.argv) == 3:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        controller.run(start_time=pd.to_datetime(sys.argv[1]),
                       end_time=pd.to_datetime(sys.argv[2]),
                       time_delta=pd.Timedelta(sys.argv[3]))
