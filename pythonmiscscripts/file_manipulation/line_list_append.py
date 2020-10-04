from pythonmiscscripts.file_manipulation.line_replace import replace_on_match, modify
from pythonmiscscripts.file_manipulation.utils import LineParser, FileModifier


def insert_unique_to_list(file_name: str, items: [str], start_str: str, list_start: str,
                          list_closure: str, list_sep: str) -> bool:
    parser = create_parser(items, start_str, list_start, list_closure, list_sep)
    return replace_on_match(file_name, [parser])


def create_parser(items: [str], start_str: str, list_start: str, list_closure: str, list_sep: str) -> LineParser:
    return LineParser(lambda l: l.startswith(start_str), lambda l: internal_list_mutation(l, items, start_str,
                                                                                          list_start,
                                                                                          list_closure, list_sep),
                      with_newline=False)


def internal_list_mutation(line: str, items: [str], start_str: str, list_start: str, list_closure: str, list_sep: str) -> str:
    list_s_ind = line.find(list_start) + len(list_start) -1
    list_e_ind = line.rfind(list_closure)
    list_end = line[list_e_ind:]
    current = line[list_s_ind + 1:list_e_ind].split(list_sep)
    if len(current) == 1 and current[0] == "":
        current = list()
    for item in items:
        if item not in current:
            current.append(item)
    return start_str + list_start + list_sep.join(current) + list_end


if __name__ == "__main__":
    parsers = [create_parser(["a", "b"], "my_list=", '"', '"', " "),
               create_parser(["c", "d"], "my_other_list=", "(", ")", ","),
               create_parser(["a", "b"], "empty=", "(", ")", ",")]
    fmod = FileModifier("line_list_append_tst.txt", parsers)
    f = fmod.read_lines_and_trim_parsers()
    modify(f)
    assert len(f.output_lines) == 3
    assert f.output_lines[0] == 'my_list="1 2 3 a b"\n'
    assert f.output_lines[1] == 'my_other_list=(a,b,c,d)\n'
    assert f.output_lines[2] == 'empty=(a,b)\n'
