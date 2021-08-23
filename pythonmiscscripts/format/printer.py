def print_on_depth(depth: int, content: str):
    print(format_with_depth(depth, content), flush=True)


def prompt(depth: int, content: str) -> str:
    return input(format_with_depth(depth, content))


def format_with_depth(depth: int, content: str) -> str:
    pad = ""
    for i in range(0, depth):
        pad += "---"
    pad += "> "
    return "%s%s" % (pad, content)


if __name__ == "__main__":
    print_on_depth(0, "Hi")
    print_on_depth(7, "Oh no")
