## Simple Install Scripts
## Installs Kali Linux Over Debian

---

### Step 1:
```bash
chmod +x *.sh
```

### Step 2:
```bash
./kali_install.sh
```

### Step 3:
```bash
./kali_defaults.sh
```

---

# *Kali* arm build-scripts

## orangepi_zero3.sh

```bash
git clone https://gitlab.com/kalilinux/build-scripts/kali-arm.git
cd kali-arm
wget mygithub_raw -O orangepi_zero3.sh && chmod +x orangepi_zero3.sh 
sudo ./common.d/build_deps.sh
sudo ./orangepi_zero3.sh
```