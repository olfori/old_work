import csv
import os

from os import path


class CsvWorker:
    def __init__(self, columns, dir_name):
        self.columns = columns
        self.dir_name = dir_name

    def count_files_in_folder(self):
        '''Count statistics files in /csv/ folder '''
        cc = 0
        for fname in os.listdir(self.dir_name):
            if fname[0] == 's':
                cc += 1
        return cc

    def last_filename(self):
        '''get the string last filename in static/stat/: stat_0.csv...stat_N.csv'''
        count = self.count_files_in_folder()
        if count:
            last_name = '{0}{1}{2}'.format('stat_', count-1, '.csv')
            return last_name
        return ''

    def last_csv_path(self):
        '''get the path to the last filename in static/stat/'''
        name = self.last_filename()
        csv_name = path.join(self.dir_name, name)
        return csv_name

    def create_csv(self):
        '''create csv file in static/stat/ with header from COLUMNS constant'''
        csv_name = self.last_csv_path()
        print(csv_name)
        with open(csv_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)
            writer.writeheader()

    def csv_row_count(self):
        '''return row count in last file in static/stat/'''
        cc = 0
        f_name = self.last_csv_path()
        with open(f_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            for l in reader.reader:
                cc += 1
            return cc

    def last_csv_read(self):
        '''read last csv from static/stat/ and return list '''
        f_name = self.last_csv_path()
        li_res = []
        with open(f_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader.reader:
                li_res.append(row)
            return li_res
