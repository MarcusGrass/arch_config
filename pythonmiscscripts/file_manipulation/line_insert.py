from pythonmiscscripts.file_manipulation.file_modifier import LineParser, FileModifier, OpenFileModification, \
    ManipulationResult


def insert_on_match(file_name: str, match: str, replacement: str, index_delta: int) -> ManipulationResult:
    lp = LineParser(lambda l: match in l, lambda l: replacement)
    with FileModifier(file_name=file_name, parsers=lp) as fm:
        f = fm.read_lines_and_trim_parsers()
        if len(f.parsers) == 0:
            return ManipulationResult.NO_CHANGE
        if modify(f, match, replacement, index_delta):
            return ManipulationResult.CHANGED
        else:
            return ManipulationResult.NO_CHANGE


def modify(f: OpenFileModification, match: str, replacement: str, index_delta: int) -> bool:
    success = False
    ins_now = -999
    for line in f.input_lines:
        f.output_lines.append(line)
        if ins_now >= 0:
            ins_now -= 1
        if ins_now == 0:
            f.output_lines.append(replacement)
        if match in line:
            if index_delta == 0:
                f.output_lines.insert(len(f.output_lines) - 2, replacement)
            elif index_delta < 0:
                f.output_lines.insert(len(f.output_lines) - 1 + index_delta, replacement)
            else:
                ins_now = index_delta
    return success


if __name__ == "__main__":
    pass
