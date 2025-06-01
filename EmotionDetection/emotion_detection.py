import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text using Watson NLP API.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing emotion scores (anger, disgust, fear, joy, sadness)
              and the dominant emotion. Returns None for all values if status_code is 400.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, headers=headers, json=input_json)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        response.raise_for_status()  # Raise an exception for other bad status codes
        # Convert response text to dictionary
        response_dict = json.loads(response.text)
        # Extract emotion scores
        emotions = response_dict.get('emotionPredictions', [{}])[0].get('emotion', {})
        anger_score = emotions.get('anger', 0.0)
        disgust_score = emotions.get('disgust', 0.0)
        fear_score = emotions.get('fear', 0.0)
        joy_score = emotions.get('joy', 0.0)
        sadness_score = emotions.get('sadness', 0.0)
        # Find dominant emotion
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        # Return formatted output
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
    except requests.exceptions.RequestException as e:
        return {
            'anger': 0.0,
            'disgust': 0.0,
            'fear': 0.0,
            'joy': 0.0,
            'sadness': 0.0,
            'dominant_emotion': None,
            'error': str(e)
        }