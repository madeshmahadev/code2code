"""
Module contains the CodeUnit class, which represents a code unit (e.g., class, function, etc.) in a programming language.
"""
from typing import List
from dataclasses import dataclass

@dataclass
class CodeUnit:
    # The actual content of the code unit (e.g., class, function, etc.)
    content: str
    # The file path where this code unit is located
    file_path: str
    # The programming language of the code unit
    language: str
    # The type of code unit (e.g., class, function, interface, etc.)
    unit_type: str 
    # The name of the code unit (e.g., class name, function name, etc.)
    name: str
    # A list of dependencies for this code unit
    dependencies: List[str]