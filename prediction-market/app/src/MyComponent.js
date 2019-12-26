import React, { Component } from "react";
import {
  AccountData,
  ContractData,
} from "@drizzle/react-components";
import PropTypes from 'prop-types'
import AgentBets from './components/AgentBets';
import PredictionGraph from './components/PredictionGraph';
import MakeBetModal from './components/MakeBetModal';
import UpdateConsumptionModal from './components/UpdateConsumptionModal';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import "./App.css";

class MyComponent extends Component {
  constructor(props, context) {
    super(props);
    this.methods = context.drizzle.contracts.PredictionMarket.methods;
    this.isOwnerDataKey = this.methods["isOwner"].cacheCall({from: this.props.accounts[0]});
    this.ownerDataKey = this.methods["owner"].cacheCall();
    this.isOwner = false;
  }

  renderPredictionMarketOptions() {
    if (this.isOwner) {
      return (
        <div>
        <UpdateConsumptionModal predictionMarket = {this.props.PredictionMarket} />
        </div>
      )
    } else {
      return (
        <div>
        <MakeBetModal />
        </div>
      )
    }
  }

  renderBetHistory() {
    if (!this.isOwner) {
      return (
        <Box boxShadow={1} className="section" style={roundedContainerStyle}>
          <h2>Bet History</h2>
          <AgentBets PredictionMarket = {this.props.PredictionMarket} accounts = {this.props.accounts} />
        </Box>
      );
    }
  }

  render() {
    if (!(this.isOwnerDataKey in this.props.PredictionMarket.isOwner)) {
      return (
        <div style={{padding: 20, justifyContent: 'center', display: 'flex'}}>
          <CircularProgress size={300}/>
        </div>
      );
    }
    this.isOwner = this.props.PredictionMarket.isOwner[this.isOwnerDataKey].value;

    return (
      <div style={{padding: 20, alignContent: 'center'}}>
        <PredictionGraph predictionMarket={this.props.PredictionMarket} isOwner={this.isOwner}  />

        <Box boxShadow={1} className="section" style={roundedContainerStyle}>
          <h2>Active Account</h2>
          <AccountData accountIndex={0} units="ether" precision={3} />
        </Box>
        {this.renderBetHistory()}
        <Box boxShadow={1} className="section" style={roundedContainerStyle}>
          <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
            <h2>Prediction Market</h2>
            {this.renderPredictionMarketOptions()}
          </div>
          <p>
            <strong>Top tier threshold: </strong>
            <ContractData contract="PredictionMarket" method="TOP_TIER_THRESHOLD" />
          </p>
          <p>
            <strong>Mid tier threshold: </strong>
            <ContractData contract="PredictionMarket" method="MID_TIER_THRESHOLD" />
          </p>
        </Box>
      </div>
    )
  }
}

const roundedContainerStyle = {
  borderRadius: '12px',
  paddingTop: 7,
  paddingBottom: 7,
  paddingLeft: 15,
  paddingRight: 15,
  backgroundColor: '#f6f6f6'
};

MyComponent.contextTypes = {
  drizzle: PropTypes.object,
};

export default MyComponent;
