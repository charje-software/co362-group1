import React from "react";
import PropTypes from 'prop-types';
import CheckCircle from '@material-ui/icons/CheckCircle';
import BettingIcon from '@material-ui/icons/Receipt';
import WaitingIcon from '@material-ui/icons/Timelapse';
import RankingIcon from '@material-ui/icons/BarChart';
import ClaimingIcon from '@material-ui/icons/MonetizationOn';
import BubbleIcon from '@material-ui/icons/BubbleChart';
import ComputerIcon from '@material-ui/icons/Computer';
import BulletPointIcon from '@material-ui/icons/Adjust';
import '../index.css';

export default class About extends React.Component {

  constructor(props, context) {
    super(props);
    this.pm = context.drizzle.contracts.PredictionMarket;
  }

  // Red gradient for betting cycle diagram
  stepIconGradient = svgProps => (
    <svg {...svgProps}>
      <defs>
        <linearGradient id="gradient2">
          <stop offset="30%" stopColor="#78036e" />
          <stop offset="70%" stopColor="#d91a1a" />
        </linearGradient>
      </defs>
      {React.cloneElement(svgProps.children[0], {
        fill: 'url(#gradient2)',
      })}
    </svg>
  );

  renderAgentInfo() {
    return (
      <div style={agentInfoStyle}>
        <h1 style={titleStyle}>
          {<ComputerIcon style={{fontSize: '100px', paddingRight: 15}} />}
          What do agents do?
        </h1>
        <h3 style={agentPointStyle}>
          {<BulletPointIcon style={agentIconStyle} />}
          Make monetary gains for accurately predicting future energy consumption
        </h3>
        <h3 style={agentPointStyle}>
          {<BulletPointIcon style={agentIconStyle} />}
          Develop advanced prediction algorithms or models to improve prediction
        </h3>
        <h3 style={agentPointStyle}>
          {<BulletPointIcon style={agentIconStyle} />}
          Help energy suppliers get a better prediction of energy consumption to improve demand/supply management
        </h3>
      </div>
    )
  }

  renderBettingCycle() {
    return (
      <div>
        <h3 style={titleStyle}>One betting cycle explained.</h3>
        <div style={bettingCycleStyle}>
          <h3>
            The prediction market is live at {this.pm.address}
          </h3>
          <CheckCircle 
            style={{paddingLeft: '5px', fontSize: '28px'}}
            component={svgProps => (
              <svg {...svgProps}>
                <defs>
                  <linearGradient id="gradient1">
                    <stop offset="30%" stopColor="#4beb76" />
                    <stop offset="70%" stopColor="#5bde80" />
                  </linearGradient>
                </defs>
                {React.cloneElement(svgProps.children[0], {
                  fill: 'url(#gradient1)',
                })}
              </svg>
            )} />
          </div>
          <div style={stepCardRowStyle}>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>
                {<BettingIcon style={stepIconStyle} component={this.stepIconGradient} />}
                Betting</p>
              <p>
                Predict the energy prices of the next day. You must predict for 48 data points
                throughout the day.
              </p>
            </div>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>
                {<WaitingIcon style={stepIconStyle} component={this.stepIconGradient} />}
                Waiting
              </p>
              <p>
                Wait for the oracle to feed in the true energy consumption for the next day.
              </p>
            </div>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>
                {<RankingIcon style={stepIconStyle} component={this.stepIconGradient} />} 
                Ranking
              </p>
              <p>
                Rank your bet to see if you fall into any winning category.
              </p>
            </div>
            <div style={stepCardStyle}>
              <p style={stepTitleStyle}>
                {<ClaimingIcon style={stepIconStyle} component={this.stepIconGradient} />}
                Claiming
              </p>
              <p>
                If you've won, collect your winnings! We have different winning thresholds 
                to award the best with more.
              </p>
            </div>
          </div>
        </div>
    );
  }

  renderIntro() {
    return (
      <div style={introStyle}>
        <h1 style={{...titleStyle, color: 'white', paddingLeft: 100}}>
          Monetising IOT device data using blockchain and ML.
        </h1>
        <BubbleIcon style={{...titleStyle, fontSize: '100px', color: 'white'}} />
        <h3 style={{color: 'white', paddingLeft: 260}}>
          This prediction market system monetizes data that is collected 
          from IoT devices. The IoT devices are usually deployed with an 
          agent that has access to streams of sensor data and a machine 
          learning framework for training prediction algorithms. The 
          monetisation of the individual's data occurs via this prediction 
          market which is implemented as a smart contract.
        </h3>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderIntro()}
        {this.renderBettingCycle()}
        {this.renderAgentInfo()}
      </div>
    );
  }
}

About.contextTypes = {
  drizzle: PropTypes.object
}

const titleStyle = {
  justifyContent: 'center',
  fontFamily: 'Raleway',
  display: 'flex',
  fontSize: '40px',
  alignItems: 'center',
};

const introStyle = {
  display: 'flex', 
  backgroundColor: 'black', 
  padding: 50, 
  alignItems: 'center'
}

const stepCardRowStyle = {
  paddingLeft: 100,
  paddingRight: 100,
  marginBottom: 80,
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

const stepIconStyle = {
  fontSize: '45px',
  paddingRight: '7px'
};

const stepCardStyle = {
  borderRadius: '12px', 
  paddingLeft: 30,
  paddingRight: 30,
  marginBottom: 30,
  borderWidth: '3px',
  borderStyle: 'solid',
  borderColor: 'black',
  height: '350px',
  width: '180px',
};

const bettingCycleStyle = {
  display: 'flex', 
  flexDirection: 'row', 
  alignItems: 'center', 
  marginBottom: 18, 
  justifyContent: 'center'
};

// Style for each point in 'What do agents do?'
const agentPointStyle = {
  display: 'flex', 
  alignItems: 'center', 
  paddingLeft: 80
};

// Style for bullet points
const agentIconStyle = {
  ...stepIconStyle,
  color: '#ad1868'
};

const agentInfoStyle =  {
  backgroundColor: '#e6e6e6', 
  display: 'flex', 
  flexDirection: 'column', 
  padding: 50
};
