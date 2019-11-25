const PredictionMarket = artifacts.require("PredictionMarket");

STAGE_LENGTH = 24
PREDICTIONS_PER_BET = 48

contract("No Winners test", async accounts => {
  ORACLE = accounts[0];
  AGENT = accounts[1];
  BET_AMOUNT = 100;
  ORACLE_CONSUMPTION = 500;
  AGENT_PREDICTIONS = [];
  AGENT_PREDICTION = 800;
  for (var i = 0; i < PREDICTIONS_PER_BET; i++) {
    AGENT_PREDICTIONS.push(AGENT_PREDICTION);
  }

  let pm

  beforeEach('setup contract', async function () {
    pm = await PredictionMarket.deployed();
  });

  it ('Placing a bet outside of threshold will receive no winnings', async () => {
    await pm.placeBet(AGENT_PREDICTIONS, {from: AGENT, value: BET_AMOUNT});

    // pass from BETTING to WAITING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    // pass from WAITING to CLAIMING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
    }

    await pm.rank({from: AGENT});

    // CLAIMING: pass from ranking part to actual claiming part
    for (var i = 0; i < STAGE_LENGTH; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    const contractBalance1 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT});
    const contractBalance2 = await web3.eth.getBalance(pm.address);

    assert.equal(contractBalance1, contractBalance2);
  });
});