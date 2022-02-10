# נייבא את הספרייה
import pyttsx3
# נאתחל את הספרייה לתוך משתנה
tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', voices[1].id)
# input פקודת
# name = input("Enter name: ")
# פקודה שמכינה במנוע הדיבור את הטקסט שאותו תקריא
tts.say("Welcome to my Python course")
# פקודת ההקראה. לאחר שתופעל פקודה זו, התוכנית תחכה עד שתסתיים ההקראה
tts.runAndWait()