#!/bin/bash
# aMiscreant
# ToDo
# export DEBIAN_FRONTEND=noninteractive
# set apt-get install/upgrade variable
# sudo DEBIAN_FRONTEND=noninteractive apt-get -y \
#    -o Dpkg::Options::="--force-confnew" \
#    -o Dpkg::Options::="--force-confdef" install <packages>

set -e

echo "[*] Switching from Debian to Kali Rolling..."

# Step 1: Add Kali keyring
echo "[*] Adding Kali archive keyring..."
sudo wget -q https://archive.kali.org/archive-keyring.gpg -O /usr/share/keyrings/kali-archive-keyring.gpg

# Step 2: Clean Debian repos
echo "[*] Removing Debian repository entries..."
sudo sed -i '/debian/d' /etc/apt/sources.list || true
if [ -d /etc/apt/sources.list.d ]; then
    sudo rm -f /etc/apt/sources.list.d/debian.list 2>/dev/null || true
    sudo rm -f /etc/apt/sources.list.d/debian.sources 2>/dev/null || true
    # Also purge any lines mentioning "debian"
    for f in /etc/apt/sources.list.d/*; do
        sudo sed -i '/debian/d' "$f" 2>/dev/null || true
    done
fi

# Step 3: Add Kali repo
echo "[*] Adding Kali repository..."
echo "deb [signed-by=/usr/share/keyrings/kali-archive-keyring.gpg] http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" | \
    sudo tee /etc/apt/sources.list

# Step 4: Clean
echo "[*] Cleaning apt-get soucres..."
# Clean out old lists
sudo apt clean          # removes downloaded .deb files
sudo rm -rf /var/lib/apt/lists/*   # removes old repo indexes

# Step 5: Update + upgrade
echo "[*] Updating package lists..."
sudo apt-get update

echo "[*] Performing Upgrade (this will take a while)..."
sudo apt-get upgrade -y

# Step 6: Clean-up
echo "[*] Cleaning up..."
sudo apt-get autoremove -y

echo "[+] Conversion complete! You are now on Kali Rolling (reboot recommended)."
echo "[*] Please run ./kali_defaults.sh after rebooting"
sleep 10
sudo reboot
