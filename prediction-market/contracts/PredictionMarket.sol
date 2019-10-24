pragma solidity >=0.4.21 <0.6.0;

contract PredictionMarket {
  // Stages enum
  uint BETTING = 1;
  uint RANKING = 2;
  uint CLAIMING = 3;

  // Groups
  mapping(address => Agent) public group1;
  mapping(address => Agent) public group2;
  mapping(address => Agent) public group3;
  mapping(uint => uint) stageToGroupNumber; // only used in stageToGroup()

  function stageToGroup(uint stage) private view returns(mapping(address => Agent) storage) {
    uint group = stageToGroupNumber[stage];
    if (group == 1) {
      return group1;
    } else if (group == 2) {
      return group2;
    } else {
      return group3;
    }
  }

  mapping(uint => GroupInfo) stageToGroupInfo;

  struct Agent {
    uint amountBet;
    uint demandPrediction;
    bool won;
  }

  // TODO change name
  struct GroupInfo {
    address[] agents; // keyset to group
    uint totalWinners;
    uint totalBetAmount;
    uint consumption;
  }

  uint WINNING_THRESHOLD = 100;

  constructor() public {
    stageToGroupNumber[BETTING] = 1;
    stageToGroupNumber[RANKING] = 2;
    stageToGroupNumber[CLAIMING] = 3;

    // stageToGroupInfo[BETTING] = GroupInfo(agents1, 0, 0, 0);
    // stageToGroupInfo[RANKING] = GroupInfo(agents2, 0, 0, 0);
    // stageToGroupInfo[CLAIMING] = GroupInfo(agents3, 0, 0, 0);
  }


  // True if agent has placed bet in current betting stage.
  function hasPlacedBet(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(BETTING);
    return group[agent].amountBet != 0;
  }

  function canRank(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(RANKING);
    return group[agent].amountBet != 0;
  }

  function canClaim(address agent) public view returns(bool) {
    mapping(address => Agent) storage group = stageToGroup(CLAIMING);
    return group[agent].amountBet != 0;
  }

  // Records bet from a specific address. Only allows for one bet per user
  // until the next day or whenever distributeWinnings is called.
  function placeBet(uint demandPrediction) public payable {
    require(!hasPlacedBet(msg.sender), "Agent has already bet");

    mapping(address => Agent) storage group = stageToGroup(BETTING);
    GroupInfo storage groupInfo = stageToGroupInfo[BETTING];

    group[msg.sender].amountBet = msg.value;
    group[msg.sender].demandPrediction = demandPrediction;
    group[msg.sender].won = false;
    groupInfo.agents.push(msg.sender);
    groupInfo.totalBetAmount += msg.value;
  }

  function rank() public payable {
    require(canRank(msg.sender), "Agent cannot rank now");

    mapping(address => Agent) storage group = stageToGroup(RANKING);
    GroupInfo storage groupInfo = stageToGroupInfo[RANKING];
    uint demandPrediction = group[msg.sender].demandPrediction;
    if (demandPrediction <= groupInfo.consumption + WINNING_THRESHOLD && demandPrediction >= groupInfo.consumption - WINNING_THRESHOLD) {
      group[msg.sender].won = true;
      groupInfo.totalWinners++;
    }
  }

  // Distribute winnings back to agents who bet.
  // TODO agent removing itself from agent key set
  function claimWinnings() public payable {
    require(canClaim(msg.sender), "Agent cannot claim at this time");

    mapping(address => Agent) storage group = stageToGroup(CLAIMING);
    GroupInfo storage groupInfo = stageToGroupInfo[CLAIMING];
    if (group[msg.sender].won) {
      uint reward = groupInfo.totalBetAmount / groupInfo.totalWinners;
      msg.sender.transfer(reward);
    }
    delete group[msg.sender];
  }

  function updateConsumption(uint consumption) public payable {
    // TODO require that the address of the sender is Oracle
    address[] storage agents = stageToGroupInfo[CLAIMING].agents;
    mapping(address => Agent) storage group = stageToGroup(CLAIMING);

    for (uint i = 0; i < agents.length; i++) {
      delete group[agents[i]];
    }

    agents.length = 0;

    uint tmp = BETTING;
    BETTING = CLAIMING;
    CLAIMING = RANKING;
    RANKING = tmp;

    stageToGroupInfo[RANKING].consumption = consumption;
  }
}
