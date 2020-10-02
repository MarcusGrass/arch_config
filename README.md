## Instructions, ps I take no responsibility if you use this and brick you machine or end up with issues

Good place to start for formatting disks and getting the os installed with bios https://www.ostechnix.com/install-arch-linux-latest-version/

With UEFI https://www.tecmint.com/arch-linux-installation-and-configuration-guide/

Good info on getting the os to play nice with full screen https://wiki.archlinux.org/index.php/VirtualBox (Probably going to need to add a kernel parameter to get it working).

Basic partitioning without luks (using cfdisk)  
EFI > 512M 600 is fine  
SWAP = 2*RAM  
ROOT ~ 10% Of total, at least 30G  
HOME = remaining  

Basic partitioning with luks encrypted boot (using cfdisk)  
BIOS = 1G  
EFI > 512M 600 is fine  
SWAP = 2*RAM  
ROOT ~ 10% Of total, at least 30G  
HOME = remaining  

* [**Dual Boot**](install/dual_boot.md)  
* [**Bluetooth**](install/bluetooth.md)  
* [**Nice to haves**](install/nice_to_haves.md)  
* [**Aur package install**](install/aurpkginstall.md)  
