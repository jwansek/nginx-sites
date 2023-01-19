import database
import os
import re

CONFIG = database.autoLogger.CONFIG

logs_dir = os.path.split(CONFIG.get("export", "out_path"))[0]

for filename in os.listdir(logs_dir):
    full_path = os.path.join(logs_dir, filename)
    if len(re.findall(r"\.\d+", filename)) > 0 and os.path.split(CONFIG.get("export", "out_path"))[-1] in filename:
        with open(full_path, "r") as f:
            lines = f.readlines()

        first_dt = lines[0].split("\t")[3]
        last_dt = lines[-1].split("\t")[3]
        new_name = "%s --> %s (%i).log" % (first_dt, last_dt, len(lines))

        os.rename(full_path, os.path.join(logs_dir, new_name))
        print("'%s' -> '%s'" % (filename, new_name))
