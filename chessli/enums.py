from enum import Enum

__all__ = ["PerfType", "Variant", "Color", "Room", "Mode", "Position"]


class StrEnum(str, Enum):
    """A String enum"""


class PuzzleDBSource(str, Enum):
    remote = "remote"
    local = "local"


class SinceEnum(StrEnum):
    last_time = "last_time"
    yesterday = "yesterday"
    one_hour = "one_hour"
    last_week = "last_week"
    forever = "forever"


class Nag(Enum):
    good = 1  # A good move.  by ``!`` in PGN notation.
    mistake = 2  # A mistake.  by ``?`` in PGN notation.
    brilliant = 3  # A brilliant move.  by ``!!`` in PGN notation.
    blunder = 4  # A blunder.  by ``??`` in PGN notation.
    speculative = 5  # A speculative move. ``!?`` in PGN notation.
    dubious = 6  # A dubious move.  by ``?!`` in PGN notation.


class GameType(StrEnum):
    ANTICHESS = "antichess"
    ATOMIC = "atomic"
    CHESS960 = "chess960"
    CRAZYHOUSE = "crazyhouse"
    HORDE = "horde"
    KING_OF_THE_HILL = "kingOfTheHill"
    RACING_KINGS = "racingKings"
    THREE_CHECK = "threeCheck"


class PerfType(StrEnum):
    ANTICHESS = GameType.ANTICHESS.value
    ATOMIC = GameType.ATOMIC.value
    CHESS960 = GameType.CHESS960.value
    CRAZYHOUSE = GameType.CRAZYHOUSE.value
    HORDE = GameType.HORDE.value
    KING_OF_THE_HILL = GameType.KING_OF_THE_HILL.value
    RACING_KINGS = GameType.RACING_KINGS.value
    THREE_CHECK = GameType.THREE_CHECK.value

    BULLET = "bullet"
    BLITZ = "blitz"
    RAPID = "rapid"
    CLASSICAL = "classical"
    ULTRA_BULLET = "ultraBullet"


class Color(Enum):
    white = 1
    black = 0
