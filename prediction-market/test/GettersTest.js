const PredictionMarket = artifacts.require("PredictionMarket");

STAGE_LENGTH = 24
PREDICTIONS_PER_BET = 48

contract("Getters test", async accounts => {
  ORACLE = accounts[0];
  AGENT1 = accounts[1];
  AGENT2 = accounts[2];
  BET_AMOUNT = 100;
  MID_TIER_WINNING_SCALE = 1;
  TOP_TIER_WINNING_SCALE = 3;
  ORACLE_CONSUMPTION = 500;
  AGENT1_PREDICTIONS = [];
  AGENT2_PREDICTIONS = [];
  AGENT1_PREDICTION = 550;
  AGENT2_PREDICTION = 600;
  for (var i = 0; i < PREDICTIONS_PER_BET; i++) {
    AGENT1_PREDICTIONS.push(AGENT1_PREDICTION);
    AGENT2_PREDICTIONS.push(AGENT2_PREDICTION);
  }

  let pm

  beforeEach('setup contract', async function () {
    pm = await PredictionMarket.deployed();
  });

  it ('getBetPredictionsFromStage works correctly', async () => {
    await pm.placeBet(AGENT1_PREDICTIONS, {from: AGENT1, value: BET_AMOUNT});
    await pm.placeBet(AGENT2_PREDICTIONS, {from: AGENT2, value: BET_AMOUNT});

    const betting = await pm.BETTING.call();
    const predictions = await pm.getBetPredictionsFromStage.call(betting, {from: AGENT1});

    assert.equal(predictions[0].toNumber(), AGENT1_PREDICTION);
    assert.equal(predictions[47].toNumber(), AGENT1_PREDICTION);
  });

  it ('getPredictions works correctly', async () => {
    const predictions = await pm.getPredictions.call(0, {from: AGENT1});

    assert.equal(predictions[0].toNumber(), AGENT1_PREDICTION);
    assert.equal(predictions[47].toNumber(), AGENT1_PREDICTION);
  });

  it ('getPredictionsForAddress works correctly', async () => {
    const predictions = await pm.getPredictionsForAddress.call(AGENT2, 0, {from: AGENT1});

    assert.equal(predictions[0].toNumber(), AGENT2_PREDICTION);
    assert.equal(predictions[47].toNumber(), AGENT2_PREDICTION);
  });

  it ('getCurrentParticipants works correctly', async () => {
    const participants = await pm.getCurrentParticipants.call();

    assert.equal(participants[0], AGENT1);
    assert.equal(participants[1], AGENT2);
  });

  it ('getOracleConsumptionsFromStage works correctly', async () => {
    // pass from BETTING to WAITING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
        await pm.updateConsumption(0, {from: ORACLE});
    }

    // pass from WAITING to CLAIMING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
        await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
    }

    const claiming = await pm.CLAIMING.call();
    const consumptions = await pm.getOracleConsumptionsFromStage.call(claiming);

    assert.equal(consumptions[0].toNumber(), ORACLE_CONSUMPTION);
    assert.equal(consumptions[47].toNumber(), ORACLE_CONSUMPTION);
  });

  it ('getOracleConsumptions works correctly', async () => {
    const consumptions = await pm.getOracleConsumptions.call(2);

    assert.equal(consumptions[0].toNumber(), ORACLE_CONSUMPTION);
    assert.equal(consumptions[47].toNumber(), ORACLE_CONSUMPTION);
  });

  it ('getBetWinningScale works correctly', async () => {
    await pm.rank({from: AGENT1});
    await pm.rank({from: AGENT2});

    const agent1WinningScale = await pm.getBetWinningScale.call(2, {from: AGENT1});
    const agent2WinningScale = await pm.getBetWinningScale.call(2, {from: AGENT2});

    assert.equal(agent1WinningScale.toNumber(), TOP_TIER_WINNING_SCALE);
    assert.equal(agent2WinningScale.toNumber(), MID_TIER_WINNING_SCALE);
  });
});