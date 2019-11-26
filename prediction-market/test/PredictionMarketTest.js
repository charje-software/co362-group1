const PredictionMarket = artifacts.require("PredictionMarket");

STAGE_LENGTH = 24
PREDICTIONS_PER_BET = 48

contract("PredictionMarket one cycle", async accounts => {
  ORACLE = accounts[0];
  AGENT1 = accounts[1]; // top tier agent
  AGENT2 = accounts[2]; // mid tier agent
  AGENT3 = accounts[3]; // losing agent

  BET_AMOUNT = 400;
  TOTAL_BET_AMOUNT = BET_AMOUNT * 3;
  FOLLOWING_GROUP_TOTAL_BET_AMOUNT = 0;  // total bet amount for following group

  BASE_WINNING_SCALE = 0;
  MID_TIER_WINNING_SCALE = 1;
  TOP_TIER_WINNING_SCALE = 3;

  AGENT1_REWARD = 900;
  AGENT2_REWARD = 300;
  AGENT3_REWARD = 0;

  AGENT1_PREDICTIONS = [];
  AGENT2_PREDICTIONS = [];
  AGENT3_PREDICTIONS = [];
  AGENT1_PREDICTION = 450;
  AGENT2_PREDICTION = 400;
  AGENT3_PREDICTION = 700;
  for (var i = 0; i < PREDICTIONS_PER_BET; i++) {
    AGENT1_PREDICTIONS.push(AGENT1_PREDICTION + i);
    AGENT2_PREDICTIONS.push(AGENT2_PREDICTION + i);
    AGENT3_PREDICTIONS.push(AGENT3_PREDICTION + i);
  }
  ORACLE_CONSUMPTION = 500;

  let pm

  beforeEach('setup contract', async function () {
    pm = await PredictionMarket.deployed();
  });

  it ('Updates total bet amount for current betting group', async () => {
    await pm.placeBet(AGENT1_PREDICTIONS, {from: AGENT1, value: BET_AMOUNT});
    await pm.placeBet(AGENT2_PREDICTIONS, {from: AGENT2, value: BET_AMOUNT});
    await pm.placeBet(AGENT3_PREDICTIONS, {from: AGENT3, value: BET_AMOUNT});

    const betting = await pm.BETTING.call();
    const bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    const totalBetAmount = bettingGroupInfo.totalBetAmount;

    assert.equal(totalBetAmount.toNumber(), TOTAL_BET_AMOUNT);
  });

  it ('Initialises agent\'s bet in group mapping', async () => {
    const betting = await pm.BETTING.call();
    const agentPredictions = await pm.getBetPredictionsFromStage.call(betting, {from: AGENT1});

    const agentBet = await pm.group1.call(AGENT1);

    assert.equal(agentBet.amount.toNumber(), BET_AMOUNT);
    assert.equal(agentPredictions[0].toNumber(), AGENT1_PREDICTION);
    assert.equal(agentPredictions[47].toNumber(), AGENT1_PREDICTION + 47);
    assert.equal(agentBet.winningScale.toNumber(), BASE_WINNING_SCALE);
  });

  it ('Oracle update should shift betting group to waiting group', async () => {
    // Pass BETTING and progress to WAITING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    betting = await pm.BETTING.call();
    waiting = await pm.WAITING.call();
    bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), FOLLOWING_GROUP_TOTAL_BET_AMOUNT);
    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), TOTAL_BET_AMOUNT);
  });

  it ('Oracle update should shift waiting group to claiming group and put oracle data in group info', async () => {
    // Pass WAITING and progress to CLAIMING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(ORACLE_CONSUMPTION + i, {from: ORACLE});
    }

    const claiming = await pm.CLAIMING.call();
    const claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);
    const claimingGroupOracleConsumption = await pm.getOracleConsumptionsFromStage.call(claiming);

    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), TOTAL_BET_AMOUNT);
    assert.equal(claimingGroupOracleConsumption[0].toNumber(), ORACLE_CONSUMPTION);
    assert.equal(claimingGroupOracleConsumption[47].toNumber(), ORACLE_CONSUMPTION + 47);
  });

  it ('History of predictions and oracle consumptions are recorded correctly', async () => {
    const agentPredictions = await pm.getPredictions.call(2, {from: AGENT1}); // Agent predictions from day before
    const oracleConsumptions = await pm.getOracleConsumptions.call(2); // Oracle consumptions from day before

    assert.equal(oracleConsumptions[0].toNumber(), ORACLE_CONSUMPTION);
    assert.equal(oracleConsumptions[47].toNumber(), ORACLE_CONSUMPTION + 47);
    assert.equal(agentPredictions[0].toNumber(), AGENT1_PREDICTION);
    assert.equal(agentPredictions[47].toNumber(), AGENT1_PREDICTION + 47);
  })

  it ('Agent calling rank should set correct scales according to threshold', async () => {
    await pm.rank({from: AGENT1});
    await pm.rank({from: AGENT2});
    await pm.rank({from: AGENT3});

    const agentWinningScale1 = await pm.getBetWinningScale.call(2, {from: AGENT1});
    const agentWinningScale2 = await pm.getBetWinningScale.call(2, {from: AGENT2});
    const agentWinningScale3 = await pm.getBetWinningScale.call(2, {from: AGENT3});

    assert.equal(agentWinningScale1.toNumber(), TOP_TIER_WINNING_SCALE);
    assert.equal(agentWinningScale2.toNumber(), MID_TIER_WINNING_SCALE);
    assert.equal(agentWinningScale3.toNumber(), BASE_WINNING_SCALE);
  });

  it ('Claiming group info should have correct counts', async () => {
    const claiming = await pm.CLAIMING.call();
    const claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);

    assert.equal(claimingGroupInfo.topTierCount.toNumber(), 1);
    assert.equal(claimingGroupInfo.midTierCount.toNumber(), 1);
    assert.equal(claimingGroupInfo.baseCount.toNumber(), 1);
  });

  it ('Agent claim winnings based on tier correctly', async () => {
    // CLAIMING: pass STAGE_LENGTH periods to allow agents to claim
    for (var i = 0; i < STAGE_LENGTH; i++) {
      await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
    }

    const contractBalance1 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT1});
    const contractBalance2 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT2});
    const contractBalance3 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT3});
    const contractBalance4 = await web3.eth.getBalance(pm.address);

    assert.equal(contractBalance1, TOTAL_BET_AMOUNT);
    assert.equal(contractBalance2, TOTAL_BET_AMOUNT - AGENT1_REWARD);
    assert.equal(contractBalance3, TOTAL_BET_AMOUNT - AGENT1_REWARD - AGENT2_REWARD);
    assert.equal(contractBalance4, TOTAL_BET_AMOUNT - AGENT1_REWARD - AGENT2_REWARD - AGENT3_REWARD);
  });

  it ('Oracle update should shift claiming group to betting group and clear', async () => {
    // Pass CLAIMING and progress to BETTING
    for (var i = 0; i < STAGE_LENGTH; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    const betting = await pm.BETTING.call();
    const bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    const bettingGroupOracleConsumption = await pm.getOracleConsumptionsFromStage.call(betting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(bettingGroupOracleConsumption.length, 0);
    assert.equal(bettingGroupInfo.topTierCount.toNumber(), 0);
    assert.equal(bettingGroupInfo.midTierCount.toNumber(), 0);
    assert.equal(bettingGroupInfo.baseCount.toNumber(), 0);
  });

});
