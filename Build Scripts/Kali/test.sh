#!/usr/bin/env bash
#
# Full Orange Pi Zero 3 (ARM64) image build
# Uses mainline Linux v6.6
#

set -e
# -------------------------
# Configuration
# -------------------------
hw_model=${hw_model:-"orangepi-zero3"}
architecture=${architecture:-"arm64"}
desktop=${desktop:-"xfce"}
KERNEL_VERSION="6.6.0-amiscreant"
ROOTFS_URL=${ROOTFS_URL:-"https://images.kali.org/kali-rolling/kali-linux-2025.1-arm64-minimal.tar.gz"}
WORK_DIR=${WORK_DIR:-"$HOME/opi-build"}
IMAGE_NAME=${IMAGE_NAME:-"orangepi-zero3-kali-${KERNEL_VERSION}"}

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# -------------------------
# Download / extract rootfs
# -------------------------
status() { echo -e "\n===== $1 =====\n"; }

status "Downloading minimal ARM64 rootfs"
if [ ! -f rootfs.tar.gz ]; then
    wget -O rootfs.tar.gz "$ROOTFS_URL"
fi

status "Extracting rootfs"
mkdir -p rootfs
tar -xzf rootfs.tar.gz -C rootfs

# -------------------------
# Prepare chroot environment (QEMU for ARM64)
# -------------------------
status "Copying qemu-user-static for ARM64 emulation"
sudo apt install -y qemu-user-static binfmt-support
cp /usr/bin/qemu-aarch64-static rootfs/usr/bin/

# -------------------------
# Build mainline kernel
# -------------------------
status "Cloning Linux v6.6"
git clone --depth 1 --branch v6.6 https://github.com/torvalds/linux.git kernel-mainline
cd kernel-mainline

export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-

# Use saved defconfig or generate from current system
if [ -f ~/kernel-config-backup/amiscreant_defconfig ]; then
    cp ~/kernel-config-backup/amiscreant_defconfig .config
    make olddefconfig
else
    echo "No defconfig found, aborting"
    exit 1
fi

status "Building Debian packages"
make -j$(nproc) bindeb-pkg

cd ..

# -------------------------
# Install kernel packages into rootfs
# -------------------------
status "Installing kernel into rootfs"
dpkg --root rootfs -i kernel-mainline/*.deb

# -------------------------
# Setup DTB + boot files
# -------------------------
status "Injecting DTB and linking kernel/initrd"
mkdir -p rootfs/boot/dtb/allwinner
cp kernel-mainline/arch/arm64/boot/dts/allwinner/sun50i-h618-orangepi-zero3.dtb \
   rootfs/boot/dtb/allwinner/

ln -sf vmlinuz-$KERNEL_VERSION rootfs/boot/Image
ln -sf initrd.img-$KERNEL_VERSION rootfs/boot/uInitrd

# Optional DTB fix script inside rootfs
mkdir -p rootfs/usr/local/sbin
cat <<'EOF' > rootfs/usr/local/sbin/fix-dtb.sh
#!/bin/bash
set -e
KERNEL="6.6.0-amiscreant"
ln -sf /boot/vmlinuz-$KERNEL /boot/Image
ln -sf /boot/uInitrd-$KERNEL /boot/uInitrd
mkdir -p /boot/dtb/allwinner
cp -v /usr/lib/linux-image-$KERNEL/allwinner/sun50i-h618-orangepi-zero3.dtb /boot/dtb/allwinner/
EOF
chmod +x rootfs/usr/local/sbin/fix-dtb.sh

# -------------------------
# Setup network, U-Boot, extlinux
# -------------------------
status "Setting up network and bootloader"
# Example: add eth0/wlan0, copy scripts, update extlinux.conf
# You can reuse your third-stage setup here
# (copy extlinux scripts, update cmdline, etc.)

# -------------------------
# Final image preparation
# -------------------------
status "Creating SD card image"
IMG_SIZE=2G
dd if=/dev/zero of=${IMAGE_NAME}.img bs=1M count=0 seek=$(( IMG_SIZE ))
parted -s ${IMAGE_NAME}.img mklabel msdos
parted -s -a minimal ${IMAGE_NAME}.img mkpart primary ext4 5MiB 100%

LOOP=$(sudo losetup --show -f -P ${IMAGE_NAME}.img)
sudo mkfs.ext4 "${LOOP}p1"
mkdir -p mnt
sudo mount "${LOOP}p1" mnt
sudo rsync -aHAX --progress rootfs/ mnt/
sync
sudo umount mnt
sudo losetup -d $LOOP

status "Image build completed: ${WORK_DIR}/${IMAGE_NAME}.img"
