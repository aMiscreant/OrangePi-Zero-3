#!/usr/bin/env bash
# aMiscreant

# Settings
KERNEL_SOURCE="https://github.com/torvalds/linux.git"
KERNEL_BRANCH="v6.6"
KERNEL_OUTPUT_DIR="kernel-mainline"
ORANGE_PI_FIRMWARE="https://github.com/orangepi-xunlong/firmware"
# Configure custom defconfig
CUSTOM_DEFCONFIG=""

# Cross compile setup (edit if toolchain differs)
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-

# ========= Menu ========= #
menu () {
  clear
  echo "=============================="
  echo " Orange Pi Kernel Build Script"
  echo "=============================="
  echo "1) Download Kernel"
  echo "2) Download OrangePi Firmware"
  echo "3) Install Build Dependencies"
  echo "4) Configure Kernel (menuconfig)"
  echo "5) Compile Kernel"
  echo "6) Compile Kernel .debs"
  echo "7) Clean Kernel Directory"
  echo "8) Exit"
  echo "=============================="
  read -rp "Select an option: " choice

  case $choice in
    1) download_kernel ;;
    2) download_firmware ;;
    3) download_dependencies ;;
    4) configure_kernel ;;
    5) compile_kernel ;;
    6) compile_kernel_debs ;;
    7) compile_clean ;;
    8) exit 0 ;;
    *) echo "Invalid option"; sleep 2 ;;
  esac
  menu
}

# ========= Functions ========= #
download_kernel() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[*] Downloading Kernel Source..."
    git clone --depth=1 --branch "$KERNEL_BRANCH" "$KERNEL_SOURCE" "$KERNEL_OUTPUT_DIR"
    echo "[+] Kernel Source Downloaded"
  else
    echo "[=] Kernel source already exists in $KERNEL_OUTPUT_DIR"
  fi
  sleep 2
}

download_firmware() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[!] Please download kernel source first!"
    sleep 2
    return
  fi
  if [ ! -d "$KERNEL_OUTPUT_DIR/firmware" ]; then
    echo "[*] Downloading Orange Pi Firmware..."
    git clone "$ORANGE_PI_FIRMWARE" "$KERNEL_OUTPUT_DIR/firmware"
    echo "[+] Firmware downloaded"
  else
    echo "[=] Firmware already exists"
  fi
  sleep 2
}

download_dependencies() {
  echo "[*] Installing build dependencies..."
  sudo apt update
  sudo apt install -y \
    build-essential clang g++ gawk make fakeroot git wget curl unzip rsync file patch bzip2 \
    python3 python3-distutils python3-setuptools perl swig gettext libncurses5-dev libssl-dev \
    libelf-dev libtool autoconf automake pkg-config libgmp-dev libmpfr-dev libmpc-dev flex bison \
    bc xsltproc debhelper debhelper-compat libdb-dev libleveldb-dev sunxi-tools u-boot-tools \
    crust-firmware dpkg-dev dwarves cpio liblzma-dev kernel-wedge device-tree-compiler ninja-build \
    cmake cmake-format crossbuild-essential-arm64
  echo "[+] Dependencies installed"
  sleep 2
}

configure_kernel() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[!] Kernel source not found. Download it first."
    sleep 2
    return
  fi

  cd "$KERNEL_OUTPUT_DIR" || exit

  if [ -n "$CUSTOM_DEFCONFIG" ]; then
    CONFIG_PATH="arch/arm64/configs/$CUSTOM_DEFCONFIG"
    if [ -f "$CONFIG_PATH" ]; then
      echo "[*] Using custom defconfig: $CONFIG_PATH"
      make O=out ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE "$CUSTOM_DEFCONFIG"
    else
      echo "[!] Custom defconfig $CUSTOM_DEFCONFIG not found in arch/arm64/configs. Using default."
      make O=out ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE defconfig
    fi
  else
    echo "[*] No custom defconfig set. Using default."
    make O=out ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE defconfig
  fi

  echo "[*] Launching menuconfig..."
  make O=out ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE menuconfig
}

compile_kernel() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[!] Kernel source not found. Download it first."
    sleep 2
    return
  fi
  cd "$KERNEL_OUTPUT_DIR" || exit
  echo "[*] Starting kernel build..."
  make ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE O=out -j"$(nproc)"
  echo "[+] Kernel build complete"
}

compile_kernel_debs() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[!] Kernel source not found. Download it first."
    sleep 2
    return
  fi
  cd "$KERNEL_OUTPUT_DIR" || exit
  echo "[*] Starting kernel build..."
  make ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE bindeb-pkg O=out -j"$(nproc)"
  echo "[+] Kernel build complete"
}

compile_clean() {
  if [ ! -d "$KERNEL_OUTPUT_DIR" ]; then
    echo "[!] Please download kernel source first!"
    sleep 2
    return
  fi
  if [ ! -d "$KERNEL_OUTPUT_DIR/out" ]; then
    echo "[*] Cleaning directory..."
    cd $KERNEL_OUTPUT_DIR && rm -rf out && make ARCH=$ARCH mrproper
    echo "[+] Directory cleaned."
  else
    echo "[=] Directory already cleaned."
  fi
  sleep 2
}
# ========= Start ========= #
menu
