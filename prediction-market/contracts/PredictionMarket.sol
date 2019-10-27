pragma solidity >=0.4.21 <0.6.0;

import "../node_modules/@openzeppelin/contracts/math/SafeMath.sol";

contract PredictionMarket {
  using SafeMath for uint256;

  // Stages
  uint256 public BETTING = 1;
  uint256 public RANKING = 2;
  uint256 public CLAIMING = 3;

  // Groups
  mapping(address => Agent) public group1;
  mapping(address => Agent) public group2;
  mapping(address => Agent) public group3;
  mapping(uint256 => uint256) stageToGroupNumber; // Only used in stageToGroup() and constructor()

  // Returns the group corresponding to a Stage.
  function stageToGroup(uint256 stage) private view returns(mapping(address => Agent) storage) {
    uint256 group = stageToGroupNumber[stage];
    if (group == 1) {
      return group1;
    } else if (group == 2) {
      return group2;
    } else {
      return group3;
    }
  }

  mapping(uint256 => GroupInfo) public stageToGroupInfo;

  struct Agent {
    uint256 amountBet;
    uint256 demandPrediction;
    bool win;
  }

  // TODO: think if name is semantically correct.
  struct GroupInfo {
    address[] agents;       // Keyset to corresponding group
    uint256 totalWinners;
    uint256 totalBetAmount;
    uint256 consumption;    // Oracle-provided actual aggregate demand
  }

  uint256 WINNING_THRESHOLD = 100;

  constructor() public {
    stageToGroupNumber[BETTING] = 1;
    stageToGroupNumber[RANKING] = 2;
    stageToGroupNumber[CLAIMING] = 3;
  }


  // Returns true if agent has placed bet in current betting stage.
  function hasPlacedBet(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(BETTING);
    return group[agent].amountBet != 0;
  }

  // Returns true if agent can rank in current ranking stage.
  function canRank(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(RANKING);
    return group[agent].amountBet != 0;
  }

  // Returns true if agent can claim winnings in current claiming stage.
  function canClaim(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(CLAIMING);
    return group[agent].amountBet != 0;
  }

  // Called by betting agent to place a bet. Adds the agent to the current
  // betting group.
  function placeBet(uint256 demandPrediction) public payable {
    require(!hasPlacedBet(msg.sender), "Agent has already bet");

    mapping(address => Agent) storage group = stageToGroup(BETTING);
    GroupInfo storage groupInfo = stageToGroupInfo[BETTING];

    group[msg.sender].amountBet = msg.value;
    group[msg.sender].demandPrediction = demandPrediction;
    group[msg.sender].win = false;
    groupInfo.agents.push(msg.sender);
    groupInfo.totalBetAmount = groupInfo.totalBetAmount.add(msg.value);
  }

  // Called by betting agent to rank themselves. Sets `win` to true if
  // `demandPrediction` is within the threshold.
  function rank() public payable {
    require(canRank(msg.sender), "Agent cannot rank now");

    mapping(address => Agent) storage group = stageToGroup(RANKING);
    GroupInfo storage groupInfo = stageToGroupInfo[RANKING];

    uint256 demandPrediction = group[msg.sender].demandPrediction;
    if (demandPrediction <= groupInfo.consumption + WINNING_THRESHOLD &&
        demandPrediction >= groupInfo.consumption - WINNING_THRESHOLD) {
      group[msg.sender].win = true;
      groupInfo.totalWinners++;
    }
  }

  // Distribute winnings back to agents who bet.
  function claimWinnings() public payable {
    require(canClaim(msg.sender), "Agent cannot claim at this time");

    mapping(address => Agent) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];

    if (group[msg.sender].win) {
      uint256 reward = groupInfo.totalBetAmount / groupInfo.totalWinners;
      msg.sender.transfer(reward);
    }
    delete group[msg.sender];
    // TODO: agent removing itself from agent key set.
  }

  // Called by Oracle to tell contract the aggregate demand for a time period.
  function updateConsumption(uint256 consumption) public payable {
    // TODO: require that the address of the sender is Oracle.
    address[] storage agents = stageToGroupInfo[CLAIMING].agents;
    mapping(address => Agent) storage group = stageToGroup(CLAIMING);

    for (uint256 i = 0; i < agents.length; i++) {
      delete group[agents[i]];
    }

    agents.length = 0;

    // Rotate stages.
    // TODO: not sure about the logic of this. Also can't do it because uint cannot be negative.
    // BETTING = (BETTING - 1).mod(3);
    // RANKING = (RANKING - 1).mod(3);
    // CLAIMING = (CLAIMING - 1).mod(3);

    uint256 tmp = BETTING;
    BETTING = CLAIMING;
    CLAIMING = RANKING;
    RANKING = tmp;

    stageToGroupInfo[RANKING].consumption = consumption;
  }
}
