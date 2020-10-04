import argparse
import re
from dataclasses import dataclass
from pythonmiscscripts.file_manipulation.utils import LineParser, ManipulationResult
from pythonmiscscripts.file_manipulation.line_list_append import insert_unique_to_list
from pythonmiscscripts.file_manipulation.eof_append import append_lines_to_end
from pythonmiscscripts.file_manipulation.next_line_append import insert_after_match


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
        if line.startswith("|-sda3") and "crypto_LUKS" in line:
            root = parse_uuid(line)
        elif line.startswith("|-sda4") and "swap" in line:
            swap = parse_uuid(line)
        elif line.startswith("`-sda5") and "crypto_LUKS" in line:
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
        print("Failed to update %s, needs manual fixing" % grub_default, flush=True)
        return

    cmd_line = "cryptdevice=UUID=%s:croot" \
               " root=/dev/mapper/croot cryptkey=rootfs:%s" % (root_uuid, root_key_file)
    success = insert_unique_to_list(file_name=grub_default, items=cmd_line.split(" "),
                                    start_str="GRUB_CMDLINE_LINUX=", list_start='"', list_closure='"', list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        linux_line = 'GRUB_CMDLINE_LINUX="' + cmd_line + '"'
        success = insert_after_match(grub_default, LineParser(match=lambda l: l.startswith("GRUB_DISTRIBUTOR"),
                                                              replacer=lambda _: linux_line))

    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % grub_default, flush=True)


def update_mkinitcpio(root_key_file: str):
    mkinit = "/etc/mkinitcpio.conf"
    items = [root_key_file]
    success = insert_unique_to_list(file_name=mkinit, items=items,
                                    start_str="FILES=", list_start="(", list_closure=")", list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % mkinit, flush=True)
        return

    items = ["keyboard", "keymap", "encrypt"]
    success = insert_unique_to_list(file_name=mkinit, items=items,
                                    start_str="HOOKS=", list_start="(", list_closure=")", list_sep=" ")
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % mkinit, flush=True)


def update_crypttab(uuids: DevUuids, home_key_file: str):
    crypttab = "/etc/crypttab"
    swap = "swap    UUID=%s    /dev/urandom    swap,cipher=aes-cbc-essiv:sha256,size=256" % uuids.swap
    home = "home    UUID=%s    %s" % (uuids.home, home_key_file)
    success = append_lines_to_end(crypttab, [swap, home])
    if success == ManipulationResult.NO_MATCH:
        print("Failed to update %s, needs manual fixing" % crypttab, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes lsblk output and configures crypto")
    parser.add_argument("-in", dest="lsblk", type=str)
    parser.add_argument("-ckf", dest="root_key_file", type=str)
    parser.add_argument("-hkf", dest="home_key_file", type=str)
    args = parser.parse_args()
    lsblk = args.lsblk
    home_key = args.home_key_file
    root_key = args.root_key_file
    if lsblk is None or home_key is None or root_key is None:
        print("Missing arguments expected -in, -ckf, and -hkf")
        exit(-1)
    parsed_uuids = get_uuids(lsblk_output=lsblk)
    update_default_grub(parsed_uuids.root, root_key)
    update_mkinitcpio(root_key)
    update_crypttab(parsed_uuids, home_key)
    # with open("lsblk_tst.txt", "r") as file:
    #     print(get_uuids(file.read()))
