from getpass import getpass
from typing import Optional

from pythonmiscscripts.format.printer import prompt, print_on_depth, format_with_depth


def request_str(depth: int, content: str) -> str:
    while True:
        val = prompt(depth, content)
        correct = confirm(depth, "Entered value: <%s> is this correct?\n" % val)
        if correct:
            return val


def confirm(depth: int, content: str) -> bool:
    parsed = None
    while parsed is None:
        parsed = parse_res(prompt(depth, content).strip())
    return parsed


def parse_res(s: str) -> Optional[bool]:
    s = s.lower()
    if s == "y" or s == "yes":
        return True
    if s == "n" or s == "no":
        return False
    return None


def request_pass(depth: int) -> str:
    pass1 = getpass(prompt=format_with_depth(depth, "Enter password: "))
    pass2 = getpass(prompt=format_with_depth(depth, "Enter password again: "))
    if pass1 != pass2:
        print_on_depth(depth, "Password doesn't match.")
        exit(-1)
    return pass1


if __name__ == "__main__":
    request_pass(1)
