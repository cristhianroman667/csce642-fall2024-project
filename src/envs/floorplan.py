import gymnasium as gym
import numpy as np

from gymnasium import spaces
from gymnasium.utils import seeding

from ..utils import Design


class FloorplanEnv(gym.Env):
    """
    The Floorplan environment
    """

    def __init__(self, name):
        self.action_space = spaces.Box(
          low=np.array([-3] * 2),
          high=np.array([3] * 2),
          dtype=np.float32
        )
        self.observation_space = spaces.Box(
          low=np.array([-5] * 20),
          high=np.array([5] * 20),
          dtype=np.float32
        )
        self._seed()
        self._reset()
        self.nA = 2
        self.name = "Floorplan"
        self.design_name = name

    def reset(self, seed=123):
        return self._reset()

    def step(self, action):
        return self._step(action)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action)
        action = np.argmax(action)
        if action == 0:
          # perform the swap
          n1 = np.random.randint(self.nblocks)
          n2 = np.random.randint(self.nblocks)
          self.design.swap_blocks(f'sb{n1}', f'sb{n2}')
          new_f = self.design.get_hpwl()
          reward = - (new_f - self.prev_f)

          self.prev_f = new_f
          done = True if reward < 10 else False

        elif action == 1:
          # perform a rotation
          nn = np.random.randint(self.nblocks)
          self.design.rotate_block(f'sb{nn}')
          new_f = self.design.get_hpwl()
          reward = - (new_f - self.prev_f)

          self.prev_f = new_f
          done = True if reward < 10 else False

        # else:
        #   # perform a delete and insert
        #   nn = np.random.randint(self.nblocks)
        #   self.design.delete(f'sb{nn}')
        #   self.design.insert(f'sb{nn}')
        #   new_f = self.design.get_hpwl()
        #   reward = - (new_f - self.prev_f)

        #   self.prev_f = new_f
        #   done = True if reward < 10 else False

        return self.design.get_features(), reward, done, False, {}

    def _get_obs(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def _reset(self):
        self.design = Design('n200')
        self.design.parse()
        self.nblocks = len(self.design.blocks)
        self.prev_f = self.design.get_hpwl()

        return self.design.get_features(), {}




