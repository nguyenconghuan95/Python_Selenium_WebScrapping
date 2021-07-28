#!/usr/bin/python

import sys, re, os
import argparse

from selenium import webdriver

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir + "/lib/")

from common import *
from db_common import *
from stockdb import *
from stocktracker import *

class Config:
    def __init__(self, default={}):
        self.debug  = default.get("debug", False)
        self.dbname = default.get("dbname") or "./db/stock_follow.db"
        self.dbmode = default.get("dbmode") or "append"
        self.website = default.get("website") or "https://finance.vietstock.vn"
        self.stock_code = default.get("stock_code") or "POW"
        self.gui = default.get("gui", False)
        self.print_info()

    def print_info(self):
        print("*********************************************")
        print("debug: %s" % self.debug)
        print("dbname: %s" % self.dbname)
        print("dbmode: %s" % self.dbmode)
        print("stock_code: %s" % self.stock_code)
        print("website: %s" % self.website)
        print("gui: %s" % self.gui)
        print("*********************************************")

class StockScrapper:
    def __init__(self):
        pass

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--db_file", type=str, help="database filename", required=False)
        parser.add_argument("--debug", action="store_true", default=False, help="enable print data to debug", required=False)
        parser.add_argument("-n", "--new", action="store_const", const="new", dest="mode", help="create new database file (the exist db will be removed)")
        parser.add_argument("-a", "--append", action="store_const", const='append', dest='mode', help='append the exist db file')
        
        parser.add_argument("-c", "--stock_code", type=str, help="stock code to search or add", required=False)
        parser.add_argument("--add_code", action="store_true", help="add one stock code to db", required='--stock_code' in sys.argv)
        parser.add_argument("-w", "--website", type=str, help="provide base website for scrapping", required=False)
        parser.add_argument("-g", "--gui", action="store_true", default=False, help="use GUI for browser", required=False)

        args = parser.parse_args()

        self.config = Config({
            "debug": args.debug,
            "dbname": args.db_file or '/mnt/d/HuanNguyen/Projects/Python_Web_Scrapping/db/stock_follow.db',
            "dbmode": args.mode,
            "stock_code": args.stock_code,
            "add_code": args.add_code,
            "website": args.website,
            "gui": args.gui,
            "args": args
        })

    def main(self):
        self.setup_libraries()

    def setup_libraries(self):
        self.stockdb = Stock(self.config)
        self.stocktracker = StockTracker({"config": self.config, "stockdb": self.stockdb})
        self.stocktracker.main()
        return None

def main():
    global stocktracker
    stockscrapper = StockScrapper()
    stockscrapper.parse_arguments()
    stockscrapper.main()

if __name__ == "__main__": main()
