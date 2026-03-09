import sys
from pykeepass import PyKeePass

BANNER = """
╔═══════════════════════════════════════╗
║       KeePass Viewer by VusalHC       ║
║         github.com/vusalhc            ║
╚═══════════════════════════════════════╝
"""

def view(kdbx_file, password):
    print(BANNER)
    print(f"[*] Fayl  : {kdbx_file}")
    print(f"[*] Şifrə : {password}")
    print(f"[*] Açılır...\n")

    try:
        kp = PyKeePass(kdbx_file, password=password)
        print(f"[+] Uğurla açıldı!\n")
        print("=" * 40)

        for entry in kp.entries:
            print(f"  Başlıq     : {entry.title}")
            print(f"  İstifadəçi : {entry.username}")
            print(f"  Şifrə      : {entry.password}")
            print(f"  URL        : {entry.url}")
            print("  " + "-" * 36)

    except Exception as e:
        print(f"[-] Xəta: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"İstifadə: python3 {sys.argv[0]} <fayl.kdbx> <şifrə>")
        sys.exit(1)

    view(sys.argv[1], sys.argv[2])
