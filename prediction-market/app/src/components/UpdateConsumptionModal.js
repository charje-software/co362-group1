import React from 'react';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import NavigationIcon from '@material-ui/icons/Navigation';
import TextField from '@material-ui/core/TextField';
import PropTypes from 'prop-types';

export default class UpdateConsumptionModal extends React.Component {

  constructor(props, context) {
    super(props);
    this.drizzle = context.drizzle;
    this.state = {
      open: false, // for the modal opening/closing
      consumption: '0' // consumption value being fed in
    };
    this.currTimePeriodDataKey = this.drizzle.contracts.PredictionMarket.methods["currTimePeriod"].cacheCall();
  }

  openModal = () => {
    this.setState({open: true});
  };

  closeModal = () => {
    this.setState({open: false});
  };

  onClickUpdate = async () => {
    if (isNaN(this.state.consumption)) return;

    // Calling function - will prompt MetaMask verification
    await this.drizzle.contracts.PredictionMarket.methods["updateConsumption"]
              .cacheSend(this.state.consumption);

    // Reset form and close modal
    this.setState({consumption: '0'});
    this.closeModal();
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

  renderUpdateConsumptionButton() {
    return (
      <Fab variant="extended"
        onClick={this.openModal}
        style={fabStyle}>
        <AddIcon
          style={iconStyle}
          color="inherit"
          component={this.svgGradient}
        />
        Update Consumption
      </Fab>
    );
  }

  getPeriodBeingUpdated() {
    if (this.currTimePeriodDataKey in this.props.predictionMarket.currTimePeriod) {
      const currTimePeriod = this.props.predictionMarket.currTimePeriod[this.currTimePeriodDataKey].value;
      const hour = Math.floor(currTimePeriod / 2);
      if (currTimePeriod % 2 === 0) {
        return ` spanning time period ${hour}:00 - ${hour}:30.`;
      }
      return ` spanning time period ${hour}:30 - ${(hour + 1) % 24}:00.`;
    }
    return ".";
  }

  renderUpdateConsumptionModal() {
    return (
      <Modal
        open={this.state.open}
        onClose={this.closeModal}
        style={modalStyle}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={this.state.open}>
          <div style={formStyle}>
            <h2>Input true values of consumption.</h2>
            <p>Actual consumption values should be updated by the oracle at 30 minute intervals throughout the day.</p>
            <p>Manually update the total consumption for the next 30 minute interval{this.getPeriodBeingUpdated()}</p>
            <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
              <TextField
                label="Consumption (kWh)"
                multiline
                rowsMax="1"
                value={this.state.consumption}
                error={isNaN(parseInt(this.state.consumption))}
                helperText={isNaN(parseInt(this.state.consumption)) ? 'Must be a number' : ''}
                onChange={input => this.setState({consumption: input.target.value})}
                margin="normal"
                variant="outlined"
              />
              <Fab variant="extended"
                style={fabStyle}
                onClick={this.onClickUpdate}
              >
                <NavigationIcon
                  style={iconStyle}
                  component={this.svgGradient}
                />
                UPDATE
              </Fab>
            </div>
          </div>
        </Fade>
      </Modal>
    );
  }

  render() {
    return (
      <div>
        {this.renderUpdateConsumptionButton()}
        {this.renderUpdateConsumptionModal()}
      </div>
    );
  }

}

const modalStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const formStyle = {
  borderRadius: 20,
  backgroundColor: 'white',
  padding: 25,
  outline: 'none'
};

const fabStyle = {
  marginTop: 17,
  marginRight: 20,
  backgroundColor: 'white'
};

const iconStyle = {
  marginRight: 5
};

UpdateConsumptionModal.contextTypes = {
  drizzle: PropTypes.object
}
