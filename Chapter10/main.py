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
import datetime
import pandas as pd

from dbmodel import DbModel


def init_db():
    db = DbModel('kzz_data')
    return db


# def get_kzz_miniute_old(symbol):
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Pragma': 'no-cache',
#         'Upgrade-Insecure-Requests': '1',
#         # "Cookie": "device_id=225ffbaa9a9242741146afd88c66fafc; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1NzUwMzg0MTY5LCJjaWQiOiJkOWQwbjRBWnVwIn0.D4oMci4NhePHMOuAY3f1tB2-yzhYjLJPDl7ukI3ypL-fsjbJs_dGLDl-1J7y7sptyCKHY58fU_s53-5DHFkZj8C6cPJeKuLLtDeT9xIPVUsQj6rnD-5iHitLzP1sKe3t0uk9IBIsyTHj0_94H0WXAfwycXg0_tQbMCY9hSObl1rZzNUV27Bt6CIEuIzgkkZiWedsWIDDq-3nPSzAa8-BwlICfYjJzmyLoYVbx7rwuncLPkt7L9MF_MoKUPFy7TLfSII_mPi4PR7oFwl2MWtV74LqoKT8ijvhEglreIW5pjMfcWgtguiljwjnVpiIE_hEy4Id_kcJvIM6hWq_hvPjFA; u=781595750415430; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595178962,1595750416; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595750426",
#         "Cookie": "device_id=225ffbaa9a9242741146afd88c66fafc; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1NzUwMzg0MTY5LCJjaWQiOiJkOWQwbjRBWnVwIn0.D4oMci4NhePHMOuAY3f1tB2-yzhYjLJPDl7ukI3ypL-fsjbJs_dGLDl-1J7y7sptyCKHY58fU_s53-5DHFkZj8C6cPJeKuLLtDeT9xIPVUsQj6rnD-5iHitLzP1sKe3t0uk9IBIsyTHj0_94H0WXAfwycXg0_tQbMCY9hSObl1rZzNUV27Bt6CIEuIzgkkZiWedsWIDDq-3nPSzAa8-BwlICfYjJzmyLoYVbx7rwuncLPkt7L9MF_MoKUPFy7TLfSII_mPi4PR7oFwl2MWtV74LqoKT8ijvhEglreIW5pjMfcWgtguiljwjnVpiIE_hEy4Id_kcJvIM6hWq_hvPjFA; u=781595750415430; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595178962,1595750416; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595750426; is_overseas=0",
#         'Origin': 'https://xueqiu.com',
#         'Referer': 'https://xueqiu.com/S/{}'.format(symbol),
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
#     }
#     all_datas = []
#     ts = int(time.time() * 1000)
#     for _ in range(100):
#         url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={}&period=1m&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance".format(
#             symbol, ts
#         )
#
#         r = requests.get(url, headers=headers)
#         datas = r.text
#         datas = json.loads(datas)
#         datas = datas.get("data", {}).get("item", [])
#         ts = datas[0][0]
#         print(_)
#         if _:
#             datas = datas[:-1]
#         if not datas or (datas[0][0] == datas[-1][0]):
#             break
#         print(datas[0][0])
#         print(datas[-1][0])
#         all_datas.extend(datas[::-1])
#         time.sleep(5)
#     # print(datas)
#     # raise Exception(22)\
#     datas = all_datas[::-1]
#     data_list = []
#     for index, row in enumerate(datas):
#         close_diff = 0
#         volumn_diff = 0
#         volumn_chng = 0
#         if index:
#             close_diff = row[5] - datas[index - 1][5]
#             volumn_diff = row[1] - datas[index - 1][1]
#             if datas[index - 1][1]:
#                 volumn_chng = (row[1] - datas[index - 1][1]) / datas[index - 1][1]
#         data_list.append(
#             {
#                 "volume": row[1],
#                 "close_diff": close_diff,
#                 "volumn_diff": volumn_diff,
#                 "volumn_chng": volumn_chng,
#                 "close": row[5],
#                 "chg": row[6],
#                 "date": datetime.datetime.fromtimestamp(row[0] / 1000).strftime("%H:%M"),
#             }
#         )
#
#     pre_ema_12 = None
#     pre_ema_26 = None
#     pre_dif = None
#     pre_dea = None
#     pre_macd = None
#     pre_macd_chng_pct = None
#
#     def calcute_rsi(data_list):
#         a = sum([i["close_diff"] for i in data_list if i["close_diff"] > 0])
#         b = abs(sum([i["close_diff"] for i in data_list if i["close_diff"] < 0]))
#         if not (a + b):
#             return 0
#         rsi = a / (a + b) * 100
#         return rsi
#
#     # data_list = data_list[-263:]
#     print(len(data_list))
#     for index, row in enumerate(data_list):
#         rsi6 = None
#         rsi12 = None
#         rsi24 = None
#         if index >= 5:
#             rsi6_list = data_list[(index + 1) - 6:index + 1]
#             rsi6 = calcute_rsi(rsi6_list)
#         if index >= 11:
#             rsi12_list = data_list[(index + 1) - 12:index + 1]
#             rsi12 = calcute_rsi(rsi12_list)
#         if index >= 23:
#             rsi24_list = data_list[(index + 1) - 24:index + 1]
#             rsi24 = calcute_rsi(rsi24_list)
#
#         tclose = row["close"]
#         if pre_ema_12 is None:
#             ema_12 = tclose
#         else:
#             ema_12 = pre_ema_12 * (11.0 / 13) + tclose * (2.0 / 13)
#         if pre_ema_26 is None:
#             ema_26 = row["close"]
#         else:
#             ema_26 = pre_ema_26 * (25.0 / 27) + tclose * (2.0 / 27)
#         dif = ema_12 - ema_26
#         if pre_dea is None:
#             dea = 0
#         else:
#             dea = pre_dea * (8.0 / 10) + (2.0 / 10) * dif
#         macd = 2 * (dif - dea)
#         dif_cross_dea_above = False
#         dif_cross_dea_below = False
#         if pre_dif is not None and pre_dea is not None \
#                 and dif is not None and dea is not None:
#             if pre_dif < pre_dea and dif > dea:
#                 dif_cross_dea_above = True
#             if pre_dif > pre_dea and dif < dea:
#                 dif_cross_dea_below = True
#         macd_chng_pct = 0
#         if pre_macd:
#             macd_chng_pct = 1.0 * (macd - pre_macd) / abs(pre_macd)
#         dea_chng_pct = 0
#         if pre_dea:
#             dea_chng_pct = (dea - pre_dea) / abs(pre_dea)
#         dif_chng_pct = 0
#         if pre_dif:
#             dif_chng_pct = (dif - pre_dif) / abs(pre_dif)
#
#         row.update({
#             "dif": dif,
#             "pre_dif": pre_dif,
#             "dea": dea,
#             "pre_dea": pre_dea,
#             "ema_12": ema_12,
#             "ema_26": ema_26,
#             "macd": macd,
#             "pre_macd": pre_macd,
#             "dif_cross_dea_above": dif_cross_dea_above,
#             "dif_cross_dea_below": dif_cross_dea_below,
#             "pre_macd_chng_pct": pre_macd_chng_pct,
#             "macd_chng_pct": macd_chng_pct,
#             "dea_chng_pct": dea_chng_pct,
#             "dif_chng_pct": dif_chng_pct,
#             "rsi6": rsi6,
#             "rsi12": rsi12,
#             "rsi24": rsi24,
#         })
#         pre_ema_12 = ema_12
#         pre_ema_26 = ema_26
#         pre_dif = dif
#         pre_dea = dea
#         pre_macd = macd
#         pre_macd_chng_pct = macd_chng_pct
#     # print(len(buy_list))
#     # raise Exception(22)
#     buy_list = {'x': [], 'y': []}
#     data_list = data_list[24:]
#     # print(data_list[0])
#     for index, row in enumerate(data_list):
#         pre_macd_chng_pct = row["pre_macd_chng_pct"]
#         macd_chng_pct = row["macd_chng_pct"]
#         macd = row["macd"]
#         dea = row["dea"]
#         dif = row["dif"]
#         dea_chng_pct = row["dea_chng_pct"]
#         dif_chng_pct = row["dif_chng_pct"]
#         rsi6 = row["rsi6"]
#         rsi12 = row["rsi12"]
#         rsi24 = row["rsi24"]
#         chg = row["chg"]
#         volumn_chng = row["volumn_chng"]
#         # print(row["date"], pre_macd_chng_pct, macd_chng_pct)
#         if (pre_macd_chng_pct < 0 and macd_chng_pct > 0 and macd < 0
#             and dea < 0 and dif < 0
#             and dea_chng_pct < 0
#             and rsi6 < 50 and rsi12 < 50 and rsi24 < 50
#             and dea > dif
#             and chg > 0
#             and dea - dif > 0.1
#             and volumn_chng > 0.1
#             and rsi24 > rsi12 and rsi24 > rsi6
#             ):
#             # and rsi6 < rsi12 and rsi12 < rsi24:
#             #  and dif_chng_pct < 0:
#             # and dif_chng_pct > dea_chng_pct:
#             # and dif_chng_pct > 0 and dea_chng_pct < 0:
#             # and macd < -0.1:
#             buy_list["y"].append(row["close"])
#             buy_list["x"].append(index)
#     df = pd.DataFrame(data_list)
#     print(df.columns)
#     print(df)
#     df.to_csv(r"drive/My Drive/l_gym/local_data/{}.csv".format(symbol))
#     return df
def get_kzz_miniute(symbol, db):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        # "Cookie": "device_id=225ffbaa9a9242741146afd88c66fafc; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1NzUwMzg0MTY5LCJjaWQiOiJkOWQwbjRBWnVwIn0.D4oMci4NhePHMOuAY3f1tB2-yzhYjLJPDl7ukI3ypL-fsjbJs_dGLDl-1J7y7sptyCKHY58fU_s53-5DHFkZj8C6cPJeKuLLtDeT9xIPVUsQj6rnD-5iHitLzP1sKe3t0uk9IBIsyTHj0_94H0WXAfwycXg0_tQbMCY9hSObl1rZzNUV27Bt6CIEuIzgkkZiWedsWIDDq-3nPSzAa8-BwlICfYjJzmyLoYVbx7rwuncLPkt7L9MF_MoKUPFy7TLfSII_mPi4PR7oFwl2MWtV74LqoKT8ijvhEglreIW5pjMfcWgtguiljwjnVpiIE_hEy4Id_kcJvIM6hWq_hvPjFA; u=781595750415430; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595178962,1595750416; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595750426",
        # "Cookie": "device_id=225ffbaa9a9242741146afd88c66fafc; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1NzUwMzg0MTY5LCJjaWQiOiJkOWQwbjRBWnVwIn0.D4oMci4NhePHMOuAY3f1tB2-yzhYjLJPDl7ukI3ypL-fsjbJs_dGLDl-1J7y7sptyCKHY58fU_s53-5DHFkZj8C6cPJeKuLLtDeT9xIPVUsQj6rnD-5iHitLzP1sKe3t0uk9IBIsyTHj0_94H0WXAfwycXg0_tQbMCY9hSObl1rZzNUV27Bt6CIEuIzgkkZiWedsWIDDq-3nPSzAa8-BwlICfYjJzmyLoYVbx7rwuncLPkt7L9MF_MoKUPFy7TLfSII_mPi4PR7oFwl2MWtV74LqoKT8ijvhEglreIW5pjMfcWgtguiljwjnVpiIE_hEy4Id_kcJvIM6hWq_hvPjFA; u=781595750415430; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595178962,1595750416; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595750426; is_overseas=0",
        "Cookie": "device_id=225ffbaa9a9242741146afd88c66fafc; xq_a_token=4db837b914fc72624d814986f5b37e2a3d9e9944; xqat=4db837b914fc72624d814986f5b37e2a3d9e9944; xq_r_token=2d6d6cc8e57501dfe571d2881cabc6a5f2542bf8; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYwMDQ4MzAwNywiY3RtIjoxNTk3OTI4NzcwMDA3LCJjaWQiOiJkOWQwbjRBWnVwIn0.K94C6RifmCuvCguScRhUCR22NTY-e9-6Jky8LWKaqLGDGFFFyAPoJupGY0kEHMYKAhMxDRoiW0XSLWO9gBfpj1ryM2mXUo_-wFIyNKR8FM4dagY4VU_tBowOQ5xiV_4sKT-LGbRDJiNaadrmyZpECD2cRb9FeaaBGo414G9MgwVyNO4g7aTDYo5Titd9OSkLqnfAQQMc2bZ4Ht_7o267ZHiybPR3Fu7bqPS8G-8llaDB5g0iLL2l9rRPl5qgaMVfedLNgBx7lsNqXvPKTLwLO2LDl3ENT9sMpn8SjdMr-SMZrFe8jVFg0SznDXls7IH4W2BSsQxwqitUee7RL9-egQ; u=121597928805224; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595750416,1597337136,1597928805; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1597928821",
        'Origin': 'https://xueqiu.com',
        'Referer': 'https://xueqiu.com/S/{}'.format(symbol),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
    }
    all_datas = []
    ts = int(time.time() * 1000)
    for _ in range(100):
        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={}&period=1m&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance".format(
            symbol, ts
        )

        r = requests.get(url, headers=headers)
        datas = r.text
        datas = json.loads(datas)
        datas = datas.get("data", {}).get("item", [])
        ts = datas[0][0]
        print(_)
        if _:
            datas = datas[:-1]
        if not datas or (datas[0][0] == datas[-1][0]):
            break
        print(datas[0][0])
        print(datas[-1][0])
        all_datas.extend(datas[::-1])
        time.sleep(5)
    # print(datas)
    # raise Exception(22)\
    datas = all_datas[::-1]
    data_list = []
    for index, row in enumerate(datas):
        data_list.append({
            "symbol": symbol,
            "ts": row[0],
            "data": json.dumps(row),
            "d_type": "1m",
        })

    sql = """
            insert or replace into kzz_data(symbol,ts,data,d_type) values(?,?,?,?)
    """
    db.executemany(sql, ((
        row["symbol"],
        row["ts"],
        row["data"],
        row["d_type"],
    ) for row in data_list))


