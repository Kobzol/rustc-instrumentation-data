import glob
import os
import shutil
import subprocess
from collections import defaultdict

files = sorted(glob.glob("out.*.txt"))
for file in files:
    tmp_path = "/tmp/out.txt"
    if os.path.isfile(tmp_path):
        os.unlink(tmp_path)
    subprocess.run(["rustfilt", "-i", file, "-o", tmp_path])
    shutil.copy(tmp_path, file)

entries = defaultdict(int)
prefixes = ["core::ptr::drop_in_place<"]
for file in files:
    with open(file) as f:
        for line in f:
            location = line.split(" - ")[0].strip()
            data = line.split(" - ")[1]
            name, count = data.split(": ")
            name = name.strip()
            count = int(count)
            for prefix in prefixes:
                if name.startswith(prefix):
                    name = name[len(prefix):-1]
            entries[(name, location)] += count
            # entries[name] += count

entries = sorted(entries.items(), key=lambda v: v[1], reverse=True)
with open("output.txt", "w") as f:
    for (name, count) in entries:
        print(f"{name[0]} [{name[1]}]: {count}", file=f)
        # print(f"{name}: {count}", file=f)
