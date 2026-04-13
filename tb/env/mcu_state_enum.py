from enum import Enum

class McuStateEnum(Enum):
    READY   = 0b1000_0000
    BUSY    = 0b0100_0000
    DEBUG   = 0b0010_0000
