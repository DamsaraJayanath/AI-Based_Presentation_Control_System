# AI-Based Presentation Control System

This project is a presentation controller built using Python, OpenCV, MediaPipe, Scikit-learn, and SpeechRecognition. It allows users to control presentation slides using either hand gestures or voice commands, providing a touch-free presentation experience.

## Key Features
1. Control presentation slides using hand gestures
2. Control slides using voice commands such as “next” and “previous”
3. Real-time hand tracking and gesture recognition
4. Random Forest model trained on a custom hand gesture dataset
5. Live webcam feedback with gesture prediction and confidence score

<h2>File Structure</h2>
<ul>
  <li><code>Model.ipynb</code> – Jupyter notebook used to extract MediaPipe hand landmarks and train a gesture recognition model using Random Forest.</li>
  <li><code>gesture_model.pkl</code> – Saved trained model (exported via Joblib).</li>
  <li><code>presentation_control.py</code> – Main script to run either hand gesture or voice command mode for controlling slides.</li>
</ul>

<h2>Hand Gesture Mode</h2>
<ol>
  <li>Detects hand landmarks using <strong>MediaPipe</strong>.</li>
  <li>Extracts (x, y) positions of 21 landmarks and classifies the gesture using a <strong>Random Forest model</strong>.</li>
  <li>If "next" gesture is detected with high confidence for a duration, it sends a <code>→</code> (next slide).</li>
  <li>If "previous" gesture is detected, it sends a <code>←</code> (previous slide).</li>
</ol>

<h2>Voice Command Mode</h2>
<ol>
  <li>Listens to your microphone using the <strong>SpeechRecognition</strong> library.</li>
  <li>Recognizes voice commands like "next" or "previous".</li>
  <li>Triggers respective key presses to control the slides.</li>
</ol>

<h2>How to Run</h2>
<pre><code>python Final.py</code></pre>
<p>Then, input either <code>0</code> (hand gesture mode) or <code>1</code> (voice command mode) when prompted.</p>

<h2>🛠 Requirements</h2>
<ul>
  <li>Python 3.x</li>
  <li>Webcam and/or microphone</li>
  <li>Python libraries:</li>
  <ul>
    <li>opencv-python</li>
    <li>mediapipe</li>
    <li>numpy</li>
    <li>scikit-learn</li>
    <li>joblib</li>
    <li>pyautogui</li>
    <li>speechrecognition</li>
  </ul>
</ul>

<h2>📦 Install Dependencies</h2>
<pre><code>pip install opencv-python mediapipe numpy scikit-learn joblib pyautogui SpeechRecognition </code></pre>

<h2>Dataset</h2>
<p>
The dataset for training gestures was created manually using MediaPipe landmarks extracted from the webcam feed. The trained model is included as <code>gesture_model.pkl</code>.
</p>


<h2>💡 Future Enhancements</h2>
<ul>
  <li>Support for more gestures (e.g., start/pause slideshow)</li>
  <li>Improved voice intent recognition (e.g., "go back one slide")</li>
  <li>GUI interface for better usability</li>
</ul>

<h2>💡 Tip</h2>
<p>
You can use your own hand gesture dataset to personalize this system. Make sure to capture two clear hand gestures—one for <strong>"next"</strong> and one for <strong>"previous"</strong>. Once your data is ready, run the <code>Model.ipynb</code> notebook with your dataset to train and export a new model.
</p>

