#!/usr/bin/env python3
"""
Interactive Orange Pi Zero 3 Header Tool (Revamped)
Supports GPIO, PH*/PC*, SPI/UART/I2C/CS lookups and <&pio> mapping.
"""

from colorama import Fore, Style, init
init(autoreset=True)

# ────────────────────────────────────────────────
# Bank mapping
BANK_INDEX = {'PA':0, 'PB':1, 'PC':2, 'PD':3, 'PE':4, 'PF':5, 'PG':6, 'PH':7}

# Header definition: (pin, name, bank, offset)
PINS = [
    (1,  "3.3V", None, None),
    (2,  "5V", None, None),
    (3,  "SPI1_CS0 / UART2_TX", 'PH', 5),
    (4,  "I2C3-SDA", None, None),
    (5,  "SPDIF_OUT", 'PH', 4),
    (6,  "I2C3-SCK", None, None),
    (7,  "PC9 / GPIO-73", 'PC', 9),
    (8,  "UART5-TX", 'PH', 2),
    (9,  "GND", None, None),
    (10, "UART5-RX", 'PH', 3),
    (11, "SDC2_CMD", 'PC', 6),
    (12, "PC11", 'PC', 11),
    (13, "SDC2_CLK", 'PC', 5),
    (14, "GND", None, None),
    (15, "PC8", 'PC', 8),
    (16, "PC15", 'PC', 15),
    (17, "3.3V", None, None),
    (18, "PC14", 'PC', 14),
    (19, "UART2_RTS / SPI1-MOSI", 'PH', 7),
    (20, "GND", None, None),
    (21, "UART2_CTS / SPI1-MISO", 'PH', 8),
    (22, "PC7", 'PC', 7),
    (23, "UART2_RX / SPI1-SCK", 'PH', 6),
    (24, "SPI1-CS", 'PH', 9),
    (25, "GND", None, None),
    (26, "PC10", 'PC', 10),
]
# ────────────────────────────────────────────────

def gpio_number(bank, offset):
    """Return absolute GPIO number."""
    return None if bank is None else BANK_INDEX[bank]*32 + offset

def pio_tuple(bank, offset):
    """Return device tree form <&pio x y 0>."""
    if bank is None: return ""
    return f"<&pio {BANK_INDEX[bank]} {offset} 0>"

# column layout
SEPARATOR_COL = 48

# ────────────────────────────────────────────────
def print_header(highlight=None):
    """Display colorized header layout."""
    left, right = PINS[::2], PINS[1::2]
    print(f"{'Pin':>3} | {'Name / GPIO':<40} || Pin | Name / GPIO")
    print("-"*90)

    for l, r in zip(left, right):
        def fmt(p):
            pin, name, bank, off = p
            gnum = gpio_number(bank, off)
            base = f"{name}"
            if bank:
                base += f" ({bank}{off}, GPIO-{gnum})"
            if highlight and highlight.lower() in base.lower():
                return f"{Fore.YELLOW}{base}{Style.RESET_ALL}"
            elif name in ("GND","3.3V","5V"):
                return f"{Fore.CYAN}{base}{Style.RESET_ALL}"
            return base

        left_col  = f"{l[0]:>3} | {fmt(l)}"
        right_col = f"{r[0]:>3} | {fmt(r)}"
        print(f"{left_col:<{SEPARATOR_COL}}|| {right_col}")
    print()

# ────────────────────────────────────────────────
def search(term):
    """Search for GPIO name, PH*/PC*, SPI/UART/I2C/CS, etc."""
    t = term.upper()
    found = False
    for pin, name, bank, off in PINS:
        gnum = gpio_number(bank, off)
        match = False

        # Numeric GPIO lookup
        if t.isdigit() and gnum == int(t):
            match = True
        # GPIO name (PH5, PC7, etc.)
        elif len(t) >= 3 and t[0] == 'P' and t[1] in BANK_INDEX:
            if bank == t[:2] and str(off) == t[2:]:
                match = True
        # Keyword search (SPI, UART, I2C, CS, etc.)
        elif any(k in name.upper() for k in ["SPI", "UART", "I2C", "CS", "PWM", "SDC", "SPDIF"]) and t in name.upper():
            match = True
        # substring general search
        elif t in name.upper():
            match = True

        if match:
            found = True
            color = Fore.GREEN
            print(f"{color}Pin {pin:<2} | {name:<35} | {bank or '-'}{off if off is not None else ''} | "
                  f"GPIO-{gnum if gnum else '-'} | {pio_tuple(bank,off)}{Style.RESET_ALL}")
    if not found:
        print(f"{Fore.RED}No match for '{term}'{Style.RESET_ALL}")

# ────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interactive Orange Pi Zero 3 Header Tool (revamped)")
    parser.add_argument("--show", action="store_true", help="Display header map interactively")
    parser.add_argument("--lookup", type=str, help="Lookup by GPIO number, bank name, or interface")
    args = parser.parse_args()

    if args.show:
        print_header()
        while True:
            try:
                val = input(Fore.MAGENTA + "Search/Highlight (GPIO/PHx/SPI/UART/q): " + Style.RESET_ALL).strip()
                if val.lower() in ("q","quit","exit"): break
                print_header(highlight=val)
                search(val)
            except KeyboardInterrupt:
                break
    elif args.lookup:
        search(args.lookup)
    else:
        parser.print_help()
