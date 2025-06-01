"""
Flask web application for emotion detection using the EmotionDetection package.

This module provides a web interface to analyze text for emotions using the Watson NLP API.
It handles user input via a form, processes the text, and displays the emotion analysis results.
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector
app = Flask(__name__)
@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests via a web form.

    Returns:
        Rendered HTML template with the emotion detection result or an error message.
    """
    if request.method == "POST":
        text_to_analyze = request.form.get("text")
        # Check for None, empty, or whitespace-only input
        if text_to_analyze is None or not text_to_analyze.strip():
            return render_template("index.html", output="Invalid text! Please try again!", text="")
        result = emotion_detector(text_to_analyze)
        if "error" in result or result['dominant_emotion'] is None:
            return render_template("index.html", output="Invalid text! Please try again!", text="")
        formatted_output = (
            "For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']}, and "
            f"'sadness': {result['sadness']}. The dominant emotion is "
            f"{result['dominant_emotion']}."
        )
        return render_template("index.html", output=formatted_output, text="")
    return render_template("index.html", output=None, text=None)
if __name__ == "__main__":
    # Entry point for running the Flask application.
    # Runs the server on host 0.0.0.0 and port 5000 with debug mode enabled.
    app.run(host="0.0.0.0", port=5000, debug=True)
    