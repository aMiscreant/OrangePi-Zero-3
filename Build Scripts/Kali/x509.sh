#!/usr/bin/env bash
# aMiscreant
# Generate new x509 certs

# Subject default: OrangePi
OPI="OrangePi"
# Dir for keys default: /etc/keys
KEY_DIR="/etc/keys"
# Valid for default: 365
DAYS=3650
# default: bits size
# {2048}/{4096}
BITS=2048

# Generate Certificates
generate_cert () {
  # Stage 1:
  if [ ! -d "$KEY_DIR" ]; then
      echo "[*] Directory $KEY_DIR does not exist. Creating..."
      sudo mkdir -p "$KEY_DIR"
  else
      echo "[=] Directory $KEY_DIR already exists"
  fi

  # Stage 2:
  # Check if openssl exists ...
  if command -v openssl >/dev/null 2>&1; then
      echo "[*] openssl found, Generating Certificates..."
      openssl genrsa -out x509_evm.priv $BITS
      openssl req -new -x509 -key x509_evm.priv -out x509_evm.pem -days $DAYS \
          -subj "/CN=$OPI-EVM/"
      openssl x509 -in x509_evm.pem -outform der -out $KEY_DIR/x509_evm.der

      openssl genrsa -out x509_ima.priv $BITS
      openssl req -new -x509 -key x509_ima.priv -out x509_ima.pem -days $DAYS \
          -subj "/CN=$OPI-IMA/"
      openssl x509 -in x509_ima.pem -outform der -out $KEY_DIR/x509_i
  else
      echo "[!] Error: openssl is not installed or not in PATH"
      exit 1
  fi
}

generate_cert