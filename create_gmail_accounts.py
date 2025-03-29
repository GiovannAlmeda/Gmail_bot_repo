import sys
sys.path.insert(0, "./gologin")

import json
import random
import string
import time
import requests
from pygologin import GoLogin
from playwright.sync_api import sync_playwright

# Manual API key and proxy setup (based on what you've provided)
GOLOGIN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2U2ZjI1ZDM2ZThmODM4Mjc5NjdlZTQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2U2ZmEwYmI4YTAzZjE0NjViNDI5ODAifQ.yFZ8VNA97vcYoRklFnVqKbkYILi2AaxnGWUzN-B8wCQ"
CAPMONSTER_KEY = "5208dabf5c425c432367db24a690a2bf"
SMS_API_KEY = "349135fdc777c53e439B7095f1ceefc1"

PROXY = {
    "ip": "109.236.82.42",
    "port": "9999",
    "username": "y8ievdchn3-mobile.res-country-US-hold-session-67e70030d3dc6",
    "password": "Y4493zklzpwUTHsV"
}

ACCOUNT_COUNT = 15
OUTPUT_FILE = "accounts.txt"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def log_account(email, password):
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{email}:{password}\n")

print("🚀 Starting Gmail automation bot...")

def create_browser_profile():
    gl = GoLogin({
        "token": GOLOGIN_API_KEY
    })

    profile_id = gl.create({
        "name": f"gmail-bot-{random_string(5)}",
        "os": "mac",
        "browserType": "chrome",
        "navigator": {
            "language": "en-US",
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "platform": "MacIntel",
            "resolution": "1920x1080",
            "hardwareConcurrency": 4,
            "deviceMemory": 8,
            "maxTouchPoints": 0
        },
        "proxy": {
            "mode": "socks5",
            "host": PROXY["ip"],
            "port": int(PROXY["port"]),
            "username": PROXY["username"],
            "password": PROXY["password"]
        }
    })

    gl.profile_id = profile_id
    debug_port = gl.start()  # Fixed: no argument passed
    return profile_id, debug_port, gl

# Main run loop
with sync_playwright() as p:
    for i in range(ACCOUNT_COUNT):
        print(f"\n🔁 Creating account {i+1}/{ACCOUNT_COUNT}...")

        first_name = random_string(6).capitalize()
        last_name = random_string(7).capitalize()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(100,999)}"
        password = random_string(12)

        print(f"👤 Name: {first_name} {last_name}")
        print(f"📧 Username: {username}")
        print(f"🔐 Password: {password}")

        profile_id, port, gl = create_browser_profile()

        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            page = browser.contexts[0].pages[0]

            print("🌐 Visiting Gmail signup page...")
            page.goto("https://accounts.google.com/signup", timeout=60000)

            time.sleep(10)  # Pause to watch

        except Exception as e:
            print(f"❌ Error during browser session: {e}")

        finally:
            gl.stop()

        log_account(f"{username}@gmail.com", password)

print("\n✅ All accounts processed and saved.")
