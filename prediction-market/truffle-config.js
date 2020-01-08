const path = require("path");

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
    // used by CI/CD pipeline on master branch when deploying
    master: {
      host: "146.169.41.214", // ip of docker container
      port: 8545,
      network_id: "*"
    },
    // used by CI/CD pipeline during testing stage
    testing: {
      host: "trufflesuite-ganache-cli",
      port: 8545,
      network_id: "*"
    }
  }
};
