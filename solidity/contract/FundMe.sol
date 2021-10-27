//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        //uint256 minimumUSD = getConversionRate(1000000000000000000);
        //require(getConversionRate(msg.value) >= minimumUSD, "Required 1 ether or more!!!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        addressToAmountFunded[msg.sender] -= msg.value;
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = ((ethPrice * ethAmount) / 10**18);
        return ethAmountInUsd;
    }
}
