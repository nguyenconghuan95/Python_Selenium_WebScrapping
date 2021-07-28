import os, sys
import datetime

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir + "/./")

from db_common import *
from common import *

class Stock:
    config = None

    def __init__(self, myconfig):
        self.config = myconfig
        self.initialize_db()

    def initialize_db(self):
        dbname, dbmode = self.config.dbname, self.config.dbmode
        if (dbmode == 'new') or (not is_file_exist(dbname)):
            self.remove_db()
            self.setup()
            self.create_schema()
        else:
            self.setup()
        return dbmode

    def remove_db(self):
        os.system('rm -rf %s' % self.config.dbname)
        return None

    def create_schema(self):
        db_create_table('stock_paths', 'stock_name TEXT, stock_code TEXT NOT NULL UNIQUE, path TEXT NOT NULL, key_element TEXT NOT NULL')
        db_create_table('stock_info', 'date TEXT, time TEXT, stock_code TEXT NOT NULL UNIQUE, current_price FLOAT, change_percentage FLOAT')
        return None

    def setup(self):
        return db_setup(self.config.dbname)

    def insert_stock_paths(self, value):
        [stock_code, stock_name, path] = value
        db_query('INSERT INTO stock_paths VALUES ("%s", "%s", "%s")' % (stock_name, stock_code, path))
        return db_lastrowid()

    def insert_stock_info(self, value):
        [stock_code, current_price] = value
        d_full = datetime.datetime.now()
        date = d_full.date().strftime("%y-%m-%d")
        time = d_full.time().strftime("%H:%M")
        change_percentage = 0
        db_query('INSERT INTO stock_info VALUES ("%s", "%s", "%s", %f, %f)' % (date, time, stock_code, float(current_price), change_percentage))
        return db_lastrowid()

    def insert_stock_db(self, value):
        [stock_code, stock_name, path, current_price] = value
        current_price = float(current_price)
        path_lastrowid = self.insert_stock_paths(['%s' % stock_code, '%s' % stock_name, '%s' % path])
        info_lastrowid = self.insert_stock_info(['%s' % stock_code, '%s' % current_price])
        db_commit()
        return [path_lastrowid, info_lastrowid]

    def update_stock_paths(self, value):
        [stock_code, stock_name, path] = value
        db_query("""UPDATE stock_paths
                    SET stock_name='{}', path='{}'
                    WHERE stock_code='{}'""".format(stock_name, path, stock_code))
        return db_lastrowid()

    def update_stock_info(self, value):
        [stock_code, new_price] = value
        d_full = datetime.datetime.now()
        date = d_full.date().strftime("%y-%m-%d")
        time = d_full.time().strftime("%H:%M")
        old_price = self.get_stock_price(stock_code)
        if self.config.debug:
            print("<<< {} >>>".format(self.update_stock_info.__name__))
            print("\t%s" % value)
            print("\t%s" % old_price)
        change_percentage = round((float(new_price) - old_price)/old_price * 100, 3)
        db_query("""UPDATE stock_info 
                    SET date='{}', time='{}',
                        current_price={}, change_percentage={}
                    WHERE stock_code='{}'""".format(date, time, new_price, change_percentage, stock_code))
        return db_lastrowid()

    def update_stock_db(self, value):
        [stock_code, stock_name, path, current_price] = value
        info_lastrowid = self.update_stock_info(['%s' % stock_code, '%s' % current_price])
        path_lastrowid = self.update_stock_paths(['%s' % stock_code, '%s' % stock_name, '%s' % path])
        db_commit()
        return [path_lastrowid, info_lastrowid]


    def remove_stock_code(self, stock_code):
        db_query('DELETE FROM stock_paths WHERE stock_code = "%s"' % stock_code)
        db_query('DELETE FROM stock_info WHERE stock_code = "%s"' % stock_code)
        return None

    def get_stock_path(self, stock_code):
        return db_query('SELECT path FROM stock_paths WHERE stock_code = "%s"' % stock_code)

    def get_stock_name(self, stock_code):
        return db_query('SELECT stock_name FROM stock_paths WHERE stock_code = "%s"' % stock_code)

    def list_all_stock_code(self):
        return db_query('SELECT stock_code FROM stock_paths')

    def get_stock_price(self, stock_code):
        return db_query('SELECT current_price FROM stock_info WHERE stock_code = "%s"' %stock_code)[0][0]

    def get_all_stock_info(self, stock_code):
        return db_query('SELECT * FROM stock_info WHERE stock_code = "%s"' % stock_code)

    def is_code_exist(self, stock_code):
        if self.config.debug:
            print("<<< {} >>>".format(self.is_code_exist.__name__))
            print("\t%s" % self.get_all_stock_info(stock_code))
        return len(self.get_all_stock_info(stock_code)) > 0


