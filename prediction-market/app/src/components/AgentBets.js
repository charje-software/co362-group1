import React, { Component } from 'react'
import PropTypes from 'prop-types'
import CircularProgress from '@material-ui/core/CircularProgress';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

class AgentBets extends Component {
  constructor(props, context) {
    super(props);
    this.contracts = context.drizzle.contracts;
    this.methods = this.contracts.PredictionMarket.methods;
    this.betPredictionsDataKey = this.methods["getBetPredictionsForAgent"].cacheCall({from: this.props.accounts[0]});
    this.betAmountsDataKey = this.methods["getBetAmountsForAgent"].cacheCall({from: this.props.accounts[0]});
    this.betWinningScalesDataKey = this.methods["getBetWinningScalesForAgent"].cacheCall({from: this.props.accounts[0]});
    this.betTimestampsDataKey = this.methods["getBetTimestampsForAgent"].cacheCall({from: this.props.accounts[0]});
  }

  hasFetchedData() {
    const pm = this.props.PredictionMarket;
    if((this.betPredictionsDataKey in pm.getBetPredictionsForAgent)
    && (this.betAmountsDataKey in pm.getBetAmountsForAgent)
      && (this.betWinningScalesDataKey in pm.getBetWinningScalesForAgent)
      && (this.betTimestampsDataKey in pm.getBetTimestampsForAgent)) {
      return true
    }
    return false;
  }

  processRowData(betPredictions, betAmounts, betWinningScales, betTimestamps) {
    let rows = [];
    for (let i = 0; i < 7; i++) {
      // Check timestamp !== 0 to see if bet exists for that period
      if (betTimestamps[i] !==  '0') {
        let betStatus = 'RANK CATEGORY ' + betWinningScales[i];
        if (i === 0) betStatus = 'BETTING';
        if (i === 1) betStatus = 'WAITING';
        if (i === 2) betStatus = 'CLAIMING';
        rows.push([new Date(betTimestamps[i] * 1000).toUTCString(),
                     betAmounts[i] / (10 ** 18),
                     betPredictions[i],
                     betStatus,
        ]);
      }
    }
    return rows;
  }

  renderTableRows(rowData) {
    return (
      rowData.map(row => (
        <TableRow key={row[0]}>
          <TableCell style={tableTitle} component="th" scope="row">
            {row[0]}
          </TableCell>
          <TableCell>{row[1]}</TableCell>
          <TableCell>
            {row[2].join(", ")}
          </TableCell>
          <TableCell>{row[3]}</TableCell>
        </TableRow>
      ))
    )
  }

  render() {
    if(!this.hasFetchedData()) {
      return (
        <div style={{justifyContent: 'center', display: 'flex', paddingBottom: 40}}>
          <CircularProgress size={100}/>
        </div>
      )
    }

    const pm = this.props.PredictionMarket;
    const betPredictions = pm.getBetPredictionsForAgent[this.betPredictionsDataKey].value;
    const betAmounts = pm.getBetAmountsForAgent[this.betAmountsDataKey].value;
    const betWinningScales = pm.getBetWinningScalesForAgent[this.betWinningScalesDataKey].value;
    const betTimestamps = pm.getBetTimestampsForAgent[this.betTimestampsDataKey].value;
    const rowData = this.processRowData(betPredictions, betAmounts, betWinningScales, betTimestamps);

    if (rowData.length === 0) {
      return (
        <div style = {{paddingBottom: 20}}>
          <em>You have not placed any bets over the last 7 days.</em>
        </div>
      )
    }

    return (
      <div>
        <Table aria-label="simple table" style={{width: '100%'}}>
          <TableHead>
            <TableRow>
              <TableCell style={tableTitle}>Timestamp</TableCell>
              <TableCell style={tableTitle}>Amount Bet (Ether)</TableCell>
              <TableCell style={tableTitle}>Predictions (kWh)</TableCell>
              <TableCell style={tableTitle}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {this.renderTableRows(rowData)}
          </TableBody>
        </Table>
      </div>
    )
  }
}

const tableTitle = {
  fontWeight: 900,
  fontFamily: 'Poppins',
};

AgentBets.contextTypes = {
  drizzle: PropTypes.object,
};
export default AgentBets
