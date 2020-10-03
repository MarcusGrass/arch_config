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

mkdir /mnt/home  
mkdir /mnt/efi  
mount /dev/mapper/croot /mnt  
mount /dev/mapper/home /mnt/home  
mount /dev/sda2 /mnt/efi  
swapon /dev/sda4

genfstab -U -p /mnt >> /mnt/etc/fstab

pacstrap /mnt base base-devel linux linux-firmware  
arch-chroot /mnt

pacman -S grub  
pacman -S efibootmgr  
pacman -S lvm2  


-- now set up post boot auto decryption, no need for swap --  
dd bs=512 count=4 if=/dev/random of=/root/croot.keyfile iflag=fullblock  
chmod 000 /root/croot.keyfile  
dd bs=512 count=4 if=/dev/random of=/etc/cryptsetup-keys.d/home.key iflag=fullblock  
chmod 000 /etc/cryptsetup-keys.d/home.key  
cryptsetup -v luksAddKey /dev/sda3 /root/croot.keyfile  
cryptsetup -v luksAddKey /dev/sda5 /etc/cryptsetup-keys.d/home.key    

-- boot doesn't unencrypt home --

/etc/mkinitcpio.conf
FILES=(/root/croot.keyfile)

/etc/default/grub  
GRUB_ENABLE_CRYPTODISK=y  

/etc/default/grub  
GRUB_CMDLINE_LINUX="... cryptdevice=UUID=(device-UUID for /dev/sda3):croot root=/dev/mapper/croot cryptkey=rootfs:/root/croot.keyfile ..."  

swap	UUID=(device UUID for /dev/sda4)	/dev/urandom	swap,cipher=aes-xts-plain64,size=256
home    UUID=(device UUID for /dev/sda5)    /etc/cryptsetup-keys.d/home.key

/etc/hostname  
add hostname  

/etc/locale.gen  
uncomment en_US.UTF-8 UTF-8  

locale-gen  
echo LANG=en_US.UTF-8 > /etc/locale.conf  
export LANG=en_US.UTF-8  
ln -s /usr/share/zoneinfo/Europe/Stockholm /etc/localtime  
hwclock --systohc --utc  
passwd  

-- Fix wifi necessities --  
pacman -S iwd  
pacman -S dhcpcd  

-- add gramar user --  

grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB --recheck  
grub-install --target=i386-pc --recheck /dev/sda  
mkinitcpio -P linux  
grub-mkconfig -o /boot/grub/grub.cfg  

exit  
reboot  