const path = require("path");
var HDWalletProvider = require("truffle-hdwallet-provider");
const secrets = require("./secrets.json");
const mnemonic = secrets.Mnemonic;
const ropstenApiKey = secrets.InfuraApiKey;

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "app/src/contracts"),
  networks: {
    // use this when testing with local ganache
    development: {
      host: "127.0.0.1",  // localhost
      port: 7545,
      network_id: "*"
    },
    // use for demos on college network
    internal_demo: {
      host: "146.169.41.214", // ip of VM running ganache-cli
      port: 8545,
      network_id: "*"
    },
    // use for public demo
    public_demo: {
      // runs ganache-cli but may restart when idle and lose contract state
      host: "charje-ganache-test.herokuapp.com", 
      port: 80,
      network_id: "*"
    },
    // used by CI/CD pipeline during testing stage
    testing: {
      host: "trufflesuite-ganache-cli",
      port: 8545,
      network_id: "*"
    },
    // used to deploy to public Ropsten test network
    ropsten: {
      provider: function() {
        return new HDWalletProvider(mnemonic, ropstenApiKey)
      },
      network_id: 3
    },
  }
};
