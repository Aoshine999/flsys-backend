from flask import Blueprint, request, jsonify
from .handlers import ModelHandler, PredictionHandler, TrainingHistoryHandler, TrainingLogHandler

api_bp = Blueprint('api', __name__)

@api_bp.route('/models/', methods=['GET'])
def get_models():
    try:
        models = ModelHandler.get_available_models()
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/predict/', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        image_data = data.get('image_data')
        print(data,model_id,image_data)
        if not model_id or not image_data:
            return jsonify({"error": "Missing required parameters"}), 400
            
        predictions = PredictionHandler.predict(model_id, image_data)
        return jsonify({"predictions": predictions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/models/<model_id>/training_history/', methods=['GET'])
def get_training_history(model_id):
    try:
        history = TrainingHistoryHandler.get_history(model_id)
        return jsonify(history)
    except FileNotFoundError:
        return jsonify({"error": "History file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@api_bp.route('/models/with_training_logs/', methods=['GET'])
def get_models_with_training_logs():
    try:
        models = TrainingLogHandler.get_models_with_logs()
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/models/<model_id>/training_log/', methods=['GET'])
def get_model_training_log(model_id):
    try:
        log_content = TrainingLogHandler.get_model_log(model_id)
        return jsonify({"model_id": model_id, "log_content": log_content})
    except FileNotFoundError:
        return jsonify({"error": "Training log file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500 