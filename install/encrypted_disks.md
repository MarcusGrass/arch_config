## Encrypted disks with luks (password on boot)  
Partitioning (using cfdisk)  
BIOS 1G  /dev/sda1  
EFI > 512M 600 is fine  /dev/sda2  
ROOT ~ 10% Of total, at least 30G  /dev/sda3  
SWAP = 2*RAM  /dev/sda4  
HOME = remaining  /dev/sda5  

Grub does not recognize luks2 yet as of this time.
cryptsetup -y -v luksFormat /dev/sda3 --type luks1
cryptsetup -y -v luksFormat /dev/sda5 --type luks1

cryptsetup open /dev/sda3 croot  
cryptsetup open /dev/sda5 home  

mkfs.fat -F32 /dev/sda2
mkfs.ext4 /dev/mapper/croot
mkfs.ext4 /dev/mapper/home
mkswap /dev/sda4  

mount /dev/mapper/croot /mnt  
mkdir /mnt/home  
mkdir /mnt/efi  
mount /dev/mapper/home /mnt/home  
mount /dev/sda2 /mnt/efi  
swapon /dev/sda4

pacstrap /mnt base base-devel linux linux-firmware  
genfstab -U -p /mnt >> /mnt/etc/fstab
arch-chroot /mnt

if using intel run below to avoid boot issues  
pacman -S intel-ucode

(Can do steps in install/chroot_encrypted_disks.sh manually)   

pacman -S openssl
pacman -S openssh
pacman -S git  
mkdir /home/setup  
cd /home/setup  
git clone https://github.com/MarcusGrass/arch_config.git  
cd arch_config    
chmod +x install/chroot_encrypted_disks.sh  
./install/chroot_encrypted_disks.sh  
