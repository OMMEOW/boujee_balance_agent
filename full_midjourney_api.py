import subprocess
import json
import time
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FullMidjourneyAPI:
    def __init__(self):
        self.server_id = "1382982900638552064"
        self.channel_id = "1382982901091668020"
        # self.salai_token = NjQ3NDg1NDgzODQ4NTY0NzM4.GTGm_9.lCEh8gT0146vGn4vhbQU8ZZIqP9epyHdu1O2Vo
        
        
    def create_env_file(self):
        """Create .env file for midjourney-client"""
        try:
            env_content = f"""SERVER_ID="{self.server_id}"
CHANNEL_ID="{self.channel_id}"
SALAI_TOKEN="{self.salai_token}"
"""
            
            with open("midjourney-client/.env", "w") as f:
                f.write(env_content)
            
            logger.info("Created .env file for midjourney-client")
            return True
            
        except Exception as e:
            logger.error(f"Error creating .env file: {e}")
            return False

    def create_midjourney_script(self, prompt):
        """Create a Node.js script to run midjourney-client"""
        try:
            script_content = f'''
import "dotenv/config";
import {{ Midjourney }} from "./src";
import fetch from "node-fetch";
import fs from "fs";
import path from "path";

async function main() {{
    try {{
        console.log("Starting Midjourney API automation...");
        
        const client = new Midjourney({{
            ServerId: process.env.SERVER_ID,
            ChannelId: process.env.CHANNEL_ID,
            SalaiToken: process.env.SALAI_TOKEN,
            Debug: true,
            Ws: true,
        }});
        
        console.log("Connecting to Discord...");
        await client.Connect();
        console.log("Connected successfully!");
        
        console.log("Generating image with prompt:", "{prompt}");
        const Imagine = await client.Imagine(
            "{prompt}",
            (uri: string, progress: string) => {{
                console.log("Progress:", progress);
            }}
        );
        
        console.log("Image generation completed!");
        console.log("Result:", JSON.stringify(Imagine));
        
        if (Imagine && Imagine.attachments && Imagine.attachments.length > 0) {{
            const imageUrl = Imagine.attachments[0].url;
            console.log("Image URL:", imageUrl);
            
            // Download the image
            console.log("Downloading image...");
            const response = await fetch(imageUrl);
            if (response.ok) {{
                const buffer = await response.arrayBuffer();
                
                // Create screenshots directory
                const screenshotsDir = "../frontend/screenshots";
                if (!fs.existsSync(screenshotsDir)) {{
                    fs.mkdirSync(screenshotsDir, {{ recursive: true }});
                }}
                
                // Save the image
                const timestamp = Date.now();
                const filename = `${{screenshotsDir}}/midjourney_api_${{timestamp}}.png`;
                fs.writeFileSync(filename, Buffer.from(buffer));
                
                console.log("Image saved successfully:", filename);
                console.log("SUCCESS:", filename);
            }} else {{
                console.error("Failed to download image:", response.status);
                process.exit(1);
            }}
        }} else {{
            console.error("No image attachments found in response");
            process.exit(1);
        }}
        
        client.Close();
        console.log("Midjourney client closed");
        
    }} catch (error) {{
        console.error("Error:", error);
        process.exit(1);
    }}
}}

main();
'''
            
            # Write the script
            with open("midjourney-client/generate_image_api.ts", "w", encoding="utf-8") as f:
                f.write(script_content)
            
            logger.info("Created midjourney-client API script")
            return True
            
        except Exception as e:
            logger.error(f"Error creating midjourney script: {e}")
            return False

    def run_midjourney_api(self, prompt):
        """Run midjourney-client API to generate and download image"""
        try:
            logger.info(f"Running full Midjourney API with prompt: {prompt}")
            
            # Create the script
            if not self.create_midjourney_script(prompt):
                return False
            
            # Install node-fetch if not available
            try:
                subprocess.run(["npm", "install", "node-fetch"], cwd="midjourney-client", check=True, capture_output=True)
            except:
                pass  # node-fetch might already be installed
            
            # Run the script
            result = subprocess.run([
                "npx", "tsx", "generate_image_api.ts"
            ], cwd="midjourney-client", capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Midjourney API executed successfully")
                logger.info(f"Output: {result.stdout}")
                
                # Check if image was saved
                if "SUCCESS:" in result.stdout:
                    # Extract filename from output
                    for line in result.stdout.split('\n'):
                        if "SUCCESS:" in line:
                            filename = line.split("SUCCESS:")[1].strip()
                            logger.info(f"Image generated via API: {filename}")
                            return filename
                
                return True
            else:
                logger.error(f"Midjourney API failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running midjourney API: {e}")
            return False

    def run_automation(self, prompt):
        """Run the complete full API automation"""
        try:
            # Step 1: Create .env file
            if not self.create_env_file():
                logger.error("Failed to create .env file")
                return False
            
            # Step 2: Run midjourney-client API
            result = self.run_midjourney_api(prompt)
            
            return result
            
        except Exception as e:
            logger.error(f"Full API automation failed: {e}")
            return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python full_midjourney_api.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    automation = FullMidjourneyAPI()
    result = automation.run_automation(prompt)
    
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main() 