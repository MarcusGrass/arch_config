from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.input_utils.parse_input import confirm
from pythonmiscscripts.install_utils.install_yay import install_yay
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.os_io.commands import pacman_install, yay_install

base = [
    "grub",
    "sudo",
    "cronie",
    "ntp",
    "unzip",
    "gcc",
    "linux-headers",
    "dhcpcd",
    "iwd",
    "openssh",
    "openssl",
    "gnupg",
    "gnome-keyring",
    "bash-completion",
    "neovim",
    "python",
    "python-pip",
    "git",
    "bluez-utils",
    "pulseaudio",
    "pulseaudio-bluetooth",
    "pulseaudio-alsa",
    "pavucontrol",
    "pass",
    "os-prober",
    "docker",
    "docker-compose",
    "dnsutils",
    "netcat"
]
xmonad = [
    "xterm",
    "alacritty",
    "xorg-server",
    "xmonad",
    "xmonad-contrib",
    "xmobar",
    "dmenu",
    "dunst",
    "xorg-xinit",
    "xorg-xinput",
    "xorg-xrandr",
    "xscreensaver",
    "xclip",
    "maim",
    "feh",
    "pinta",
    "redshift",
    "papirus-icon-theme",
    # xmobar deps
    "otf-font-awesome",
    "ttf-ubuntu-font-family",
    "trayer",
    "xdotool",


]
programming = [
    "rustup",
    "lld",  # Linker
    "clang",  # g++ etc
    "jdk11-openjdk",
    "jdk8-openjdk",
    "openjdk11-src",
    "openjdk8-src",
    "maven",
    "subversion",
    "nodejs",
    "npm",
    "dbeaver",
    "discord",
]

nvidia = [
    "nvidia",
    "nvidia-settings",
]

non_nvidia = [
    "arandr",
    "autorandr",
]

yay = [
    "google-chrome",
    "spotify",
    "steam",
    "slack-desktop",
    "discord",
    "intellij-idea-ultimate-edition-jre",
    "intellij-idea-ultimate-edition",
    "ttf-mononoki",
    # Neovim ide
    "watchman-bin"  # File watching
]


def install_all(depth: int, data: InstallData) -> [str]:
    print_on_depth(depth, "Preparing packag install")
    to_install = base
    if bool(data.user_opts.xmonad):
        print_on_depth(depth, "Include xmonad deps")
        to_install += xmonad
    if bool(data.user_opts.programming):
        print_on_depth(depth, "Include programming deps")
        to_install += programming
    if bool(data.user_opts.nvidia):
        print_on_depth(depth, "Include nvidia drivers")
        to_install += nvidia
    else:
        print_on_depth(depth, "Exclude nvidia drivers")
        to_install += non_nvidia
    print_on_depth(depth, "Installing %s packages" % len(to_install))
    for pkg in to_install:
        res = pacman_install(depth + 1, pkg)
        if not res.was_successful():
            print_on_depth(depth, "Failed to install pkg: %s" % pkg)
    print_on_depth(depth, "Successfully installed pacman packages")

    if bool(data.user_opts.yay):
        install_yay(depth + 1)
        for pkg in yay:
            if confirm(depth + 1, "Install package %s with yay? " % pkg):
                yay_install(depth + 1, pkg).or_print_err()


if __name__ == "__main__":
    # print(install_all(default_opts()))
    pass
