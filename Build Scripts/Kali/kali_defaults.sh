#!/bin/bash
# aMiscreant
# export DEBIAN_FRONTEND=noninteractive

set -e

NEW_HOSTNAME="kali"

# Stage 1:
echo "[*] Installing Kali Defaults"
sudo apt-get install kali-defaults 

# Stage 2:
echo "[*] Changing hostname..."

sudo hostnamectl set-hostname "$NEW_HOSTNAME"
echo "[+] Hostname changed to $NEW_HOSTNAME"

sudo hostnamectl set-hostname kali
sudo sed -i "s/\borange[^[:space:]]*/kali/g" /etc/hosts

# Stage 3:
echo "[*] Installing kali AllWinner"
sudo apt-get install -y kali-sbc-allwinner || echo "[!] Failed to install kali-sbc-allwinner EXPECTED, continuing..."
# Stage 3b:
echo "[*] Fixing missing packages.."
sudo apt-get update && sudo apt-get update --fix-missing && sudo apt-get upgrade -y

# Stage 4:
echo "[*] Installing Kali Themes / Desktop Env"
sudo apt-get update && sudo apt-get upgrade -y \
    kali-themes \
    kali-menu \
    kali-screensaver \
    kali-desktop-xfce

# Stage 5:
echo "[*] Fixing missing packages.."
sudo apt-get update && sudo apt-get update --fix-missing && sudo apt-get upgrade -y

# Stage 6:
echo "[*] Fully Upgrading"
sudo apt-get full-upgrade -y

echo "[*] Installing Kali Tweaks && Tools {bluetooth/wifi/password/crypto}"
sudo apt-get install kali-tweaks -y
sudo apt-get install -y kali-tools-802-11 kali-tools-bluetooth kali-tools-crypto-stego kali-tools-top10 kali-tools-wireless kali-tools-passwords
echo "[*] Fixing missing packages.."
sudo apt-get update && sudo apt-get update --fix-missing && sudo apt-get upgrade -y

# Stage 7:
echo "[*] Cleaning up..."
sudo apt-get autoremove -y

# Stage 7b:
# optional

# Stage 8:
echo "[*] Rebooting OrangePi"
sudo reboot

optional() {
  sudo apt install -y libgtk-4-bin gstreamer1.0-gl \
    xdg-desktop-portal-gtk gstreamer1.0-libav \
    gstreamer1.0-plugins-bad python3-asn1crypto \
    docbook-xml fonts-dejavu libgtk-4-media-gstreamer \
    libegl1-mesa-dev gstreamer1.0-alsa
}