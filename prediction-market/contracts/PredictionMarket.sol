pragma solidity >=0.4.21 <0.6.0;

import "../node_modules/@openzeppelin/contracts/math/SafeMath.sol";

contract PredictionMarket {
  using SafeMath for uint256;

  // Stages
  uint256 public BETTING = 1;
  uint256 public WAITING1 = 2;
  uint256 public WAITING2 = 3;
  uint256 public WAITING3 = 4;
  uint256 public RANKING = 5;
  uint256 public CLAIMING = 6;

  // Groups: mapping of agent's addresses to their bets.
  mapping(address => Bet) public group1;
  mapping(address => Bet) public group2;
  mapping(address => Bet) public group3;
  mapping(address => Bet) public group4;
  mapping(address => Bet) public group5;
  mapping(address => Bet) public group6;
  mapping(uint256 => uint256) stageToGroupNumber; // Only used in stageToGroup() and constructor()

  // Returns the group corresponding to a Stage.
  function stageToGroup(uint256 stage) private view returns(mapping(address => Bet) storage) {
    uint256 group = stageToGroupNumber[stage];
    if (group == 1) {
      return group1;
    } else if (group == 2) {
      return group2;
    } else if (group == 3) {
      return group3;
    } else if (group == 4) {
      return group4;
    } else if (group == 5) {
      return group5;
    } else {
      return group6;
    }
  }

  mapping(uint256 => GroupInfo) public stageToGroupInfo;

  struct Bet {
    uint256 amount;
    uint256[] predictions;
    bool win;
  }

  // TODO: think if name is semantically correct.
  struct GroupInfo {
    address[] agents;       // List of agents in the group
    uint256 totalWinners;
    uint256 totalBetAmount;
    uint256[] consumption;    // Oracle-provided actual aggregate demand
  }

  uint256 public currTimePeriod = 0; // Index of current period within 24 hour period

  uint256 public WINNING_THRESHOLD = 100;
  uint256 public PREDICTIONS_PER_BET = 48;
  uint256 public STAGE_LENGTH = 24; // Number of time periods within a stage

  constructor() public {
    stageToGroupNumber[BETTING] = 1;
    stageToGroupNumber[WAITING1] = 2;
    stageToGroupNumber[WAITING2] = 3;
    stageToGroupNumber[WAITING3] = 4;
    stageToGroupNumber[RANKING] = 5;
    stageToGroupNumber[CLAIMING] = 6;
  }


  // Returns true if agent has placed bet in current betting stage.
  function hasPlacedBet(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(BETTING);
    return group[agent].amount != 0;
  }

  // Returns true if agent can rank in current ranking stage.
  function canRank(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(RANKING);
    return group[agent].amount != 0;
  }

  // Returns true if agent can claim winnings in current claiming stage.
  function canClaim(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    return group[agent].amount != 0;
  }

  // Called by betting agent to place a bet. Adds the agent to the current
  // betting group.
  function placeBet(uint256[48] memory predictions) public payable {
    require(!hasPlacedBet(msg.sender), "Agent has already placed a bet");
    require(msg.value > 0, "Bet amount has to be greater than 0");

    mapping(address => Bet) storage group = stageToGroup(BETTING);
    GroupInfo storage groupInfo = stageToGroupInfo[BETTING];

    group[msg.sender].amount = msg.value;
    group[msg.sender].predictions = predictions;
    group[msg.sender].win = false;
    groupInfo.agents.push(msg.sender);
    groupInfo.totalBetAmount = groupInfo.totalBetAmount.add(msg.value);
  }

  // Called by betting agent to rank themselves. Sets `win` to true if
  // `predictions` is within the threshold.
  function rank() public payable {
    require(canRank(msg.sender), "Agent cannot rank at this time");

    mapping(address => Bet) storage group = stageToGroup(RANKING);
    GroupInfo storage groupInfo = stageToGroupInfo[RANKING];

    uint256[] storage predictions = group[msg.sender].predictions;

    // Calculate total error
    uint256 totalErr = 0;
    for (uint256 i = 0; i < PREDICTIONS_PER_BET; i++) {
      if (groupInfo.consumption[i] > predictions[i]) {
        totalErr = totalErr.add(groupInfo.consumption[i].sub(predictions[i]));
      } else {
        totalErr = totalErr.add(predictions[i].sub(groupInfo.consumption[i]));
      }
    }

    if (totalErr <= WINNING_THRESHOLD * PREDICTIONS_PER_BET) {
      group[msg.sender].win = true;
      groupInfo.totalWinners++;
    }
  }

  // Distribute winnings back to agents who bet.
  function claimWinnings() public payable {
    require(canClaim(msg.sender), "Agent cannot claim at this time");

    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];

    if (group[msg.sender].win) {
      // As agent has won, total winners will not be 0.
      uint256 reward = groupInfo.totalBetAmount.div(groupInfo.totalWinners);
      msg.sender.transfer(reward);
    }
    delete group[msg.sender];
    // TODO: agent removing itself from agent key set.
  }

  // Called by Oracle to tell contract the consumption for a time period.
  function updateConsumption(uint256 consumption) public payable {
    // TODO: require that the address of the sender is Oracle.
    if (currTimePeriod < STAGE_LENGTH) {
      stageToGroupInfo[WAITING2].consumption.push(consumption);
    } else {
      stageToGroupInfo[WAITING3].consumption.push(consumption);
    }
    currTimePeriod++;

    if (currTimePeriod.mod(STAGE_LENGTH) == 0) {
      GroupInfo storage claimingGroupInfo = stageToGroupInfo[CLAIMING];
      address[] storage agents = claimingGroupInfo.agents;
      mapping(address => Bet) storage group = stageToGroup(CLAIMING);

      // Clear group info and group mapping.
      for (uint256 i = 0; i < agents.length; i++) {
        delete group[agents[i]];
      }

      agents.length = 0;
      claimingGroupInfo.totalBetAmount = 0;
      claimingGroupInfo.totalWinners = 0;
      claimingGroupInfo.consumption.length = 0;

      uint256 tmp = BETTING;
      BETTING = CLAIMING;
      CLAIMING = RANKING;
      RANKING = WAITING3;
      WAITING3 = WAITING2;
      WAITING2 = WAITING1;
      WAITING1 = tmp;

      // If reached a new day, reset currTimePeriod
      if (currTimePeriod == PREDICTIONS_PER_BET) {
        currTimePeriod = 0;
      }
    }

  }

  function getBetPredictionsFromStage(uint256 stage) public view returns(uint256[] memory) {
    return stageToGroup(stage)[msg.sender].predictions;
  }

  function getOracleConsumptionFromStage(uint256 stage) public view returns(uint256[] memory) {
    return stageToGroupInfo[stage].consumption;
  }
}
