import pywinauto

app = pywinauto.application.Application().connect(best_match="Ultimate Chicken Horse")
window_ids = pywinauto.findwindows.find_windows("Ultimate Chicken Horse")
window = app.window_(handle=window_ids[0])
window.set_focus()
