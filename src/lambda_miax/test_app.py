import os

import app

def test_app():
    os.environ["MIAX_API_KEY"] = "AIzaSyDHAEqnHMPZ5UTM_JSnEY0u65HFHiH6XaY"
    app.handler([], [])
