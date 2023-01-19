from logging.handlers import RotatingFileHandler
import database
import logging
import pickle
import sys
import os

CONFIG = database.autoLogger.CONFIG

NUM_TO_GET = CONFIG.getint("export", "logs_per_request")
OUT_DIR = CONFIG.get("export", "out_path")

class ForeverRollingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        self.last_backup_cnt = 0
        super(ForeverRollingFileHandler, self).__init__(*args, **kwargs)

    # override
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.last_backup_cnt += 1
        nextName = "%s.%d" % (self.baseFilename, self.last_backup_cnt)
        self.rotate(self.baseFilename, nextName)
        if not self.delay:
            self.stream = self._open()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = ForeverRollingFileHandler(
    filename = OUT_DIR, 
    maxBytes = CONFIG.getint("export", "log_bytes"),
    mode = "a",
    encoding = "UTF-8",
    delay = 0
)
logger.addHandler(handler)
 
def main():
    with database.Database() as db:
        
        if not os.path.exists(".oldest_dt.pickle"):
            with open(".oldest_dt.pickle", "wb") as f:
                oldest = db.get_oldest_dt()
                pickle.dump(oldest, f)
        else:
            with open(".oldest_dt.pickle", "rb") as f:
                oldest = pickle.load(f)

        print("oldest: " + str(oldest))
        while True:
            logs = db.get_log(NUM_TO_GET, oldest)
            print("Fetched %d log items" % len(logs))
            for line in logs:
                service, remote_addr, remote_user, utc_time, request, status, bytes_sent, referrer, http_agent = line
                if remote_user is None:
                    remote_user = ""
                if referrer is None:
                    referrer = ""
                if http_agent is None:
                    http_agent = ""

                l = [service, remote_addr, remote_user, str(utc_time), request, str(status), str(bytes_sent), referrer, http_agent]
                logging.info("\t".join(l))
                #print("\t".join(l))

            oldest = logs[-1][3]
            with open(".oldest_dt.pickle", "wb") as f:
                pickle.dump(oldest, f)
            if len(logs) != NUM_TO_GET:
                break

    import rename

if __name__ == "__main__":
    cwd = os.getcwd()
    os.chdir(os.path.split(__file__)[0])
    main()
    os.chdir(cwd)

