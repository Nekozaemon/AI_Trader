import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import platform
import subprocess
from core.ml_models import AdaptiveAlphaModel
from utils.device_manager import DeviceOptimizer

def setup_device():
    dev = DeviceOptimizer()
    config = dev.get_optimal_config()
    
    # Platform-specific installs
    if 'arm' in platform.machine().lower():
        subprocess.run([
            'pip', 'install', 'tflite-runtime', 
            '--extra-index-url', 'https://google-coral.github.io/py-repo/'
        ], check=True)
    elif dev.gpu_available:
        subprocess.run(['pip', 'install', 'tensorflow[and-cuda]'], check=True)
    
    # Model initialization
    model = AdaptiveAlphaModel()
    model._convert_model_to_lite()

if __name__ == '__main__':
    setup_device()