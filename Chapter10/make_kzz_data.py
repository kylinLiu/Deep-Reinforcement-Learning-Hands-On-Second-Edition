# coding: utf-8
"""
# @Time    : 2020/8/6 9:45
# @Author  : Kylin
# @File    : main.py.py
# @Software: PyCharm
# @Descript:
"""
import time
import requests
import json
import datetime, time
import pandas as pd

from dbmodel import DbModel
import csv


def init_db():
    db = DbModel('kzz_data')
    return db


def get_kzz_miniute(symbol, db):
    sql = """
    select * from kzz_data
    where symbol=?
    ORDER  by ts
    """
    datas = db.fetchall(sql, (symbol,))
    print(len(datas))
    csv_header = ["<DATE>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<VOL>",
                  "chg", "percent", "turnoverrate", "amount", ]
    data_list = []
    for row in datas:
        ts = row["ts"]
        timeArray = time.localtime(ts / 1000)

        DATE = int(time.strftime("%Y%m%d", timeArray))
        TIME = int(time.strftime("%H%M%S", timeArray))
        data = json.loads(row["data"])
        volumn = data[1]
        open_c = data[2]
        high = data[3]
        low = data[4]
        close = data[5]
        chg = data[6]
        percent = data[7]
        turnoverrate = data[8]
        amount = data[9]
        volume_post = data[10]
        amount_post = data[11]
        pe = data[12]
        pb = data[13]
        ps = data[14]
        pcf = data[15]
        market_capital = data[16]
        balance = data[17]
        hold_volume_cn = data[18]
        hold_ratio_cn = data[19]
        net_volume_cn = data[20]
        hold_volume_hk = data[21]
        hold_ratio_hk = data[22]
        net_volume_hk = data[23]
        data_list.append(
            [DATE, TIME, open_c, high, low, close, volumn,
             chg, percent, turnoverrate, amount
             ]
        )
    csv_file = "data_val/kzz_{}.csv".format(symbol)
    # csv_file = "data/kzz_{}.csv".format(symbol)
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        for row in data_list:
            writer.writerow(row)


stock_list = [
    # 'SH113586', 'SH113581', 'SH113585',
    # 'SZ123046', 'SZ128108', 'SH113565', 'SH113572', 'SH113575',
    # 'SZ123056', 'SH113554', 'SZ128045', 'SZ123051', 'SZ128097', 'SH113571', 'SZ123044', 'SH113022',
    # 'SH113031', 'SZ128089', 'SZ128021', 'SH113514', 'SH113552', 'SZ128086', 'SH110060', 'SZ127015',
    # 'SZ128088', 'SZ123040', 'SH113518', 'SH110042', 'SZ123030', 'SZ123026', 'SH113536', 'SZ127003',
    # 'SZ128092', 'SZ123041', 'SZ128059', 'SZ128115', 'SZ128084', 'SH113558', 'SH113027', 'SH113509',
    # 'SH113029', 'SZ123020', 'SH113541', 'SH113577', 'SZ123034', 'SZ128022', 'SH113548', 'SH113580',
    # 'SZ128079', 'SZ128043', 'SH113035', 'SH113521', 'SZ123029', 'SZ128106', 'SH113555', 'SZ123018',
    # 'SH113028', 'SH113520', 'SZ123027', 'SZ128029', 'SZ123002', 'SZ128098', 'SZ123032', 'SZ128105',
    # 'SZ123022', 'SZ128074', 'SH110066', 'SH113561', 'SH113543', 'SH113526', 'SH113019', 'SZ128075',
    # 'SH132021', 'SZ128066', 'SH113547', 'SH113566', 'SH113008', 'SZ128013', 'SH113545', 'SZ128030',
    # 'SZ128036', 'SH113542', 'SZ123038', 'SZ128096', 'SH113582', 'SH113553', 'SZ128039', 'SZ128102',
    # 'SZ128019', 'SH113578', 'SZ123031', 'SH110058', 'SH110057', 'SZ128078', 'SH113550', 'SZ128053',
    # 'SH113034', 'SZ123045', 'SZ123037', 'SZ123052', 'SH113564', 'SZ128051', 'SH110048', 'SZ123047',
    # 'SZ128099', 'SZ128112', 'SZ128090', 'SZ128082', 'SZ128104', 'SH110071', 'SH113590', 'SH113504',
    # 'SZ128071', 'SZ128050', 'SZ128028', 'SZ128103', 'SZ123050', 'SH113570', 'SZ128117', 'SZ128114',
    # 'SH113556',
    # 'SZ128069', 'SZ128017', 'SZ128116', 'SZ128025', 'SZ128052', 'SZ128107', 'SH113562',
    # 'SH132018', 'SH113020', 'SZ128085', 'SZ128094', 'SZ123048', 'SZ128057', 'SH113534', 'SZ123054',
    # 'SZ128049', 'SZ123049', 'SZ128067', 'SZ128091', 'SH113544', 'SZ127005', 'SZ128111', 'SH110051',
    # 'SZ123025', 'SZ128046', 'SH110055', 'SZ123043', 'SH113567', 'SH113036', 'SH113576', 'SZ128110',
    # 'SZ128048', 'SZ123017', 'SZ123055', 'SZ128056', 'SH113525', 'SH110069', 'SH113030', 'SZ123010',
    # 'SH113568', 'SH113588', 'SH110056', 'SZ128095', 'SZ128040', 'SZ128058', 'SZ120003', 'SH110038',
    # 'SZ123014', 'SH113546', 'SZ127013', 'SZ123012', 'SH113549', 'SH113557', 'SZ128034', 'SZ128118',
    # 'SH113591', 'SZ128109', 'SZ128065', 'SH113537', 'SH113583', 'SZ127007', 'SH113579', 'SZ128064',
    # 'SH110043', 'SZ128073', 'SH110062', 'SH113032', 'SH113563', 'SH113584', 'SZ123028', 'SH110065',
    # 'SZ127017', 'SZ123053', 'SZ123039', 'SZ123057', 'SH110033', 'SZ128081', 'SZ128087', 'SH113587',
    # 'SZ120004', 'SH110067', 'SH113025', 'SH110061', 'SH113011', 'SH110034', 'SH110063', 'SZ128113',
    # 'SH110041', 'SH113033', 'SZ123042', 'SZ127014', 'SZ128042', 'SZ128076', 'SZ127016', 'SH110052',
    # 'SH113592', 'SH113527', 'SH110047', 'SH113559', 'SZ128093', 'SZ128026', 'SZ123033', 'SZ128063',
    # 'SH110064', 'SH113528', 'SH110070', 'SH113014', 'SZ127011', 'SH113505', 'SH113519', 'SH113532',
    # 'SZ128083', 'SH132005', 'SH113524', 'SZ128070', 'SH113516', 'SZ123036', 'SH113013', 'SH110068',
    # 'SH132022', 'SZ127006', 'SH113589', 'SH113573', 'SZ123035', 'SZ128041', 'SZ123011', 'SH110053',
    # 'SZ127008', 'SH113574', 'SZ128012', 'SZ123024', 'SZ127012', 'SH132014', 'SZ123007', 'SH110031',
    # 'SH113017', 'SH110044',
    'SZ123023', 'SZ128018', 'SZ128015', 'SZ123004', 'SZ128072', 'SZ128033',
    'SH113012', 'SZ128044', 'SH113026', 'SH110059', 'SH113021', 'SZ128101', 'SZ127018', 'SZ128035',
    'SH113024', 'SH113530', 'SH132008', 'SH113009', 'SZ127004', 'SH113535', 'SH113508', 'SZ123015',
    'SZ128014', 'SH113502', 'SH113569', 'SH132004', 'SH113016', 'SZ128032',
    'SH132013', 'SZ128100',
    'SH132009', 'SH110045', 'SZ128023', 'SH132015', 'SH132011', 'SZ128010', 'SH132007', 'SZ123013',
    'SZ128037', 'SZ128062']
