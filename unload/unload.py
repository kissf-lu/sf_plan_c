# -*- coding: utf-8 -*-


from simpy import Environment

from ..config.config import land_init_params


class UnLoad:

    def __init__(self, queue):
        # self.time = 0      # 机器同步时钟，与系统同步
        self.last_time = 0
        self.queue = queue

    def unload(self):
        """
        unload mail from truck!
        """

