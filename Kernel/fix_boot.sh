#!/bin/bash
# dpkg -i image.deb \
#         headers.deb
# ./fix_boot.sh
# KERNEL_VERSION_STRING must be changed to match
# Example:
#         KERNEL="6.6.0-amiscreant"

set -e

#KERNEL="6.6.0-amiscreant"
KERNEL="KERNEL_VERSION_STRING"

# Point Image and initrd
ln -sf /boot/vmlinuz-$KERNEL /boot/Image
ln -sf /boot/uInitrd-$KERNEL /boot/uInitrd

# Fix DTB: copy only the board DTB to /boot/dtb/allwinner
mkdir -p /boot/dtb/allwinner
cp -v /usr/lib/linux-image-$KERNEL/allwinner/sun50i-h618-orangepi-zero3.dtb \
       /boot/dtb/allwinner/