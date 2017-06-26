# -*- coding: utf-8 -*-
"""

"""

import queue


unload_wait_queue = {
    'unload_r1_m1_1': queue.PriorityQueue(),
    'unload_r1_m1_2': queue.PriorityQueue(),
    'unload_r1_m1_3': queue.PriorityQueue(),
    'unload_r1_m1_4': queue.PriorityQueue()
}
unload_service_queue = {
    'unload_r1_m1_1': queue.PriorityQueue(),
    'unload_r1_m1_2': queue.PriorityQueue(),
    'unload_r1_m1_3': queue.PriorityQueue(),
    'unload_r1_m1_4': queue.PriorityQueue()
}
