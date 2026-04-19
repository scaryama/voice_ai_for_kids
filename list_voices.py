"""pyttsx3 사용 가능한 모든 음성 리스트 출력"""
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print(f"총 {len(voices)}개 음성 사용 가능:\n")
for i, voice in enumerate(voices):
    print(f"[{i}] ID: {voice.id}")
    print(f"    Name: {voice.name}")
    print(f"    Age: {voice.age}")
    print(f"    Gender: {voice.gender}")
    print()
