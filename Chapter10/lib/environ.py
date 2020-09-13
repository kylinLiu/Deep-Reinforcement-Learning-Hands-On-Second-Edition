import gym
import gym.spaces
from gym.utils import seeding
from gym.envs.registration import EnvSpec
import enum
import numpy as np

from . import data

DEFAULT_BARS_COUNT = 10
DEFAULT_COMMISSION_PERC = 0.1

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


class Actions(enum.Enum):
    Skip = 0
    Buy = 1
    Close = 2


class State:
    def __init__(self, bars_count, commission_perc,
                 reset_on_close, reward_on_close=True,
                 volumes=True):
        assert isinstance(bars_count, int)
        assert bars_count > 0
        assert isinstance(commission_perc, float)
        assert commission_perc >= 0.0
        assert isinstance(reset_on_close, bool)
        assert isinstance(reward_on_close, bool)
        self.bars_count = bars_count
        self.commission_perc = commission_perc
        self.reset_on_close = reset_on_close
        self.reward_on_close = reward_on_close
        self.volumes = volumes

    def reset(self, prices, offset):
        assert isinstance(prices, data.Prices)
        assert offset >= self.bars_count - 1
        self.have_position = False
        self.open_price = 0.0
        self._prices = prices
        self._offset = offset

    @property
    def shape(self):
        # [h, l, c] * bars + position_flag + rel_profit

        return len(csv_header) * self.bars_count + 1 + 1,

    def encode(self):
        """
        Convert current state into numpy array.
        """
        res = np.ndarray(shape=self.shape, dtype=np.float32)
        shift = 0
        for bar_idx in range(-self.bars_count + 1, 1):
            ofs = self._offset + bar_idx
            for k in csv_header:
                res[shift] = getattr(self._prices, k)[ofs]
                shift += 1
        res[shift] = float(self.have_position)
        shift += 1
        if not self.have_position:
            res[shift] = 0.0
        else:
            res[shift] = self._cur_close() / self.open_price - 1.0
        return res

    def _cur_close(self):
        """
        Calculate real close price for the current bar
        """
        open = self._prices.open[self._offset]
        rel_close = self._prices.close[self._offset]
        return open * (1.0 + rel_close)

    def step_OLD(self, action):
        """
        Perform one step in our price, adjust offset, check for the end of prices
        and handle position change
        :param action:
        :return: reward, done
        """
        assert isinstance(action, Actions)
        reward = 0.0
        done = False
        close = self._cur_close()
        if action == Actions.Buy and not self.have_position:
            self.have_position = True
            self.open_price = close
            reward -= self.commission_perc
        elif action == Actions.Close and self.have_position:
            reward -= self.commission_perc
            done |= self.reset_on_close
            if self.reward_on_close:
                reward += 100.0 * (close / self.open_price - 1.0)
            self.have_position = False
            self.open_price = 0.0

        self._offset += 1
        prev_close = close
        close = self._cur_close()
        done |= self._offset >= self._prices.close.shape[0] - 1

        if self.have_position and not self.reward_on_close:
            reward += 100.0 * (close / prev_close - 1.0)

        return reward, done

    def step2(self, action):
        """
        Perform one step in our price, adjust offset, check for the end of prices
        and handle position change
        :param action:
        :return: reward, done
        """
        assert isinstance(action, Actions)
        reward = 0.0
        done = False
        real_closes = self._prices.real_close.tolist()
        len_all = len(real_closes)
        after_offset = self._offset + 60
        after_offset = len_all if after_offset > len_all else after_offset
        pre_offset = 0 if after_offset < 120 else after_offset - 120
        after_offset = pre_offset + 120

        close = real_closes[self._offset]
        pre_closes = real_closes[pre_offset:self._offset + 1]
        max_pre_close = max(pre_closes)
        max_pre_index = pre_closes.index(max_pre_close)
        print("max_pre_index", max_pre_index)
        print("len(pre_closes)", len(pre_closes))
        min_pre_close = close
        if pre_closes[max_pre_index:]:
            min_pre_close = min(pre_closes[max_pre_index:])
        pre_reward = ((max_pre_close - close) / close) - ((close - min_pre_close) / min_pre_close)

        after_closes = real_closes[self._offset:after_offset + 1]

        max_after_close = max(after_closes)

        max_after_index = after_closes.index(max_after_close)
        print("max_after_index", max_after_index)
        print("len(after_closes)", len(after_closes))
        min_after_close = close
        if after_closes[max_after_index:]:
            min_after_close = min(pre_closes[min_after_close:])
        # min_after_close = min(after_closes[:max_after_index])

        after_reward = ((max_after_close - close) / close) - ((close - min_after_close) / min_after_close)
        org_reward = after_reward - pre_reward

        # after_closes = self._prices.real_close[self._offset:]
        #
        # after_max_close = max(pre_closes)
        # after_min_close = min(pre_closes)
        #
        # close = self._cur_close()
        if action == Actions.Buy:
            reward = org_reward
        elif action == Actions.Close:
            reward = -1 * org_reward
        elif action == Actions.Skip and self.have_position:
            reward = org_reward
        elif action == Actions.Skip and not self.have_position:
            reward = -1 * org_reward

        if action == Actions.Buy and not self.have_position:
            self.have_position = True
            self.open_price = close
        elif action == Actions.Close and self.have_position:
            done |= self.reset_on_close
            self.have_position = False

        self._offset += 1
        done |= self._offset >= self._prices.close.shape[0] - 1

        return reward, done

    def step(self, action):
        """
        Perform one step in our price, adjust offset, check for the end of prices
        and handle position change
        :param action:
        :return: reward, done
        """
        assert isinstance(action, Actions)
        reward = 0.0
        done = False
        real_closes = self._prices.real_close.tolist()
        len_all = len(real_closes)
        after_offset = self._offset + 60
        after_offset = len_all if after_offset > len_all else after_offset
        pre_offset = 0 if after_offset < 120 else after_offset - 120
        after_offset = pre_offset + 120

        close = real_closes[self._offset]
        pre_closes = real_closes[pre_offset:self._offset + 1]
        max_pre_close = max(pre_closes)
        min_pre_close = min(pre_closes)
        pre_reward = ((max_pre_close - close) / close) - ((close - min_pre_close) / min_pre_close)

        after_closes = real_closes[self._offset:after_offset + 1]

        max_after_close = max(after_closes)
        min_after_close = min(after_closes)

        after_reward = ((max_after_close - close) / close) - ((close - min_after_close) / min_after_close)
        print(after_reward, pre_reward)
        org_reward = after_reward + pre_reward

        if action == Actions.Buy:
            reward = org_reward
        elif action == Actions.Close:
            reward = -1 * org_reward
        elif action == Actions.Skip and self.have_position:
            reward = org_reward
        elif action == Actions.Skip and not self.have_position:
            reward = -1 * org_reward

        if action == Actions.Buy and not self.have_position:
            self.have_position = True
            self.open_price = close
        elif action == Actions.Close and self.have_position:
            done |= self.reset_on_close
            self.have_position = False

        self._offset += 1
        done |= self._offset >= self._prices.close.shape[0] - 1

        return reward, done

    def step3(self, action):
        """
        Perform one step in our price, adjust offset, check for the end of prices
        and handle position change
        :param action:
        :return: reward, done
        """
        assert isinstance(action, Actions)
        reward = 0.0
        done = False
        real_closes = self._prices.real_close.tolist()
        len_all = len(real_closes)
        after_offset = self._offset + 60
        after_offset = len_all if after_offset > len_all else after_offset
        pre_offset = 0 if after_offset < 120 else after_offset - 120
        after_offset = pre_offset + 120

        close = real_closes[self._offset]
        pre_closes = real_closes[pre_offset:self._offset + 1]
        max_pre_close = max(pre_closes)
        min_pre_close = min(pre_closes)
        max_pre_index = pre_closes[::-1].index(max_pre_close)
        if max_pre_index:
            min_pre_close = min(pre_closes[::-1][:max_pre_index])
        pre_reward = ((max_pre_close - close) / close) - ((close - min_pre_close) / min_pre_close)

        after_closes = real_closes[self._offset:after_offset + 1]

        max_after_close = max(after_closes)
        min_after_close = min(after_closes)
        max_after_index = after_closes.index(max_after_close)
        if max_after_index:
            min_after_close = min(after_closes[:max_after_index])

        after_reward = ((max_after_close - close) / close) - ((close - min_after_close) / min_after_close)
        print(after_reward, pre_reward)
        org_reward = after_reward + pre_reward

        if action == Actions.Buy:
            reward = org_reward
        elif action == Actions.Close:
            reward = -1 * org_reward
        elif action == Actions.Skip and self.have_position:
            reward = org_reward
        elif action == Actions.Skip and not self.have_position:
            reward = -1 * org_reward

        if action == Actions.Buy and not self.have_position:
            self.have_position = True
            self.open_price = close
        elif action == Actions.Close and self.have_position:
            done |= self.reset_on_close
            self.have_position = False

        self._offset += 1
        done |= self._offset >= self._prices.close.shape[0] - 1

        return reward, done


