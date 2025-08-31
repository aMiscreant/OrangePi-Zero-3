#!/usr/bin/env bash
#
# Kali Linux ARM build-script for OrangePi Zero 3 (64-bit)
# Adapted for mainline kernel 6.6.0-amiscreant
#
# ------------------------
#
# ToDo Fix format for kali-arm build scripts
# ToDo Change kernel config to defconfig for git push
# ToDo ERROR No Boot Partition Found
# ------------------------

set -e

hw_model=${hw_model:-"orangepi-zero3"}
architecture=${architecture:-"arm64"}
desktop=${desktop:-"xfce"}

# ------------------------
# Load default base_image configs
# ------------------------
source ./common.d/base_image.sh

# ------------------------
# Network configs
# ------------------------
basic_network
add_interface eth0
add_interface wlan0

# ------------------------
# Third stage setup
# ------------------------
cat <<'EOF' >>"${work_dir}/third-stage"
status_stage3 'Install required packages'
eatmydata apt-get install -y u-boot-menu u-boot-tools file alsa-utils

status_stage3 'Run u-boot update'
u-boot-update

status_stage3 'Fix wireless regulatory database'
update-alternatives --set regulatory.db /lib/firmware/regulatory.db-upstream

status_stage3 'Remove cloud-init where not used'
eatmydata apt-get -y purge --autoremove cloud-init
EOF

# ------------------------
# Run third stage
# ------------------------
include third_stage

# ------------------------
# Clean system
# ------------------------
include clean_system

# ------------------------
# Kernel section
# ------------------------
status "Compile Kernel"
status "Cloning Linux v6.6"
git clone https://github.com/torvalds/linux.git kernel-mainline
cd kernel-mainline
git fetch origin
git checkout v6.6

export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-

# ------------------------
# Use your saved defconfig
# ------------------------
cp ~/kernel-config-backup/amiscreant_defconfig .config
make olddefconfig
# make defconfig

# ------------------------
# Build Debian packages
# ------------------------
make -j$(nproc) bindeb-pkg

# ------------------------
# Install kernel packages inside ARM rootfs
# ------------------------
cd ..
if [ "$(arch)" == 'aarch64' ]; then
    rm linux-libc-dev*.deb || true
    mv "${work_dir}/var/lib/dpkg/statoverride" "${work_dir}/var/lib/dpkg/statoverride.bak"
    dpkg --root "${work_dir}" -i linux-*.deb
    mv "${work_dir}/var/lib/dpkg/statoverride.bak" "${work_dir}/var/lib/dpkg/statoverride"
else
    mv "${work_dir}/var/lib/dpkg/statoverride" "${work_dir}/var/lib/dpkg/statoverride.bak"
    dpkg --root "${work_dir}" -i linux-image-*.deb
    mv "${work_dir}/var/lib/dpkg/statoverride.bak" "${work_dir}/var/lib/dpkg/statoverride"
fi

cd "${repo_dir}/"

# ------------------------
# Full image assembly
# ------------------------
make_image
parted -s "${image_dir}/${image_name}.img" mklabel msdos
parted -s -a minimal "${image_dir}/${image_name}.img" mkpart primary ext4 5MiB 100%
make_loop
mkfs_partitions
make_fstab

mkdir -p "${base_dir}/root"
mount_opts=""
if [[ $fstype == ext4 ]]; then
    mount_opts="-o noatime,data=writeback,barrier=0"
fi
mount -t "$fstype" $mount_opts "${rootp}" "${base_dir}/root"

# ------------------------
# Update extlinux.conf and cmdline
# ------------------------
ROOT_UUID=$(blkid -s UUID -o value "${rootp}")
sed -i -e "0,/append.*/s//append root=UUID=${ROOT_UUID} rootfstype=${fstype} earlyprintk console=ttyS0,115200 console=tty1 console=both swiotlb=1 coherent_pool=1m ro rootwait/g" \
    "${work_dir}/boot/extlinux/extlinux.conf"

sed -i -e "s|.*GNU/Linux Rolling|menu label Kali Linux|g" "${work_dir}/boot/extlinux/extlinux.conf"
sed -i -e "s|root=UUID=.*|root=UUID=${ROOT_UUID}|" "${work_dir}/etc/kernel/cmdline"

echo 'U_BOOT_MENU_LABEL="Kali Linux"' >>"${work_dir}/etc/default/u-boot"
echo 'U_BOOT_PARAMETERS="earlyprintk console=ttyAML0,115200 console=tty1 console=both swiotlb=1 coherent_pool=1m ro rootwait"' >>"${work_dir}/etc/default/u-boot"

# ------------------------
# Inject mainline kernel DTB fix script
# ------------------------
mkdir -p "${base_dir}/root/usr/local/sbin"
cat <<'DTBEOF' >"${base_dir}/root/usr/local/sbin/fix-dtb.sh"
#!/bin/bash
set -e
KERNEL="6.6.0-amiscreant"
ln -sf /boot/vmlinuz-$KERNEL /boot/Image
ln -sf /boot/uInitrd-$KERNEL /boot/uInitrd
mkdir -p /boot/dtb/allwinner
cp -v /usr/lib/linux-image-$KERNEL/allwinner/sun50i-h618-orangepi-zero3.dtb /boot/dtb/allwinner/
DTBEOF
chmod +x "${base_dir}/root/usr/local/sbin/fix-dtb.sh"

# ------------------------
# Sync rootfs to work_dir
# ------------------------
rsync -HPavz -q "${work_dir}/" "${base_dir}/root/"
sync

cd "${repo_dir}/"
include finish_image
