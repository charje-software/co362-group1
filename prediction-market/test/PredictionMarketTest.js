const PredictionMarket = artifacts.require("PredictionMarket");

contract("test: predictionMarket", async accounts => {

  ORACLE = accounts[0];
  AGENT1 = accounts[1];     // winning agent
  AGENT2 = accounts[2];     // losing agent
  AGENT1_BET_AMOUNT = 1;    // 1 wei
  AGENT2_BET_AMOUNT = 2;    // 2 wei
  AGENT1_PREDICTION = 550;  // within threshold
  AGENT2_PREDICTION = 700;  // outside threshold
  ORACLE_CONSUMPTION = 500;

  it ('Updates total bet amount for current betting group', async () => {
    let pm = await PredictionMarket.deployed();

    await pm.placeBet(AGENT1_PREDICTION, {from: AGENT1, value: AGENT1_BET_AMOUNT});
    await pm.placeBet(AGENT2_PREDICTION, {from: AGENT2, value: AGENT2_BET_AMOUNT});

    const bettingGroup = await pm.BETTING.call();
    const bettingGroupInfo = await pm.stageToGroupInfo.call(bettingGroup);
    const totalBetAmount = bettingGroupInfo.totalBetAmount;

    assert.equal(totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
  });

  it ('Initialises agent\'s bet in group mapping', async () => {
    let pm = await PredictionMarket.deployed();

    const agentBet1 = await pm.group1.call(AGENT1);
    const agentBet2 = await pm.group1.call(AGENT2);

    assert.equal(agentBet1.amount.toNumber(), AGENT1_BET_AMOUNT);
    assert.equal(agentBet2.amount.toNumber(), AGENT2_BET_AMOUNT);
    assert.equal(agentBet1.prediction.toNumber(), AGENT1_PREDICTION);
    assert.equal(agentBet2.prediction.toNumber(), AGENT2_PREDICTION);
    assert.equal(agentBet1.win, false);
    assert.equal(agentBet2.win, false);
  });

  it ('Oracle update should shift betting group to waiting group', async () => {
    let pm = await PredictionMarket.deployed();

    var betting = await pm.BETTING.call();
    var waiting = await pm.WAITING.call();
    var bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    var waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), 0);

    await pm.updateConsumption(0, {from: ORACLE});

    betting = await pm.BETTING.call();
    waiting = await pm.WAITING.call();
    bettingGroupInfo = await pm.stageToGroupInfo.call(betting);
    waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);

    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
  });

  it ('Oracle update should shift waiting group to ranking group and put oracle data in group info', async () => {
    let pm = await PredictionMarket.deployed();

    var waiting = await pm.WAITING.call();
    var ranking = await pm.RANKING.call();
    var waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);
    var rankingGroupInfo = await pm.stageToGroupInfo.call(ranking);

    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(rankingGroupInfo.totalBetAmount.toNumber(), 0);

    await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});

    waiting = await pm.WAITING.call();
    ranking = await pm.RANKING.call();
    waitingGroupInfo = await pm.stageToGroupInfo.call(waiting);
    rankingGroupInfo = await pm.stageToGroupInfo.call(ranking);

    assert.equal(waitingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(rankingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(rankingGroupInfo.consumption.toNumber(), ORACLE_CONSUMPTION);
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

  it ('Ranking group info should have correct totalWinners', async () => {
    let pm = await PredictionMarket.deployed();

    const ranking = await pm.RANKING.call();
    const rankingGroupInfo = await pm.stageToGroupInfo.call(ranking);

    assert.equal(rankingGroupInfo.totalWinners.toNumber(), 1);
  });

  it ('Oracle update should shift ranking group to claiming group', async () => {
    let pm = await PredictionMarket.deployed();

    var ranking = await pm.RANKING.call();
    var claiming = await pm.CLAIMING.call();
    var rankingGroupInfo = await pm.stageToGroupInfo.call(ranking);
    var claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);

    assert.equal(rankingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), 0);

    await pm.updateConsumption(0, {from: ORACLE});

    ranking = await pm.RANKING.call();
    claiming = await pm.CLAIMING.call();
    rankingGroupInfo = await pm.stageToGroupInfo.call(ranking);
    claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);

    assert.equal(rankingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
  });

  it ('Agent can claim winnings if their bet won', async () => {
    let pm = await PredictionMarket.deployed();

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

    var claiming = await pm.CLAIMING.call();
    var betting = await pm.BETTING.call();
    var claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);
    var bettingGroupInfo = await pm.stageToGroupInfo.call(betting);

    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), AGENT1_BET_AMOUNT + AGENT2_BET_AMOUNT);
    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), 0);

    await pm.updateConsumption(0, {from: ORACLE});

    claiming = await pm.CLAIMING.call();
    betting = await pm.BETTING.call();
    claimingGroupInfo = await pm.stageToGroupInfo.call(claiming);
    bettingGroupInfo = await pm.stageToGroupInfo.call(betting);

    assert.equal(claimingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(bettingGroupInfo.totalBetAmount.toNumber(), 0);
    assert.equal(bettingGroupInfo.consumption.toNumber(), 0);
    assert.equal(bettingGroupInfo.totalWinners.toNumber(), 0);
  });

});
