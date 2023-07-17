import cx_Freeze

executables = [cx_Freeze.Executable("Kiara.py", base="Win32GUI", icon="logo.ico")]

cx_Freeze.setup(
    name = "Kiara",
    author = "Sobhan Bose",
    version = "1.0.3",
    options = {"build_exe": {"packages": ["tkinter", "pygame", "webbrowser", "time", "datetime", "threading", "playsound", "speech_recognition", "gtts", "apiai", "json", "random", "PIL", "urllib", "pytemperature", "pyautogui", "pyperclip", "os", "sys"], "include_files": ["Intro_Images", "Notes", "Screens", "Screenshots", "System_Files"], "excludes":["Tkinter"]}},
    executables = executables
)
