import pandas as pd
import openpyxl
from datetime import datetime
import pytz
import json
import os
import subprocess
import sys
from openpyxl import load_workbook
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentAutomation:
    def __init__(self):
        self.excel_file = "1234.xlsx"
        self.openai_api_key = "sk-proj-1234567890abcdef"  # Replace with your actual key
        self.platform_colors = {
            'FFFFC0CB': 'Instagram',  # Pink
            'FF0000FF': 'Facebook',   # Blue
            'FF00FF00': 'LinkedIn',   # Green
            'FFFFFF00': 'WhatsApp'    # Yellow
        }
        self.platform_content_types = {
            'Instagram': ['carousel', 'reels', 'image', 'stories'],
            'Facebook': ['post', 'image', 'video'],
            'LinkedIn': ['post', 'article', 'image'],
            'WhatsApp': ['marketing', 'catalogue', 'image']
        }
        
    def get_color_coded_content(self):
        """Read Excel file and get content based on color-coded cells"""
        try:
            wb = load_workbook(self.excel_file)
            ws = wb["CALANDER"]
            
            content_items = []
            ist = pytz.timezone('Asia/Kolkata')
            today = datetime.now(ist).strftime('%Y-%m-%d')
            
            for row in range(2, ws.max_row + 1):
                brand = ws.cell(row=row, column=1).value
                products = ws.cell(row=row, column=2).value
                date_cell = ws.cell(row=row, column=3).value
                
                if date_cell:
                    # Convert date to string format
                    if isinstance(date_cell, datetime):
                        date_str = date_cell.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date_cell)
                    
                    if date_str == today:
                        # Check each column for "Yes" cells with colors
                        for col in range(4, ws.max_column + 1):
                            cell = ws.cell(row=row, column=col)
                            if cell.value == "Yes":
                                cell_color = cell.fill.start_color.rgb
                                if cell_color in self.platform_colors:
                                    platform = self.platform_colors[cell_color]
                                    content_types = self.platform_content_types.get(platform, ['post'])
                                    
                                    for content_type in content_types:
                                        content_items.append({
                                            'brand': brand,
                                            'products': products,
                                            'platform': platform,
                                            'content_type': content_type,
                                            'date': date_str
                                        })
            
            wb.close()
            return content_items
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            return []

    def generate_openai_content(self, brand, products, platform, content_type):
        """Generate caption and Midjourney prompt using OpenAI"""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            # Enhanced prompt for Boujee Balance luxury brand
            prompt = f"""
            Create content for Boujee Balance (BB), a luxury mattress brand specializing in premium mattresses and luxury dog mattresses.
            
            Brand: {brand}
            Products: {products}
            Platform: {platform}
            Content Type: {content_type}
            
            Please provide:
            1. A compelling caption (50-100 words) that emphasizes luxury, comfort, and premium quality
            2. A detailed Midjourney image prompt for generating a high-quality product image
            
            Format the response as JSON with 'caption' and 'midjourney_prompt' fields.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            # Try to parse as JSON, if not, create structured response
            try:
                import json
                return json.loads(content)
            except:
                # If not valid JSON, create structured response
                lines = content.split('\n')
                caption = ""
                midjourney_prompt = ""
                
                for line in lines:
                    if 'caption' in line.lower() or 'caption:' in line:
                        caption = line.split(':', 1)[1].strip() if ':' in line else line
                    elif 'midjourney' in line.lower() or 'prompt' in line.lower():
                        midjourney_prompt = line.split(':', 1)[1].strip() if ':' in line else line
                
                return {
                    'caption': caption or f"Experience luxury comfort with {brand} - Premium {products} for ultimate relaxation",
                    'midjourney_prompt': midjourney_prompt or f"Luxury {products} from {brand}, premium quality, elegant design, professional product photography"
                }
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                'caption': f"Discover the luxury of {brand} - Premium {products} for ultimate comfort and style",
                'midjourney_prompt': f"Professional product photography of luxury {products} from {brand}, elegant design, premium materials, studio lighting"
            }

    def save_prompts_to_json(self, content_items):
        """Save generated prompts to JSON file"""
        prompts = []
        
        for item in content_items:
            content = self.generate_openai_content(
                item['brand'], 
                item['products'], 
                item['platform'], 
                item['content_type']
            )
            
            prompts.append({
                'brand': item['brand'],
                'products': item['products'],
                'platform': item['platform'],
                'content_type': item['content_type'],
                'caption': content['caption'],
                'midjourney_prompt': content['midjourney_prompt']
            })
            
            logger.info(f"Generated content for {item['brand']} - {item['platform']}")
        
        # Save to JSON file
        with open('generated_prompts.json', 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(prompts)} prompts to generated_prompts.json")
        return prompts

    def run_discord_automation(self, prompts):
        """Run hybrid Discord automation for each prompt"""
        for i, prompt_data in enumerate(prompts):
            logger.info(f"Processing prompt {i+1}/{len(prompts)}: {prompt_data['brand']}")
            
            # Call hybrid Discord automation script
            try:
                result = subprocess.run([
                    sys.executable, 
                    'working_hybrid_automation.py',
                    prompt_data['midjourney_prompt']
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Hybrid Discord automation successful for prompt {i+1}")
                else:
                    logger.error(f"Hybrid Discord automation failed for prompt {i+1}: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Error running hybrid Discord automation: {e}")

    def run_automation(self):
        """Main automation workflow"""
        logger.info("Starting content automation...")
        
        # Step 1: Get content from Excel
        content_items = self.get_color_coded_content()
        if not content_items:
            logger.warning("No content found for today")
            return
        
        logger.info(f"Found {len(content_items)} content items for today")
        
        # Step 2: Generate prompts
        prompts = self.save_prompts_to_json(content_items)
        
        # Step 3: Run Discord automation
        self.run_discord_automation(prompts)
        
        logger.info("Automation completed!")

if __name__ == "__main__":
    automation = ContentAutomation()
    automation.run_automation() 