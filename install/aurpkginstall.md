## How to install aur packages with pacman
1.	cd into downloads dir to avoid clutter  
2.	git clone https://aur.archlinux.org/<pkg>.git  
3.	cd into new dir  
4.	makepkg -s  
5.	sudo pacman -U <generated-pkg>.pkg.tar.xz  
Done  

