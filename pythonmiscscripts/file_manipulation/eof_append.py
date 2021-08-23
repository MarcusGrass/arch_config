from pythonmiscscripts.file_manipulation.file_modifier import FileModifier, OpenFileModification, \
    null_match_parser, LineParser, ManipulationResult


def append_lines_to_end(file_name: str, lines: [str]) -> ManipulationResult:
    parsers = create_parsers(lines)
    return FileModifier.modify(file_name, parsers, modify)


def create_parsers(lines: [str]) -> [LineParser]:
    parsers = list()
    for line in lines:
        parsers.append(null_match_parser(line))
    return parsers


def modify(f: OpenFileModification) -> bool:
    any_change = False
    redundant_matchers = []
    for line in f.input_lines:
        f.output_lines.append(line)
        for i in range(0, len(f.parsers)):
            if line == f.parsers[i].generate_replacement(""):
                redundant_matchers.append(i)
    for i in range(0, len(f.parsers)):
        if i in redundant_matchers:
            continue
        f.output_lines.append(f.parsers[i].generate_replacement(""))
        any_change = True
    for i in range(0, len(redundant_matchers)):
        f.parsers.pop()
    return any_change


if __name__ == "__main__":
    l1 = "some"
    l2 = "lines"
    skip = "lines"
    to_append = "appended"
    line_parsers = create_parsers([to_append, skip])
    assert len(line_parsers) == 2
    fmod = FileModifier("eof_append_tst.txt", line_parsers)
    modify(fmod.read_lines_and_trim_parsers())
    after = fmod.modified
    assert len(after) == 3
    assert after[0] == l1 + "\n"
    assert after[1] == l2 + "\n"
    assert after[2] == to_append + "\n"
