from typing import Callable
from dataclasses import dataclass


@dataclass
class LineParser:
    match: Callable
    replacer: Callable

    def generate_replacement(self, line: str):
        if self.match(line):
            return self.replacer(line) + "\n"
        else:
            return None


@dataclass
class FileLinesMutator:
    transformer: Callable

    def transform(self, lines: list):
        return self.transformer(lines)


@dataclass
class OpenFileModification:
    output_lines: [str]
    input_lines: [str]
    parsers: [LineParser]


class FileModifier(object):
    def __init__(self, file_name: str, parsers: [LineParser]):
        self.file_name = file_name
        self.parsers = parsers
        self.file = None
        self.input_lines = None
        self.modified = list()

    def __enter__(self):
        return self.read_lines_and_trim_parsers()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            if self.has_committable_change():
                print("Updating file %s, line diff=%s" % (self.file_name, len(line) - len(self.modified)), flush=True)
                FileModifier.write(self.file_name, self.modified)
            else:
                print("Change already present in %s, will not write" % self.file_name, flush=True)

    def read_lines_and_trim_parsers(self) -> [str]:
        with open(self.file_name, "r") as file:
            self.input_lines = file.readlines()
        self.remove_unneeded_parses(self.input_lines)
        return OpenFileModification(input_lines=self.input_lines, output_lines=self.modified, parsers=self.parsers)

    def remove_unneeded_parses(self, lines: list) -> [LineParser]:
        needed = list()
        for replacer in self.parsers:
            if not FileModifier.replacement_present(lines, replacer):
                needed.append(replacer)
        self.parsers = needed

    def has_committable_change(self):
        return self.input_lines != self.modified and len(self.modified) != 0

    @staticmethod
    def replacement_present(lines: list, parser: LineParser) -> bool:
        for line in lines:
            none_on_miss = parser.generate_replacement(line)
            if none_on_miss is not None:
                if none_on_miss in lines:
                    return True
        return False

    @staticmethod
    def write(file_name: str, lines: list):
        with open(file_name, "w") as file:
            file.writelines(lines)


if __name__ == "__main__":
    fmod = FileModifier("file_mod_tst.txt", [LineParser(lambda l: l.startswith("some"),
                                                        lambda _: "some_present_change")])
    open_mod = fmod.read_lines_and_trim_parsers()
    for line in open_mod.input_lines:
        open_mod.output_lines.append(line)
        for parse in open_mod.parsers:
            result = parse.generate_replacement(line)
            if result is not None:
                open_mod.output_lines.append(result)
    assert fmod.has_committable_change() is False

    fmod = FileModifier("file_mod_tst.txt", [LineParser(lambda l: l.startswith("some"),
                                                        lambda _: "some_missing_change")])
    open_mod = fmod.read_lines_and_trim_parsers()
    for line in open_mod.input_lines:
        open_mod.output_lines.append(line)
        for parse in open_mod.parsers:
            result = parse.generate_replacement(line)
            if result is not None:
                open_mod.output_lines.append(result)
    assert fmod.has_committable_change() is True

    fmod = FileModifier("file_mod_tst.txt", [LineParser(lambda l: l.startswith("some"),
                                                        lambda _: "some_missing_change")])

    assert fmod.has_committable_change() is False
