// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EDTLP {
    struct PuzzleDetail {
        bytes puzzle;
        bytes32 commitment;
        uint deliveryTime;
        uint coins;
        address puzzleSolver;
        bytes solution;
        bytes proof;
        bool isSolved;
        bool isDisputed;
        uint disputeEndTime; // Added to keep track of the end of the dispute period
    }

    struct PuzzleSet {
        uint numberOfPuzzles;
        mapping(uint => PuzzleDetail) details;
        uint startTime;
        address client;
        address server;
        uint deposit;
    }

    mapping(uint => PuzzleSet) public puzzleSets;
    uint public disputeDuration = 3600 * 24; // Set the dispute time to 1 day by default
    uint public puzzleSetCounter = 0; // Counter to keep track of puzzle sets

    event PuzzleSetCreated(uint indexed puzzleSetId);
    event PuzzleSolved(uint indexed puzzleSetId, uint puzzleId, address solver);
    event PaymentIssued(uint indexed puzzleSetId, uint puzzleId, address solver);
    event DisputeRaised(uint indexed puzzleSetId, uint puzzleId, address disputer);
    event WithdrawalAllowed(uint indexed puzzleSetId, uint puzzleId, address server);
    
    modifier onlyClient(uint puzzleSetId) {
        if (puzzleSets[puzzleSetId].client != address(0)) {
        require(msg.sender == puzzleSets[puzzleSetId].client, "Only the client can call this function.");
        } else {
            // We should make it mandatoru to register the client address to prevent extraction
        }
        _;
    }

    modifier onlyServer(uint puzzleSetId) {
        require(msg.sender == puzzleSets[puzzleSetId].server, "Only the server can call this function.");
        _;
    }

    modifier onlySolver(uint puzzleSetId, uint puzzleId) {
        require(msg.sender == puzzleSets[puzzleSetId].details[puzzleId].puzzleSolver, "Only the solver can call this function.");
        _;
    }

    function createPuzzleSet(
        uint _numberOfPuzzles,
        uint[] memory _deliveryTimes,
        uint[] memory _coins,
        address solver
    ) public payable {
        uint totalCoins = 0;
        for(uint i = 0; i < _coins.length; i++) {
            totalCoins += _coins[i];
        }
        require(msg.value == totalCoins, "Deposit must equal the sum of coins.");

        uint puzzleSetId = puzzleSetCounter++;
        PuzzleSet storage puzzleSet = puzzleSets[puzzleSetId];
        puzzleSet.numberOfPuzzles = _numberOfPuzzles;
        puzzleSet.deposit = msg.value;
        puzzleSet.server = msg.sender;
        puzzleSet.startTime = block.timestamp; // Start time should be set when creating the puzzle set.

        for(uint i = 0; i < _numberOfPuzzles; i++) {
            PuzzleDetail storage detail = puzzleSet.details[i];
            detail.deliveryTime = _deliveryTimes[i];
            detail.coins = _coins[i];
            detail.puzzleSolver = solver;
        }

        emit PuzzleSetCreated(puzzleSetId);
    }

    function initializePuzzle(uint puzzleSetId, bytes[] memory p, bytes32[] memory g) public onlyClient(puzzleSetId) {
        PuzzleSet storage puzzleSet = puzzleSets[puzzleSetId];
        require(p.length == g.length && p.length == puzzleSet.numberOfPuzzles, "Invalid puzzle or commitment count.");

        for(uint i = 0; i < puzzleSet.numberOfPuzzles; i++) {
            PuzzleDetail storage detail = puzzleSet.details[i];
            detail.puzzle = p[i];
            detail.commitment = g[i]; // Now storing commitments
        }
        puzzleSet.startTime = block.timestamp;
    }

    function submitSolution(uint puzzleSetId, uint puzzleId, bytes memory solution, bytes memory proof) public {
        PuzzleDetail storage detail = puzzleSets[puzzleSetId].details[puzzleId];

        require(block.timestamp <= puzzleSets[puzzleSetId].startTime + detail.deliveryTime, "Solution is late.");
        require(detail.puzzleSolver == address(0) || detail.puzzleSolver == msg.sender, "Solver not authorised or already assigned.");
        require(!detail.isSolved, "Solution already provided.");

        detail.solution = solution;
        detail.proof = proof;
        detail.isSolved = true;
        detail.disputeEndTime = block.timestamp + disputeDuration; // Setting the end time for a dispute period

        if(detail.puzzleSolver == address(0)) {
            detail.puzzleSolver = msg.sender;
        }

        emit PuzzleSolved(puzzleSetId, puzzleId, msg.sender);
    }

    // TO ADD `onlyServer` guard
    function confirmPayment(uint puzzleSetId, uint puzzleId, bool isValidSolution) public {
        PuzzleDetail storage detail = puzzleSets[puzzleSetId].details[puzzleId];

        require(detail.isSolved, "Puzzle has not been solved.");
        require(!detail.isDisputed, "Puzzle is currently disputed.");
        require(detail.coins > 0, "Payment for this puzzle has already been issued.");

        // If the solution is valid and the server confirms it
        if(isValidSolution) {
            uint paymentAmount = detail.coins;
            detail.coins = 0; // Prevent reentrancy by setting coins to 0 before transfer
            payable(detail.puzzleSolver).transfer(paymentAmount);
            emit PaymentIssued(puzzleSetId, puzzleId, detail.puzzleSolver);
        } else {
            // If the solution is not valid, allow for a dispute to be raised
            detail.isDisputed = true;
            detail.disputeEndTime = block.timestamp + disputeDuration; // Set the dispute end time
            emit DisputeRaised(puzzleSetId, puzzleId, msg.sender);
        }
    }

    function resolveDispute(uint puzzleSetId, uint puzzleId) public onlySolver(puzzleSetId, puzzleId) {
        PuzzleDetail storage detail = puzzleSets[puzzleSetId].details[puzzleId];
        require(block.timestamp < detail.disputeEndTime, "Dispute period has ended.");
        require(detail.isDisputed, "No dispute raised.");

        bool isValid = verifySolution(puzzleSetId, puzzleId);
        if(isValid) {
            payable(detail.puzzleSolver).transfer(detail.coins);
            emit PaymentIssued(puzzleSetId, puzzleId, detail.puzzleSolver);
        } else {
            // Solution is invalid
            puzzleSets[puzzleSetId].deposit -= detail.coins;
            payable(puzzleSets[puzzleSetId].server).transfer(detail.coins);
            emit DisputeRaised(puzzleSetId, puzzleId, msg.sender);
        }
        detail.isDisputed = false;
        detail.coins = 0; // Prevent reentrancy
    }

    function verifySolution(uint puzzleSetId, uint puzzleId) internal view returns (bool) {
        PuzzleDetail storage detail = puzzleSets[puzzleSetId].details[puzzleId];
        bytes32 computedHash = sha256(abi.encodePacked(detail.solution, detail.proof));
        return computedHash == detail.commitment;
    }

    function withdrawUnclaimedCoins(uint puzzleSetId, uint puzzleId) public  onlyServer(puzzleSetId){
        PuzzleDetail storage detail = puzzleSets[puzzleSetId].details[puzzleId];
        require(!detail.isSolved && block.timestamp >= detail.disputeEndTime, "Cannot withdraw before dispute end time or if the puzzle is solved.");

        uint coins = detail.coins;
        detail.coins = 0; // Prevent reentrancy
        payable(msg.sender).transfer(coins);

        emit WithdrawalAllowed(puzzleSetId, puzzleId, msg.sender);
    }

}

