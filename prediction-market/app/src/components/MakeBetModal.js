
import React from 'react';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import NavigationIcon from '@material-ui/icons/Navigation';
import TextField from '@material-ui/core/TextField';


export default class TransitionsModal extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      open: false, // for the modal opening/closing
      predictions: '', // 48 data point prediction
      betAmount: '0' // Amount to bet in ether
    };

  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  handlePredictionInput = input => {
    // const predictions = this.parsePredictions(input.target.value);
  };

  parsePredictions(input) {
    // input is in form "[10, 20, 30...]"
    return input.replace(/\s/g,'') // remove whitespace
                .split(","); // split entries by comma
  }

  render() {
    return (
      <div>
        <Fab variant="extended" 
          aria-label="like" 
          onClick={this.handleOpen}
          color="black"
          style={{marginTop: 18, marginRight: 20, backgroundColor: 'white'}}>
          <AddIcon
            style={{paddingRight: 3}}
            color="inherit"
            component={svgProps => {
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
            }}
          />
          Make Bet
        </Fab>
        
        <Modal
          open={this.state.open}
          onClose={this.handleClose}
          style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}
          closeAfterTransition
          BackdropComponent={Backdrop}
          BackdropProps={{
            timeout: 500,
          }}
        >
          <Fade in={this.state.open}>
            <div style={{borderRadius: 20, backgroundColor: 'white', padding: 20}}>
              <h2>Predict the energy prices of tomorrow.</h2>
              <p>A prediction consists of 48 data points throughout the day. Please separate your predictions with a comma.</p>
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
                  onChange={input => this.setState({betAmount: input.target.value})}
                  margin="normal"
                  variant="outlined"
                />
                <Fab variant="extended" 
                  aria-label="like" 
                  style={{marginTop: 17, marginRight: 20, backgroundColor: 'secondary'}}
                >
                  <NavigationIcon
                    style={{marginRight: 5}}
                    component={svgProps => {
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
                    }}
                  />
                  BET
                </Fab>
              </div>
            </div>
          </Fade>
        </Modal>
      </div>
    );
  }
  
}




