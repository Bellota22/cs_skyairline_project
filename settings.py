from selenium import webdriver
URL_FORMATTED = 'https://www.skyairline.com/english/flujo-compra/busqueda-vuelos?fromCityCode={from_country_code}&fromCityCode={to_country_code}&toCityCode={to_country_code}&toCityCode={from_country_code}&departureDateString={departure_date}&departureDateString={return_date}&fareTypeCategory=1&adults=1&currency=USD&isNewSearch=true&flightType=triptype_roundtrip&flightOriginalType=triptype_roundtrip'

CLASSNAME_DENY_SUBS = 'pa-subs-btn-link'

MONTH_MAP = {
                    'ene': 'Jan',
                    'feb': 'Feb',
                    'mar': 'Mar',
                    'abr': 'Apr',
                    'may': 'May',
                    'jun': 'Jun',
                    'jul': 'Jul',
                    'ago': 'Aug',
                    'sep': 'Sep',
                    'oct': 'Oct',
                    'nov': 'Nov',
                    'dic': 'Dec'
                }
list_of_flights = {
            'Peru':{
                'Trujillo':'TRU',
                'Ayacucho':'AYP',
                'Tumbes':'TBP',
                'Cusco':'CUZ',
                'Pucallpa':'PCL',
                'Talara':'TYL',
                'Piura':'PIU',
                'Juliaca':'JUL',
                'Iquitos':'IQT',
                'Tarapoto':'TPP',
                'Lima':'LIM',
                'Jauja':'JAU',
                'Arequipa':'AQP',
                'Cajaamarca':'CJA',
                'Chiclayo':'CIX',
            }
        
        }
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


