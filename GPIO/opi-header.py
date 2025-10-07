#!/usr/bin/env python3
"""
Orange Pi Zero 3 Header Pin Lookup + Device Tree Overlay Helper
2x13 Header, GPIO numbers, and <&pio X Y 0> mapping
"""

# Mapping of bank letter to numeric index
BANK_INDEX = {
    'PA': 0,
    'PB': 1,
    'PC': 2,
    'PD': 3,
    'PE': 4,
    'PF': 5,
    'PG': 6,
    'PH': 7,
}

# Pin mapping: (pin, name, bank, offset)
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

def gpio_number(bank, offset):
    """Compute full GPIO number from bank and offset."""
    if bank is None or offset is None:
        return None
    return BANK_INDEX[bank] * 32 + offset

def to_pio_tuple(bank, offset, flags=0):
    """Return <&pio bank_index offset flags>"""
    if bank is None or offset is None:
        return None
    return f"<&pio {BANK_INDEX[bank]} {offset} {flags}>"

def show_header():
    """Display formatted 2x13 header with GPIO + PIO info"""
    left = PINS[::2]
    right = PINS[1::2]

    print(f"{'Pin':>2} | {'Name':<35} | {'GPIO':<8} | {'PIO Tuple':<18} || {'Pin':>2} | {'Name':<35} | {'GPIO':<8} | {'PIO Tuple'}")
    print("-"*120)

    for l, r in zip(left, right):
        l_gpio = gpio_number(l[2], l[3])
        r_gpio = gpio_number(r[2], r[3])
        l_pio = to_pio_tuple(l[2], l[3]) or ""
        r_pio = to_pio_tuple(r[2], r[3]) or ""

        print(f"{l[0]:>2} | {l[1]:<35} | {str(l_gpio) if l_gpio else '':<8} | {l_pio:<18} || {r[0]:>2} | {r[1]:<35} | {str(r_gpio) if r_gpio else '':<8} | {r_pio}")

def lookup_gpio(gpio_number_value):
    """Find pin by GPIO number"""
    for pin, name, bank, offset in PINS:
        if gpio_number(bank, offset) == gpio_number_value:
            print(f"GPIO-{gpio_number_value} (bank {bank}, offset {offset}) = pin {pin}: {name}")
            print(f"Overlay syntax: {to_pio_tuple(bank, offset)}")
            return
    print(f"GPIO-{gpio_number_value} not found on 2x13 header.")

def lookup_overlay(expr):
    """Lookup GPIO name (e.g., PC7 or ph4) and show overlay form."""
    expr = expr.upper().strip()
    if len(expr) < 3 or expr[0] != 'P' or expr[1] not in BANK_INDEX:
        print("Invalid GPIO name format. Use like PC7, PH5, etc.")
        return
    bank = expr[:2]
    try:
        offset = int(expr[2:])
    except ValueError:
        print("Invalid offset in name.")
        return

    gpio_num = gpio_number(bank, offset)
    print(f"{expr} → GPIO-{gpio_num}")
    print(f"Overlay syntax: {to_pio_tuple(bank, offset)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Orange Pi Zero 3 Header / Overlay Helper")
    parser.add_argument("--show", action="store_true", help="Display 2x13 header map")
    parser.add_argument("--gpio", type=int, help="Lookup pin by GPIO number")
    parser.add_argument("--overlay", type=str, help="Lookup overlay tuple from name (e.g., PC7)")
    args = parser.parse_args()

    if args.show:
        show_header()
    elif args.gpio is not None:
        lookup_gpio(args.gpio)
    elif args.overlay:
        lookup_overlay(args.overlay)
    else:
        parser.print_help()
