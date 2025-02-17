import time
import psutil
import warnings
from threading import Thread
import torch  # Added import

class ResourceGuardian(Thread):
    def __init__(self, max_cpu=80, max_ram=90):
        super().__init__(daemon=True)
        self.max_cpu = max_cpu
        self.max_ram = max_ram
        self.running = True

    def run(self):
        while self.running:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent

            if cpu > self.max_cpu:
                warnings.warn(f"CPU overload ({cpu}%). Throttling processes.")
                self._throttle_workers()

            if ram > self.max_ram:
                warnings.warn(f"RAM overload ({ram}%). Freeing memory cache.")
                self._clear_memory()

    def _throttle_workers(self):
        from core.trade_executor import UniversalTrader
        if hasattr(UniversalTrader.executor, '_max_workers'):
            UniversalTrader.executor._max_workers = max(1, UniversalTrader.executor._max_workers - 1)

    def _clear_memory(self):
        import tensorflow as tf
        tf.keras.backend.clear_session()
        
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except NameError:
            pass  # Torch not installed