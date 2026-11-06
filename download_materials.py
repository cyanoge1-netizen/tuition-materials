#!/usr/bin/env python3
"""
Tuition Materials Downloader
Downloads NCTB Textbooks, Dakhil Books & Chapter Guides directly from GitHub.
Eliminates all third-party app dependencies and ads.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse

REPO_RAW_BASE = "https://raw.githubusercontent.com/cyanoge1-netizen/tuition-materials/main"
MANIFEST_URL = f"{REPO_RAW_BASE}/manifest.json"
DEFAULT_DEST = "/sdcard/Documents/TUITION" if os.path.exists("/sdcard") else "./TUITION_DOWNLOADS"

C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_CYAN   = "\033[36m"
C_GREEN  = "\033[32m"
C_YELLOW = "\033[33m"
C_RED    = "\033[31m"
C_BLUE   = "\033[34m"

def fetch_manifest():
    local_manifest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.json")
    if os.path.exists(local_manifest):
        try:
            with open(local_manifest, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    print(C_CYAN + f"[*] Fetching catalog manifest from GitHub..." + C_RESET)
    try:
        req = urllib.request.Request(MANIFEST_URL, headers={"User-Agent": "TuitionDownloader/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(C_RED + f"[-] Error loading manifest from GitHub: {e}" + C_RESET)
        return None

def download_file(item, dest_root):
    rel_path = item["path"]
    size_mb = item.get("size_mb", 0)
    dest_path = os.path.join(dest_root, rel_path)

    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1024:
        print(C_GREEN + f"  [✓] Exists ({size_mb:.1f} MB): {item['filename']}" + C_RESET)
        return True

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    temp_path = dest_path + ".tmp"

    parsed = urllib.parse.urlsplit(item["download_url"])
    encoded_path = urllib.parse.quote(parsed.path)
    safe_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, encoded_path, parsed.query, parsed.fragment))

    print(C_BOLD + f"  [*] Downloading: {item['filename']} ({size_mb:.1f} MB)..." + C_RESET)
    start = time.time()
    try:
        req = urllib.request.Request(safe_url, headers={"User-Agent": "TuitionDownloader/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(temp_path, "wb") as f:
            total = int(resp.getheader("Content-Length", item.get("size_bytes", 0)))
            downloaded = 0
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                now = time.time()
                elapsed = max(0.1, now - start)
                speed_kb = (downloaded / 1024) / elapsed

                if total > 0:
                    pct = int(downloaded * 100 / total)
                    bar = "█" * (pct // 4) + "░" * (25 - (pct // 4))
                    sys.stdout.write(
                        f"\r  {C_CYAN}[{bar}] {pct:>3}% {downloaded/(1024*1024):.1f}/{total/(1024*1024):.1f} MB ({speed_kb:.0f} KB/s){C_RESET}"
                    )
                else:
                    sys.stdout.write(f"\r  {C_CYAN}[Downloading] {downloaded/(1024*1024):.1f} MB ({speed_kb:.0f} KB/s){C_RESET}")
                sys.stdout.flush()

        print()
        os.replace(temp_path, dest_path)
        try:
            os.chmod(dest_path, 0o666)
        except Exception:
            pass
        print(C_GREEN + f"  [+] Saved successfully." + C_RESET)
        return True
    except KeyboardInterrupt:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(C_YELLOW + "\n  [!] Download cancelled." + C_RESET)
        raise
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(C_RED + f"\n  [-] Download failed: {e}" + C_RESET)
        return False

def interactive_menu(manifest):
    files = manifest.get("files", [])
    classes = sorted(list(set(x["class"] for x in files)))

    while True:
        print("\n" + C_CYAN + "=" * 65 + C_RESET)
        print(C_BOLD + C_CYAN + "📚 Tuition Materials Downloader (GitHub Repository)".center(65) + C_RESET)
        print(C_CYAN + "=" * 65 + C_RESET)
        print(f"Repository: {manifest.get('repo')} | Total: {manifest.get('total_files')} files ({manifest.get('total_size_mb')} MB)\n")

        print(C_BOLD + "Select Class to Download:\n" + C_RESET)
        for i, c in enumerate(classes, 1):
            c_files = [x for x in files if x["class"] == c]
            c_size = sum(x["size_mb"] for x in c_files)
            print(f"  {C_CYAN}[{i}]{C_RESET} {c:<12} ({len(c_files)} files, {c_size:.1f} MB)")

        print("\n" + C_BOLD + "Batch Actions:" + C_RESET)
        print(C_GREEN + f"  [A] Download ALL materials ({manifest.get('total_size_mb')} MB)" + C_RESET)
        print(C_YELLOW + "  [G] Download all Guides only" + C_RESET)
        print(C_BLUE + "  [D] Download all Dakhil materials only" + C_RESET)
        print(C_RED + "  [0] Exit" + C_RESET)

        choice = input(C_BOLD + "\nEnter choice: " + C_RESET).strip().upper()
        if choice == "0" or choice == "Q" or choice == "EXIT":
            print("Bye!")
            break

        to_download = []
        if choice == "A":
            to_download = files
        elif choice == "G":
            to_download = [x for x in files if "Guides" in x["path"]]
        elif choice == "D":
            to_download = [x for x in files if "Dakhil" in x["path"]]
        elif choice.isdigit() and 1 <= int(choice) <= len(classes):
            sel_class = classes[int(choice) - 1]
            to_download = [x for x in files if x["class"] == sel_class]
        else:
            print(C_RED + "Invalid choice." + C_RESET)
            continue

        if not to_download:
            print(C_YELLOW + "[-] No files matched criteria." + C_RESET)
            continue

        dest = input(f"Destination folder [{DEFAULT_DEST}]: ").strip()
        if not dest:
            dest = DEFAULT_DEST

        total_mb = sum(x["size_mb"] for x in to_download)
        print(C_BOLD + f"\nStarting download of {len(to_download)} files ({total_mb:.1f} MB) to {dest}...\n" + C_RESET)

        success = 0
        for it in to_download:
            if download_file(it, dest):
                success += 1

        print(C_GREEN + C_BOLD + f"\nFinished! {success}/{len(to_download)} files ready at: {dest}" + C_RESET)
        input("Press Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description="Tuition Materials Downloader")
    parser.add_argument("--all", action="store_true", help="Download all files in repository")
    parser.add_argument("--class", dest="cls", help="Download specific class (e.g. 'Class 5', 'Class 6')")
    parser.add_argument("--guides", action="store_true", help="Download only guide books")
    parser.add_argument("--dakhil", action="store_true", help="Download only Dakhil books")
    parser.add_argument("--list", action="store_true", help="List all available files")
    parser.add_argument("--dest", default=DEFAULT_DEST, help="Destination directory")

    args = parser.parse_args()
    manifest = fetch_manifest()
    if not manifest:
        sys.exit(1)

    files = manifest.get("files", [])

    if args.list:
        print(f"{'Class':<12} | {'Size':<9} | Path")
        print("-" * 65)
        for f in files:
            print(f"{f['class']:<12} | {f['size_mb']:>6.1f} MB | {f['path']}")
        print(f"\nTotal: {len(files)} files, {manifest.get('total_size_mb')} MB")
        return

    # Non-interactive CLI flags
    if args.all or args.cls or args.guides or args.dakhil:
        targets = files
        if args.cls:
            targets = [x for x in targets if args.cls.lower() in x["class"].lower()]
        if args.guides:
            targets = [x for x in targets if "Guides" in x["path"]]
        if args.dakhil:
            targets = [x for x in targets if "Dakhil" in x["path"]]

        print(C_BOLD + f"Downloading {len(targets)} files ({sum(x['size_mb'] for x in targets):.1f} MB) to {args.dest}..." + C_RESET)
        for it in targets:
            download_file(it, args.dest)
        print(C_GREEN + "Done!" + C_RESET)
        return

    # Interactive mode
    try:
        interactive_menu(manifest)
    except KeyboardInterrupt:
        print("\nExiting... Bye!")

if __name__ == "__main__":
    main()
