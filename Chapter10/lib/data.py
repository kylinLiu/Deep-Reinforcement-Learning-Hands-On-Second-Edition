import os
import csv
import glob
import numpy as np
import collections

# csv_header = [
#     # 'DATE', 'TIME',
#     'amount', 'chg', 'close', 'close_diff', 'dea', 'dea_chng_pct', 'dif', 'dif_chng_pct',
#     # 'dif_cross_dea_above', 'dif_cross_dea_below',
#     'ema_12', 'ema_26', 'high', 'low', 'macd', 'macd_chng_pct',
#     'open', 'percent', 'pre_dea', 'pre_dif', 'pre_macd', 'pre_macd_chng_pct', 'rsi12', 'rsi24', 'rsi6',
#     # 'turnoverrate',
#     'volume', 'volume_chng', 'volume_diff']
csv_header = ['amount', 'chg', 'close', 'close_diff', 'high', 'low', 'open', 'percent', 'volume', 'volume_chng',
              'volume_diff']

Prices = collections.namedtuple(
    'Prices',
    field_names=csv_header + ["real_close"])


def read_csv(file_name, sep=',', filter_data=True, fix_open_price=False, relative=False):
    print("Reading", file_name)
    with open(file_name, 'rt', encoding='utf-8') as fd:
        reader = csv.reader(fd, delimiter=sep)
        h = next(reader)
        # if '<OPEN>' not in h and sep == ',':
        #     return read_csv(file_name, ';', filter_data=filter_data)
        indices = [h.index(s) for s in csv_header]
        data_tmp = {i: [] for i in csv_header}
        data_tmp.update({"real_close": []})
        # o, h, l, c, v, chg, percent, turnoverrate, amount = [], [], [], [], [], [], [], [], []
        count_out = 0
        count_filter = 0
        count_fixed = 0
        prev_vals = None
        for row in reader:
            # vals = list(map(float, [row[idx] for idx in indices]))
            vals = []
            for idx in indices:
                try:
                    vals.append(float(row[idx]))
                except:
                    if row[idx] == 'False':
                        row[idx] = 0.0
                    elif row[idx] == 'True':
                        row[idx] = 1.0
                    else:
                        row[idx] = None

                    vals.append(row[idx])
            # vals = list(row)
            # if filter_data and all(map(lambda v: abs(v - vals[0]) < 1e-8, vals[:-1])):
            #     count_filter += 1
            #     continue
            count_filter += 1
            po = vals[csv_header.index('open')]
            ph = vals[csv_header.index('high')]
            pl = vals[csv_header.index('low')]
            pc = vals[csv_header.index('close')]
            data_tmp['real_close'].append(pc)

            # fix open price for current bar to match close price for the previous bar
            if fix_open_price and prev_vals is not None:
                # ppo = prev_vals[indices.index('open')]
                # pph = prev_vals[indices.index('high')]
                # ppl = prev_vals[indices.index('low')]
                ppc = prev_vals[csv_header.index('close')]
                if abs(po - ppc) > 1e-8:
                    count_fixed += 1
                    po = ppc
                    pl = min(pl, po)
                    ph = max(ph, po)
            if relative:
                ph = (ph - po) / po
                pl = (pl - po) / po
                pc = (pc - po) / po
            count_out += 1
            for idx, k in enumerate(csv_header):
                data_tmp[k].append(vals[idx])
            data_tmp['open'][-1] = po
            data_tmp['high'][-1] = ph
            data_tmp['low'][-1] = pl
            data_tmp['close'][-1] = pc
            prev_vals = vals
    print("Read done, got %d rows, %d filtered, %d open prices adjusted" % (
        count_filter + count_out, count_filter, count_fixed))
    kargs = {i: np.array(data_tmp[i], dtype=np.float32) for i in csv_header}
    kargs.update({"real_close": np.array(data_tmp["real_close"], dtype = np.float32)})
    return Prices(**kargs)


def prices_to_relative(prices):
    """
    Convert prices to relative in respect to open price
    :param ochl: tuple with open, close, high, low
    :return: tuple with open, rel_close, rel_high, rel_low
    """
    assert isinstance(prices, Prices)
    rh = (prices.high - prices.open) / prices.open
    rl = (prices.low - prices.open) / prices.open
    rc = (prices.close - prices.open) / prices.open
    return Prices(open=prices.open, high=rh, low=rl, close=rc, volume=prices.volume,
                  chg=prices.chg, percent=prices.percent,
                  turnoverrate=prices.turnoverrate, amount=prices.amount
                  )


def load_relative(csv_file, filter_data=True):
    # return prices_to_relative(read_csv(csv_file, filter_data=filter_data))
    return read_csv(csv_file, filter_data=filter_data, relative=True)


def price_files(dir_name):
    result = []
    for path in glob.glob(os.path.join(dir_name, "*.csv")):
        result.append(path)
    return result


def load_year_data(year, basedir='data'):
    y = str(year)[-2:]
    result = {}
    for path in glob.glob(os.path.join(basedir, "*_%s*.csv" % y)):
        result[path] = load_relative(path)
    return result
