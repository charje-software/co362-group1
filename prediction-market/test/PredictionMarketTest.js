const PredictionMarket = artifacts.require("PredictionMarket");

contract("test: predictionMarket", async accounts => {
  it ('updates balance correctly', async () => {
    let instance = await PredictionMarket.deployed();
    await instance.placeBet(700, {from: accounts[0], value: 2});
    await instance.placeBet(800, {from: accounts[1], value: 3});
    const totalBets = await instance.totalBets.call();
    assert.equal(totalBets.toString(), '5');
  });

  it ('updates agent list correctly', async () => {
    let instance = await PredictionMarket.deployed();
    const agent1 = await instance.agents.call(0);
    const agent2 = await instance.agents.call(1);
    assert.equal(agent1, accounts[0]);
    assert.equal(agent2, accounts[1]);
  });

  it ('records the demand prediction correctly', async () => {
    let instance = await PredictionMarket.deployed();
    const agent1 = await instance.agentInfo.call(accounts[0]);
    const agent2 = await instance.agentInfo.call(accounts[1]);
    assert.equal(agent1[1], 700);
    assert.equal(agent2[1], 800);
  });

  it ('clears bet list after winnings distribution', async () => {
    let instance = await PredictionMarket.deployed();
    await instance.distributeWinnings({from: accounts[0]});
    const totalBets = await instance.totalBets.call();
    assert.equal(totalBets.toString(), '0');
  });
});
