pragma solidity >=0.4.21 <0.6.0;

import "../node_modules/@openzeppelin/contracts/math/SafeMath.sol";
import "../node_modules/@openzeppelin/contracts/ownership/Ownable.sol";

contract PredictionMarket is Ownable {
  using SafeMath for uint256;

  // Group stages
  uint256 public BETTING = 1;
  uint256 public WAITING = 2;
  uint256 public CLAIMING = 3;

  uint256 public TOP_TIER_THRESHOLD = 75;    // Threshold for top tier bet winners
  uint256 public MID_TIER_THRESHOLD = 150;   // Threshold for mid tier bet winners
  uint256 public TOP_TIER_WINNING_SCALE = 3; // Scaled winnings for top tier winners
  uint256 public MID_TIER_WINNING_SCALE = 1; // Scaled winnings for mid tier winners
  uint256 public BASE_WINNING_SCALE = 0;     // Base winnings scale

  uint256 public PREDICTIONS_PER_BET = 48;   // Number of predictions within a bet
  uint256 public STAGE_LENGTH = 24;          // Number of time periods within a stage

  uint256 public currTimePeriod = 0;         // Index of current period within 24 hour period
  uint256 public currDay = 0;                // Current day relative to start of contract life

  // Groups: mapping of agent's addresses to their bets.
  mapping(address => Bet) public group1;
  mapping(address => Bet) public group2;
  mapping(address => Bet) public group3;
  mapping(uint256 => uint256) stageToGroupNumber; // Only used in stageToGroup() and constructor()

  mapping(address => mapping(uint256 => Bet)) public history;
  mapping(uint256 => uint256[48]) public oracleHistory;
  mapping(uint256 => uint256[48]) public averagePredictionsHistory;
  mapping(uint256 => uint256) public groupCountHistory;

  // Returns the group corresponding to a Stage.
  function stageToGroup(uint256 stage) private view returns(mapping(address => Bet) storage) {
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

  struct Bet {
    uint256 amount;
    uint256[48] predictions;
    uint256 winningScale;
    uint256 timestamp;
  }

  struct GroupInfo {
    address[] agents;         // List of agents in the group
    uint256 topTierCount;
    uint256 midTierCount;
    uint256 baseCount;
    uint256 totalBetAmount;
    uint256[] consumption;    // Oracle-provided actual aggregate demand
  }

  constructor() public {
    stageToGroupNumber[BETTING] = 1;
    stageToGroupNumber[WAITING] = 2;
    stageToGroupNumber[CLAIMING] = 3;
  }

  // Returns true if agent can place a bet in current betting stage.
  function canBet(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(BETTING);
    return group[agent].amount == 0 && currTimePeriod < STAGE_LENGTH;
  }

  // Returns true if agent can rank in current claiming stage.
  function canRank(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    return group[agent].amount != 0 && currTimePeriod < STAGE_LENGTH;
  }

  // Returns true if agent can claim winnings in current claiming stage.
  function canClaim(address agent) public view returns(bool) {
    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    return group[agent].amount != 0 && currTimePeriod >= STAGE_LENGTH;
  }

  // Called by betting agent to place a bet. Adds the agent to the current
  // betting group.
  function placeBet(uint256[48] memory predictions) public payable {
    require(canBet(msg.sender), "Agent cannot bet at this time or has already placed a bet.");
    require(msg.value > 0, "Bet amount has to be greater than 0");

    mapping(address => Bet) storage group = stageToGroup(BETTING);
    GroupInfo storage groupInfo = stageToGroupInfo[BETTING];

    group[msg.sender].amount = msg.value;
    history[msg.sender][currDay + 1].amount = msg.value;
    group[msg.sender].predictions = predictions;
    history[msg.sender][currDay + 1].predictions = predictions;
    group[msg.sender].winningScale = BASE_WINNING_SCALE;
    history[msg.sender][currDay + 1].winningScale = BASE_WINNING_SCALE;
    group[msg.sender].timestamp = now;
    history[msg.sender][currDay + 1].timestamp = group[msg.sender].timestamp;
    groupInfo.baseCount++;
    groupInfo.agents.push(msg.sender);
    groupInfo.totalBetAmount = groupInfo.totalBetAmount.add(msg.value);

    for (uint256 i = 0; i < PREDICTIONS_PER_BET; i++) {
      averagePredictionsHistory[currDay + 1][i] = averagePredictionsHistory[currDay + 1][i].add(predictions[i]);
    }

    groupCountHistory[currDay + 2]++;
  }

  // Called by betting agent to rank themselves. Sets `win` to true if
  // `predictions` is within the threshold.
  function rank() public payable {
    require(canRank(msg.sender), "Agent cannot rank at this time");

    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];

    uint256[48] storage predictions = group[msg.sender].predictions;

    // Calculate total error
    uint256 totalErr = 0;
    for (uint256 i = 0; i < PREDICTIONS_PER_BET; i++) {
      if (groupInfo.consumption[i] > predictions[i]) {
        totalErr = totalErr.add(groupInfo.consumption[i].sub(predictions[i]));
      } else {
        totalErr = totalErr.add(predictions[i].sub(groupInfo.consumption[i]));
      }
    }

    if (totalErr <= TOP_TIER_THRESHOLD * PREDICTIONS_PER_BET) {
      group[msg.sender].winningScale = TOP_TIER_WINNING_SCALE;
      history[msg.sender][currDay - 1].winningScale = TOP_TIER_WINNING_SCALE;
      groupInfo.topTierCount++;
      groupInfo.baseCount--;
    } else if (totalErr <= MID_TIER_THRESHOLD * PREDICTIONS_PER_BET) {
      group[msg.sender].winningScale = MID_TIER_WINNING_SCALE;
      history[msg.sender][currDay - 1].winningScale = MID_TIER_WINNING_SCALE;
      groupInfo.midTierCount++;
      groupInfo.baseCount--;
    }
  }

  // Distribute winnings back to agents who bet.
  function claimWinnings() public payable {
    require(canClaim(msg.sender), "Agent cannot claim at this time");

    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];
    Bet storage bet = group[msg.sender];

    uint256 denominator = groupInfo.baseCount * BASE_WINNING_SCALE +
                          groupInfo.midTierCount * MID_TIER_WINNING_SCALE +
                          groupInfo.topTierCount * TOP_TIER_WINNING_SCALE;
    uint256 reward = 0;
    if (denominator != 0) {
      reward = (bet.winningScale.mul(groupInfo.totalBetAmount)).div(denominator);
    }

    msg.sender.transfer(reward);

    delete group[msg.sender];
    // TODO: agent removing itself from agent key set.
  }

  // Called by Oracle to tell contract the consumption for a time period.
  function updateConsumption(uint256 consumption) public payable onlyOwner {
    // TODO: require that the address of the sender is Oracle.
    stageToGroupInfo[WAITING].consumption.push(consumption);
    oracleHistory[currDay][currTimePeriod] = consumption;
    currTimePeriod++;

    if (currTimePeriod == PREDICTIONS_PER_BET) {
      // Recording list of betting agents in group history
      GroupInfo storage bettingGroupInfo = stageToGroupInfo[BETTING];
      GroupInfo storage claimingGroupInfo = stageToGroupInfo[CLAIMING];
      address[] storage agents = claimingGroupInfo.agents;
      mapping(address => Bet) storage group = stageToGroup(CLAIMING);

      // Clear group info and group mapping.
      for (uint256 i = 0; i < agents.length; i++) {
        delete group[agents[i]];
      }

      agents.length = 0;
      claimingGroupInfo.totalBetAmount = 0;
      claimingGroupInfo.baseCount = 0;
      claimingGroupInfo.midTierCount = 0;
      claimingGroupInfo.topTierCount = 0;
      claimingGroupInfo.consumption.length = 0;

      uint256 tmp = BETTING;
      BETTING = CLAIMING;
      CLAIMING = WAITING;
      WAITING = tmp;

      // Reached a new day, reset currTimePeriod and increment currDay
      currTimePeriod = 0;
      currDay++;
    }

  }

  // Get calling agent's predictions for stage
  function getBetPredictionsFromStage(uint256 stage) public view returns(uint256[48] memory) {
    return stageToGroup(stage)[msg.sender].predictions;
  }

  // Get calling agent's predictions for (day ahead - day offset)
  function getPredictions(uint256 dayOffset) public view returns(uint256[48] memory) {
    return getPredictionsForAddress(msg.sender, dayOffset);
  }

  // Get addr's predictions for (day ahead - day offset)
  function getPredictionsForAddress(address addr, uint256 dayOffset) public view returns(uint256[48] memory) {
    return history[addr][currDay + 1 - dayOffset].predictions;
  }

  // Get average prediction for (day ahead - day offset)
  function getAveragePredictions(uint256 dayOffset) public view returns(uint256[48] memory) {
    uint256 numAgents = groupCountHistory[currDay + 2 - dayOffset];
    uint256[48] memory averagePredictions;
    if (numAgents == 0) return averagePredictions;
    for (uint256 i = 0; i < PREDICTIONS_PER_BET; i++) {
      averagePredictions[i] = averagePredictionsHistory[currDay + 1 - dayOffset][i].div(numAgents);
    }
    return averagePredictions;
  }

  // Get Oracle consumptions for stage
  function getOracleConsumptionsFromStage(uint256 stage) public view returns(uint256[] memory) {
    return stageToGroupInfo[stage].consumption;
  }

  // Get Oracle consumptions for (day ahead - day offset)
  function getOracleConsumptions(uint256 dayOffset) public view returns(uint256[48] memory) {
    return oracleHistory[currDay + 1 - dayOffset];
  }

  // Get array of agents that have placed a bet in the current betting period
  function getCurrentParticipants() public view returns(address[] memory) {
    return stageToGroupInfo[BETTING].agents;
  }

  // Get bet's winning scale for (day ahead - day offset)
  function getBetWinningScale(uint256 dayOffset) public view returns(uint256) {
    return history[msg.sender][currDay + 1 - dayOffset].winningScale;
  }

  // Get agent bet predictions from history over past 7 days. Always returns bets in betting, waiting,
  // claiming stages at first 3 indices, if any.
  function getBetPredictionsForAgent() public view returns(uint256[48][7] memory) {
    uint256[48][7] memory agentPredictions;
    for (uint256 i = 0; i < 7; i++) {
      agentPredictions[i] = history[msg.sender][currDay + 1 - i].predictions;
    }

    return agentPredictions;
  }

  // Get agent bet amounts from history over past 7 days. Always returns bets in betting, waiting,
  // claiming stages at first 3 indices, if any.
  function getBetAmountsForAgent() public view returns(uint256[7] memory) {
    uint256[7] memory betAmounts;
    for (uint256 i = 0; i < 7; i++) {
      betAmounts[i] = history[msg.sender][currDay + 1 - i].amount;
    }

    return betAmounts;
  }

  // Get agent bet winning scales from history over past 7 days. Always returns bets in betting, waiting,
  // claiming stages at first 3 indices, if any.
  function getBetWinningScalesForAgent() public view returns(uint256[7] memory) {
    uint256[7] memory winningScales;
    for (uint256 i = 0; i < 7; i++) {
      winningScales[i] = history[msg.sender][currDay + 1 - i].winningScale;
    }

    return winningScales;
  }

  // Get agent bet timestamps from history over past 7 days. Always returns bets in betting, waiting,
  // claiming stages at first 3 indices, if any.
  function getBetTimestampsForAgent() public view returns(uint256[7] memory) {
    uint256[7] memory betTimestamps;
    for (uint256 i = 0; i < 7; i++) {
      betTimestamps[i] = history[msg.sender][currDay + 1 - i].timestamp;
    }

    return betTimestamps;
  }

}
