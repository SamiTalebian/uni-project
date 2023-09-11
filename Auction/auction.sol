// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Auction {
    struct Contract {
        address contractAddress;
        uint startTime;
        uint finishTime;
        uint minBid;
        address[] bidders;
        address[] members;
        bool publicAuction;
    }

    Contract[] public contracts;
    mapping(address => mapping(uint => uint)) public bids;
    event Transfer(address indexed from, address indexed to, uint256 value);

    function createContract(
        address contractAddress,
        uint startTime,
        uint finishTime,
        uint minBid,
        address[] memory members,
        bool publicAuction
    ) external {
        require(startTime < finishTime, "Invalid finish time.");
        require(minBid > 0, "Invalid minimum bid.");

        contracts.push(
            Contract(
                contractAddress,
                startTime,
                finishTime,
                minBid,
                new address[](0),
                members,
                publicAuction
            )
        );
    }

    function addMember(uint contractIndex, address member) external {
        Contract storage contractData = contracts[contractIndex];

        // require(
        //     msg.sender == contractData.contractAddress,
        //     "Only contract owner can add members."
        // );
        contractData.members.push(member);
    }

    function getContract(
        uint contractIndex
    )
        external
        view
        returns (
            address contractAddress,
            uint startTime,
            uint finishTime,
            uint minBid,
            address[] memory bidders,
            address[] memory members,
            bool publicAuction
        )
    {
        Contract storage contractData = contracts[contractIndex];

        return (
            contractData.contractAddress,
            contractData.startTime,
            contractData.finishTime,
            contractData.minBid,
            contractData.bidders,
            contractData.members,
            contractData.publicAuction
        );
    }

    function transferFunds(
        address payable from,
        uint256 amount
    ) external payable {
        require(msg.sender != address(0), "Invalid sender address");
        require(from != address(0), "Invalid recipient address");

        // from.transfer(amount);
        payable(msg.sender).transfer(amount);

        // Emit an event to log the transfer
        emit Transfer(from, msg.sender, amount);
    }
}
