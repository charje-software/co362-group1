const PredictionMarket = artifacts.require("PredictionMarket");

contract("test: predictionMarket", async accounts => {

  ORACLE = accounts[0];
  AGENT1 = accounts[1];
  AGENT2 = accounts[2];
  AGENT1_BET_AMOUNT = 1;
  AGENT2_BET_AMOUNT = 2;
  AGENT1_PREDICTION = 550;
  AGENT2_PREDICTION = 700;
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

  it ('Initialises agent in group mapping', async () => {
    let pm = await PredictionMarket.deployed();

    const agent1 = await pm.group1.call(AGENT1);
    const agent2 = await pm.group1.call(AGENT2);

    assert.equal(agent1.amountBet.toNumber(), AGENT1_BET_AMOUNT);
    assert.equal(agent2.amountBet.toNumber(), AGENT2_BET_AMOUNT);
    assert.equal(agent1.demandPrediction.toNumber(), AGENT1_PREDICTION);
    assert.equal(agent2.demandPrediction.toNumber(), AGENT2_PREDICTION);
    assert.equal(agent1.win, false);
    assert.equal(agent2.win, false);
  });

  it ('Oracle update should shift betting group to ranking group and update consumption in group info', async () => {
    let pm = await PredictionMarket.deployed();

    var bettingGroup = await pm.BETTING.call();
    const currBettingGroupInfo = await pm.stageToGroupInfo.call(bettingGroup);

    await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});

    bettingGroup = await pm.BETTING.call();
    const rankingGroup = await pm.RANKING.call();
    const nextBettingGroupInfo = await pm.stageToGroupInfo.call(bettingGroup);
    const nextRankingGroupInfo = await pm.stageToGroupInfo.call(rankingGroup);

    // TODO: find out if possible to test groupInfo.agents array.
    assert.equal(currBettingGroupInfo.totalBetAmount.toNumber(), nextRankingGroupInfo.totalBetAmount.toNumber());
    assert.equal(nextBettingGroupInfo.consumption.toNumber(), 0);
    assert.equal(nextRankingGroupInfo.consumption.toNumber(), ORACLE_CONSUMPTION);
  });

  it ('Agent calling rank should set win to true if within threshold', async () => {
    let pm = await PredictionMarket.deployed();

    await pm.rank({from: AGENT1});
    await pm.rank({from: AGENT2});

    const agent1 = await pm.group1.call(AGENT1);
    const agent2 = await pm.group1.call(AGENT2);

    assert.equal(agent1.win, true);
    assert.equal(agent2.win, false);
  });

  it ('Oracle update should shift ranking group to claiming group', async () => {
    let pm = await PredictionMarket.deployed();

    const rankingGroup = await pm.RANKING.call();
    var claimingGroup = await pm.CLAIMING.call();
    const currRankingGroupInfo = await pm.stageToGroupInfo.call(rankingGroup);
    const currClaimingGroupInfo = await pm.stageToGroupInfo.call(claimingGroup);

    assert.equal(currClaimingGroupInfo.totalBetAmount.toNumber(), 0);

    await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});

    claimingGroup = await pm.CLAIMING.call();
    const nextClaimingGroupInfo = await pm.stageToGroupInfo.call(claimingGroup);

    assert.equal(currRankingGroupInfo.totalBetAmount.toNumber(), nextClaimingGroupInfo.totalBetAmount.toNumber());
    assert.equal(currRankingGroupInfo.consumption.toNumber(), nextClaimingGroupInfo.consumption.toNumber());
  });

  it ('Only winning agents should receive money', async () => {
    let pm = await PredictionMarket.deployed();

    const claimingGroup = await pm.CLAIMING.call();
    const claimingGroupInfo = await pm.stageToGroupInfo.call(claimingGroup);

    const winnings1 = await pm.claimWinnings({from: AGENT1});
    const winnings2 = await pm.claimWinnings({from: AGENT2});

    // TODO: find a way to test withdrawal amount.
    // assert.equal(winnings1.toNumber(), 3);
    // assert.equal(winnings2.toNumber(), 0);
  });

});
