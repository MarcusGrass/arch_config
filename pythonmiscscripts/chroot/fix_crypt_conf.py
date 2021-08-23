import re
from dataclasses import dataclass

from pythonmiscscripts.file_manipulation.eof_append import append_lines_to_end
from pythonmiscscripts.file_manipulation.file_modifier import LineParser, ManipulationResult
from pythonmiscscripts.file_manipulation.line_delete import delete_on_match
from pythonmiscscripts.file_manipulation.line_list_append import insert_unique_to_list
from pythonmiscscripts.file_manipulation.next_line_append import insert_after_match
from pythonmiscscripts.globals import ROOT, SWAP, HOME, ROOT_SUFFIX, SWAP_SUFFIX, HOME_SUFFIX, CRYPT_ROOT, CRYPT_SWAP
from pythonmiscscripts.os_io.commands import mkfile
from pythonmiscscripts.templates.templates import to_openswap_hook, to_openswap_install


@dataclass
class DevUuids:
    root: str
    home: str
    swap: str


def get_uuids(lsblk_output: str) -> DevUuids:
    root = None
    home = None
    swap = None
    for line in lsblk_output.split("\n"):
        if ROOT_SUFFIX in line and "crypto_LUKS" in line:
            root = parse_uuid(line)
        elif SWAP_SUFFIX in line and "crypto_LUKS" in line:
            swap = parse_uuid(line)
        elif HOME_SUFFIX in line and "crypto_LUKS" in line:
            home = parse_uuid(line)
    if root is None or swap is None or home is None:
        raise Exception("Failed to parse lsblk no match, root=%s, home=%s, swap=%s" % (root, home, swap))
    if len(root) != 36 or len(swap) != 36 or len(home) != 36:
        raise Exception("Failed to parse lsblk wrong uuid length, root=%s, home=%s, swap=%s" % (root, home, swap))
    return DevUuids(root=root, home=home, swap=swap)


def parse_uuid(line: str) -> str:
    return re.sub(' +', ' ', line).replace("\n", "").split(" ")[3]


def update_default_grub(root_uuid: str, root_key_file: str):
    grub_default = "/etc/default/grub"
    success = append_lines_to_end(grub_default, ["GRUB_ENABLE_CRYPTODISK=y"])
    if success == ManipulationResult.NO_MATCH:
        print("Failed to append cryptodisk to update %s, needs manual fixing" % grub_default, flush=True)
        return

    cmd_line = "cryptdevice=UUID=%s:croot" \
               " root=%s cryptkey=rootfs:%s" \
               " resume=%s" % (root_uuid, CRYPT_ROOT, root_key_file, CRYPT_SWAP)
    success = insert_unique_to_list(file_name=grub_default, items=cmd_line.split(" "),
                                    start_str="GRUB_CMDLINE_LINUX=", list_start='"', list_closure='"', list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        linux_line = 'GRUB_CMDLINE_LINUX="' + cmd_line + '"'
        success = insert_after_match(grub_default, LineParser(match=lambda l: l.startswith("GRUB_DISTRIBUTOR"),
                                                              replacer=lambda _: linux_line))

    if success == ManipulationResult.NO_MATCH:
        print("Failed to add cmdline linux update to %s, needs manual fixing" % grub_default, flush=True)


def update_mkinitcpio(depth: int, swap_key_file: str, root_key_file: str):
    hooks = "/etc/initcpio/hooks/openswap"
    install = "/etc/initcpio/install/openswap"
    if mkfile(depth, "/etc/initcpio/hooks/openswap"):
        content = to_openswap_hook(swap_key=swap_key_file, swap_part=SWAP_SUFFIX)
        with open(hooks, "w") as f:
            f.write(content)
    if mkfile(depth, install):
        content = to_openswap_install(swap_part=SWAP_SUFFIX)
        with open(install, "w") as f:
            f.write(content)

    mkinit = "/etc/mkinitcpio.conf"
    items = [root_key_file]
    success = insert_unique_to_list(file_name=mkinit, items=items,
                                    start_str="FILES=", list_start="(", list_closure=")", list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % mkinit, flush=True)
        return

    items = ["keyboard", "fsck", "keymap", "encrypt", "openswap", "resume", "filesystems"]  # Order is important here
    success = insert_unique_to_list(file_name=mkinit, items=items,
                                    start_str="HOOKS=", list_start="(", list_closure=")", list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % mkinit, flush=True)


def update_crypttab(uuids: DevUuids, home_key_file: str):
    crypttab = "/etc/crypttab"
    home = "home    UUID=%s    %s" % (uuids.home, home_key_file)
    success = append_lines_to_end(crypttab, [home])
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % crypttab, flush=True)


def update_fstab():
    delete_on_match("/etc/fstab", "# %s" % CRYPT_SWAP, remove=2)
    append_lines_to_end("/etc/fstab", ["%s\tswap\tswap\tdefaults\t0 0" % CRYPT_SWAP])


def fix_conf(root_key: str, home_key: str, swap_key: str, lsblk: str):
    parsed_uuids = get_uuids(lsblk_output=lsblk)
    update_default_grub(parsed_uuids.root, root_key)
    update_mkinitcpio(0, swap_key, root_key)
    update_crypttab(parsed_uuids, home_key)
    update_fstab()


if __name__ == "__main__":
    pass
