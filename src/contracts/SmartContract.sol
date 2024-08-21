// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SmartContract {

    struct PuzzlePart {
        uint coin;
        uint upperBound;
        uint extraTime;
        bytes commitment;
        bytes solution;
        bytes witness;
        uint256 timestamp;
        address solver;
        bool paidOut;
    }

    modifier onlyHelper() {
        require(msg.sender == helperID, "Only the helper can call this function.");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    uint public startTime;
    uint public extraTime;
    address public helperID;
    uint public initialTimestamp;

    mapping(uint => PuzzlePart) public puzzleParts;
    uint amountOfPuzzleParts;
    uint public nextUnsolvedPuzzlePart = 0;
    address owner;

    constructor() public payable {
        owner = msg.sender;
    }

    function initialize(
        uint[] memory _coins,
        uint _startTime,
        uint[] memory _extraTimes,
        uint[] memory _upperBounds,
        address _helperID
    ) public payable onlyOwner {

        require(_coins.length == _upperBounds.length, "The length of the coins and upperBounds arrays should be the same.");
        require(_coins.length > 0, "The length of the coins array should be greater than 0.");
        require(_helperID != address(0), "The helper ID should not be the zero address.");

        startTime = _startTime;
        helperID = _helperID;
        initialTimestamp = block.timestamp;

        uint receivedValue = msg.value;
        for (uint i = 0; i < _coins.length; i++) {
            puzzleParts[i] = PuzzlePart({
                coin: _coins[i],
                upperBound: _upperBounds[i],
                extraTime: _extraTimes[i],
                commitment: "",
                solution: "",
                witness: "",
                timestamp: 0,
                solver: address(0),
                paidOut: false
            });
            receivedValue -= _coins[i];
        }

        require(receivedValue == 0, "The total value sent should be equal to the sum of the coins.");

        amountOfPuzzleParts = _coins.length;
    }


    function commitments() public view returns (bytes[] memory) {
        bytes[] memory commitments = new bytes[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            commitments[i] = puzzleParts[i].commitment;
        }
        return commitments;
    }

    function setCommitments(bytes[] calldata _commitments) public onlyHelper {
        require(_commitments.length == amountOfPuzzleParts, "The length of the commitments array should be equal to the amount of puzzle parts.");
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            puzzleParts[i].commitment = _commitments[i];
        }
    }

    function coins() public view returns (uint[] memory) {
        uint[] memory coins = new uint[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            coins[i] = puzzleParts[i].coin;
        }
        return coins;
    }

    function upperBounds() public view returns (uint[] memory) {
        uint[] memory upperBounds = new uint[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            upperBounds[i] = puzzleParts[i].upperBound;
        }
        return upperBounds;
    }

    function addSolution(bytes calldata solution, bytes calldata witness) public {
        puzzleParts[nextUnsolvedPuzzlePart].solution = solution;
        puzzleParts[nextUnsolvedPuzzlePart].witness = witness;
        puzzleParts[nextUnsolvedPuzzlePart].timestamp = block.timestamp;
        puzzleParts[nextUnsolvedPuzzlePart].solver = msg.sender;
        nextUnsolvedPuzzlePart++;
    }

    function getCommitmentAt(uint puzzlePartIndex) public view returns (bytes memory) {
        require(puzzlePartIndex < amountOfPuzzleParts, "The puzzle part index is out of bounds.");
        require(puzzleParts[puzzlePartIndex].commitment.length > 0, "The commitment is not set yet.");
        return puzzleParts[puzzlePartIndex].commitment;
    }

    function getSolutionAt(uint puzzlePartIndex) public returns (bytes memory, bytes memory, uint) {
        require(puzzlePartIndex < amountOfPuzzleParts, "The puzzle part index is out of bounds.");

        bytes memory solutionMemory = puzzleParts[puzzlePartIndex].solution;
        bytes memory witnessMemory = puzzleParts[puzzlePartIndex].witness;
        uint timestamp = puzzleParts[puzzlePartIndex].timestamp;

        return (solutionMemory, witnessMemory, timestamp);
    }

    function getUpperBoundAt(uint puzzlePartIndex) public view returns (uint) {
        require(puzzlePartIndex < amountOfPuzzleParts, "The puzzle part index is out of bounds.");
        return puzzleParts[puzzlePartIndex].upperBound;
    }

    function solutions() public view returns (bytes[] memory, bytes[] memory, uint[] memory) {
        bytes[] memory solutions = new bytes[](amountOfPuzzleParts);
        bytes[] memory witnesses = new bytes[](amountOfPuzzleParts);
        uint[] memory timestamps = new uint[](amountOfPuzzleParts);
        for (uint i = 0; i < amountOfPuzzleParts; i++) {
            solutions[i] = puzzleParts[i].solution;
            witnesses[i] = puzzleParts[i].witness;
            timestamps[i] = puzzleParts[i].timestamp;
        }
        return (solutions, witnesses, timestamps);
    }

    function pay(uint puzzlePartIndex) public onlyOwner {
        require(!puzzleParts[puzzlePartIndex].paidOut, "The puzzle part has already been paid out.");
        puzzleParts[puzzlePartIndex].paidOut = true;
        payable(puzzleParts[puzzlePartIndex].solver).transfer(puzzleParts[puzzlePartIndex].coin);
    }

    function payBack(uint puzzlePartIndex) public onlyOwner {
        require(!puzzleParts[puzzlePartIndex].paidOut, "The puzzle part has already been paid out.");
        puzzleParts[puzzlePartIndex].paidOut = true;
        payable(owner).transfer(address(this).balance);
    }
}

