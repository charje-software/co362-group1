import React from "react";
import PropTypes from 'prop-types';
import {VictoryChart, VictoryGroup, VictoryVoronoiContainer,
        VictoryScatter, VictoryAxis, VictoryLine, VictoryLegend} from 'victory';
import Fab from '@material-ui/core/Fab';
import CircularProgress from '@material-ui/core/CircularProgress';

const MONTH_NAMES = ["Tomorrow", "Today", "Yesterday", "2 Days Before", 
                     "3 Days Before", "4 Days Before", "5 Days Before"];

class PredictionGraph extends React.Component {

    constructor(props, context) {
      super(props);
      this.oracleDataKeys = [];
      this.agentPredictionDataKeys = [];
      for (let i = 0; i < 7; i++) {
        this.oracleDataKeys.push(
          context.drizzle.contracts.PredictionMarket.methods["getOracleConsumptions"].cacheCall(i)
        );
        this.agentPredictionDataKeys.push(
          context.drizzle.contracts.PredictionMarket.methods["getPredictions"].cacheCall(i)
        );
      }
      this.state = {currentDay: 1};
    }
    
    hasFetchedData() {
      for (let i = 0; i < 7; i++) {
        const oracleDataKey = this.oracleDataKeys[i];
        const agentPredictionKey = this.agentPredictionDataKeys[i];
        if (!(oracleDataKey in this.props.predictionMarket.getOracleConsumptions) ||
            !(agentPredictionKey in this.props.predictionMarket.getPredictions)) {
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
          <p style={{color: 'white'}}>{MONTH_NAMES[this.state.currentDay]}</p>
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
      return (
        <VictoryGroup data={data} style={{ data: { fill: 'navy' }}}>
          <VictoryLine name='agentPredictions'/>
          <VictoryScatter style={{data: {fill: 'navy'}}}/>
        </VictoryGroup>
      );
    }

    render() {
        if (!this.hasFetchedData()) {
          return (
            <div style={{justifyContent: 'center', display: 'flex'}}>
              <CircularProgress size={150}/>
            </div>
          );
        }

        const day = this.state.currentDay;
        const pm = this.props.predictionMarket;

        const oracleDataKey = this.oracleDataKeys[day];
        var oracleData = this.formatData(pm.getOracleConsumptions[oracleDataKey].value);
        // VictoryGraphs cannot handle empty data arrays
        if (oracleData.length === 0) {
          oracleData.push({x: -1, y: -1});
        }

        const agentPredictionKey = this.agentPredictionDataKeys[day];
        var agentPredictionData = 
          this.formatData(pm.getPredictions[agentPredictionKey].value);
        
        if (agentPredictionData.length === 0) {
          agentPredictionData.push({x: -1, y: -1});
        }

        return (
          <div className="section">
            <h1 style={{fontFamily: 'Poppins', display: 'flex', justifyContent: 'center'}}>
              Oracle Energy Consumptions
            </h1>
            <div style={{borderRadius: '8px', backgroundColor: 'white'}}>
              <VictoryChart
                containerComponent={
                  <VictoryVoronoiContainer
                    labels={({ datum }) => `${Math.round(datum.x, 2)}, ${Math.round(datum.y, 2)}`}
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
                  colorScale={[ "#a10d2d", "navy" ]}
                  data={[{name: "Real Consumption"}, {name: "Your Prediction" }]}
                />
                {this.renderOraclePrices(oracleData)}
                {this.renderAgentPredictions(agentPredictionData)}
              </VictoryChart>
            </div>
            {this.renderGraphFooter()}
          </div>
        );
    }

    formatData(data) {
      let formattedData = [];
      for (let i = 0; i < data.length; i++) {
        const y = parseInt(data[i]);
        if (y === 0) break;
        formattedData.push({x: i, y: y});
      }
      return formattedData;
    }

    periodToTime = (period) => {
      return `${period/2}:00`;
    }
}

PredictionGraph.contextTypes = {
  drizzle: PropTypes.object
}
  
export default PredictionGraph;