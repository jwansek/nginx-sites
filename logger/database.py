import autoLogger
import pymysql

class Database:
    def __enter__(self):
        self.__connection = pymysql.connect(
            **autoLogger.CONFIG["mysql"],
            charset = "utf8mb4"
        )
        return self
    
    def __exit__(self, type, value, traceback):
        self.__connection.commit()
        self.__connection.close()

    def append_log(self, service, remote_addr, remote_user, utc_time, time_offset, request, status, bytes_sent, referrer, http_agent):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO access_log (service, remote_addr, remote_user, `utc_time`, time_offset, request, status, bytes_sent, referrer, http_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (service, remote_addr, remote_user, utc_time, time_offset, request, status, bytes_sent, referrer, http_agent))

    def get_log(self, num_to_get, from_):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
            SELECT service, remote_addr, remote_user, `utc_time`, request, status, bytes_sent, referrer, http_agent
            FROM access_log 
            WHERE `utc_time` > %s 
            ORDER BY `utc_time`
            LIMIT %s;
            """, (from_, num_to_get))
            return cursor.fetchall()
 
    def get_oldest_dt(self):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT MIN(`utc_time`) FROM access_log;")
            return cursor.fetchone()[0]

    def get_youngest_dt(self):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT MAX(`utc_time`) FROM access_log;")
            return cursor.fetchone()[0]

if __name__ == "__main__":
    with Database() as db:
        print(db.get_log())
