Getting sound to work with a bluetooth headset was difficult.

pulseaudio  
pulseaudio-bluetooth  
pulsemixer  
pulseaudio --start  
bluez  
bluez-utils  

AsusBt500 drivers from their site (need linux-headers)  
blacklist conflicted drivers by adding  
/etc/modprobe.d/bluetooth-blacklist.conf  
blacklist btrtl  
blacklist btusb  
blacklist btintel  
blacklist btbcm  

Then set up using bluetooth guide on arch wiki.
