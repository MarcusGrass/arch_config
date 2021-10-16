from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.install_utils.update_bt_conf import update_bt_conf
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.os_io.commands import run_cmd


def prep_system(depth: int, data: InstallData):
    if data.user_opts.programming:
        run_cmd(depth, "rustup toolchain install stable").or_print_err()

    # Start services
    print_on_depth(depth, "Enabling services now")
    run_cmd(depth, "sudo systemctl enable --now bluetooth").or_print_err()
    run_cmd(depth, "sudo systemctl enable --now cronie").or_print_err()
    run_cmd(depth, "sudo systemctl enable --now dhcpcd").or_print_err()
    run_cmd(depth, "sudo systemctl enable --now ntpd").or_print_err()
    run_cmd(depth, "sudo pulseaudio -D").or_print_err()

    # Set bluetooth agent on
    print_on_depth(depth, "Setting up default BT agent")
    run_cmd(depth, "sudo bluetoothctl -- default-agent").or_print_err()
    run_cmd(depth, "sudo bluetoothctl -- power on").or_print_err()
    update_bt_conf()
    print(depth, "Successfully prepped system")


