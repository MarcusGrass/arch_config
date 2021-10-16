from pythonmiscscripts.file_manipulation.file_modifier import FileModifier, \
    OpenFileModification


def delete_on_match(file_name: str, match: str, lines_above=0, remove=0):
    with FileModifier(file_name, []) as fm:
        modify(fm.read_lines_and_trim_parsers(), match, lines_above, remove)


def modify(f: OpenFileModification, match, lines_above, remove) -> bool:
    rem = False
    skip = 0
    for it in range(0, len(f.input_lines)):
        if skip > 0:
            skip -= 1
            continue
        f.output_lines.append(f.input_lines[it])
        if match in f.input_lines[it]:
            rem = True
            skip = remove
            for i in range(0, lines_above + 1):
                f.output_lines.pop()
                skip -= 1
    return rem


if __name__ == "__main__":
    fmod = FileModifier("line_delete.txt", [])
    f = fmod.read_lines_and_trim_parsers()
    print(modify(f, "delete1", 0, 2))
    print(f.output_lines)

