# Visitor to *typecheck* MiniC files
from typing import List
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.Errors import MiniCInternalError, MiniCTypeError

from enum import Enum


# NEW: ADD FutInteger
class BaseType(Enum):
    Float, Integer, Boolean, String, FutInteger = range(5)


class MiniCTypingVisitor(MiniCVisitor):
    # TODO Add your own typer here
    pass
