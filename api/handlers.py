from services.file_service import FileService
from services.prediction_service import PredictionService

class ModelHandler:
    @staticmethod
    def get_available_models():
        return FileService.get_available_models()
        
    @staticmethod
    def get_models_with_training_logs():
        return FileService.get_models_with_training_logs()

class PredictionHandler:
    @staticmethod
    def predict(model_id, image_data):
        prediction_service = PredictionService()
        return prediction_service.predict(model_id, image_data)

class TrainingHistoryHandler:
    @staticmethod
    def get_history(model_id):
        return FileService.get_training_history(model_id)
        
class TrainingLogHandler:
    @staticmethod
    def get_models_with_logs():
        return FileService.get_models_with_training_logs()
        
    @staticmethod
    def get_model_log(model_id):
        return FileService.get_model_training_log(model_id) 