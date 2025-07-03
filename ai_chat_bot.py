import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# === Config ===
chromedriver_path = r"chrome_driver\chromedriver.exe"
profile_path = r"C:\SeleniumProfiles\Akkio"
prompts_file = "prompts.json"
interval_seconds = 5

# === Load prompts ===
with open(prompts_file, "r", encoding="utf-8") as f:
    prompts_data = json.load(f)
prompts = list(prompts_data.values())

# === Chrome setup ===
options = Options()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
driver.get("https://app.akkio.com/")

print("✅ Akkio opened. Please wait for it to fully load.")
input("🔘 Press Enter to start sending prompts every 1 minute...")


def wait_for_generation_to_finish(driver, timeout=120):
    cancel_button_selector = "button.chat-explore-input-cancel-button"
    wait = WebDriverWait(driver, timeout)

    try:
        # Wait until Cancel button appears (generation starts)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cancel_button_selector)))
        print("⏳ Generation started...")

        # Then wait until Cancel button disappears (generation ends)
        wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, cancel_button_selector)))
        print("✅ Generation finished.")
    except Exception as e:
        print(f"⚠️ Timeout waiting for generation to finish: {e}")
        
        
def timing_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time
        result = func(*args, **kwargs)
        end_time = time.time()    # End time
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to run.")
        return result
    return wrapper

@timing_wrapper
def ai_chat_bot():
    # === Main loop ===
    for idx, prompt in enumerate(prompts, start=1):
        try:
            # Find and send prompt to textbox
            textbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.chat-explore-container-input"))
            )
            textbox.clear()
            textbox.send_keys(prompt)
            time.sleep(0.5)
            textbox.send_keys(Keys.ENTER)
            print(f"✅ Sent Prompt {idx}: {prompt[:50]}...")

            # ✅ Wait for response generation to finish
            wait_for_generation_to_finish(driver)

            # Click Save button
            try:
                save_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'slot-content')]//div[contains(@data-icon-name, 'SaveIcon')]"))
                )
                save_btn.click()
                print(f"💾 Clicked Save button after prompt {idx}")
            except Exception as e:
                print(f"⚠️ Could not click Save button after prompt {idx}: {e}")

        except Exception as e:
            print(f"❌ Error on prompt {idx}: {e}")

        # Wait 60 seconds before the next prompt (including after last one)
        print(f"⏳ Waiting {interval_seconds} seconds before next prompt...")
        time.sleep(interval_seconds)

    print("✅ All prompts sent. Done.")

# === Start the chat bot ===
print("🚀 Starting AI chat bot...")
ai_chat_bot()