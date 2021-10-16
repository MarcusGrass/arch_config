from pythonmiscscripts.opts.user_opts import UserOpts
from pythonmiscscripts.templates.template_writer import ToTmpl
import os


def to_user_persistence(opts: UserOpts) -> str:
    tmpl = ToTmpl("/opts.tmpl",
                  props={
                      "USER_NAME": opts.user_name,
                      "HOST_NAME": opts.host_name,
                      "GIT_USER": opts.git_user,
                      "EMAIL": opts.email,
                      "XMONAD": opts.xmonad,
                      "PROGRAMMING": opts.programming,
                      "NVIDIA": opts.nvidia,
                      "YAY": opts.yay,
                  })
    return tmpl.to_tmpl_fmt()


def from_user_persistence(file_name: str) -> UserOpts:
    with open(file_name) as f:
        args = dict()
        for line in f.readlines():
            kv = line.split("=")
            k = kv[0].lower().strip()
            v = kv[1].strip()
            args[k] = v

        return UserOpts(
            host_name=args["host_name"],
            user_name=args["user_name"],
            git_user=args["git_user"],
            email=args["email"],
            xmonad=args["xmonad"] == "True",
            programming=args["programming"] == "True",
            nvidia=args["nvidia"] == "True",
            yay=args["yay"] == "True"
        )


def to_openswap_hook(swap_key: str, swap_part: str) -> str:
    tmpl = ToTmpl("/etc/initcpio/hooks/openswap",
                  props={
                      "SWAP_KEY_FILE": swap_key,
                      "SWAP_PART": swap_part,
                  })
    return tmpl.to_tmpl_fmt()


def to_openswap_install(swap_part: str) -> str:
    tmpl = ToTmpl("/etc/initcpio/install/openswap",
                  props={
                      "SWAP_PART": swap_part,
                  })
    return tmpl.to_tmpl_fmt()


def to_xmobarrc(with_battery: bool, num_cpus: int) -> str:
    acts_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "xmobar_actions.txt")
    actions = ""
    with open(acts_file, "r") as f:
        for line in f.readlines():
            actions += line.strip()
    bat_enable = " | %battery%"
    bat_value = """        -- battery
    , Run Battery       [ "--template" , "Batt: <acstatus>"
          , "--Low"      , "10"        -- units: %
    , "--High"     , "70"        -- units: %
    , "--low"      , "red"
    , "--normal"   , "green"
    , "--high"     , "orange"

    , "--" -- battery specific options
                               -- discharging status
    , "-o"   , "<left>% (<timeleft>)"
                                              -- AC "on" status
    , "-O"   , "Charging: <left>% (<timeleft>)" -- dAA520
                                                         -- charged status
    , "-i"   , "Charged" -- #006000
    ] 50"""
    if not with_battery:
        bat_enable = ""
        bat_value = ""
    cpus = "<total0>%"
    for i in range(1, num_cpus):
        cpus += "|<total%s>%%" % i
    tmpl = ToTmpl("/.xmobarrc",
                  props={
                      "BATTERY": bat_enable,
                      "BATTERY_CFG": bat_value,
                      "ACTIONS": actions,
                      "CPUS": cpus
                  })
    return tmpl.to_tmpl_fmt()


if __name__ == "__main__":
    # print(to_xmobarrc(True, 6, ""))
    # print(from_user_persistence("/home/gramar/code/arch_config/pythonmiscscripts/templates/opts.tmpl"))
    # print(to_xmobarrc(False, multiprocessing.cpu_count()))
    pass
