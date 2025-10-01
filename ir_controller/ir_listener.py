# ir_listener.py
import subprocess
from utils.matcher import normalize_code


def listen_for_ir(device="/dev/lirc0", normalize=True):
    """
    Yields each raw IR code captured from the device using mode2.

    If normalize=True, yields a normalized (hashable) version of the code.
    """
    try:
        proc = subprocess.Popen(
            ["mode2", "-d", device],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1  # line buffered
        )

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            if line.startswith("code:"):
                code = line.split("code:")[-1].strip()
                if normalize:
                    yield normalize_code(code)
                else:
                    yield code

    except KeyboardInterrupt:
        print("[IR] Listener stopped.")
    except Exception as e:
        print(f"[IR] Error: {e}")
    finally:
        if 'proc' in locals():
            proc.terminate()
            proc.wait()
