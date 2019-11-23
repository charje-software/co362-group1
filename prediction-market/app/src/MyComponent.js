import React from "react";
import {
  AccountData,
  ContractData,
} from "@drizzle/react-components";
import PredictionGraph from './components/PredictionGraph';
import MakeBetModal from './components/MakeBetModal';
import Box from '@material-ui/core/Box';

export default ({ accounts, PredictionMarket }) => (
  <div>
    <div style={headerStyle}>
        <h1 style={{fontFamily: 'Poppins', color: 'white'}}>
          CHARJE
        </h1>
        <p style={{color: 'white'}}>
          Monetizing data from IOT devices using blockchain and ML.
        </p>
    </div>

    <div style={{padding: 20, alignContent: 'center'}}>
      <PredictionGraph predictionMarket={PredictionMarket} />
      
      <Box boxShadow={1} className="section" style={roundedContainerStyle}>
        <h2>Active Account</h2>
        <AccountData accountIndex={0} units="ether" precision={3} />
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
  </div>
);

const headerStyle = {
  display: 'flex', 
  flexDirection: 'row', 
  alignItems: 'center', 
  justifyContent: 'space-around', 
  background: 'linear-gradient(to right bottom, #4e036e, #d91a1a)',
  borderRadius: 0,
};

const roundedContainerStyle = {
  borderRadius: '12px', 
  paddingTop: 7, 
  paddingBottom: 7,
  paddingLeft: 15,
  backgroundColor: '#f6f6f6'
};
