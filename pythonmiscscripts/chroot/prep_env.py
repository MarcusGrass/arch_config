from pythonmiscscripts.file_manipulation.eof_append import append_lines_to_end
from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.opts.user_opts import UserOpts
from pythonmiscscripts.os_io.commands import mkfile, run_cmd
from pythonmiscscripts.templates.template_writer import ToTmpl


def prep_env():
    depth = 0
    print_on_depth(depth, "Prepping env as chroot")
    opts = UserOpts.prompt_for_opts(depth + 1)
    print_on_depth(depth, "Creating user %s" % opts.user_name)
    run_cmd(depth, "useradd %s" % opts.user_name)
    hostname = "/etc/hostname"
    create_with_content(depth, hostname, [opts.host_name])

    hosts = "/etc/hosts"
    create_with_content(depth, hosts, ["127.0.0.1    localhost",
                                       "::1          localhost"])

    append_lines_to_end("/etc/locale.gen", ["en_US.UTF-8 UTF-8"])
    create_with_content(depth, "/etc/locale.conf", ["LANG=en_US.UTF-8"])
    run_cmd(depth, "locale-gen").get_or_throw()
    run_cmd(depth, "ln -s /usr/share/zoneinfo/Europe/Stockholm /etc/localtime").get_or_throw()
    run_cmd(depth, "timedatectl set-timezone Europe/Stockholm").get_or_throw()
    run_cmd(depth, "hwclock --systohc --utc").get_or_throw()

    run_cmd(depth, "useradd -m %s" % opts.user_name).get_or_throw()
    append_lines_to_end("/etc/sudoers", ["%s    ALL=(ALL) NOPASSWD:ALL" % opts.user_name])
    run_cmd(depth, "systemctl --now enable systemd-networkd systemd-resolved iwd").or_print_err()
    run_cmd(depth, "systemctl --now enable dhcpcd").or_print_err()
    tmpl = ToTmpl(template_path="/opts.tmpl", props=opts.__dict__).to_tmpl_fmt()
    save = "/home/setup/arch_config/opts"
    with open(save, "w+") as f:
        f.write(tmpl)
    print_on_depth(depth, "Done prepping env, saved opts to %s" % save)
    print_on_depth(depth, "Remember to run: passwd %s" % opts.user_name)


def create_with_content(depth: int, file: str, content: [str]):
    mkfile(depth, file)
    append_lines_to_end(file, content)


if __name__ == "__main__":
    print(InstallData.default().to_json())
