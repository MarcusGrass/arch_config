from pythonmiscscripts.file_manipulation.utils import LineParser, FileModifier, OpenFileModification, ManipulationResult


def replace_on_match(file_name: str, line_replacers: [LineParser]) -> ManipulationResult:
    return FileModifier.modify(file_name, line_replacers, modify)


def modify(f: OpenFileModification) -> bool:
    modified = True
    for line in f.input_lines:
        any_match = False
        for line_replacer in f.parsers:
            result = line_replacer.generate_replacement(line)
            if result is not None:
                f.output_lines.append(result)
                any_match = True
                modified = True
        if not any_match:
            f.output_lines.append(line)
    return modified


if __name__ == "__main__":
    l1 = "touched"
    l2 = "untouched"
    l3 = "also touched"
    replacers = [LineParser(lambda l: l.startswith("touch"), lambda _: l1),
                 LineParser(lambda l: l.startswith("also touch"), lambda _: l3)]
    fmod = FileModifier("line_replace_tst.txt", replacers)
    modify(fmod.read_lines_and_trim_parsers())
    after = fmod.modified
    assert len(after) == 3
    assert after[0] == l1 + "\n"
    assert after[1] == l2 + "\n"
    assert after[2] == l3 + "\n"