stock_list = [
                 "SH113586",
                 "SH113581",
                 "SH113575",
                 "SZ128097",
                 "SZ128108",
                 "SH113585",
                 "SH113571",
                 "SH113565",
                 "SZ123046",
                 "SH113035",
                 # "SZ123056",
                 # "SH113587",
                 # "SZ128115",
                 # "SZ123044",
                 # "SZ128112",
                 # "SZ128102",
                 # "SH113572",
                 # "SH113577",
                 # "SH113022",
                 # "SH113550",
                 # "SH110060",
                 # "SZ128084",
                 # "SH110058",
                 # "SZ123041",
                 # "SZ128045",
                 # "SZ128092",
                 # "SH113019",
                 # "SH113543",
                 # "SZ128029",
                 # "SH110042",
                 # "SH113518",
                 # "SH113514",
                 # "SH113544",
                 # "SH113547",
                 # "SH113592",
                 # "SH113554",
                 # "SZ123027",
                 # "SZ128086",
                 # "SH113504",
                 # "SH113509",
                 # "SH113028",
                 # "SH113031",
                 # "SH113561",
                 # "SH113555",
                 # "SH113553",
                 # "SH113520",
                 # "SZ128017",
                 # "SZ127015",
                 # "SZ128075",
                 # "SH132021",
                 # "SZ123002",
                 # "SZ123022",
                 # "SZ123062",
                 # "SH113595",
                 # "SZ123029",
                 # "SZ128057",
                 # "SH113541",
                 # "SZ123038",
                 # "SH110066",
                 # "SZ127003",
                 # "SH113027",
                 # "SZ123051",
                 # "SZ128021",
                 # "SZ128125",
                 # "SZ123026",
                 # "SZ123020",
                 # "SZ128106",
                 # "SZ128104",
                 # "SH113566",
                 # "SH113580",
                 # "SZ128090",
                 # "SZ128050",
                 # "SH113582",
                 # "SZ128078",
                 # "SH113537",
                 # "SH113548",
                 # "SH113029",
                 # "SZ123030",
                 # "SH113020",
                 # "SH113564",
                 # "SZ123017",
                 # "SH113008",
                 # "SH113521",
                 # "SH113536",
                 # "SZ128099",
                 # "SH110071",
                 # "SZ128066",
                 # "SZ128079",
                 # "SZ128067",
                 # "SH113578",
                 # "SZ123063",
                 # "SZ128074",
                 # "SZ128105",
                 # "SH113033",
                 # "SZ128058",
                 # "SZ128049",
                 # "SZ128096",
                 # "SH132018",
                 # "SZ127019",
                 # "SZ128013",
             ][:10]

db = init_db()
for symbol in stock_list:
    print(symbol)
    get_kzz_miniute(symbol, db)
    time.sleep(10)
    # break
