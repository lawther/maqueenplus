import ast, re, os, sys
import itertools
from typing import Generator

#
# Replaces all names starting with an underscore with a minimal
# name.
#
# This is intended as a minifying operation, not as an obfuscation.
#
# Usage: python minimal-renamer.py filename.py
# Output: filename-min.py
#


def minimal_name_generator() -> Generator[str, None, None]:
    """
    Returns minimal length identifiers, prefixed with an underscore, eg
    _a, _b, ... , _aa, _ab etc
    """
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    length = 1

    while True:
        for combination in itertools.product(letters, repeat=length):
            yield "_" + "".join(combination)
        length += 1


def get_and_add_next_name(used: set[str], gen: Generator[str, None, None]) -> str:
    """
    Returns the next minimal name that does not clash with any existing names.
    """
    newname = next(gen)
    while newname in used:
        newname = next(gen)
    used.add(newname)
    return newname


def do_rename(pairs: dict[str, str], code: str) -> str:
    for key in pairs:
        code = re.sub(rf"\b({key})\b", pairs[key], code, re.MULTILINE)
    return code


def minify_underscored_names(filename: str) -> str:
    with open(filename, "r") as file:
        code: str = file.read()
        parsed: ast.Module = ast.parse(code)

    funcs: set[ast.FunctionDef | ast.AsyncFunctionDef] = {
        node
        for node in ast.walk(parsed)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    names: set[str] = {
        str(node.id)
        for node in ast.walk(parsed)
        if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)
    }
    attrs: set[str] = {
        str(node.attr)
        for node in ast.walk(parsed)
        if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load)
    }

    for func in funcs:
        if func.args.args:
            for arg in func.args.args:
                names.add(str(arg.arg))
        if func.args.kwonlyargs:
            for arg in func.args.kwonlyargs:
                names.add(str(arg.arg))
        if func.args.vararg:
            names.add(str(func.args.vararg.arg))
        if func.args.kwarg:
            names.add(str(func.args.kwarg.arg))

    pairs: dict[str, str] = {}
    used: set[str] = set()

    # Note down all the things so we don't clash with them
    for func in funcs:
        used.add(func.name)
    for name in names:
        used.add(name)
    for attr in attrs:
        used.add(attr)

    gen: Generator[str, None, None] = minimal_name_generator()

    for func in sorted(funcs, key=lambda x: x.name):
        if func.name.endswith("__"):
            continue
        if not func.name.startswith("_"):
            continue

        pairs[func.name] = get_and_add_next_name(used, gen)

    for name in sorted(names):
        if name == "_":
            continue
        if not name.startswith("_"):
            continue

        pairs[name] = get_and_add_next_name(used, gen)

    for attr in sorted(attrs):
        if not attr.startswith("_"):
            continue

        pairs[attr] = get_and_add_next_name(used, gen)

    # Look for actual strings, we don't want to replace inside these
    string_regex = r"('|\")[\x1f-\x7e]{1,}?('|\")"
    original_strings = re.finditer(string_regex, code, re.MULTILINE)
    originals = []

    for matchNum, match in enumerate(original_strings, start=1):
        originals.append(match.group().replace("\\", "\\\\"))

    # Replace all strings with a random placeholder
    placeholder = os.urandom(16).hex()
    code = re.sub(string_regex, f"'{placeholder}'", code, 0, re.MULTILINE)

    for i in range(len(originals)):
        for key in pairs:
            originals[i] = re.sub(
                r"({.*)(" + key + r")(.*})",
                "\\1" + pairs[key] + "\\3",
                originals[i],
                re.MULTILINE,
            )

    # Actually do the renaming of the variables
    while True:
        found = False
        code = do_rename(pairs, code)
        for key in pairs:
            if re.findall(rf"\b({key})\b", code):
                found = True
        if found == False:
            break

    # Replace the placeholders with the original actual strings
    replace_placeholder = r"('|\")" + placeholder + r"('|\")"
    for original in originals:
        code = re.sub(replace_placeholder, original, code, 1, re.MULTILINE)

    return code


file = sys.argv[1]

code = minify_underscored_names(file)

with open(f"{file[:-3]}-min.py", "w") as f:
    f.write(code)
