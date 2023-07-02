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

    function placeBid(uint contractIndex) external payable {
        Contract storage contractData = contracts[contractIndex];

        require(
            msg.value > contractData.minBid,
            "Bid amount is less than the minimum bid."
        );
        require(
            block.timestamp >= contractData.startTime,
            "Auction has not started yet."
        );
        require(
            block.timestamp < contractData.finishTime,
            "Auction has ended."
        );

        if (!contractData.publicAuction) {
            bool allowed = false;
            for (uint i = 0; i < contractData.members.length; i++) {
                if (contractData.members[i] == msg.sender) {
                    allowed = true;
                    break;
                }
            }
            require(allowed, "You are not allowed to bid in this auction.");
        }

        if (bids[msg.sender][contractIndex] == 0) {
            contractData.bidders.push(msg.sender);
        }

        bids[msg.sender][contractIndex] += msg.value;
    }

    function findTheWinner(uint contractIndex) external payable {
        Contract storage contractData = contracts[contractIndex];

        address winner;
        uint highestBid = 0;

        for (uint i = 0; i < contractData.bidders.length; i++) {
            address bidder = contractData.bidders[i];
            uint bidAmount = bids[bidder][contractIndex];

            if (bidAmount > highestBid) {
                winner = bidder;
                highestBid = bidAmount;
            }
        }

        payable(contractData.contractAddress).transfer(highestBid);

        for (uint i = 0; i < contractData.bidders.length; i++) {
            address bidder = contractData.bidders[i];
            uint bidAmount = bids[bidder][contractIndex];

            if (bidder != winner) {
                payable(bidder).transfer(bidAmount);
            }

            delete bids[bidder][contractIndex];
        }

        delete contractData.bidders;
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
}
