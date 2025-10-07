#!/bin/bash
# TFT Matrix screensaver for Orange Pi Zero 3
# Launch cmatrix on tty2 at boot and exit on first keypress

TTY=/dev/tty2
CMATRIX=/usr/bin/cmatrix

echo "[TFT] Waiting for system to settle..."
sleep 20

echo "[TFT] Switching to tty2..."
/usr/bin/chvt 2
sleep 10

echo "[TFT] Starting cmatrix..."
export TERM=linux
export LANG=C
setsid sh -c "exec >$TTY 2>&1 <$TTY; stty sane; $CMATRIX -s -b -u 3 -C green"
