#### *How to set up cmatrix as a screensaver on TFT.*

#### Runs at reboot

---

- Create file.

```bash
sudo tee /usr/local/bin/tft-matrix.sh > /dev/null <<'EOS'

EOS

sudo chmod +x /usr/local/bin/tft-matrix.sh

```

---

#### Systemd setup

- Save as /etc/systemd/system/tft-matrix.service

```bash
[Unit]
Description=TFT Matrix screensaver
After=multi-user.target network.service getty@tty2.service
Requires=getty@tty2.service

[Service]
Type=simple
ExecStart=/usr/local/bin/tft-matrix.sh
User=root StandardOutput=journal
StandardError=journal
Restart=no

[Install]
WantedBy=multi-user.target

```

- Enable systemd service.

```bash
sudo systemctl daemon-reload
sudo systemctl enable tft-matrix.service
sudo systemctl start tft-matrix.service
# Reboot the machine
reboot

```