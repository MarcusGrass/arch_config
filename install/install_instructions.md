## Encrypted disks with luks (password on boot)  
Partitioning (using cfdisk)  
BIOS 1G  /dev/sda1 (label BIOS BOOT)  
EFI > 512M 600 is fine  /dev/sda2 (label EFI SYSTEM)  
ROOT ~ 10% Of total, at least 30G  /dev/sda3 (label Linux filesystem)  
SWAP ~ RAM size /dev/sda4 (label Linux swap)  
HOME = remaining  /dev/sda5 (label Linux filesystem)      

If installing on an nvme disk just sub /dev/sdaX with /dev/nvme-n-pX and REMEMBER TO ADD (vmd) to /etc/mkinitcpio.conf 
modules

Grub does not recognize luks2 yet as of this time.  
cryptsetup -y -v luksFormat /dev/sda3 --type luks1  
cryptsetup -y -v luksFormat /dev/sda4 --type luks1  
cryptsetup -y -v luksFormat /dev/sda5 --type luks1  

cryptsetup open /dev/sda3 croot  
cryptsetup open /dev/sda4 cswap  
cryptsetup open /dev/sda5 home  

mkfs.fat -F32 /dev/sda2  
mkfs.ext4 /dev/mapper/croot  
mkfs.ext4 /dev/mapper/home  
mkswap /dev/mapper/cswap  

mount /dev/mapper/croot /mnt  
mkdir /mnt/home  
mkdir /mnt/efi  
mount /dev/mapper/home /mnt/home  
mount /dev/sda2 /mnt/efi  
swapon /dev/mapper/cswap

# Log in to wifi if necessary
iwctl  
station wlan0 connect <wifi_name>  

pacstrap /mnt base base-devel linux linux-firmware  
genfstab -U -p /mnt >> /mnt/etc/fstab  
arch-chroot /mnt

if using intel run below to avoid boot issues  
pacman -S intel-ucode

(Can do steps in install/chroot_encrypted_disks.sh manually)   

pacman -S git  
mkdir /home/setup  
cd /home/setup  
git clone https://github.com/MarcusGrass/arch_config.git  
cd arch_config    
chmod +x install/chroot_encrypted_disks.sh  
# Run with disk names, example args below
./install/chroot_encrypted_disks.sh sda sda3 sda4 sda5
