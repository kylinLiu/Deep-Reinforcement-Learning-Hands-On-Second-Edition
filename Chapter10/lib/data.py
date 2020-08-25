import os
import csv
import glob
import numpy as np
import collections

Prices = collections.namedtuple(
    'Prices',
    field_names=[
        'open', 'high', 'low', 'close', 'volume',
        "chg", "percent", "turnoverrate", "amount",
    ])


def read_csv(file_name, sep=',', filter_data=True, fix_open_price=False):
    print("Reading", file_name)
    with open(file_name, 'rt', encoding='utf-8') as fd:
        reader = csv.reader(fd, delimiter=sep)
        h = next(reader)
        if '<OPEN>' not in h and sep == ',':
            return read_csv(file_name, ';', filter_data=filter_data)
        indices = [h.index(s) for s in (
            '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>',
            "chg", "percent", "turnoverrate", "amount",
        )]
        o, h, l, c, v, chg, percent, turnoverrate, amount = [], [], [], [], [], [], [], [], []
        count_out = 0
        count_filter = 0
        count_fixed = 0
        prev_vals = None
        for row in reader:
            vals = list(map(float, [row[idx] for idx in indices]))
            if filter_data and all(map(lambda v: abs(v - vals[0]) < 1e-8, vals[:-1])):
                count_filter += 1
                continue

            po, ph, pl, pc, pv, pch, pp, pt, pa = vals

            # fix open price for current bar to match close price for the previous bar
            if fix_open_price and prev_vals is not None:
                ppo, pph, ppl, ppc, ppv = prev_vals
                if abs(po - ppc) > 1e-8:
                    count_fixed += 1
                    po = ppc
                    pl = min(pl, po)
                    ph = max(ph, po)
            count_out += 1
            o.append(po)
            c.append(pc)
            h.append(ph)
            l.append(pl)
            v.append(pv)
            chg.append(pch)
            percent.append(pp)
            turnoverrate.append(pt)
            amount.append(pa)
            prev_vals = vals
    print("Read done, got %d rows, %d filtered, %d open prices adjusted" % (
        count_filter + count_out, count_filter, count_fixed))
    return Prices(open=np.array(o, dtype=np.float32),
                  high=np.array(h, dtype=np.float32),
                  low=np.array(l, dtype=np.float32),
                  close=np.array(c, dtype=np.float32),
                  volume=np.array(v, dtype=np.float32),
                  chg=np.array(chg, dtype=np.float32),
                  percent=np.array(percent, dtype=np.float32),
                  turnoverrate=np.array(turnoverrate, dtype=np.float32),
                  amount=np.array(amount, dtype=np.float32), )


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


def load_relative(csv_file,filter_data=True):
    return prices_to_relative(read_csv(csv_file, filter_data=filter_data))


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
