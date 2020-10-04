from pythonmiscscripts.file_manipulation.utils import LineParser, FileModifier, OpenFileModification


def insert_after_match(file_name: str, next_line_appenders: [LineParser]) -> bool:
    with FileModifier(file_name, next_line_appenders) as f:
        return modify(f)


def modify(f: OpenFileModification) -> bool:
    success = False
    for line in f.input_lines:
        f.output_lines.append(line)
        for line_replacer in f.parsers:
            result = line_replacer.generate_replacement(line)
            if result is not None:
                success = True
                f.output_lines.append(result)
    return success


if __name__ == "__main__":
    l1 = "appendafter"
    l2 = "created"
    l3 = "donotappendafter"
    appenders = [LineParser(lambda l: l.startswith("appendafter"), lambda _: l2)]
    fmod = FileModifier("next_line_append.txt", appenders)
    modify(fmod.read_lines_and_trim_parsers())
    after = fmod.modified
    assert len(after) == 3
    assert after[0] == l1 + "\n"
    assert after[1] == l2 + "\n"
    assert after[2] == l3 + "\n"
