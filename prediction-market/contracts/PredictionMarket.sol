pragma solidity >=0.4.21 <0.6.0;

contract PredictionMarket {
  address payable[] public agents;
  address owner;
  uint256 public balance;
  struct Agent {
    uint256 amountBet;
  }

  mapping(address => Agent) public agentInfo;

  constructor() public {
    owner = msg.sender;
    balance = 0;
  }

  function agentExists(address payable agent) public view returns(bool) {
    for (uint256 i = 0; i < agents.length; i++) {
      if (agents[i] == agent) return true;
    }
    return false;
  }

  function placeBet(uint256 amount) public payable {
    require(!agentExists(msg.sender), "Agent has already betted");
    require(amount == msg.value, "Transferred incorrect amount of Ether");
    agentInfo[msg.sender].amountBet = msg.value;
    agents.push(msg.sender);
    balance = address(this).balance;
  }

  function distributeWinnings() public {
    require(agents.length > 0, "No one has betted");
    address payable winner = agents[0];
    winner.transfer(agentInfo[winner].amountBet);
  }
}
