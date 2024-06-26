// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SmartContract {

    struct PuzzlePart {
        uint coin;
        uint upperBound;
        uint256 commitment;
        uint256 solution;
        uint256 witness;
        uint256 timestamp;
        address solver;
        bool paidOut;
    }

    modifier onlyHelper() {
        require(msg.sender == helperID, "Only the helper can call this function.");
        _;
    }

    uint public startTime;
    uint public extraTime;
    address public helperID;
    uint public initialTimestamp;

    mapping(uint => PuzzlePart) public puzzleParts;
    uint amountOfPuzzleParts;
    uint public nextUnsolvedPuzzlePart = 0;

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
                solution: 0,
                witness: 0,
                timestamp: 0,
                solver: address(0),
                paidOut: false
            });
            receivedValue -= _coins[i];
        }

        require(receivedValue == 0, "The total value sent should be equal to the sum of the coins.");


        amountOfPuzzleParts = _coins.length;

    }

    function commitments() public returns (uint256[] memory) {
        uint256[] memory commitments = new uint256[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            commitments[i] = puzzleParts[i].commitment;
        }
        return commitments;
    }

    function setCommitments(uint256[] calldata _commitments) public onlyHelper {
        require(_commitments.length == amountOfPuzzleParts, "The length of the commitments array should be equal to the amount of puzzle parts.");
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            puzzleParts[i].commitment = _commitments[i];
        }
    }

    function coins() public returns (uint[] memory) {
        uint[] memory coins = new uint[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            coins[i] = puzzleParts[i].coin;
        }
        return coins;
    }

    function upperBounds() public returns (uint[] memory) {
        uint[] memory upperBounds = new uint[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            upperBounds[i] = puzzleParts[i].upperBound;
        }
        return upperBounds;
    }

    function addSolution(uint256 solution, uint256 witness) public {
        puzzleParts[nextUnsolvedPuzzlePart].solution = solution;
        puzzleParts[nextUnsolvedPuzzlePart].witness = witness;
        puzzleParts[nextUnsolvedPuzzlePart].timestamp = block.timestamp;
        puzzleParts[nextUnsolvedPuzzlePart].solver = msg.sender;
        nextUnsolvedPuzzlePart++;
    }

    function getSolutionAt(uint puzzlePartIndex) public view returns (uint256) {
        return puzzleParts[puzzlePartIndex].solution;
    }

    function payout(uint puzzlePartIndex) public onlyHelper {
        require(!puzzleParts[puzzlePartIndex].paidOut, "The puzzle part has already been paid out.");
        puzzleParts[puzzlePartIndex].paidOut = true;
        payable(puzzleParts[puzzlePartIndex].solver).transfer(puzzleParts[puzzlePartIndex].coin);

    }
}

