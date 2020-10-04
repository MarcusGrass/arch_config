from pythonmiscscripts.file_manipulation.utils import LineParser
from pythonmiscscripts.file_manipulation.line_replace import replace_on_match
from pythonmiscscripts.file_manipulation.next_line_append import insert_after_match
from pythonmiscscripts.file_manipulation.eof_append import append_lines_to_end

"""
Should be idem
"""


def update_bt_conf():
    bt_file = "/etc/bluetooth/main.conf"
    insert_after_match(bt_file, [append_general(), append_policy()])


def append_general() -> LineParser:
    return LineParser(lambda a: a.startswith("[GENERAL]"), lambda _: "ENABLE=SOURCE,SINK,MEDIA,SOCKET")


def append_policy() -> LineParser:
    return LineParser(lambda a: a.startswith("[POLICY]"), lambda _: "AutoEnable=true")


def append_pulse_system_bt():
    append_lines_to_end("/etc/pulse/system.pa", [
        "### Enable bt", "load-module module-bluetooth-policy", "load-module module-bluetooth-discover"
    ])


def append_pulse_default_bt():
    append_lines_to_end("/etc/pulse/default.pa", [
        "### Enable bt switch on connect", "load-module module-switch-on-connect"
    ])


def set_pulse_autospawn():
    replace_on_match("/etc/pulse/client.conf",
                     [LineParser(lambda l: l.startswith("autospawn = no"), lambda _: "autospawn = yes")])


if __name__ == "__main__":
    update_bt_conf()
    append_pulse_system_bt()
    append_pulse_default_bt()
    set_pulse_autospawn()
