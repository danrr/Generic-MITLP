// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SmartContract {

    struct PuzzlePart {
        uint coin;
        uint upperBound;
        bytes commitment;
        bytes solution;
        bool paidOut;
    }

    enum Status { Setup, SettingCommitments, Solving }

    modifier onlyHelper() {
        require(msg.sender == helperID, "Only the helper can call this function.");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    // TODO - consider batching the events (in groups to reduce the fixed costs)
    event Initialized( uint256 index, uint256 coins, uint256 upperBound, bytes32 prevPuzzleDetailsStorageHash);
    event CommitmentSet(uint256 index, bytes32 commitment, bytes32 prevPuzzleCommitmentStorageHash);
    event SolutionReceived(uint256 revIndex, bytes solution, bytes witness);

    address public helperID;
    uint256 public startTime;
    Status public contractStatus = Status.Setup;

    bytes32 public puzzleDetailsStorageHash = bytes32(0);
    bytes32 public puzzleCommitmentStorageHash = bytes32(0);

    uint256 public amountOfPuzzleParts = 0;
    address public owner;

    constructor() payable public {
        owner = msg.sender;
    }

    function initialize(
        uint[] memory _coins,
        uint[] memory _upperBounds,
        address _helperID
    ) public payable onlyOwner {

        require(_coins.length == _upperBounds.length, "The length of the coins and upperBounds arrays should be the same.");
        require(_coins.length > 0, "The length of the coins array should be greater than 0.");
        require(_helperID != address(0), "The helper ID should not be the zero address.");
        require(contractStatus == Status.Setup, "Contract setup is already completed.");
        require(amountOfPuzzleParts == 0, "The amount of puzzle parts should be 0.");

        helperID = _helperID;
        startTime = block.timestamp;
        owner = msg.sender;

        bytes32 _puzzleDetailsStorageHash = puzzleDetailsStorageHash;

        uint256 receivedValue = msg.value;

        for (uint256 i = _coins.length; i > 0; i--) {
                uint256 index = i - 1;

                emit Initialized(index, _coins[index], _upperBounds[index], _puzzleDetailsStorageHash);

                _puzzleDetailsStorageHash = _hashPuzzleDetails(_coins[index], _upperBounds[index], _puzzleDetailsStorageHash);
                receivedValue -= _coins[index];

        }

        require(receivedValue == 0, "The total value sent should be equal to the sum of the coins.");

        amountOfPuzzleParts += _coins.length;
        puzzleDetailsStorageHash = _puzzleDetailsStorageHash;
    }

    function setCommitments(bytes32[] calldata _commitments) public onlyHelper {
        // Change status to SettingCommitments on the first call
        if (contractStatus == Status.Setup) {
            contractStatus = Status.SettingCommitments;
        }

        require(contractStatus == Status.SettingCommitments, "Contract is not in SettingCommitments status.");
        require(_commitments.length == amountOfPuzzleParts, "The length of the commitments array should be equal to the amount of puzzle parts.");

        bytes32 _puzzleCommitmentStorageHash = puzzleCommitmentStorageHash;
        for (uint256 i = _commitments.length; i > 0; i--) {
            uint256 index = i - 1;

            emit CommitmentSet(index, _commitments[index], _puzzleCommitmentStorageHash);
            _puzzleCommitmentStorageHash = _hashPuzzleCommitment(_commitments[index], _puzzleCommitmentStorageHash);
        }

        puzzleCommitmentStorageHash = _puzzleCommitmentStorageHash;
        contractStatus = Status.Solving;
    }

    function addSolution(bytes calldata solution, bytes calldata witness, bytes32 commitment, bytes32 prevPuzzleCommitmentStorageHash, uint256 coin, uint256 upperBound, bytes32 prevPuzzleDetailsStorageHash) public {
        require(contractStatus == Status.Solving, "Contract is not in Solving status.");
        require(puzzleDetailsStorageHash != bytes32(0), "All puzzle parts have already been solved.");
        require(puzzleCommitmentStorageHash != bytes32(0), "All puzzle parts have already been solved.");


        require(puzzleCommitmentStorageHash == _hashPuzzleCommitment(commitment, prevPuzzleCommitmentStorageHash), "The provided puzzle commitment is not correct.");
        require(checkSolution(solution, witness, commitment), "The solution is not correct.");

        require(puzzleDetailsStorageHash == _hashPuzzleDetails(coin, upperBound, prevPuzzleDetailsStorageHash), "The provided puzzle details are not correct.");
        require(block.timestamp <= startTime + upperBound, "Too late: the time upper bound has been exceeded.");

        emit SolutionReceived(amountOfPuzzleParts, solution, witness);
        amountOfPuzzleParts--;

        puzzleDetailsStorageHash = prevPuzzleDetailsStorageHash;
        puzzleCommitmentStorageHash = prevPuzzleCommitmentStorageHash;

        // Once the solution is correct, the solver should be paid
        pay(coin, msg.sender);
    }

    /// We do not need to check if the puzzle part has already been paid out, because after the payment the puzzle details are updated to the next puzzle part.
    /// This assumes hash functions are collision-resistant.
    function pay(uint coin, address solver) internal {
        payable(solver).transfer(coin);
    }

    /// If the time upper bound has been exceeded, the owner can call this function to get the money back.
    /// This way they cancel the latest puzzle part and get their money back.
    function payBack(bytes32 commitment, bytes32 prevPuzzleCommitmentStorageHash, uint256 coin, uint256 upperBound, bytes32 prevPuzzleDetailsStorageHash) public onlyOwner {
        require(puzzleCommitmentStorageHash == _hashPuzzleCommitment(commitment, prevPuzzleCommitmentStorageHash), "The provided puzzle commitment is not correct.");
        require(puzzleDetailsStorageHash == _hashPuzzleDetails(coin, upperBound, prevPuzzleDetailsStorageHash), "The provided puzzle details are not correct.");
        require(block.timestamp > startTime + upperBound, "Too late: the time upper bound has been exceeded.");

        puzzleDetailsStorageHash = prevPuzzleDetailsStorageHash;
        puzzleCommitmentStorageHash = prevPuzzleCommitmentStorageHash;
        payable(owner).transfer(coin);
    }

    function checkSolution(bytes calldata solution, bytes calldata witness, bytes32 commitment) public pure returns (bool) {
        bytes memory concatenated = abi.encodePacked(solution, witness);
        bytes32 hash = keccak256(concatenated);

        return (hash == commitment);
    }

    function _hashPuzzleDetails(uint256 coin, uint256 upperBound, bytes32 prevHash) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(coin, upperBound, prevHash));
    }

    function _hashPuzzleCommitment(bytes32 commitment, bytes32 prevHash) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(commitment, prevHash));
    }

}

