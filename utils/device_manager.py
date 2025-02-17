import platform
import psutil
import tensorflow as tf
import torch
from typing import Literal

class DeviceOptimizer:
    def __init__(self):
        self.os_type = platform.system()
        self.cpu_cores = psutil.cpu_count(logical=False)
        self.gpu_available = tf.config.list_physical_devices('GPU') or torch.cuda.is_available()
        self.ram = psutil.virtual_memory().total // (1024 ** 3)  # In GB

    def get_optimal_config(self) -> dict:
        """Dynamically allocates resources based on hardware."""
        config = {
            'model_type': 'full',
            'batch_size': 64,
            'inference_threads': 2,
            'use_gpu': False,
            'quantization': 'fp32'
        }

        # Mobile/Low-end device logic
        if self.ram < 4 or self.cpu_cores <= 2:
            config.update({
                'model_type': 'lite',
                'batch_size': 8,
                'inference_threads': 1,
                'quantization': 'int8'
            })
        # High-end GPU logic
        elif self.gpu_available:
            config['use_gpu'] = True
            if self.ram >= 32:
                config['batch_size'] = 256
                config['inference_threads'] = 8

        # Edge-case for ARM (Raspberry Pi)
        if 'arm' in platform.machine().lower():
            config['model_type'] = 'arm-tflite'
            config['quantization'] = 'fp16'

        return config

    def configure_runtime(self):
        """Applies hardware-specific TensorFlow/PyTorch settings."""
        if self.os_type == 'Darwin' and not self.gpu_available:
            # Metal Performance Shaders for Apple Silicon
            tf.config.set_visible_devices([], 'GPU')  # Disable GPU to force MPS
        elif self.gpu_available:
            # CUDA/ROCm optimization
            tf.config.optimizer.set_jit(True)
            tf.config.threading.set_intra_op_parallelism_threads(self.cpu_cores // 2)
            tf.config.threading.set_inter_op_parallelism_threads(self.cpu_cores // 2)