class State1D(State):
    """
    State with shape suitable for 1D convolution
    """

    @property
    def shape(self):
        if self.volumes:
            return (6, self.bars_count)
        else:
            return (5, self.bars_count)

    def encode(self):
        res = np.zeros(shape=self.shape, dtype=np.float32)
        start = self._offset - (self.bars_count - 1)
        stop = self._offset + 1
        idx = -1
        for idx, k in csv_header:
            res[idx] = getattr(self._prices, k)[start:stop]
        if self.have_position:
            res[idx + 1] = 1.0
            res[idx + 2] = self._cur_close() / self.open_price - 1.0
        return res


class StocksEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    spec = EnvSpec("StocksEnv-v0")

    def __init__(self, prices, bars_count=DEFAULT_BARS_COUNT,
                 commission=DEFAULT_COMMISSION_PERC,
                 reset_on_close=True, state_1d=False,
                 random_ofs_on_reset=True, reward_on_close=False,
                 volumes=False):
        assert isinstance(prices, dict)
        self._prices = prices
        if state_1d:
            self._state = State1D(
                bars_count, commission, reset_on_close,
                reward_on_close=reward_on_close, volumes=volumes)
        else:
            self._state = State(
                bars_count, commission, reset_on_close,
                reward_on_close=reward_on_close, volumes=volumes)
        self.action_space = gym.spaces.Discrete(n=len(Actions))
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf,
            shape=self._state.shape, dtype=np.float32)
        self.random_ofs_on_reset = random_ofs_on_reset
        self.seed()

    def reset(self):
        # make selection of the instrument and it's offset. Then reset the state
        self._instrument = self.np_random.choice(
            list(self._prices.keys()))
        prices = self._prices[self._instrument]
        bars = self._state.bars_count
        if self.random_ofs_on_reset:
            # print(prices.high.shape)
            # print(bars)
            # raise Exception(222)
            offset = self.np_random.choice(
                prices.high.shape[0] - bars * 10) + bars
        else:
            offset = bars
        self._state.reset(prices, offset)
        return self._state.encode()

    def step(self, action_idx):
        action = Actions(action_idx)
        reward, done = self._state.step(action)
        obs = self._state.encode()
        info = {
            "instrument": self._instrument,
            "offset": self._state._offset
        }
        return obs, reward, done, info

    def render(self, mode='human', close=False):
        pass

    def close(self):
        pass

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31
        return [seed1, seed2]

    @classmethod
    def from_dir(cls, data_dir, filter_data=True, **kwargs):
        # print(kwargs)
        prices = {}
        for file in data.price_files(data_dir):
            price = data.load_relative(file, filter_data=filter_data)
            if "bars_count" in kwargs:
                bars_count = kwargs["bars_count"]
                if price.high.shape[0] > bars_count * 10:
                    prices.setdefault(file, price)
            else:

                prices.setdefault(file, price)
        return StocksEnv(prices, **kwargs)
