from typing import Protocol, Self

from tlp_lib.protocols import GMITLP_Encrypted_Message, TLP_Digest, TLP_Digests

SC_Coins = list[int]
SC_UpperBounds = list[int]
SC_ExtraTime = list[float]
SC_Solution = tuple[GMITLP_Encrypted_Message, TLP_Digest, int]
SC_Solutions = list[SC_Solution]


class SCInterface(Protocol):

    def initiate(
        self,
        coins: SC_Coins,
        start_time: int,
        extra_time: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        helper_id: int,
    ) -> Self: ...

    def add_solution(self, solution: GMITLP_Encrypted_Message, witness: TLP_Digest) -> None: ...

    def get_message_at(self, i: int, /) -> GMITLP_Encrypted_Message: ...

    def pay(self, i: int, /) -> None: ...

    def pay_back(self, i: int, /) -> None: ...

    def switch_to_account(self, account: int, /) -> None: ...
    @property
    def upper_bounds(self) -> SC_UpperBounds: ...

    @upper_bounds.setter
    def upper_bounds(self, upper_bounds: SC_UpperBounds, /): ...

    @property
    def coins(self) -> SC_Coins: ...

    @coins.setter
    def coins(self, coins: SC_Coins, /): ...

    @property
    def start_time(self) -> int: ...

    @start_time.setter
    def start_time(self, start_time: int, /): ...

    @property
    def commitments(self) -> TLP_Digests: ...

    @commitments.setter
    def commitments(self, commitments: TLP_Digests, /): ...

    @property
    def solutions(self) -> SC_Solutions: ...

    @property
    def initial_timestamp(self) -> int: ...
