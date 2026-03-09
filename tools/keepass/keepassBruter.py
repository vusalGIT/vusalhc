import sys
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError
from concurrent.futures import ThreadPoolExecutor, as_completed

BANNER = """
╔═══════════════════════════════════════╗
║       KeePass Bruter by VusalHC       ║
║         github.com/vusalhc            ║
╚═══════════════════════════════════════╝
"""

found_password = None

def check(kdbx_file, password):
    global found_password
    if found_password:
        return None
    try:
        PyKeePass(kdbx_file, password=password)
        found_password = password
        return password
    except CredentialsError:
        return None

def brute(kdbx_file, wordlist):
    print(BANNER)
    print(f"[*] Hədəf   : {kdbx_file}")
    print(f"[*] Wordlist: {wordlist}")
    print(f"[*] Thread  : 6")
    print(f"[*] Başlayır...\n")

    with open(wordlist, 'r', errors='ignore') as f:
        passwords = [line.strip() for line in f]

    total = len(passwords)

    try:
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(check, kdbx_file, p): p for p in passwords}
            for i, future in enumerate(as_completed(futures)):
                print(f"\r[~] İrəliləyiş: {i+1}/{total} | Yoxlanılır: {futures[future]:<20}", end='', flush=True)
                result = future.result()
                if result:
                    print(f"\n\n[+] Şifrə tapıldı: {result}")
                    executor.shutdown(wait=False)
                    return

        print("\n\n[-] Şifrə tapılmadı. Wordlist bitdi.")

    except KeyboardInterrupt:
        print("\n\n[!] Quiting...")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"İstifadə: python3 {sys.argv[0]} <fayl.kdbx> <wordlist.txt>")
        sys.exit(1)

    brute(sys.argv[1], sys.argv[2])
