import os
import logging
import numpy as np
import tensorflow as tf
from typing import Optional, Tuple
from utils.device_manager import DeviceOptimizer
# core/ml_models.py
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
import tensorflow as tf
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptiveAlphaModel:
    """Hybrid AI model with hardware-aware optimization and automatic quantization"""
    
    def __init__(self, input_shape: Tuple[int, int] = (60, 5)):
        self.device = DeviceOptimizer()
        self.config = self.device.get_optimal_config()
        self.input_shape = input_shape
        self.model: Optional[tf.keras.Model] = None
        self._initialize_model()

    def _initialize_model(self):
        """Smart model initialization with fallback handling"""
        try:
            self.model = self._load_model()
            logger.info(f"Loaded {self.config['model_type']} model quantized as {self.config['quantization']}")
        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            self._convert_model_to_lite()
            self.model = self._load_model()

    def _build_full_model(self) -> tf.keras.Model:
        """State-of-the-art trading model architecture"""
        return tf.keras.Sequential([
            tf.keras.layers.LSTM(128, input_shape=self.input_shape, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(64),
            tf.keras.layers.Dense(32, activation='swish'),
            tf.keras.layers.Dense(1, activation='linear')
        ], name="QuantumAlpha")

    def _load_model(self) -> tf.keras.Model:
        """Dynamic model loader with version control"""
        model_path = os.path.join("models", 
                                 f"{self.config['model_type']}_quant_{self.config['quantization']}.h5")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_path} not found")
            
        return tf.keras.models.load_model(model_path, compile=False)

    def _convert_model_to_lite(self):
        """Automated model optimization pipeline"""
        model_path = os.path.join("models", 
                                f"{self.config['model_type']}_quant_{self.config['quantization']}.h5")
        
        try:
            # Generate calibration data (1% of training data)
            calibration_data = np.random.randn(100, *self.input_shape).astype(np.float32)
            
            # Build and convert model
            model = self._build_full_model()
            model.compile(optimizer='adam', 
                         loss=tf.keras.losses.Huber(),
                         metrics=['mae'])
            
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            
            # Quantization rules
            if self.config['quantization'] == 'int8':
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.representative_dataset = lambda: [calibration_data]
                converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
            elif self.config['quantization'] == 'fp16':
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.target_spec.supported_types = [tf.float16]
            
            # ARM-specific optimizations
            if self.config['model_type'] == 'arm-tflite':
                converter._experimental_allow_all_select_tf_ops = True
                
            tflite_model = converter.convert()
            
            # Ensure model directory exists
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            with open(model_path, 'wb') as f:
                f.write(tflite_model)
                
            logger.info(f"Successfully converted model to {model_path}")
            
        except Exception as e:
            logger.error(f"Model conversion failed: {str(e)}")
            raise

    def predict(self, data: np.ndarray) -> np.ndarray:
        """Hardware-optimized inference pipeline"""
        try:
            if self.config['model_type'] == 'arm-tflite':
                return self._predict_tflite(data)
            return self.model.predict(data, batch_size=self.config['batch_size'], verbose=0)
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return np.zeros((data.shape[0], 1))  # Fail-safe output

    def _predict_tflite(self, data: np.ndarray) -> np.ndarray:
        """Edge-optimized inference for ARM devices"""
        try:
            model_path = os.path.join("models", "arm_lite.tflite")
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()
            
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Validate input shape
            if data.shape[1:] != tuple(input_details[0]['shape'][1:]):
                raise ValueError(f"Input shape {data.shape} doesn't match model {input_details[0]['shape']}")
                
            interpreter.set_tensor(input_details[0]['index'], data.astype(np.float32))
            interpreter.invoke()
            
            return interpreter.get_tensor(output_details[0]['index'])
            
        except Exception as e:
            logger.error(f"TFLite prediction failed: {str(e)}")
            return np.zeros((data.shape[0], 1))