import ast, re, os, sys
import collections
from typing import Generator

#
# Replaces all constants in the code with their constant value.
# Removes any unused internal constant definitions.
#
# Yes, I know that Python doesn't really have 'constants'. Here,
# constants are defined as being ALL_CAPS. Internal constants are
# defined as beginning with an underscore. If someone has written
# client code that accesses these internal constants, well, they
# were being cheeky anyway.
#
# This is intended as a minifying operation, not as an obfuscation.
#
# Usage: python constant-replaceer.py filename.py
# Output: filename-decon.py
#


def is_only_capitals_numbers_and_underscores(s: str) -> bool:
    # Check if all characters in the string are either uppercase letters
    # or numbers or underscores
    return all(char.isupper() or char.isnumeric() or char == "_" for char in s)


def find_constants(code: str) -> set[str]:

    parsed: ast.Module = ast.parse(code)

    names: set[str] = {
        str(node.id)
        for node in ast.walk(parsed)
        if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)
    }

    constants = {s for s in names if is_only_capitals_numbers_and_underscores(s)}

    return constants


def remove_unused_internal_constants(constants: set[str], code: str) -> str:

    code_without_comments = re.sub(r"#.*", "", code)

    all_identifiers: list[str] = re.findall(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", code_without_comments
    )

    found_internal_constants = [
        identifier
        for identifier in all_identifiers
        if identifier in constants and identifier.startswith("_")
    ]

    constant_counts = collections.Counter(found_internal_constants)

    single_use_constants = {
        identifier for identifier, count in constant_counts.items() if count == 1
    }

    codelines = code.splitlines()
    codelines = [
        line for line in codelines if not any(c in line for c in single_use_constants)
    ]

    for c in single_use_constants:
        constants.remove(c)

    return "\n".join(codelines)


def get_constant_values(constants: set[str], code: str) -> dict[str, str]:
    codelines = code.splitlines()

    # Regular expression to match "name = value" pattern
    pattern = re.compile(r"^\s*(\w+)\s*=\s*(.+)\s*$")

    constant_values: dict[str, str] = {}
    for line in codelines:
        match = pattern.match(line)
        if match:
            name, value = match.groups()
            # Check if the name is in the set of valid names
            if name in constants:
                constant_values[name] = value.strip()

    return constant_values


def replace_constant_values(constant_values: dict[str, str], code: str) -> str:

    # Function to replace "self.FOO" with the corresponding value from the dictionary
    def replace_match(match):
        name = match.group(1)
        # Replace with the corresponding value from the dictionary
        return constant_values.get(name, match.group(0))

    # Create a regex pattern to match "self.FOO" where FOO is in the dictionary
    pattern = re.compile(r"self\.(\w+)")

    # Replace occurrences in the entire text
    return pattern.sub(replace_match, code)


filename = sys.argv[1]
with open(filename, "r") as file:
    code: str = file.read()

constants = find_constants(code)

code = remove_unused_internal_constants(constants, code)

constant_values = get_constant_values(constants, code)

code = replace_constant_values(constant_values, code)

code = remove_unused_internal_constants(constants, code)

with open(f"{filename[:-3]}-decon.py", "w") as f:
    f.write(code)
