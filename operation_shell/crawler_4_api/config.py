# separator used by search.py, categories.py, ...
SEPARATOR = ";"

# LANG = "en_US"  # can be en_US, fr_FR, ...
LANG = "zh_CN"
ANDROID_ID = "30bb76cf4819b5d2"  # "xxxxxxxxxxxxxxxx"To get your androidID, use *#*#8255#*#* on your phone to start Gtalk Monitor.
GOOGLE_LOGIN = "lbesunzhennan@gmail.com"  # "username@gmail.com"
GOOGLE_PASSWORD = "lbeprivacy"
AUTH_TOKEN = None  # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

