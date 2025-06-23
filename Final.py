import cv2
import mediapipe as mp
import numpy as np
import joblib
import pyautogui
import time
import speech_recognition as sr

# Set up PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

# Ask user to choose control method
controllMethod = input("Hand Gestures (0)/ Voice Commands (1): ")

# ------------------- HAND GESTURE CONTROL ------------------- #
if controllMethod == '0':
    print("Gesture Control Mode Selected")

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    # Load trained model
    try:
        model = joblib.load("gesture_model.pkl")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        exit()

    # Parameters
    CONFIDENCE_THRESHOLD = 0.5
    GESTURE_DURATION = 1  # seconds
    last_prediction = None
    gesture_start_time = 0

    def extract_landmarks(frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            landmarks = []
            for lm in results.multi_hand_landmarks[0].landmark:
                landmarks.extend([lm.x, lm.y])
            return np.array(landmarks).reshape(1, -1)
        return None

    cap = cv2.VideoCapture(0)
    cap.set(3, 1480)
    cap.set(4, 920)
    print("Starting gesture detection...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame.")
                break

            frame = cv2.flip(frame, 1)
            landmarks = extract_landmarks(frame)

            if landmarks is not None:
                probs = model.predict_proba(landmarks)[0]
                labels = model.classes_
                max_prob = np.max(probs)
                prediction = labels[np.argmax(probs)]

                print(f"Prediction: {prediction}, Confidence: {max_prob:.2f}")

                if max_prob >= CONFIDENCE_THRESHOLD and prediction in ["next", "previous"]:
                    if last_prediction == prediction:
                        if gesture_start_time == 0:
                            gesture_start_time = time.time()
                        elif time.time() - gesture_start_time >= GESTURE_DURATION:
                            if prediction == "next":
                                pyautogui.press("right")
                                print("Next slide")
                            elif prediction == "previous":
                                pyautogui.press("left")
                                print("Previous slide")
                            gesture_start_time = 0
                    else:
                        gesture_start_time = time.time()
                else:
                    gesture_start_time = 0
                    last_prediction = None
            else:
                print("No hand detected.")
                gesture_start_time = 0
                last_prediction = None

            last_prediction = prediction if landmarks is not None else None

            cv2.imshow("Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cap.release()
        hands.close()
        cv2.destroyAllWindows()

# ------------------- VOICE COMMAND CONTROL ------------------- #
elif controllMethod == '1':
    print("Voice Command Mode Selected")

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready! Say 'next' or 'previous'...")

    while True:
        with mic as source:
            print("Listening for command...")
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if "next" in command:
                    pyautogui.press("right")
                    print("Next slide")

                elif "previous" in command:
                    pyautogui.press("left")
                    print("Previous slide")

            except sr.WaitTimeoutError:
                print("Timeout: No speech detected.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")

else:
    print("Invalid input. Please enter 0 or 1.")
