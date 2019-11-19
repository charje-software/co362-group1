pragma solidity >=0.4.21 <0.6.0;

import "../node_modules/@openzeppelin/contracts/math/SafeMath.sol";

contract PredictionMarket {
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

  mapping(address => mapping(uint256 => uint256[48])) public history;
  mapping(uint256 => uint256[48]) public oracleHistory;

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
    uint256[] predictions;
    uint256 winningScale;
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
    group[msg.sender].predictions = predictions;
    group[msg.sender].winningScale = BASE_WINNING_SCALE;
    groupInfo.baseCount++;
    groupInfo.agents.push(msg.sender);
    groupInfo.totalBetAmount = groupInfo.totalBetAmount.add(msg.value);

    history[msg.sender][currDay + 1] = predictions;
  }

  // Called by betting agent to rank themselves. Sets `win` to true if
  // `predictions` is within the threshold.
  function rank() public payable {
    require(canRank(msg.sender), "Agent cannot rank at this time");

    mapping(address => Bet) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];

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

    if (totalErr <= TOP_TIER_THRESHOLD * PREDICTIONS_PER_BET) {
      group[msg.sender].winningScale = TOP_TIER_WINNING_SCALE;
      groupInfo.topTierCount++;
      groupInfo.baseCount--;
    } else if (totalErr <= MID_TIER_THRESHOLD * PREDICTIONS_PER_BET) {
      group[msg.sender].winningScale = MID_TIER_WINNING_SCALE;
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
    uint256 reward = (bet.winningScale.mul(groupInfo.totalBetAmount)).div(denominator);
    msg.sender.transfer(reward);

    delete group[msg.sender];
    // TODO: agent removing itself from agent key set.
  }

  // Called by Oracle to tell contract the consumption for a time period.
  function updateConsumption(uint256 consumption) public payable {
    // TODO: require that the address of the sender is Oracle.
    stageToGroupInfo[WAITING].consumption.push(consumption);
    oracleHistory[currDay][currTimePeriod] = consumption;
    currTimePeriod++;

    if (currTimePeriod == PREDICTIONS_PER_BET) {
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

  function getBetPredictionsFromStage(uint256 stage) public view returns(uint256[] memory) {
    return stageToGroup(stage)[msg.sender].predictions;
  }

  function getOracleConsumptionFromStage(uint256 stage) public view returns(uint256[] memory) {
    return stageToGroupInfo[stage].consumption;
  }

  // Get predictions for (day ahead - day offset)
  // Note: we do not need to check if (dayOffset > currDay + 1) because uint256 wraps
  // around to the max uint value, which will map to an uninitialised array.
  function getPredictions(uint256 dayOffset) public view returns(uint256[48] memory) {
    return history[msg.sender][currDay + 1 - dayOffset];
  }

  // Get Oracle consumptions for (day ahead - day offset)
  function getOracleConsumptions(uint256 dayOffset) public view returns(uint256[48] memory) {
    return oracleHistory[currDay + 1 - dayOffset];
  }
}
