import React from "react";
import PropTypes from 'prop-types';
import {VictoryChart, VictoryGroup, VictoryVoronoiContainer,
        VictoryScatter, VictoryAxis, VictoryLine, VictoryLegend} from 'victory';
import Fab from '@material-ui/core/Fab';
import CircularProgress from '@material-ui/core/CircularProgress';

const TIME_MARKERS = ["Tomorrow", "Today", "Yesterday", "2 Days Before",
                     "3 Days Before", "4 Days Before", "5 Days Before"];

class PredictionGraph extends React.Component {

    constructor(props, context) {
      super(props);
      this.oracleDataKeys = [];
      this.agentPredictionDataKeys = [];
      this.averagePredictionDataKeys = [];
      for (let i = 0; i < 7; i++) {
        this.oracleDataKeys.push(
          context.drizzle.contracts.PredictionMarket.methods["getOracleConsumptions"].cacheCall(i)
        );
        if (props.isOwner) {
          this.averagePredictionDataKeys.push(
            context.drizzle.contracts.PredictionMarket.methods["getAveragePredictions"].cacheCall(i)
          );
        } else {
          this.agentPredictionDataKeys.push(
            context.drizzle.contracts.PredictionMarket.methods["getPredictions"].cacheCall(i)
          );
        }
      }
      this.state = {currentDay: 1};
    }

    hasFetchedData() {
      for (let i = 0; i < 7; i++) {
        const oracleDataKey = this.oracleDataKeys[i];
        const agentPredictionKey = this.agentPredictionDataKeys[i];
        const averagePredictionKey = this.averagePredictionDataKeys[i];
        const pm = this.props.predictionMarket;
        if (!(oracleDataKey in pm.getOracleConsumptions) &&
            !(agentPredictionKey in pm.getPredictions) &&
            !(averagePredictionKey in pm.getAveragePredictions)) {
          return false;
        }
      }
      return true;
    }

    renderGraphFooter() {
      return (
        <div
          style={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-around',
            alignItems: 'center',
            borderRadius: 35,
            background: 'linear-gradient(to right bottom, #2d1896, #0d2ca8)',
            padding: 10,
        }}>
          <Fab
            variant="extended"
            size="medium"
            color="primary"
            aria-label="add"
            onClick={() => void this.setState({currentDay: this.state.currentDay + 1})}
            disabled={this.state.currentDay === 6}
          >
            BACK
          </Fab>
          <p style={{color: 'white'}}>{TIME_MARKERS[this.state.currentDay]}</p>
          <Fab
            variant="extended"
            size="medium"
            color="primary"
            aria-label="add"
            onClick={() => void this.setState({currentDay: this.state.currentDay - 1})}
            disabled={this.state.currentDay === 0}
          >
            NEXT
          </Fab>
        </div>
      );
    }

    renderOraclePrices(data) {
      return (
        <VictoryGroup data={data} style={{ data: { fill: '#a10d2d' }}}>
          <VictoryAxis dependentAxis fixLabelOverlap />
          <VictoryAxis crossAxis fixLabelOverlap
            label="Time"
            tickValues={[4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]}
            tickFormat={this.periodToTime}
          />
          <VictoryLine name='oracle'/>
          <VictoryScatter style={{ data: { fill: '#a10d2d' }}}/>
        </VictoryGroup>
      );
    }

    renderAgentPredictions(data) {
      if (!this.props.isOwner) {
        return (
          <VictoryGroup data={data} style={scatterStyle}>
            <VictoryLine name='agentPredictions'/>
            <VictoryScatter style={scatterStyle}/>
          </VictoryGroup>
        );
      }
    }

    renderAveragePredictions(data) {
      if (this.props.isOwner) {
        return (
          <VictoryGroup data={data} style={{ data: { fill: '#4e036e' }}}>
            <VictoryLine name='averagePredictions'/>
            <VictoryScatter style={scatterStyle}/>
          </VictoryGroup>
        )
      }
    }

    render() {
        if (!this.hasFetchedData()) {
          return (
            <div style={{justifyContent: 'center', display: 'flex', paddingTop: 30}}>
              <CircularProgress size={150}/>
            </div>
          );
        }

        const day = this.state.currentDay;
        const pm = this.props.predictionMarket;

        const oracleDataKey = this.oracleDataKeys[day];
        var oracleData = this.formatData(pm.getOracleConsumptions[oracleDataKey].value);

        const agentPredictionKey = this.agentPredictionDataKeys[day];
        const averagePredictionKey = this.averagePredictionDataKeys[day];
        var agentPredictionData = [];
        var averagePredictionData = [];
        var graphLineLabels = [];
        if (this.props.isOwner) {
          graphLineLabels = [{name: "Real Consumption"}, {name: "Average Prediction"}]
          averagePredictionData = this.formatData(pm.getAveragePredictions[averagePredictionKey].value);
        } else {
          graphLineLabels = [{name: "Real Consumption"}, {name: "Your Prediction"}];
          agentPredictionData = this.formatData(pm.getPredictions[agentPredictionKey].value);
        }

        return (
          <div className="section" style={{maxWidth: '720px'}}>
            <h1 style={{fontFamily: 'Poppins', display: 'flex', justifyContent: 'center'}}>
              Energy Consumption Data
            </h1>
            <div style={{borderRadius: '8px', backgroundColor: 'white'}}>
              <VictoryChart
                containerComponent={
                  <VictoryVoronoiContainer
                    labels={({ datum }) => `${this.periodToTime(datum.x)}, ${Math.round(datum.y, 2)}`}
                    voronoiBlacklist={['oracle']}
                  />
                }
                domain={{y: [0, 2500]}}
                animate={{
                  onExit: {duration: 400}
                }}
              >
                <VictoryLegend
                  orientation="horizontal"
                  colorScale={[ "#a10d2d", "navy"]}
                  data={graphLineLabels}
                />
                {this.renderOraclePrices(oracleData)}
                {this.renderAgentPredictions(agentPredictionData)}
                {this.renderAveragePredictions(averagePredictionData)}
              </VictoryChart>
            </div>
            {this.renderGraphFooter()}
          </div>
        );
    }

    formatData(data) {
      if (data === null) return;
      let formattedData = [];
      for (let i = 0; i < data.length; i++) {
        const y = parseInt(data[i]);
        if (y === 0) break;
        formattedData.push({x: i, y: y});
      }
      // VictoryChart data cannot take an empty array
      if (formattedData.length === 0) {
        formattedData.push({x: 0, y: 0});
      }
      return formattedData;
    }

    periodToTime = (period) => {
      const hour = Math.floor((period + 1) / 2);
      if ((period + 1) % 2 === 0) {
        return `${hour}:00`
      }
      return `${hour}:30`;
    }
}

const scatterStyle = {
  data: {
    fill: 'navy'
  }
};

PredictionGraph.contextTypes = {
  drizzle: PropTypes.object
}

export default PredictionGraph;
