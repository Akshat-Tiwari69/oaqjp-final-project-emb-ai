from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    if request.method == "POST":
        text_to_analyze = request.form.get("text")
        # Check for None, empty, or whitespace-only input
        if text_to_analyze is None or not text_to_analyze.strip():
            return render_template("index.html", output="Invalid text! Please try again!", text=text_to_analyze or "")
        
        result = emotion_detector(text_to_analyze)
        if "error" in result or result['dominant_emotion'] is None:
            return render_template("index.html", output=f"Error: {result.get('error', 'Unable to process the request')}", text=text_to_analyze)
        
        formatted_output = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']}, "
            f"and 'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )
        return render_template("index.html", output=formatted_output, text=text_to_analyze)
    
    return render_template("index.html", output=None, text=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)