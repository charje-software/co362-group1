pragma solidity >=0.4.21 <0.6.0;

contract PredictionMarket {
  address payable[] public agents;
  address payable owner;
  uint public totalBets;

  struct Agent {
    uint amountBet;
  }

  mapping(address => Agent) public agentInfo;

  event Distribute(address receiver, uint amount);

  constructor() public {
    owner = msg.sender;
    totalBets = address(this).balance;
  }

  function agentExists(address agent) public view returns(bool) {
    for (uint i = 0; i < agents.length; i++) {
      if (agents[i] == agent) return true;
    }
    return false;
  }

  // Records bet from a specific address. Only allows for one bet per user
  // until the next day (or whenever distributeWinnings is called) 
  function placeBet() public payable {
    require(!agentExists(msg.sender), "Agent has already bet");
    agentInfo[msg.sender].amountBet = msg.value;
    agents.push(msg.sender);
    totalBets = address(this).balance;
  }

  // Winnings are transferred back to agent. Currently 
  // transfers the same amount as you bet 
  function distributeWinnings() public payable {
    require(agentExists(msg.sender), "Agent has not bet");
    uint value = agentInfo[msg.sender].amountBet;
    msg.sender.transfer(value);
    delete agentInfo[msg.sender];
    agents.length = 0;
  }
}
