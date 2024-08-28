import os
import shutil
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

ASSETSDIR = "assets"
ASSETS = os.path.join(ASSETSDIR, "minecraft")
PATCH = os.path.join("patch", "minecraft")
OUTPUT = os.path.join("output", "3dscraft", "resourcepacks", "minecraft")
JSON2MP = os.path.join("tools", "json2mp")

if len(sys.argv) > 1:
    ASSETS = os.path.join(sys.argv[1], "minecraft")
    print(f"Using provided ASSETS path: {sys.argv[1]}")
else:
    print(f"Using default ASSETS path: {ASSETSDIR}")

if not os.path.exists(ASSETS):
    print(f"Error: ASSETS directory does not exist: {ASSETS}")
    sys.exit(1)

if not os.path.exists(PATCH):
    print(f"Error: PATCH directory does not exist: {PATCH}")
    sys.exit(1)

if not os.path.exists(OUTPUT):
    print("Creating OUTPUT directory: output")
    os.makedirs(OUTPUT)

lock = Lock()

def process_file(src, dest):
    with lock:
        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
    if src.endswith(".json"):
        mp_dest = dest.replace(".json", ".mp")
        print(f"Converting {src} using json2mp")
        try:
            subprocess.run([JSON2MP, "-i", src, "-o", mp_dest], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {src}: {e}")
            return False
    else:
        print(f"Copying file {src}")
        shutil.copy2(src, dest)
    return True

with ThreadPoolExecutor() as executor:
    futures = []
    with open("files.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                paths = [path.strip() for path in line.split(',')]

                if len(paths) == 2:
                    dest = os.path.join(OUTPUT, paths[0])
                    src = os.path.join(ASSETS, paths[1])
                else:
                    dest = os.path.join(OUTPUT, paths[0])
                    src = os.path.join(ASSETS, paths[0])

                if os.path.isdir(src):
                    for root, _, files in os.walk(src):
                        for file in files:
                            full_src_path = os.path.join(root, file)
                            relative_path = os.path.relpath(full_src_path, ASSETS)
                            full_dest_path = os.path.join(OUTPUT, relative_path)
                            futures.append(executor.submit(process_file, full_src_path, full_dest_path))
                elif os.path.isfile(src):
                    futures.append(executor.submit(process_file, src, dest))
                else:
                    print(f"Error: Source path does not exist: {src}")
                    sys.exit(1)

    for future in as_completed(futures):
        if not future.result():
            sys.exit(1)

print("Processing and copying files from PATCH to OUTPUT...")
with ThreadPoolExecutor() as executor:
    futures = []
    for root, _, files in os.walk(PATCH):
        for file in files:
            full_src_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_src_path, PATCH)
            full_dest_path = os.path.join(OUTPUT, relative_path)
            futures.append(executor.submit(process_file, full_src_path, full_dest_path))

    for future in as_completed(futures):
        if not future.result():
            sys.exit(1)

print("Operation completed.")
print(" -")
print("   Place the contents inside of the new 'OUTPUT' directory in the root of your SD card, then you may start playing 3DSCraft.")
print("   - ChatGPT and Team Omega.")
print(" -")
print("   For copyright reasons, you are strictly forbidden from sharing this around in any way. It is for your use only, through your legal act of buying Minecraft and getting the assets.")
print(" -")
print(" - 3DSCraft ResourcePacker done.")

