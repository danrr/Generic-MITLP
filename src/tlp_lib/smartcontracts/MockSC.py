from datetime import datetime
from typing import Any, Self

from tlp_lib.protocols import GCTLP_Encrypted_Message, GCTLP_Encrypted_Messages, GCTLPInterface, TLP_Digest, TLP_Digests
from tlp_lib.smartcontracts.protocols import SC_Coins, SC_ExtraTime, SC_UpperBounds


class MockSC:
    commitments: TLP_Digests
    start_time: int
    upper_bounds: SC_UpperBounds
    coins: SC_Coins
    solutions: GCTLP_Encrypted_Messages = []
    initial_timestamp: int
    gctlp: GCTLPInterface
    helper_id: Any
    extra_time: SC_ExtraTime

    def initiate(
        self,
        coins: SC_Coins,
        start_time: int,
        extra_time: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        gctlp: GCTLPInterface,
        helper_id: Any,
    ) -> Self:
        self.coins = coins
        self.start_time = start_time
        self.extra_time = extra_time
        self.upper_bounds = upper_bounds
        self.gctlp = gctlp
        self.helper_id = helper_id
        self.commitments = []
        self.solutions = []
        self.initial_timestamp = int(datetime.now().timestamp())
        return self

    def add_solution(self, solution: GCTLP_Encrypted_Message, witness: TLP_Digest):
        time = int(datetime.now().timestamp())
        assert time >= self.initial_timestamp + self.start_time
        self.check_solution(self.get_commitment_at(len(self.solutions)), solution, witness)

        self.solutions.append(solution)

    def verify_solution(self, i: int, /) -> bool:
        solution = self.get_solution_at(i)
        return len(solution) != 0

    def check_solution(self, commitment: TLP_Digest, solution: GCTLP_Encrypted_Message, witness: TLP_Digest) -> bool:
        try:
            self.gctlp.verify(solution, witness, commitment)
            return True
        except AssertionError:
            return False

    def switch_to_account(self, account: int):
        pass

    def pay_back(self, i: int, /):
        print(f"paying back {self.coins[i]}")

    def get_commitment_at(self, i: int, /) -> TLP_Digest:
        return self.commitments[i]

    def get_solution_at(self, i: int, /) -> GCTLP_Encrypted_Message:
        return self.solutions[i]

    def get_upper_bound_at(self, i: int, /) -> int:
        return self.upper_bounds[i]
