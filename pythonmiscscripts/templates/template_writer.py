import os

START = "{{%"
END = "%}}"


class ToTmpl(object):
    def __init__(self, template_path: str, props: dict):
        self.template_path = os.path.dirname(__file__) + template_path
        self.props = props

    def to_tmpl_fmt(self) -> str:
        with open(self.template_path) as f:
            lines = f.readlines()

        formatted = []
        for line in lines:
            tokens = extract_all_tokens(line)
            for token in tokens:
                if token.lower() in self.props:
                    use = token.lower()
                elif token in self.props:
                    use = token
                else:
                    raise Exception("No property supplied for token=%s" % token)
                line = replace_token(line, token, self.props[use])
            formatted.append(line)

        return "".join(formatted)


def extract_all_tokens(target: str) -> [str]:
    tokens = []
    tg_copy = target
    while True:
        extracted = extract_token(tg_copy)
        if extracted == "":
            break
        hit = START + extracted + END
        tokens.append(extracted)
        tg_copy = tg_copy.replace(hit, "")
        if "{{%" not in tg_copy and "%}}" not in tg_copy:
            break
    return tokens


def extract_token(target: str) -> str:
    if target.find(START) == -1 or target.find(END) == -1:
        return ""
    return target[target.find(START) + len(START): target.find("%}}")]


def replace_token(target: str, token: str, value: str) -> str:
    original = target
    while True:
        repl = original.replace(START + token + END, str(value))
        if original == repl:
            break
        original = repl
    return repl


if __name__ == "__main__":
    tmpl = ToTmpl("/opts.tmpl",
                  props={
                        "USER_NAME": "gramar",
                        "HOST_NAME": "grarch",
                        "GIT_USER": "MarcusGrass",
                        "EMAIL": "marcus.grass@gmail.com",
                        "XMONAD": "True",
                        "PROGRAMMING": "True",
                        "NVIDIA": "False",
                        "YAY": "True",
                    })
    print(tmpl.to_tmpl_fmt())
