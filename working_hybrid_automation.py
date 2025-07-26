import time
import os
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkingHybridAutomation:
    def __init__(self):
        self.email = "koyande.om27@gmail.com"
        self.password = "Autowhat@2025"
        self.channel_url = "https://discord.com/channels/1382982900638552064/1382982901091668020"
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with headless options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Chrome driver setup successful with webdriver-manager")
            except Exception as e:
                logger.warning(f"webdriver-manager failed: {e}")
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("Chrome driver setup successful with system ChromeDriver")
                
        except Exception as e:
            logger.error(f"Chrome driver setup failed: {e}")
            raise

    def login_to_discord(self):
        """Login to Discord"""
        try:
            logger.info("Logging into Discord...")
            self.driver.get("https://discord.com/login")
            
            # Wait for login form
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Enter credentials
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            logger.info("Discord login successful")
            
        except Exception as e:
            logger.error(f"Discord login failed: {e}")
            raise

    def navigate_to_channel(self):
        """Navigate to the specific Discord channel"""
        try:
            logger.info("Navigating to Discord channel...")
            self.driver.get(self.channel_url)
            time.sleep(3)
            logger.info("Successfully navigated to Discord channel")
            
        except Exception as e:
            logger.error(f"Failed to navigate to channel: {e}")
            raise

    def send_prompt(self, prompt):
        """Send the Midjourney prompt"""
        try:
            logger.info("Sending prompt to Discord...")
            
            # Find the message input field
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-slate-editor='true']"))
            )
            
            # Type /imagine and press space
            message_input.send_keys("/imagine")
            message_input.send_keys(Keys.SPACE)
            time.sleep(1)
            
            # Clean the prompt (remove any Midjourney prefixes)
            clean_prompt = prompt
            if "Midjourney v6" in clean_prompt:
                clean_prompt = clean_prompt.split("Midjourney v6")[1].strip()
            if clean_prompt.startswith("--ar 1:1:"):
                clean_prompt = clean_prompt.split("--ar 1:1:")[1].strip()
            
            # Send the clean prompt
            message_input.send_keys(clean_prompt)
            message_input.send_keys(Keys.ENTER)
            
            logger.info("Prompt sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            raise

    def wait_for_image_and_download(self):
        """Wait for image generation and download it"""
        try:
            logger.info("Waiting for image generation...")
            
            # Wait for image to appear
            time.sleep(45)  # Wait for generation
            
            # Scroll to bottom to see latest messages
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Look for generated images - get ALL images first
            image_selectors = [
                "img[src*='cdn.discordapp.com/attachments']",
                "img[src*='media.discordapp.net']"
            ]
            
            all_images = []
            for selector in image_selectors:
                try:
                    images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for img in images:
                        image_url = img.get_attribute('src')
                        if image_url:
                            all_images.append({
                                'element': img,
                                'url': image_url
                            })
                except:
                    continue
            
            if all_images:
                # Get the most recent image (last one in the list)
                latest_image = all_images[-1]
                image_url = latest_image['url']
                
                logger.info(f"Found {len(all_images)} images, downloading the most recent one")
                
                # Download the most recent image
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    # Save the image
                    os.makedirs("frontend/screenshots", exist_ok=True)
                    filename = f"frontend/screenshots/midjourney_working_{int(time.time())}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    logger.info(f"Most recent image downloaded successfully: {filename}")
                    return filename
                else:
                    logger.error(f"Failed to download image: HTTP {response.status_code}")
            else:
                logger.warning("No images found")
            
            return None
                
        except Exception as e:
            logger.error(f"Failed to capture image: {e}")
            return None

    def run_automation(self, prompt):
        """Run the complete working hybrid automation"""
        try:
            # Step 1: Login
            self.login_to_discord()
            
            # Step 2: Navigate to channel
            self.navigate_to_channel()
            
            # Step 3: Send prompt
            self.send_prompt(prompt)
            
            # Step 4: Wait and download image
            image_path = self.wait_for_image_and_download()
            
            if image_path:
                logger.info("Working automation completed successfully")
                return image_path
            else:
                logger.error("Working automation failed - no image captured")
                return None
                
        except Exception as e:
            logger.error(f"Working automation failed: {e}")
            return None
        finally:
            self.driver.quit()

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python working_hybrid_automation.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    automation = WorkingHybridAutomation()
    result = automation.run_automation(prompt)
    
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main() 