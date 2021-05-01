import webbrowser

try:
    webbrowser.open_new("www.microsoft.com")
except Exception as e:
    print(e.with_traceback)