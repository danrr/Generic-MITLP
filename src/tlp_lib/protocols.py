from collections.abc import Sequence
from typing import Generator, NamedTuple, NotRequired, Optional, Protocol, TypedDict, Unpack

from tlp_lib import TLP
from tlp_lib.wrappers import SHA512Wrapper
from tlp_lib.wrappers.protocols import HashFunc, RandGen, RandGenModN, RSAKeyGen, SymEnc

TLP_Public = NamedTuple("TLP_Public", [("n", int), ("t", int), ("r", int)])
TLP_Public_Input = TLP_Public | tuple[int, int, int]
TLP_Secret = NamedTuple("TLP_Secret", [("p", int), ("q", int), ("phi_n", int), ("a", int)])
TLP_Secret_Input = TLP_Secret | tuple[int, int, int, int]

TLP_Puzzle = NamedTuple("TLP_Puzzle", [("encrypted_key", int), ("encrypted_message", bytes)])
type TLP_Puzzles = list[TLP_Puzzle]
type TLP_Message = bytes
type TLP_Messages = list[TLP_Message]
type TLP_Digest = bytes
type TLP_Digests = list[TLP_Digest]
type TLP_Key = tuple[TLP_Public, TLP_Secret]
type TLP_Interval = int


class TLPKwargs(TypedDict):
    sym_enc: NotRequired[SymEnc]
    gen_modulus: NotRequired[RSAKeyGen]


class TLPInterface(Protocol):
    def __init__(
        self,
        *,
        sym_enc: Optional[SymEnc] = None,
        gen_modulus: Optional[RSAKeyGen] = None,
        seed: Optional[int] = None,
        random: Optional[RandGenModN] = None,
    ): ...

    def setup(self, interval: TLP_Interval, squarings_per_second: int, keysize: int = 2048) -> TLP_Key: ...

    def generate(self, pk: TLP_Public_Input, a: int, message: TLP_Message) -> TLP_Puzzle: ...

    def solve(self, pk: TLP_Public_Input, puzzle: TLP_Puzzle) -> TLP_Message: ...


TLP_type = type[TLPInterface]

MITLP_Auxiliary_Info = NamedTuple("MITLP_Auxiliary_Info", [("hash_name", str), ("len_commitment", int), ("len_r", int)])
MITLP_Public = NamedTuple("MITLP_Public", [("aux", MITLP_Auxiliary_Info), ("n", int), ("t", int), ("r_0", int)])
MITLP_Public_Input = MITLP_Public | tuple[MITLP_Auxiliary_Info, int, int, int]
MITLP_Secret = NamedTuple("MITLP_Secret", [("a", int), ("r_bin", Sequence[bytes]), ("d", Sequence[bytes])])
MITLP_Secret_Input = MITLP_Secret | tuple[int, Sequence[bytes], Sequence[bytes]]


GMITLP_Public = NamedTuple(
    "GMITLP_Public", [("aux", MITLP_Auxiliary_Info), ("n", int), ("t", Sequence[int]), ("r_0", int)]
)
GMITLP_Public_Input = GMITLP_Public | tuple[MITLP_Auxiliary_Info, int, Sequence[int], int]

GMITLP_Secret = NamedTuple("GMITLP_Secret", [("a", Sequence[int]), ("r_bin", Sequence[bytes]), ("d", Sequence[bytes])])
GMITLP_Secret_Input = GMITLP_Secret | tuple[Sequence[int], Sequence[bytes], Sequence[bytes]]

type GMITLP_Intervals = list[TLP_Interval]


class GMITLPKwargs(TypedDict):
    tlp: NotRequired[TLP_type]
    hash_func: NotRequired[HashFunc]
    gen_modulus: NotRequired[RSAKeyGen]


class GMITLPInterface(Protocol):
    def __init__(
        self,
        *,
        tlp: TLP_type = TLP,
        hash_func: HashFunc = SHA512Wrapper,
        random: Optional[RandGen] = None,
        seed: Optional[int] = None,
        **kwargs: Unpack[TLPKwargs],
    ): ...

    def setup(
        self, intervals: GMITLP_Intervals, squaring_per_second: int, keysize: int = 2048
    ) -> tuple[GMITLP_Public, GMITLP_Secret]: ...

    def generate(
        self, m: TLP_Messages, pk: GMITLP_Public_Input, sk: GMITLP_Secret_Input
    ) -> tuple[TLP_Puzzles, TLP_Digests]: ...

    def solve(
        self, pk: GMITLP_Public_Input, puzz: TLP_Puzzles
    ) -> Generator[tuple[TLP_Message, TLP_Digest], None, None]: ...

    def verify(self, m: TLP_Message, d: bytes, h: TLP_Digest) -> None: ...


GMITLP_type = type[GMITLPInterface]

Server_Info = NamedTuple("Aux_server_info", [("squarings", int)])
type GMITLP_Client_Key = int
type GMITLP_Encrypted_Message = bytes
type GMITLP_Encrypted_Messages = list[GMITLP_Encrypted_Message]
