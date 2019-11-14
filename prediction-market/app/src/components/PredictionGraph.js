import React from "react";
import PropTypes from 'prop-types';
import {VictoryChart, VictoryGroup, VictoryVoronoiContainer,
        VictoryScatter, VictoryAxis, VictoryLine, VictoryLegend} from 'victory';
import Fab from '@material-ui/core/Fab';
import CircularProgress from '@material-ui/core/CircularProgress';

class PredictionGraph extends React.Component {

    constructor(props, context) {
      super(props);
      this.dataKeys = [];
      for (let i = 0; i < 7; i++) {
        this.dataKeys.push(
          context.drizzle.contracts.PredictionMarket.methods["getOracleConsumptions"].cacheCall(i)
        );
      }
      this.state = {currentDay: 0};
    }
    
    hasFetchedData() {
      for (let i = 0; i < 7; i++) {
        const dataKey = this.dataKeys[i];
        if (!(dataKey in this.props.predictionMarket.getOracleConsumptions)) {
          return false;
        }
      }
      return true;
    }

    renderGraphHeader() {
      return (
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
          <Fab
            variant="extended"
            size="medium"
            color="primary"
            aria-label="add"
            style={{marginTop: 15}}
            onClick={() => void this.setState({currentDay: this.state.currentDay + 1})}
            disabled={this.state.currentDay === 6}          
          >
            BACK
          </Fab>
          <h2 style={{fontFamily: 'Poppins'}}>ORACLE ENERGY CONSUMPTIONS</h2>
          <Fab
            variant="extended"
            size="medium"
            color="primary"
            aria-label="add"
            style={{marginTop: 15}}
            onClick={() => void this.setState({currentDay: this.state.currentDay - 1})}
            disabled={this.state.currentDay === 0}  
          >
            NEXT
          </Fab>
        </div>
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

        const dataKey = this.dataKeys[this.state.currentDay];
        var data = this.formatData(this.props.predictionMarket.getOracleConsumptions[dataKey].value);
        // VictoryGraphs cannot handle empty data arrays
        if (data.length === 0) {
          data.push({x: -1, y: -1});
        }

        return (
          <div className="section">
            {this.renderGraphHeader()}
            <div style={{borderRadius: '8px', backgroundColor: 'white'}}>
              <VictoryChart
                  containerComponent={
                    <VictoryVoronoiContainer
                      labels={({ datum }) => `${Math.round(datum.x, 2)}, ${Math.round(datum.y, 2)}`}
                      voronoiBlacklist={['oracle']}
                    />
                  }
                  domain={{y: [0, 2500]}}
              >
                <VictoryLegend
                  orientation="horizontal"
                  colorScale={[ "grey", "navy" ]}
                  data={[{name: "Real Consumption"}, {name: "Your Prediction" }]}
                />
                <VictoryGroup data={data}>
                  <VictoryAxis dependentAxis fixLabelOverlap />
                  <VictoryAxis crossAxis fixLabelOverlap 
                    label="Time"
                    tickValues={[4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]}
                    tickFormat={this.periodToTime}
                  />
                  <VictoryLine name='oracle'/> 
                  <VictoryScatter style={{ data: { fill: this.getPlotPointColor } }}/>
                </VictoryGroup>
                {/* <VictoryGroup data={agentPredictions}>
                  <VictoryLine name="line2"/>
                  <VictoryScatter/>
                </VictoryGroup> */}
              </VictoryChart>
            </div>
          </div>
        );
    }

    formatData(consumptions) {
      let data = [];
      for (let i = 0; i < consumptions.length; i++) {
        const c = parseInt(consumptions[i]);
        if (c === 0) break;
        data.push({x: i, y: c});
      }
      return data;
    }

    // Very simple function for now. As we add more graph
    // lines we will change this.
    getPlotPointColor = (data) => {
      if (data.y > 150) {
          return "yellow";
      } else if (data.y > 110) {
          return "orange";
      } else {
          return "red";
      }
    }

    periodToTime = (period) => {
      return `${period/2}:00`;
    }
}

PredictionGraph.contextTypes = {
  drizzle: PropTypes.object
}
  
export default PredictionGraph;