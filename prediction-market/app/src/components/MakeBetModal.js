import React from 'react';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import NavigationIcon from '@material-ui/icons/Navigation';
import TextField from '@material-ui/core/TextField';
import PropTypes from 'prop-types';

export default class MakeBetModal extends React.Component {

  constructor(props, context) {
    super(props);
    this.drizzle = context.drizzle;
    this.state = {
      open: false, // for the modal opening/closing
      predictions: '', // 48 data point prediction
      betAmount: '0' // Amount to bet in ether
    };
  }

  openModal = () => {
    this.setState({open: true});
  };

  closeModal = () => {
    this.setState({open: false});
  };

  onClickBet = async () => {
    const predictions = this.parsePredictions(this.state.predictions);

    // Converting betAmount to Wei and handling errors
    const betAmount = parseInt(this.state.betAmount) * Math.pow(10, 18);
    if (isNaN(betAmount) || betAmount === 0) return;

    const data = {value: betAmount.toString()}

    // Calling function - will prompt MetaMask verification
    await this.drizzle.contracts.PredictionMarket.methods["placeBet"]
              .cacheSend(predictions, data);
    
    // Reset form and close modal
    this.setState({predictions: '', betAmount: '0'});
    this.closeModal();
  }

  parsePredictions(input) {
    // input is in form "1, 2, 3...48"
    // output is in form [1, 2, 3, ...48]
    return input.replace(/\s/g,'') // remove whitespace
                .split(","); // split entries by comma
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

  renderMakeBetButton() {
    return (
      <Fab variant="extended" 
        onClick={this.openModal}
        style={fabStyle}>
        <AddIcon
          style={iconStyle}
          color="inherit"
          component={this.svgGradient}
        />
        Make Bet
      </Fab>
    );
  }

  renderMakeBetModal() {
    return (
      <Modal
        open={this.state.open}
        onClose={this.closeModal}
        style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={this.state.open}>
          <div style={{borderRadius: 20, backgroundColor: 'white', padding: 25}}>
            <h2>Predict the energy prices of tomorrow.</h2>
            <p>A prediction consists of 48 data points throughout the day. 
              Please separate your predictions with a comma.</p>
            <p>The first prediction is the consumption for 00:30am, 
              the second is for 1:00am and so on.</p>
            <TextField
              label="Predictions"
              multiline
              rowsMax="4"
              fullWidth="true"
              value={this.state.predictions}
              onChange={input => this.setState({predictions: input.target.value})}
              margin="normal"
              variant="outlined"
            />
            <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
              <TextField
                label="ETH"
                multiline
                rowsMax="1"
                value={this.state.betAmount}
                error={isNaN(parseInt(this.state.betAmount))}
                helperText={isNaN(parseInt(this.state.betAmount)) ? 'Must be a number' : ''}
                onChange={input => this.setState({betAmount: input.target.value})}
                margin="normal"
                variant="outlined"
              />
              <Fab variant="extended" 
                style={fabStyle}
                onClick={this.onClickBet}
              >
                <NavigationIcon
                  style={iconStyle}
                  component={this.svgGradient}
                />
                BET
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
        {this.renderMakeBetButton()}
        {this.renderMakeBetModal()}
      </div>
    );
  }
  
}

const fabStyle = {
  marginTop: 17, 
  marginRight: 20, 
  backgroundColor: 'white'
};

const iconStyle = {
  marginRight: 5
};

MakeBetModal.contextTypes = {
  drizzle: PropTypes.object
}




