import time
from Color import Color


class Ticker:
    
    def __init__(self, start_time, tick_len):
        self.start_time = start_time
        self.tick_start = start_time
        self.tick_len = tick_len

        # Initializing Tick load statistics
        self.i = 0
        self.load_list = [0 for i in range(20)]     # Contains the 20 last tick load values
        self.avg_load = 0
        self.max_load = 0
        self.min_load = 0
        self.run_time = 0
        self.iter_len = 0

    def next_tick(self):
        """
        Records the used computational time of tick. Then pauses the programm
        until the time until the next tick has elapsed.
        """
        t = time.time() - self.tick_start           # Elapsed time of tick
        self.update_statistics(t)                   # Update tick stats
        time.sleep(max(0, self.tick_len - t))       # Wait until next tick start
        self.tick_start = time.time()               # Start of next tick
   
    def update_statistics(self, t):
        """
        Updates the tick statistics for the current tick.
        """
        load = round(100 * t / self.tick_len, 2)    # Compute tick load
        self.load_list.pop(0)                       # Remove last load from list
        self.load_list.append(load)                 # Append load to list
        self.i += 1                                 # Iteration number
        self.avg_load = round(sum(self.load_list) / len(self.load_list),2)
        self.max_load = round(max(self.load_list),2)
        self.min_load = round(min(self.load_list),2)
        self.run_time = max(0.01, round(time.time() - self.start_time,2))
        self.iter_len = round(self.i / self.run_time, 2)
        
    def string_stats(self):
        """
        Returns all current stats values as a list of printeable strings
        """        
        stats_list = []
        stats_list.append(f'avg_load: {self.avg_load}')
        stats_list.append(f'max_load: {self.max_load}')
        stats_list.append(f'min_load: {self.min_load}')
        stats_list.append(f'run_time: {self.run_time}')
        stats_list.append(f'iter_len: {self.iter_len}')
        return stats_list
        
        
        
        
        
        
        
        
