import React from "react";
import Box from '@material-ui/core/Box';
import '../index.css';

export default class About extends React.Component {

  renderBettingCycle() {
    return (
      <div>
        <h3 style={titleStyle}>One betting cycle explained.</h3>
        <div className="section" style={{justifyContent: 'center'}}>
          <div style={stepCardRowStyle}>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>1 Betting</p>
              <p>
                Predict the energy prices of the next day. You must predict for 48 data points
                throughout the day.
              </p>
            </div>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>2 Waiting</p>
              <p>
                Wait for the oracle to feed in the true energy consumption for the next day.
              </p>
            </div>
          </div>
          <div style={stepCardRowStyle}>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>3 Ranking</p>
              <p>
                Rank your bet to see if you win anything or not.
              </p>
            </div>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>4 Claiming</p>
              <p>
                If you've won, collect your winnings!
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div>
        <h1 style={titleStyle}>Monetising IOT device data using blockchain and ML.</h1>
        <Box boxShadow={1} className="section" style={roundedContainerStyle}>
          <p>
            This prediction market system monetizes data that is collected 
            from IoT devices. The IoT devices are usually deployed with an 
            agent that has access to streams of sensor data and a machine 
            learning framework for training prediction algorithms. 
            The monetization of the algorithms occurs via this prediction 
            market which is implemented as a smart contract.
          </p>
          <p>
            The wholesale energy price is fed into the blockchain 
            through an oracle and recorded in a smart contract. 
            The energy supplier would like to predict the demand the 
            following day and specifies a prediction market to try to 
            estimate it. Agents can interact with the smart contract 
            and have access to their household's private data, which 
            they can use to predict the energy demand for the following 
            day. They make gains for accurately predicting future energy 
            consumption, incentivising them to improve their prediction 
            algorithms.
          </p>
        </Box>
        {this.renderBettingCycle()}
      </div>
    );
  }
}

const roundedContainerStyle = {
  borderRadius: '12px', 
  padding: 25,
  paddingLeft: 35,
  paddingRight: 35,
  backgroundColor: '#f6f6f6',
  marginBottom: 30,
};

const titleStyle = {
  justifyContent: 'center',
  fontFamily: 'Raleway',
  display: 'flex',
  fontSize: '40px',
  paddingTop: 70,
  paddintBottom: 70,
};

const stepCardRowStyle = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between'
};

const stepTitleStyle = {
  fontFamily: 'Raleway',
  display: 'flex',
  fontSize: '35px',
  marginBottom: 50,
};

const stepCardStyle = {
  borderRadius: '12px', 
  paddingLeft: 35,
  paddingRight: 35,
  marginBottom: 30,
  borderWidth: '3px',
  borderStyle: 'solid',
  borderColor: 'black',
  height: '280px',
  width: '280px',
};
