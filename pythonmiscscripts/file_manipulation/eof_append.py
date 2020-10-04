from pythonmiscscripts.file_manipulation.utils import FileModifier, OpenFileModification, null_match_parser, LineParser


def append_lines_to_end(file_name: str, lines: [str]):
    parsers = create_parsers(lines)
    with FileModifier(file_name, parsers) as f:
        modify(f)


def create_parsers(lines: [str]) -> [LineParser]:
    parsers = list()
    for line in lines:
        parsers.append(null_match_parser(line))
    return parsers


def modify(f: OpenFileModification) -> bool:
    any_change = False
    for line in f.input_lines:
        f.output_lines.append(line)
    if len(f.parsers) > 0:
        f.output_lines.append("\n")
    for repl in f.parsers:
        f.output_lines.append(repl.generate_replacement(""))
        any_change = True
    return any_change


if __name__ == "__main__":
    l1 = "some"
    l2 = "lines"
    to_append = "appended"
    parsers = create_parsers([to_append])
    assert len(parsers) == 1
    fmod = FileModifier("eof_append_tst.txt", parsers)
    modify(fmod.read_lines_and_trim_parsers())
    after = fmod.modified
    assert len(after) == 4
    assert after[0] == l1 + "\n"
    assert after[1] == l2 + "\n"
    assert after[2] == "\n"
    assert after[3] == to_append + "\n"
