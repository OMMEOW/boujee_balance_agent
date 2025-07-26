import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_menu():
    """Show the automation choice menu"""
    print("\n" + "="*50)
    print("🤖 BOUJEE BALANCE AUTOMATION SYSTEM")
    print("="*50)
    print("Choose your automation method:")
    print("1. 🚀 Full Midjourney API (Pure Node.js)")
    print("   - Fastest and most reliable")
    print("   - Direct Discord API connection")
    print("   - Real-time image generation")
    print("   - No browser automation needed")
    print()
    print("2. 🔄 Hybrid System (Selenium + API)")
    print("   - More robust with fallback")
    print("   - Works even if API fails")
    print("   - Selenium for login, API for images")
    print("   - Better error handling")
    print()
    print("3. ⚡ Optimized Hybrid System")
    print("   - Fastest and most reliable")
    print("   - Smart login and navigation")
    print("   - Real-time image monitoring")
    print("   - Retry mechanisms and error handling")
    print("   - Optimized performance")
    print()
    print("4. 📊 Run Complete Automation (Excel + Images)")
    print("   - Reads Excel file for today's content")
    print("   - Generates captions and prompts")
    print("   - Creates images for all content")
    print()
    print("5. 🧪 Test Single Prompt")
    print("   - Test with a single prompt")
    print()
    print("0. ❌ Exit")
    print("="*50)

def get_user_choice():
    """Get user's choice"""
    while True:
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Invalid choice. Please enter 0, 1, 2, 3, 4, or 5.")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)

def run_full_api():
    """Run the full Midjourney API automation"""
    print("\n🚀 Running Full Midjourney API...")
    prompt = input("Enter your prompt: ").strip()
    
    if not prompt:
        print("❌ No prompt provided!")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            'full_midjourney_api.py',
            prompt
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Full API automation completed successfully!")
            print(f"Output: {result.stdout}")
        else:
            print("❌ Full API automation failed!")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running full API: {e}")

def run_hybrid():
    """Run the hybrid automation"""
    print("\n🔄 Running Hybrid System...")
    prompt = input("Enter your prompt: ").strip()
    
    if not prompt:
        print("❌ No prompt provided!")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            'simple_hybrid_automation.py',
            prompt
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Hybrid automation completed successfully!")
            print(f"Output: {result.stdout}")
        else:
            print("❌ Hybrid automation failed!")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running hybrid: {e}")

def run_optimized_hybrid():
    """Run the optimized hybrid automation"""
    print("\n⚡ Running Optimized Hybrid System...")
    prompt = input("Enter your prompt: ").strip()
    
    if not prompt:
        print("❌ No prompt provided!")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            'optimized_hybrid_automation.py',
            prompt
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Optimized hybrid automation completed successfully!")
            print(f"Output: {result.stdout}")
        else:
            print("❌ Optimized hybrid automation failed!")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running optimized hybrid: {e}")

def run_complete_automation():
    """Run the complete automation system"""
    print("\n📊 Running Complete Automation...")
    print("This will:")
    print("- Read Excel file for today's content")
    print("- Generate captions and prompts")
    print("- Create images for all content")
    
    confirm = input("\nContinue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            'main_automation.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Complete automation finished successfully!")
            print(f"Output: {result.stdout}")
        else:
            print("❌ Complete automation failed!")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running complete automation: {e}")

def test_single_prompt():
    """Test with a single prompt"""
    print("\n🧪 Testing Single Prompt...")
    print("Choose automation method:")
    print("1. Full API")
    print("2. Hybrid")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == '1':
        run_full_api()
    elif choice == '2':
        run_hybrid()
    else:
        print("❌ Invalid choice!")

def main():
    """Main function"""
    print("🎯 Welcome to Boujee Balance Automation System!")
    
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == '1':
            run_full_api()
        elif choice == '2':
            run_hybrid()
        elif choice == '3':
            run_optimized_hybrid()
        elif choice == '4':
            run_complete_automation()
        elif choice == '5':
            test_single_prompt()
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 