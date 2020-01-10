import React, { Component } from 'react'
import PropTypes from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';
import ClaimingIcon from '@material-ui/icons/MonetizationOn';
import Fab from '@material-ui/core/Fab';
import RankingIcon from '@material-ui/icons/BarChart';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Tooltip from '@material-ui/core/Tooltip';

class AgentBets extends Component {
  constructor(props, context) {
    super(props);
    this.contracts = context.drizzle.contracts;
    this.methods = this.contracts.PredictionMarket.methods;
    this.account = this.props.accounts[0];
    this.betPredictionsDataKey = this.methods["getBetPredictionsForAgent"].cacheCall({from: this.account});
    this.betAmountsDataKey = this.methods["getBetAmountsForAgent"].cacheCall({from: this.account});
    this.betWinningScalesDataKey = this.methods["getBetWinningScalesForAgent"].cacheCall({from: this.account});
    this.betTimestampsDataKey = this.methods["getBetTimestampsForAgent"].cacheCall({from: this.account});
    this.canClaimDataKey = this.methods["canClaim"].cacheCall(this.account);
    this.canRankDataKey = this.methods["canRank"].cacheCall(this.account);
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

  // Gradient component used for the icons in the buttons
  svgGradient = svgProps => {
    return (
      <svg {...svgProps}>
        <defs>
          <linearGradient id="gradient1">
            <stop offset="30%" stopColor="#d91a1a" />
            <stop offset="70%" stopColor="#4e036e" />
          </linearGradient>
        </defs>
        {React.cloneElement(svgProps.children[0], {
          fill: 'url(#gradient1)',
        })}
      </svg>
    );
  }

  onClickClaim = async () => {
    await this.methods["claimWinnings"].cacheSend();
  }

  onClickRank = async () => {
    await this.methods["rank"].cacheSend();
  }

  renderRankingStageOptions() {
    var button;

    if (this.canRankDataKey in this.props.PredictionMarket.canRank) {
      if (this.props.PredictionMarket.canRank[this.canRankDataKey].value) {
        button = (
          <Tooltip title="Rank Bet">
            <Fab size="small" onClick={this.onClickRank} style={fabStyle}>
              <RankingIcon style={iconStyle} component={this.svgGradient} />
            </Fab>
          </Tooltip>
        )
      } else if (this.canClaimDataKey in this.props.PredictionMarket.canClaim) {
        console.log(this.props.PredictionMarket.canClaim[this.canClaimDataKey].value);
        if (this.props.PredictionMarket.canClaim[this.canClaimDataKey].value) {
          button = (
            <Tooltip title="Claim Winnings">
              <Fab size="small" onClick={this.onClickClaim} style={fabStyle}>
                <ClaimingIcon style={iconStyle} component={this.svgGradient} />
              </Fab>
            </Tooltip>
          )
        }
      }
    }
    return (
      <div style={{display: 'flex', alignItems: 'center'}}>
        <div style={{color: 'purple', fontWeight: 'bold'}}>RANKING</div>
        {button}
      </div>
    )
  }

  processRowData(betPredictions, betAmounts, betWinningScales, betTimestamps) {
    let rows = [];
    for (let i = 0; i < 7; i++) {
      // Check timestamp !== 0 to see if bet exists for that period
      if (betTimestamps[i] !==  '0') {
        let betStatus = <div style={{color: 'green', fontWeight: 'bold'}}>{'WON - CATEGORY ' + betWinningScales[i]}</div>;
        if (betWinningScales[i] === '0') betStatus = <div style={{color: 'red', fontWeight: 'bold'}}>LOST</div>;
        if (i === 0) betStatus = <div style={{color: 'blue', fontWeight: 'bold'}}>BETTING</div>;
        if (i === 1) betStatus = <div style={{color: 'navy', fontWeight: 'bold'}}>WAITING</div>;
        if (i === 2) betStatus = this.renderRankingStageOptions();
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
    var rowData = []
    if (betTimestamps !== null) {
      rowData = this.processRowData(betPredictions, betAmounts, betWinningScales, betTimestamps);
    }
    // const rowData = this.processRowData(betPredictions, betAmounts, betWinningScales, betTimestamps);

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

const fabStyle = {
  margin: 10,
  width: 35,
  height: 35,
  backgroundColor: 'white',
};

const iconStyle = {
  width: 20,
  height: 20,
}

AgentBets.contextTypes = {
  drizzle: PropTypes.object,
};

export default AgentBets
