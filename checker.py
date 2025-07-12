from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import questionary
import requests
import time
import os


webhook_url = 'https://discord.com/api/webhooks/x/x'




url = input("Product URL: ").strip()


options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--log-level=3")
options.add_argument("--silent")
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
null = open(os.devnull, 'w')
service = Service(log_path=null)

driver = webdriver.Chrome(service=service, options=options)


driver.get(url)
time.sleep(3)


productName = ""

def getTitle():
    try:
        global productName
        productName = driver.find_element(By.CSS_SELECTOR, "[data-testid='main-product-name']").get_attribute("textContent").strip()
        print(f"🔍 Monitoring product: {productName}")
        os.system("title Monitoring " + productName)
    except Exception as e:
        print(f"Failed to retrieve product name: {e}")


getTitle()


# ===================== GET OPTIONS START ===============================================================================================================

color_options = []
primary_options = []
secondary_options = []

colorWrappers = driver.find_elements(By.CSS_SELECTOR, '[data-testid="swtg-image-inner-wrapper"]')
for wrapper in colorWrappers:
    try:
        img = wrapper.find_element(By.TAG_NAME, "img")
        color_name = img.get_attribute("alt")# or "Unnamed"
        if not color_name: continue
        input_elem = img.find_element(By.XPATH, "./ancestor::div[@data-testid='swtg-input-inner-wrapper']//input")
        input_id = input_elem.get_attribute("id")
        color_options.append({
            "name": color_name.title(),
            "input_id": input_id,
        })
    except Exception as e:
        print("Failed to parse one color option:", e)
    

optionWrappers = driver.find_elements(By.CSS_SELECTOR, '[data-testid="sitg-input-inner-wrapper"]')
for wrapper in optionWrappers:
    try:
        input_elem = wrapper.find_element(By.TAG_NAME, "input")
        input_id = input_elem.get_attribute("id")
        input_type = input_id.split("_")[-2]  # primary or secondary
        input_name = input_id.split("_")[-1]
        if input_type == "primary":
            primary_options.append({
                "name": input_name.title(),
            })
        elif input_type == "secondary":
            secondary_options.append({
                "name": input_name.title(),
            })

    except Exception as e:
        print("Failed to parse one color option:", e)

# ===================== GET OPTIONS END ===============================================================================================================


rawCol = questionary.select(
    "Choose a color to monitor",
    choices=[color["name"] for color in color_options],
).ask()
if rawCol == None:
    driver.quit()
    os._exit(0)

rawPrim = questionary.select(
    "Choose a primary option to monitor",
    choices=[primary["name"] for primary in primary_options],
).ask()
if rawPrim == None:
    driver.quit()
    os._exit(0)

rawSec = None
if secondary_options:
    rawSec = questionary.select(
        "Choose a secondary option to monitor",
        choices=[secondary["name"] for secondary in secondary_options],
    ).ask()
    if rawSec == None:
        driver.quit()
        os._exit(0)

colour = rawCol #input("Colour to monitor (e.g. Dark Grey, Light Wash): ").strip()
primary_size = rawPrim #input("Primary size to monitor (e.g. S, M, 30, 31): ").strip()
secondary_size = rawSec #input("Secondary size (e.g. Regular, Tall, 30, 31), or leave blank: ").strip()
interval = float(input("Check interval (in minutes): ").strip())





def acceptCookies():
    try:
        cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]")
        for btn in cookie_buttons:
            if btn.is_displayed() and btn.is_enabled():
                btn.click()
                break
    except Exception as e:
        print(f"Cookie popup handling failed: {e}")


def choosePrimary(label_text):
    try:
        id_suffix = f"{label_text.replace(' ', '')}"
        radio_id = f"radio_size_primary_{id_suffix}"
        print(f"Choosing ID: {radio_id}")
        input_elem = driver.find_element(By.ID, radio_id)
        input_elem.click()
    except:
        return

def chooseColor(label_text):
    try:
        img_elem = driver.find_element(By.XPATH, f"//img[@alt='{label_text.lower()}']")
        input_elem = img_elem.find_element(By.XPATH, "./ancestor::div[@data-testid='swtg-input-inner-wrapper']//input")
        input_elem.click()
    except:
        return
    


def sendWebhook(primary_size, secondary_size="Any"):
    data = {
        "embeds": [
            {
                "title": f"**{productName}** is in stock!",
                "url": url,
                "description": f"{primary_size} x {secondary_size or 'Any'} is now in stock.",
                "color": 0x00FF00
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Webhook sent successfully.")
        else:
            print(f"Failed to send webhook: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending webhook: {e}")


def isOptionInStock(label_text, type_):
    try:
        id_suffix = f"{label_text.replace(' ', '')}"
        radio_id = f"radio_size_{type_}_{id_suffix}"
        input_elem = driver.find_element(By.ID, radio_id)
        parent = input_elem.find_element(By.XPATH, "..")

        # If parent has attribute "data-variant" and its value is "unavailable", return False
        if parent.get_attribute("data-variant") == "unavailable":
            return False
        else:
            return True
    except:
        return False
    


def check_stock():
    driver.get(url)
    time.sleep(3)

    acceptCookies()
    time.sleep(2)

    chooseColor(colour)
    time.sleep(1)

    PrimaryisInStock = isOptionInStock(primary_size, 'primary')
    if not PrimaryisInStock or not secondary_size:
        return PrimaryisInStock, "primary"

    choosePrimary(primary_size)
    time.sleep(1)

    isInStock = isOptionInStock(secondary_size, 'secondary')
    return isInStock, "secondary"
        


def sleep_interruptible(seconds):  # makes keyboard interrupt work
    total = int(seconds)
    for _ in range(total):
        time.sleep(1)


print(f"\n🔍 Monitoring {primary_size} x {secondary_size or 'Any'} every {interval} minutes...\n")
try:
    while True:
        in_stock, size_type = check_stock()
        if in_stock:
            print(f"✅ {primary_size} x {secondary_size} IS IN STOCK! Opening browser...")
            sendWebhook(primary_size, secondary_size)
            import webbrowser
            webbrowser.open(url)
            break
        else:
            print(f"❌ {size_type.title()} option {primary_size} is out of stock. Retrying in {interval} minutes...")
        sleep_interruptible(interval * 60)
except KeyboardInterrupt:
    print("\n🔴 Stopping...")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    driver.quit()
