const PredictionMarket = artifacts.require("PredictionMarket");

contract("test: predictionMarket", async accounts => {

  STAGE_LENGTH = 24
  PREDICTIONS_PER_BET = 48

  ORACLE = accounts[0];
  AGENT1 = accounts[1];                  // winning agent
  AGENT2 = accounts[2];                  // losing agent
  AGENT1_BET_AMOUNT = 1;                 // 1 wei
  AGENT2_BET_AMOUNT = 2;                 // 2 wei
  FOLLOWING_GROUP_TOTAL_BET_AMOUNT = 0;  // total bet amount for following group
  AGENT1_PREDICTIONS = [];                     // within threshold
  AGENT2_PREDICTIONS = [];                     // outside threshold
  AGENT1_PREDICTION = 550;
  AGENT2_PREDICTION = 700;
  for (var i = 0; i < PREDICTIONS_PER_BET; i++) {
    AGENT1_PREDICTIONS.push(AGENT1_PREDICTION);
    AGENT2_PREDICTIONS.push(AGENT2_PREDICTION);
  }
  ORACLE_CONSUMPTION = 500;

  it ('Updates total bet amount for current betting group', async () => {
    let pm = await PredictionMarket.deployed();

    await pm.placeBet(AGENT1_PREDICTIONS, {from: AGENT1, value: AGENT1_BET_AMOUNT});
    await pm.placeBet(AGENT2_PREDICTIONS, {from: AGENT2, value: AGENT2_BET_AMOUNT});

    const betting = await pm.BETTING.call();
    const bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    const totalBetAmount = bettingGroupInfo.totalBetAmount;

    assert.equal(totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
  });

  it ('Initialises agent\'s bet in group mapping', async () => {
    let pm = await PredictionMarket.deployed();

    const betting = await pm.BETTING.call();
    const agentPredictions1 = await pm.getBetPredictionsFromStage.call(betting, {from: AGENT1});
    const agentPredictions2 = await pm.getBetPredictionsFromStage.call(betting, {from: AGENT2});

    const agentBet1 = await pm.group1.call(AGENT1);
    const agentBet2 = await pm.group1.call(AGENT2);

    assert.equal(agentBet1.amount.toNumber(), AGENT1_BET_AMOUNT);
    assert.equal(agentBet2.amount.toNumber(), AGENT2_BET_AMOUNT);
    assert.equal(agentPredictions1[0].toNumber(), AGENT1_PREDICTION);
    assert.equal(agentPredictions1[47].toNumber(), AGENT1_PREDICTION);
    assert.equal(agentPredictions2[0].toNumber(), AGENT2_PREDICTION);
    assert.equal(agentPredictions2[47].toNumber(), AGENT2_PREDICTION);
    assert.equal(agentBet1.win, false);
    assert.equal(agentBet2.win, false);
  });

  it ('Oracle update should shift betting group to waiting group', async () => {
    let pm = await PredictionMarket.deployed();

    // Pass BETTING and progress to WAITING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    betting = await pm.BETTING.call();
    waiting = await pm.WAITING.call();
    bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), FOLLOWING_GROUP_TOTAL_BET_AMOUNT);
    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
  });

  it ('Oracle update should shift waiting group to claiming group and put oracle data in group info', async () => {
    let pm = await PredictionMarket.deployed();

    // Pass WAITING and progress to CLAIMING
    for (var i = 0; i < STAGE_LENGTH * 2; i++) {
      await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
    }

    const claiming = await pm.CLAIMING.call();
    const claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);
    const claimingGroupOracleConsumption = await pm.getOracleConsumptionFromStage.call(claiming);

    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(claimingGroupOracleConsumption[0].toNumber(), ORACLE_CONSUMPTION);
    assert.equal(claimingGroupOracleConsumption[47].toNumber(), ORACLE_CONSUMPTION);
  });

  it ('Agent calling rank should set win to true if within threshold', async () => {
    let pm = await PredictionMarket.deployed();

    await pm.rank({from: AGENT1});
    await pm.rank({from: AGENT2});

    const agentBet1 = await pm.group1.call(AGENT1);
    const agentBet2 = await pm.group1.call(AGENT2);

    assert.equal(agentBet1.win, true);
    assert.equal(agentBet2.win, false);
  });

  it ('Claiming group info should have correct totalWinners', async () => {
    let pm = await PredictionMarket.deployed();

    const claiming = await pm.CLAIMING.call();
    const claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);

    assert.equal(claimingGroupInfo.totalWinners.toNumber(), 1);
  });

  it ('Agent can claim winnings if their bet won', async () => {
    let pm = await PredictionMarket.deployed();

    // CLAIMING: pass STAGE_LENGTH periods to allow agents to claim
    for (var i = 0; i < STAGE_LENGTH; i++) {
      await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
    }

    const contractBalance1 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT2});
    const contractBalance2 = await web3.eth.getBalance(pm.address);
    await pm.claimWinnings({from: AGENT1});
    const contractBalance3 = await web3.eth.getBalance(pm.address);

    assert.equal(contractBalance1, AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(contractBalance2, AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(contractBalance3, 0);
  });

  it ('Oracle update should shift claiming group to betting group and clear', async () => {
    let pm = await PredictionMarket.deployed();

    // Pass CLAIMING and progress to BETTING
    for (var i = 0; i < STAGE_LENGTH; i++) {
      await pm.updateConsumption(0, {from: ORACLE});
    }

    const betting = await pm.BETTING.call();
    const bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    const bettingGroupOracleConsumption = await pm.getOracleConsumptionFromStage.call(betting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(bettingGroupOracleConsumption.length, 0);
    assert.equal(bettingGroupInfo.totalWinners.toNumber(), 0);
  });

});
