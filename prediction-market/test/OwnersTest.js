const { expectRevert } = require('@openzeppelin/test-helpers');
const PredictionMarket = artifacts.require("PredictionMarket");

contract("Owner", async accounts => {
  ORACLE = accounts[0];
  AGENT1 = accounts[1];
  AGENT2 = accounts[2];
  ORACLE_CONSUMPTION = 500;

  let pm

  beforeEach('setup contract', async function () {
    pm = await PredictionMarket.deployed();
  });

  it ('Oracle is the owner', async () => {
    const oracle = await pm.isOwner.call({from: ORACLE});

    assert.equal(oracle, true);
  });

  it ('Agents are not an owner', async () => {
    const agent1 = await pm.isOwner.call({from: AGENT1});
    const agent2 = await pm.isOwner.call({from: AGENT2});

    assert.equal(agent1, false);
    assert.equal(agent2, false);
  });

  it ('Oracle can update consumption', async () => {
    await pm.updateConsumption(ORACLE_CONSUMPTION, {from: ORACLE});
  });

  it ('Agent cannot update consumption', async () => {
    await expectRevert(
      pm.updateConsumption(ORACLE_CONSUMPTION, {from: AGENT1}),
      "Ownable: caller is not the owner."
    );
  });
});
