import os
import sys

from glob import glob
import pandas as pd
import sqlite3


def importdata():
    DATABASE_NAME = "mimic3.db"
    THRESHOLD_SIZE = 5 * 10 ** 7
    CHUNKSIZE = 10 ** 6
    CONNECTION_STRING = "sqlite:///{}".format(DATABASE_NAME)

    index_column = "row_id"

    if os.path.exists(DATABASE_NAME):
        msg = "File {} already exists.".format(DATABASE_NAME)
        print(msg)
        sys.exit()

    for f in glob("*.csv"):
        print("Starting processing {}".format(f))
        if os.path.getsize(f) < THRESHOLD_SIZE:
            df = pd.read_csv(f, index_col=index_column)
            df.to_sql(f.strip(".csv").lower(), CONNECTION_STRING)
        else:
            # If the file is too large, let's do the work in chunks
            for chunk in pd.read_csv(f, index_col=index_column, chunksize=CHUNKSIZE):
                chunk.to_sql(
                    f.strip(".csv").lower(), CONNECTION_STRING, if_exists="append"
                )
        print("Finished processing {}".format(f))

    print("Should be all done!")


def verify():
    try:
        conn = sqlite3.connect('mimic3.db')
    except Exception:
        return
    sql = """
            SELECT * FROM sqlite_master
            WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'
        UNION ALL
            SELECT * FROM sqlite_temp_master
            WHERE type IN ('table','view')
            ORDER BY 1
        """
    cursor = conn.execute(sql)
    for row in cursor:
        print(row)


if __name__ == '__main__':
    importdata()
    verify()
