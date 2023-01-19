import configparser
import datetime
import database
import sys
import os

workingdir = os.path.dirname(__file__)

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(workingdir, "autoLogger.conf"))

def parse_time_offset(theStr):
    theNum = int(theStr[1:-1])
    if theStr.startswith("-"):
        return -theNum
    else:
        return theNum

def append_could_not_parse(line, service):
    with open("couldntparse.log", "a") as f:
        f.write("[%s]:%s\n" % (service, line))

def parse_line(line):
    out = {}
    quotesplit = line.split('"')
    spacesplit = line.split(" ")
    out["request"] = quotesplit[1]
    out["http_agent"] = quotesplit[-2]
    out["remote_addr"] = spacesplit[0]
    out["remote_user"] = spacesplit[2]
    out["utc_time"] = datetime.datetime.strptime(spacesplit[3], "[%d/%b/%Y:%H:%M:%S")
    out["time_offset"] = parse_time_offset(spacesplit[4])
    out["status"] = int(spacesplit[8])
    out["bytes_sent"] = int(spacesplit[9])
    out["referrer"] = quotesplit[3]
    for key, value in out.items():
        if value == "-":
            out[key] = None
    return out
    

def parse_logfile(path, service):
    lines = 0
    with database.Database() as db:
        with open(path, "r") as f:
            for line in f.readlines():
                try:
                    parsed = parse_line(line.rstrip())
                    db.append_log(service = service, **parsed)
                    lines += 1
                except ValueError:
                    append_could_not_parse(line, service)
                    print("Couldn't parse ", line)

        with open(path, "w") as f:
            f.write("")
    print("Added %d lines from log file %s" % (lines, path))

if __name__ == "__main__":
    for service, path in dict(CONFIG["logs"]).items():
        parse_logfile(path, service)
    print("Finished at %s" % datetime.datetime.now())
