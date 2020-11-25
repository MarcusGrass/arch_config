from typing import Callable, Optional
from dataclasses import dataclass
from enum import Enum


class LineParser(object):
    def __init__(self, match: Callable, replacer: Callable, with_newline: bool = True, on_line: int = None):
        self.match = match
        self.replacer = replacer
        self.with_newline = with_newline
        self.on_line = on_line

    def matches(self, line: str) -> bool:
        return self.match(line)

    def matches_line(self, on_line: int) -> bool:
        return on_line is not None and on_line == self.on_line

    def generate_replacement(self, line: str) -> Optional[str]:
        if self.match(line):
            after = self.replacer(line)
            if after is None:
                return None
            elif self.with_newline:
                return after + "\n"
            else:
                return after
        else:
            return None

    @staticmethod
    def in_place_replacer(match: str, replace: str):
        return LineParser(lambda x: match in x, lambda x: x.replace(match, replace), with_newline=False)


def null_match_parser(replacement: str) -> LineParser:
    return LineParser(lambda _: True, lambda _: replacement)


@dataclass
class OpenFileModification:
    output_lines: [str]
    input_lines: [str]
    parsers: [LineParser]


class ManipulationResult(Enum):
    NO_MATCH = 1
    NO_CHANGE = 2
    CHANGED = 3


class FileModifier(object):
    def __init__(self, file_name: str, parsers: [LineParser]):
        if not type(parsers) == list and type(parsers) == LineParser:
            self.parsers = [parsers]
        else:
            self.parsers = parsers
        self.file_name = file_name
        self.file = None
        self.input_lines = None
        self.modified = list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            if self._has_committable_change():
                print("Updating file %s, line diff=%s" % (self.file_name, len(self.modified) - len(self.input_lines)),
                      flush=True)
                self.__write()
            else:
                print("Change already present in %s, will not write" % self.file_name, flush=True)

    def read_lines_and_trim_parsers(self) -> OpenFileModification:
        with open(self.file_name, "r") as file:
            self.input_lines = file.readlines()
        self.__remove_unneeded_parses(self.input_lines)
        return OpenFileModification(input_lines=self.input_lines, output_lines=self.modified, parsers=self.parsers)

    def __all_changes_present(self) -> bool:
        return len(self.parsers) == 0

    def __remove_unneeded_parses(self, lines: list) -> [LineParser]:
        needed = list()
        for replacer in self.parsers:
            if not FileModifier.any_match(lines, replacer):
                needed.append(replacer)
        self.parsers = needed

    def _has_committable_change(self):
        if len(self.input_lines) == len(self.modified):
            for a, b in zip(self.input_lines, self.modified):
                if a != b:
                    return True
        return self.input_lines != self.modified and len(self.modified) != 0

    def __write(self):
        with open(self.file_name, "w") as file:
            file.writelines(self.modified)

    @staticmethod
    def any_match(lines: list, parser: LineParser) -> bool:
        for line in lines:
            if parser.matches_line(line):
                return True
        return False

    @staticmethod
    def modify(file_name: str, parsers: [LineParser],
               mod_method: Callable[[OpenFileModification], bool]) -> ManipulationResult:
        with FileModifier(file_name, parsers) as fm:
            f = fm.read_lines_and_trim_parsers()
            if fm.__all_changes_present():
                return ManipulationResult.NO_CHANGE
            if mod_method(f):
                return ManipulationResult.CHANGED
            else:
                return ManipulationResult.NO_MATCH


if __name__ == "__main__":
    fmod = FileModifier("file_mod_tst.txt", [LineParser(lambda l: l.startswith("some"),
                                                        lambda _: "some_present_change")])
    open_mod = fmod.read_lines_and_trim_parsers()
    for ln in open_mod.input_lines:
        open_mod.output_lines.append(ln)
        for parse in open_mod.parsers:
            result = parse.generate_replacement(ln)
            if result is not None:
                open_mod.output_lines.append(result)
    assert fmod._has_committable_change() is False

    fmod = FileModifier("file_mod_tst.txt", LineParser(lambda l: l.startswith("some"),
                                                       lambda _: "some_missing_change"))
    open_mod = fmod.read_lines_and_trim_parsers()
    for ln in open_mod.input_lines:
        open_mod.output_lines.append(ln)
        for parse in open_mod.parsers:
            result = parse.generate_replacement(ln)
            if result is not None:
                open_mod.output_lines.append(result)
    assert fmod._has_committable_change() is True

    fmod = FileModifier("file_mod_tst.txt", LineParser(lambda l: l.startswith("some"),
                                                       lambda _: "some_missing_change"))

    assert fmod._has_committable_change() is False