stock_list = [
    'SH113586', 'SH113581', 'SH113585',
    'SZ123046', 'SZ128108', 'SH113565', 'SH113572', 'SH113575',
    'SZ123056', 'SH113554', 'SZ128045', 'SZ123051', 'SZ128097', 'SH113571', 'SZ123044', 'SH113022',
    'SH113031', 'SZ128089', 'SZ128021', 'SH113514', 'SH113552', 'SZ128086', 'SH110060', 'SZ127015',
    'SZ128088', 'SZ123040', 'SH113518', 'SH110042', 'SZ123030', 'SZ123026', 'SH113536', 'SZ127003',
    'SZ128092', 'SZ123041', 'SZ128059', 'SZ128115', 'SZ128084', 'SH113558', 'SH113027', 'SH113509',
    'SH113029', 'SZ123020', 'SH113541', 'SH113577', 'SZ123034', 'SZ128022', 'SH113548', 'SH113580',
    'SZ128079', 'SZ128043', 'SH113035', 'SH113521', 'SZ123029', 'SZ128106', 'SH113555', 'SZ123018',
    'SH113028', 'SH113520', 'SZ123027', 'SZ128029', 'SZ123002', 'SZ128098', 'SZ123032', 'SZ128105',
    'SZ123022', 'SZ128074', 'SH110066', 'SH113561', 'SH113543', 'SH113526', 'SH113019', 'SZ128075',
    'SH132021', 'SZ128066', 'SH113547', 'SH113566', 'SH113008', 'SZ128013', 'SH113545', 'SZ128030',
    'SZ128036', 'SH113542', 'SZ123038', 'SZ128096', 'SH113582', 'SH113553', 'SZ128039', 'SZ128102',
    'SZ128019', 'SH113578', 'SZ123031', 'SH110058', 'SH110057', 'SZ128078', 'SH113550', 'SZ128053',
    'SH113034', 'SZ123045', 'SZ123037', 'SZ123052', 'SH113564', 'SZ128051', 'SH110048', 'SZ123047',
    'SZ128099', 'SZ128112', 'SZ128090', 'SZ128082', 'SZ128104', 'SH110071', 'SH113590', 'SH113504',
    'SZ128071', 'SZ128050', 'SZ128028', 'SZ128103', 'SZ123050', 'SH113570', 'SZ128117', 'SZ128114',
    'SH113556',
    'SZ128069', 'SZ128017', 'SZ128116', 'SZ128025', 'SZ128052', 'SZ128107', 'SH113562',
    'SH132018', 'SH113020', 'SZ128085', 'SZ128094', 'SZ123048', 'SZ128057', 'SH113534', 'SZ123054',
    'SZ128049', 'SZ123049', 'SZ128067', 'SZ128091', 'SH113544', 'SZ127005', 'SZ128111', 'SH110051',
    'SZ123025', 'SZ128046', 'SH110055', 'SZ123043', 'SH113567', 'SH113036', 'SH113576', 'SZ128110',
    'SZ128048', 'SZ123017', 'SZ123055', 'SZ128056', 'SH113525', 'SH110069', 'SH113030', 'SZ123010',
    'SH113568', 'SH113588', 'SH110056', 'SZ128095', 'SZ128040', 'SZ128058', 'SZ120003', 'SH110038',
    'SZ123014', 'SH113546', 'SZ127013', 'SZ123012', 'SH113549', 'SH113557', 'SZ128034', 'SZ128118',
    'SH113591', 'SZ128109', 'SZ128065', 'SH113537', 'SH113583', 'SZ127007', 'SH113579', 'SZ128064',
    'SH110043', 'SZ128073', 'SH110062', 'SH113032', 'SH113563', 'SH113584', 'SZ123028', 'SH110065',
    'SZ127017', 'SZ123053', 'SZ123039', 'SZ123057', 'SH110033', 'SZ128081', 'SZ128087', 'SH113587',
    'SZ120004', 'SH110067', 'SH113025', 'SH110061', 'SH113011', 'SH110034', 'SH110063', 'SZ128113',
    'SH110041', 'SH113033', 'SZ123042', 'SZ127014', 'SZ128042', 'SZ128076', 'SZ127016', 'SH110052',
    'SH113592', 'SH113527', 'SH110047', 'SH113559', 'SZ128093', 'SZ128026', 'SZ123033', 'SZ128063',
    'SH110064', 'SH113528', 'SH110070', 'SH113014', 'SZ127011', 'SH113505', 'SH113519', 'SH113532',
    'SZ128083', 'SH132005', 'SH113524', 'SZ128070', 'SH113516', 'SZ123036', 'SH113013', 'SH110068',
    'SH132022', 'SZ127006', 'SH113589', 'SH113573', 'SZ123035', 'SZ128041', 'SZ123011', 'SH110053',
    'SZ127008', 'SH113574', 'SZ128012', 'SZ123024', 'SZ127012', 'SH132014', 'SZ123007', 'SH110031',
    'SH113017', 'SH110044', 'SZ123023', 'SZ128018', 'SZ128015', 'SZ123004', 'SZ128072', 'SZ128033',
    'SH113012', 'SZ128044', 'SH113026', 'SH110059', 'SH113021', 'SZ128101', 'SZ127018', 'SZ128035',
    'SH113024', 'SH113530', 'SH132008', 'SH113009', 'SZ127004', 'SH113535', 'SH113508', 'SZ123015',
    'SZ128014', 'SH113502', 'SH113569', 'SH132004', 'SH113016', 'SZ128032',
    'SH132013', 'SZ128100',
    'SH132009', 'SH110045', 'SZ128023', 'SH132015', 'SH132011', 'SZ128010', 'SH132007', 'SZ123013',
    'SZ128037', 'SZ128062']

db = init_db()
for symbol in stock_list:
    print(symbol)
    get_kzz_miniute(symbol, db)
    time.sleep(10)

