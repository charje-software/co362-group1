import React from "react";
import {
  AccountData,
  ContractData,
} from "@drizzle/react-components";

import logo from "./logo.png";

export default ({ accounts }) => (
  <div className="App">
    <div>
      <img src={logo} alt="drizzle-logo" />
      <h1>CHARJE</h1>
      <p>Monetizing data from IOT devices using blockchain and ML.</p>
    </div>

    <div className="section">
      <h2>Active Account</h2>
      <AccountData accountIndex={0} units="ether" precision={3} />
    </div>

    <div className="section">
      <h2>Prediction Market</h2>
      <p>
        <strong>Contract Balance (Wei): </strong>
        <ContractData contract="PredictionMarket" method="totalBets" />
      </p>
    </div>
  </div>
);
