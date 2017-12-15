#!/usr/bin/python
import sqlite3
import sys

import config

def create_database(db_name, data):
    try:
        delete_table(db_name)
    except:
        pass
    create_table(db_name)
    insert_clients(db_name, data)

def create_table(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE Clients
                         (id INTEGER PRIMARY KEY,
                          client TEXT,
                          status TEXT,
                          host TEXT,
                          ifd TEXT,
                          start_time TEXT,
                          progress TEXT,
                          pids TEXT)""")
        db.commit()

def delete_table(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""DROP TABLE Clients""")
        db.commit()

def insert_clients(db_name, values):
    sql = """INSERT INTO Clients
                                (client,
                                status,
                                host,
                                ifd,
                                start_time,
                                progress,
                                pids)
                                VALUES (?, ?, ?, ?, ?, ?, ?)"""

    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.executemany(sql, values)
        db.commit()

def reset_to_defaults():
    pass

def disable_all(db_name):
    # ids = range(1, max_rows + 1)
    sql = """UPDATE Clients SET status=?"""

    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Disabled",))
        db.commit()

def enable_all(db_name):
    sql = """UPDATE Clients SET status=?"""

    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Available",))
        db.commit()

def 






class Database(object):
    '''Open a SQLite Database and control it'''

    def __init__(self, file_path):
        '''Open the file and store the path, header and data'''
        self.path = file_path
        self.data = []
        self.header = []
        self.open_csv(self.path)

    def create_table(self, file_path):
        '''Open a new csv file'''
        self.path = file_path
        self.data = []
        self.header = []
        with open(self.path, "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: self.header = row
                self.data.append(row)

    def save_csv(self):
        '''Save the data to the csv file'''
        with open(self.path, "wb") as csv_file:
            writer = csv.writer(csv_file)
            for row in self.data:
                writer.writerow(row)

    def reset_to_defaults(self):
        '''Reset every row to [id, client, "Availble", 0, 0, 0 ,0, 0]'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.clean(i)

    def disable_all(self):
        '''Disable all clients'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.data[i][2] = "Disabled"

    def enable_all(self):
        '''Enable all clients'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.data[i][2] = "Available"

    def get_available_clients(self):
        '''Return a list of all the available clients'''
        available_clients = []
        for i, row in enumerate(self.data):
            if i == 0: continue
            if row[2] == "Available": available_clients.append(row[1])
        return available_clients

    def get_row(self, id):
        '''Return a single row'''
        return self.data[id]

    def get_id(self, host):
        '''Return the ID based on host'''
        for row in self.data[1:]:
            if row[1] == host:
                return row[0]

    def get_client(self, id):
        '''Return the client name of a row based on id'''
        return self.data[id][1]

    def get_status(self, id):
        '''Return the status of a row based on id'''
        return self.data[id][2]

    def get_host(self, id):
        '''Return the host name of a row based on id'''
        return self.data[id][3]

    def get_ifd(self, id):
        '''Return the ifd path of a row based on id'''
        return self.data[id][4]

    def get_start_time(self, id):
        '''Return the start time of a row based on id'''
        return float(self.data[id][5])

    def get_progress(self, id):
        '''Return the progress of a row based on id'''
        return float(self.data[id][6])

    def get_pids(self, id):
        '''Return the pids related to the render of a row based on id'''
        if self.data[id][7] == "None":
            return None
        else:
            return map(int, self.data[id][7].split("-"))

    def disable(self, id):
        '''Set status of a single client to Disabled'''
        if id == 0: return
        self.data[id][2] = "Disabled"

    def enable(self, id):
        '''Set status of a single client to Enabled'''
        if id == 0: return
        self.data[id][2] = "Available"

    def busy(self, id):
        '''Set status of a single client to Rendering'''
        if id == 0: return
        self.data[id][2] = "Rendering"

    def set_host(self, id, host_name):
        '''Set host name of a single client'''
        if id == 0: return
        assert type(host_name) == type("str")
        self.data[id][3] = host_name

    def set_ifd(self, id, ifd_path):
        '''Set the ifd path of single client'''
        if id == 0: return
        assert type(ifd_path) == type("str")
        self.data[id][4] = ifd_path

    def set_start_time(self, id, new_time):
        '''Set the start time of single client'''
        if id == 0: return
        self.data[id][5] = new_time

    def set_progress(self, id, new_progress):
        '''Set the progress of single client'''
        if id == 0: return
        self.data[id][6] = new_progress

    def add_pid(self, id, pid):
        '''Add the PID of a process being used by a single client'''
        if id == 0: return
        try:
            pid = int(pid)
        except:
            return
        pids = self.get_pids(id)
        if pids == None:
            self.data[id][7] = str(pid)
        else:
            if pid not in pids:
                pids.append(pid)
                self.data[id][7] = "-".join(map(str, pids))

    def remove_pid(self, id, pid):
        '''Remove the PID of a process being used by a single client''' 
        if id == 0: return
        try:
            pid = int(pid)
        except:
            return
        pids = self.get_pids(id)
        if pids == None:
            return
        else:
            if pid not in pids:
                return
            else:
                pids.remove(pid)
                if len(pids) == 0:
                    self.data[id][7] = "None"
                else:
                    self.data[id][7] = "-".join(map(str, pids))

    def clean(self, id):
        '''Reset a single row'''
        if id == 0: return
        self.data[id][2] = "Available"
        self.data[id][3] = "None"
        self.data[id][4] = "None"
        self.data[id][5] = "None"
        self.data[id][6] = "None"
        self.data[id][7] = "None"


if __name__ == "__main__":
    settings = config.Settings()
    database_path = settings.render_database_file
    database_rows = []
    for client in settings.clients:
        database_rows.append((client, "Available", "None",
                              "None", "None", "None", "None"))
    
    # create_database(database_path, database_rows)
    enable_all(database_path)





    # try:
    #     client_id = int(sys.argv[1])
    #     status = sys.argv[2]
    #     host = sys.argv[3]
    #     file = sys.argv[4]
    #     time = sys.argv[5]
    #     progress = sys.argv[6]

    #     render_db = Database(database_path)
    #     if status != "None":
    #         if status == "Available":
    #             render_db.enable(client_id)
    #         elif status == "Rendering":
    #             render_db.busy(client_id)
    #         else:
    #             render_db.disable(client_id)

    #     if host != "None":
    #         render_db.set_host(client_id, host)
    #     if file != "None":
    #         render_db.set_ifd(client_id, file)
    #     if time != "None":
    #         render_db.set_start_time(client_id, time)
    #     if progress != "None":
    #         render_db.set_progress(client_id, progress)
    #     render_db.save_csv()

    # except:
    #     test_db = Database(database_path)
    #     #Uncomment for resetting database
    #     # test_db.reset_to_defaults()
    #     # test_db.save_csv()
    #     print database_path
    #     print test_db.data
    #     print test_db.header

    sys.exit()