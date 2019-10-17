const PredictionMarket = artifacts.require("PredictionMarket");

module.exports = function(deployer) {
  deployer.deploy(PredictionMarket);
};
