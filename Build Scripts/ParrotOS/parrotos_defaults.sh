#!/bin/bash
# aMiscreant

set -e

NEW_HOSTNAME="parrot"

# Stage 1:
echo "[*] Installing ParrotOS..."
sudo apt-get install -y parrot-interface parrot-core parrot-zsh-profiles parrot-updater bash-completion parrot-tools-full parrot-themes parrot-interface-home parrot-firefox-profiles

# Stage 2:
echo "[*] Changing hostname..."

sudo hostnamectl set-hostname "$NEW_HOSTNAME"
echo "[+] Hostname changed to $NEW_HOSTNAME"

sudo hostnamectl set-hostname parrot
sudo sed -i "s/\borange[^[:space:]]*/parrot/g" /etc/hosts

bash && clear

# Stage 3:
echo "[*] Fixing missing packages.."
sudo apt-get update && sudo apt-get update --fix-missing && sudo apt-get upgrade -y

# Step 4:
# ToDo
# not sure why parrot-tools-full/parrot-tools* doesn't install any tools?... docs.parrotsec.org ...
# ERROR 'parrot-privacy' has no installation ... 'parrot-meta-sdr' 'xplico' 'rocket' 'sslyze' \
# 'convoc2' 'powershell' 'shellter' 'cmospwd' 'pack' 'rainbowcrack' 'king-phisher' 'eyewitness' \
# 'edb-debugger' 'firmware-mod-kit' 'gosh' 'wpscan' 'bluelog' 'blueranger' bluesnarfer'
#
echo "[*] Installing ParrotOS Tools"
sudo apt-get install zsh-autocomplete zsh-syntax-highlighting zsh-autosuggestions \
  parrot-tools-infogathering parrot-tools-vuln parrot-tools-web parrot-tools-pwn \
  parrot-tools-maintain parrot-tools-postexploit parrot-tools-password \
  parrot-tools-wireless parrot-tools-sniff parrot-tools-forensics parrot-tools-automotive \
  parrot-tools-reversing parrot-tools-reporting parrot-meta-crypto parrot-tools-full anonsurf \
  qttranslations5-l10n libqt5svg5 qt5-gtk-platformtheme qtwayland5 gpa sirikali gocryptfs cryfs encryptpad can-utils \
  gscanbus scantool ow-tools ow-shell afflib-tools dumpzilla extundelete rifiuti ewf-tools cabextract autopsy binwalk sleuthkit \
  dc3dd dcfldd ddrescue dex2jar foremost galleta gtkhash guymager hashdeep magicrescue missidentify pasco pdf-parser pdfid pev \
  recoverjpeg reglookup regripper rifiuti2 safecopy scalpel scrounge-ntfs vinetto inetsim forensic-artifacts gpp-decrypt yara \
  arp-scan 0trace amap arping braa thc-ipv6 dmitry dnsenum dnsmap enum4linux etherape gobuster hping3 ike-scan intrace irpas \
  lbd maltego masscan nbtscan netdiscover nmap onesixtyone p0f recon-ng smbclient smbmap smtp-user-enum snmpcheck ssldump sslh \
  sslscan swaks theharvester unicornscan ismtp python3-shodan emailharvester instaloader inspy sherlock nmapsi4 backdoor-factory dbd \
  dns2tcp evil-winrm hyperion iodine laudanum ncat-w32 nishang powercat powershell-empire starkiller proxychains proxytunnel ptunnel \
  pwnat sbd sliver socat stunnel4 udptunnel webacoo webshells weevely windows-binaries brutespray cewl changeme chntpw crackle crunch \
  fcrackzip hashcat hashid hydra john johnny medusa ophcrack-cli ophcrack pdfcrack pipal pixiewps rcracki-mt rsmangler samdump2 sipcrack \
  sucrack thc-pptp-bruter truecrack twofi wordlists device-pharmer statsprocessor mimikatz powersploit wce xspy lynis \
  linux-exploit-suggester armitage beef-xss commix jsql-injection mdbtools metasploit-framework oscanner pompem set shellnoob sidguesser \
  sqldict sqlitebrowser sqlmap sqlninja sqlsus websploit unicorn-magic kerberoast netexec ghidra javasnoop rizin rizin-cutter smali \
  bettercap chaosreader darkstat dnschef dsniff sniffjoke tcpflow driftnet ettercap-graphical fiked hamster-sidejack hexinject \
  isr-evilgrade mitmproxy netsniff-ng rebind responder sslsniff sslsplit tcpreplay wifi-honey wireshark yersinia afl doona dhcpig \
  enumiax iaxflood inviteflood ohrwurm protos-sip rtpbreak rtpflood rtpinsertsound rtpmixsound sipp slowhttptest spike sipvicious \
  thc-ssl-dos unix-privesc-check voiphopper siparmyknife sctpscan cisco-ocs cisco-torch copy-router-config burpsuite caido davtest \
  dirb dirbuster ffuf nikto padbuster skipfish whatweb xsser zaproxy wafw00f parsero aircrack-ng airgeddon asleap \
  btscanner bluez-hcidump bully cowpatty eapmd5pass fern-wifi-cracker hackrf inspectrum mdk3 mfcuk mfoc mfterm libfreefare-bin \
  libnfc-bin reaver redfang rfcat rtlsdr-scanner ubertooth wifite gnunet-gtk gnunet onionshare connect-proxy bleachbit \
  snowflake-client obfs4proxy firewalld socat apparmor-utils nyx torsocks

# Stage 5:
echo "[*] Fixing missing packages.."
sudo apt-get update && sudo apt-get update --fix-missing && sudo apt-get upgrade -y

# Stage 6:
echo "[*] Cleaning up..."
sudo apt-get autoremove -y

# Stage 7:
echo "[*] Rebooting, Applying updates..."
sleep 3
reboot
