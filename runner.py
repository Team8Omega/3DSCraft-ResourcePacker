import os
import shutil
import sys

# Define paths
ASSETSDIR = "assets"
ASSETS = os.path.join(ASSETSDIR, "minecraft")
PATCH = os.path.join("patch", "minecraft")
OUTPUT = os.path.join("output", "3dscraft", "resourcepacks", "minecraft")

# Check if a custom ASSETS path is provided
if len(sys.argv) > 1:
    ASSETS = os.path.join(sys.argv[1], "minecraft")
    print(f"Using provided ASSETS path: {sys.argv[1]}")
else:
    print(f"Using default ASSETS path: {ASSETSDIR}")

# Verify that the ASSETS and PATCH directories exist
if not os.path.exists(ASSETS):
    print(f"Error: ASSETS directory does not exist: {ASSETS}")
    sys.exit(1)

if not os.path.exists(PATCH):
    print(f"Error: PATCH directory does not exist: {PATCH}")
    sys.exit(1)

# Create OUTPUT directory if it doesn't exist
if not os.path.exists(OUTPUT):
    print("Creating OUTPUT directory: output")
    os.makedirs(OUTPUT)

# Read files.txt and process each entry
with open("files.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            paths = [path.strip() for path in line.split(',')]

            if len(paths) == 2:  # If there are two paths (dest, src)
                dest = os.path.join(OUTPUT, paths[0])
                src = os.path.join(ASSETS, paths[1])
            else:  # If there is only one path (both dest and src are the same)
                dest = os.path.join(OUTPUT, paths[0])
                src = os.path.join(ASSETS, paths[0])

            if os.path.isdir(src):  # Source is a directory
                print(f"Copying directory {src} to {dest}")
                shutil.copytree(src, dest, dirs_exist_ok=True)
            elif os.path.isfile(src):  # Source is a file
                dest_dir = os.path.dirname(dest)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                print(f"Copying file {src} to {dest}")
                shutil.copy2(src, dest)
            else:
                print(f"Error: Source path does not exist: {src}")
                sys.exit(1)

# Copy all files from PATCH to OUTPUT
print("Copying all files from PATCH to OUTPUT..")
shutil.copytree(PATCH, OUTPUT, dirs_exist_ok=True)

# Completion message
print("Operation completed.")
print(" -")
print("   Place the contents inside of the new 'OUTPUT' directory in the root of your SD card, then you may start playing 3DSCraft.")
print("   - ChatGPT and Team Omega.")
print(" -")
print("   For copyright reasons, you are strictly forbidden from sharing this around in any way. It is for your use only, through your legal act of buying Minecraft and getting the assets.")
print(" -")
print(" - 3DSCraft ResourcePacker done.")
