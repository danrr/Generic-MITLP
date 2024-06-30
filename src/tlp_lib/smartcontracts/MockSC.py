from datetime import datetime
from typing import Self

from tlp_lib.protocols import GMITLP_Encrypted_Message, TLP_Digest, TLP_Digests
from tlp_lib.smartcontracts.protocols import SC_Coins, SC_ExtraTime, SC_Solutions, SC_UpperBounds


class MockSC:
    commitments: TLP_Digests
    start_time: int
    upper_bounds: SC_UpperBounds
    coins: SC_Coins
    solutions: SC_Solutions
    initial_timestamp: int
    helper_id: int
    extra_time: SC_ExtraTime

    def initiate(
        self,
        coins: SC_Coins,
        start_time: int,
        extra_time: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        helper_id: int,
    ) -> Self:
        self.coins = coins
        self.start_time = start_time
        self.extra_time = extra_time
        self.upper_bounds = upper_bounds
        self.helper_id = helper_id
        self.commitments = []
        self.solutions = []
        self.initial_timestamp = int(datetime.now().timestamp())
        return self

    def add_solution(self, solution: GMITLP_Encrypted_Message, witness: TLP_Digest):
        time = int(datetime.now().timestamp())
        self.solutions.append((solution, witness, time))

    def get_message_at(self, i: int, /) -> GMITLP_Encrypted_Message:
        return self.solutions[i][0]

    def switch_to_account(self, account: int):
        pass

    def pay(self, i: int, /):
        print(f"paying TPH' {self.coins[i]}")

    def pay_back(self, i: int, /):
        print(f"paying TPH' back {self.coins[i]}")
