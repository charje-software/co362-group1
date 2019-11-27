import React from "react";
import {
  AccountData,
  ContractData,
} from "@drizzle/react-components";
import AgentBets from './components/AgentBets';
import PredictionGraph from './components/PredictionGraph';
import MakeBetModal from './components/MakeBetModal';
import Box from '@material-ui/core/Box';
import "./App.css";

export default ({ accounts, PredictionMarket }) => (
  <div style={{padding: 20, alignContent: 'center'}}>
    <PredictionGraph predictionMarket={PredictionMarket} />

    <Box boxShadow={1} className="section" style={roundedContainerStyle}>
      <h2>Active Account</h2>
      <AccountData accountIndex={0} units="ether" precision={3} />
    </Box>

    <Box boxShadow={1} className="section" style={roundedContainerStyle}>
      <h2>Bet History</h2>
      <AgentBets PredictionMarket = {PredictionMarket} accounts = {accounts} />
    </Box>

    <Box boxShadow={1} className="section" style={roundedContainerStyle}>
      <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
        <h2>Prediction Market</h2>
        <MakeBetModal />
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
);

const roundedContainerStyle = {
  borderRadius: '12px',
  paddingTop: 7,
  paddingBottom: 7,
  paddingLeft: 15,
  paddingRight: 15,
  backgroundColor: '#f6f6f6'
};
