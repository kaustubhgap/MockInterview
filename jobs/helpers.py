import secrets
from typing import Any
import pyttsx3
import speech_recognition as sr

def make_token() -> str:
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16)  

def convert_to_string(obj:Any, connector:str) -> str:
    out = []
    if isinstance(obj, (tuple, list, set)):
        temp = []
        for element in obj:
            if isinstance(element, (str, int, float, bool)):
                temp.append(str(element))
            else:
                temp.append(convert_to_string(element, connector))
        curr_string = "|".join(temp)
        # curr_string = "|"+curr_string+"|"
        out.append(curr_string)
        out.append("\n")
        return "".join(out)
    
    elif isinstance(obj, dict):
        for key, value in obj.items():
            left = str(key)
            right = convert_to_string(value, connector)
            out.append(left+" : "+right)
        out.append("\n")
        return "".join(out)

def speak(text: str, engine: pyttsx3.engine) -> None:
    engine.say(text)      # Queue the text to be spoken
    engine.runAndWait()   # Wait for the speech to finish

if __name__ == "__main__":
    # print(make_token())
    temp = [
        [
          "1",
          "Image Processing Techniques",
          "Theoretical",
          "8"
        ],
        [
          "2",
          "Deep Learning Frameworks (PyTorch, TensorFlow, ONNX)",
          "Implementation Based",
          "9"
        ],
        [
          "3",
          "AI Model Deployment Strategies (including Edge AI)",
          "Implementation Based",
          "8"
        ],
        [
          "4",
          "Experience with Regulatory Compliance in Medical Devices",
          "Theoretical",
          "7"
        ],
        [
          "5",
          "Programming with GPUs and Performance Optimization",
          "Implementation Based",
          "9"
        ]
    ]
    print(convert_to_string(temp, connector="|"))