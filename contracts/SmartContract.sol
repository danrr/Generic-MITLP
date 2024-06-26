// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SmartContract {

    struct PuzzlePart {
        uint coin;
        uint upperBound;
        uint256 commitment;
        uint256 solution;

    }

    uint startTime;
    uint extraTime;
    address helperID;
    uint initialTimestamp;

    mapping(uint => PuzzlePart) public puzzleParts;
    uint amountOfPuzzleParts;

    constructor(
        uint[] memory _coins,
        uint _startTime,
        uint _extraTime,
        uint[] memory _upperBounds,
        address _helperID
    ) public payable {

        require(_coins.length == _upperBounds.length, "The length of the coins and upperBounds arrays should be the same.");
        require(_coins.length > 0, "The length of the coins array should be greater than 0.");
        require(_helperID != address(0), "The helper ID should not be the zero address.");

        startTime = _startTime;
        extraTime = _extraTime;
        helperID = _helperID;
        initialTimestamp = block.timestamp;

        uint receivedValue = msg.value;
        for (uint i = 0; i < _coins.length; i++) {
            puzzleParts[i] = PuzzlePart({
                coin: _coins[i],
                upperBound: _upperBounds[i],
                commitment: 0,
                solution: 0
            });
            receivedValue -= _coins[i];
        }

        require(receivedValue == 0, "The total value sent should be equal to the sum of the coins.");


        amountOfPuzzleParts = _coins.length;

    }
}
