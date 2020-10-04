## Instructions for dual boot  
install os-prober  
sudo pacman -S os-prober  
sudo mount /mnt/windows  
sudo os-prober  
grub-mkconfig -o /boot/grub/grub.cfg  
sudo umount /mnt/windows  
