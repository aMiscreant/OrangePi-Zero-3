#!/bin/bash
# aMiscreant
# ToDo
# export DEBIAN_FRONTEND=noninteractive
# set apt-get install/upgrade variable
# sudo DEBIAN_FRONTEND=noninteractive apt-get -y \
#    -o Dpkg::Options::="--force-confnew" \
#    -o Dpkg::Options::="--force-confdef" install <packages>

set -e

PARROT_LINK="https://deb.parrot.sh/parrot/pool/main/p/parrot-archive-keyring/parrot-archive-keyring_2024.12_all.deb"
PARROT_DEB="parrot-archive-keyring_2024.12_all.deb"

# Step 1: Install keyring
wget https://deb.parrot.sh/parrot/pool/main/p/parrot-archive-keyring/parrot-archive-keyring_2024.12_all.deb
dpkg -i $PARROT_DEB
sleep 1
rm -rf $PARROT_DEB

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

# Step 3: Add Parrot OS repo
sudo tee /etc/apt/sources.list.d/parrot.list > /dev/null <<EOF
deb https://deb.parrot.sh/parrot lory main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-security main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-backports main contrib non-free non-free-firmware
#deb-src https://deb.parrot.sh/parrot lory main contrib non-free non-free-firmware
#deb-src https://deb.parrot.sh/parrot lory-security main contrib non-free non-free-firmware
#deb-src https://deb.parrot.sh/parrot lory-backports main contrib non-free non-free-firmware
EOF


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

echo "[+] Conversion complete! You are now on ParrotOS lory (reboot recommended)."
echo "[*] Please run ./parrotos_defaults.sh after rebooting"
sleep 2
sudo reboot