from selenium import webdriver
URL = "https://www.skyairline.com/english"

CLASSNAME_DENY_SUBS = 'pa-subs-btn-link'

ARGUMENTS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--disable-features=WebRtcHideLocalIpsWithMdns",
    "--no-sandbox",
    "--window-size=1920,1024",
    "--disable-dev-shm-usage",
    "--disable-extensions",
    "--disable-features=VizDisplayCompositor",
    "--disable-features=Translate",
    "--no-default-browser-check",
    "--disable-default-apps",
    "--disable-popup-blocking",
    "--disable-sync",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--incognito",
    "--disable-cache",
    "--disable-application-cache",
    "--disable-gpu-shader-disk-cache",
    "--disk-cache-dir=null",
]

chrome_options = webdriver.ChromeOptions()

for args in ARGUMENTS:
    chrome_options.add_argument(args)

DRIVER = webdriver.Chrome()
