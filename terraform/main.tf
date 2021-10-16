terraform {

}
// Xmonad
resource "local_file" "xmonad" {
  filename = pathexpand("~/.xmonad/xmonad.hs")
  content = file("../.xmonad/xmonad.hs")
  file_permission = "0644"
}
resource "local_file" "haskell_ico" {
  filename = pathexpand("~/.xmonad/xpm/haskell_20.xpm")
  content = file("../.xmonad/xpm/haskell_20.xpm")
  file_permission = "0644"
}
// Xmobar
resource "local_file" "xmobarrc" {
  filename = pathexpand("~/.config/xmobar/xmobarrc")
  content = file("../.config/xmobar/xmobarrc")
  file_permission = "0644"
}

resource "local_file" "trayer_padding" {
  filename = pathexpand("~/.config/xmobar/trayer-padding-icon.sh")
  content = file("../.config/xmobar/trayer-padding-icon.sh")
  file_permission = "0644"
}
