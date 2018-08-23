from enum import Enum

class PieceType(Enum):
    I = 0
    J = 1
    L = 2
    O = 3
    S = 4
    T = 5
    Z = 6
    NUM_TYPES = 7
    G = 8

class Rotation(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3

    @classmethod
    def clockwise(cls, rotation):
        return cls((rotation.value + 1) % 4)
    
    @classmethod
    def counter_clockwise(cls, rotation):
        return cls((rotation.value - 1) % 4)

class RotationType(Enum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1


PIECE_SHAPE = {
    PieceType.I: {
        Rotation.ZERO:  ((0, 1), (1, 1), (2, 1), (3, 1)),
        Rotation.ONE:   ((2, 0), (2, 1), (2, 2), (2, 3)),
        Rotation.TWO:   ((0, 2), (1, 2), (2, 2), (3, 2)),
        Rotation.THREE: ((1, 0), (1, 1), (1, 2), (1, 3))
    },
    PieceType.J: {
        Rotation.ZERO:  ((0, 0), (0, 1), (1, 1), (2, 1)),
        Rotation.ONE:   ((2, 0), (1, 0), (1, 1), (1, 2)),
        Rotation.TWO:   ((0, 1), (1, 1), (2, 1), (2, 2)),
        Rotation.THREE: ((1, 0), (1, 1), (1, 2), (0, 2))
    },
    PieceType.L: {
        Rotation.ZERO:  ((0, 1), (1, 1), (2, 1), (2, 0)),
        Rotation.ONE:   ((1, 0), (1, 1), (1, 2), (2, 2)),
        Rotation.TWO:   ((0, 2), (0, 1), (1, 1), (2, 1)),
        Rotation.THREE: ((0, 0), (1, 0), (1, 1), (1, 2)),
    },
    PieceType.O: {
        Rotation.ZERO:  ((1, 0), (2, 0), (1, 1), (2, 1)),
        Rotation.ONE:   ((1, 0), (2, 0), (1, 1), (2, 1)),
        Rotation.TWO:   ((1, 0), (2, 0), (1, 1), (2, 1)),
        Rotation.THREE: ((1, 0), (2, 0), (1, 1), (2, 1))
    },
    PieceType.S: {
        Rotation.ZERO:  ((0, 1), (1, 1), (1, 0), (2, 0)),
        Rotation.ONE:   ((1, 0), (1, 1), (2, 1), (2, 2)),
        Rotation.TWO:   ((0, 2), (1, 2), (1, 1), (2, 1)),
        Rotation.THREE: ((0, 0), (0, 1), (1, 1), (1, 2)),
    },
    PieceType.T: {
        Rotation.ZERO:  ((0, 1), (1, 1), (2, 1), (1, 0)),
        Rotation.ONE:   ((1, 0), (1, 1), (1, 2), (2, 1)),
        Rotation.TWO:   ((0, 1), (1, 1), (2, 1), (1, 2)),
        Rotation.THREE: ((1, 0), (1, 1), (1, 2), (0, 1)),
    },
    PieceType.Z: {
        Rotation.ZERO:  ((0, 0), (1, 0), (1, 1), (2, 1)),
        Rotation.ONE:   ((2, 0), (2, 1), (1, 1), (1, 2)),
        Rotation.TWO:   ((0, 1), (1, 1), (1, 2), (2, 2)),
        Rotation.THREE: ((1, 0), (1, 1), (0, 1), (0, 2)),
    },
}

_JLSTZ_ROTAION_CHECKS = {
    (Rotation.ZERO, Rotation.ONE): (
        (0, 0), (-1, 0), (-1, -1), (0, 2), (-1, -2)
    ),
    (Rotation.ONE, Rotation.TWO): (
        (0, 0), (1, 0), (1, 1), (0, -2), (1, -2)
    ),
    (Rotation.TWO, Rotation.THREE): (
        (0, 0), (1, 0), (1, -1), (0, 2), (1, 2)
    ),
    (Rotation.THREE, Rotation.ZERO): (
        (0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)
    )
}

_I_ROTAION_CHECKS = {
    (Rotation.ZERO, Rotation.ONE): (
        (0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)
    ),
    (Rotation.ONE, Rotation.TWO): (
        (0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)
    ),
    (Rotation.TWO, Rotation.THREE): (
        (0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)
    ),
    (Rotation.THREE, Rotation.ZERO): (
        (0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)
    )
}

_ROTATION_CHECKS = dict.fromkeys(
    (PieceType.J, PieceType.L, PieceType.S, PieceType.T, PieceType.Z),
    _JLSTZ_ROTAION_CHECKS
)
_ROTATION_CHECKS.update({
    PieceType.I: _I_ROTAION_CHECKS,
    PieceType.O: dict.fromkeys((
        (Rotation.ZERO, Rotation.ONE),
        (Rotation.ONE, Rotation.TWO),
        (Rotation.TWO, Rotation.THREE),
        (Rotation.THREE, Rotation.ZERO)
    ), ((0, 0),))
})

def get_roation_checks(type_: PieceType, cur_rotation: Rotation, desired_rotation: Rotation):
    if (cur_rotation, desired_rotation) in _ROTATION_CHECKS[type_]:        
        yield from _ROTATION_CHECKS[type_][cur_rotation, desired_rotation]
    else:
        for (dx, dy) in _ROTATION_CHECKS[type_][desired_rotation, cur_rotation]:
            yield (-dx, -dy)