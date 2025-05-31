#!/usr/bin/env python3
"""
Generate a modern KidBrowser logo using OpenAI's gpt-image-1 model.
This script creates a family-friendly logo with the new color scheme.
"""

import openai
import requests
import os
from datetime import datetime

# Set up OpenAI client (requires OPENAI_API_KEY environment variable)
client = openai.OpenAI()

def generate_logo():
    """Generate a modern KidBrowser logo with the new color scheme."""
    
    # Logo prompt for KidBrowser with the new color scheme
    logo_prompt = """
    Design a modern, clean logo for "KidBrowser" - a safe YouTube browser for children.

    Style Requirements:
    - Modern, minimal design with rounded corners and soft edges
    - Professional yet family-friendly aesthetic
    - Clean typography with the brand name "KidBrowser"
    - Primary color: Light red (#ef4444) with subtle gradients to darker red (#dc2626)
    - White background or transparent background
    - Simple, memorable icon that represents both browsing/technology and child safety
    - Should work well at small sizes (40x40px) and large sizes
    - Avoid overly cartoonish elements - aim for a trustworthy, modern tech company feel
    - Color palette similar to Notion's soft, muted red tones

    Icon Concepts (choose one):
    - A browser window with a shield overlay
    - A stylized "K" or "KB" monogram with protective elements
    - A simplified browser tab with child-safe elements
    - A clean compass or navigation symbol representing safe browsing

    The logo should convey:
    - Trust and safety for parents
    - Modern technology and reliability
    - Child-friendly without being too playful
    - Professional software company quality

    Format: Square logo that can be used as a favicon and header logo.
    Style: Modern SaaS company aesthetic, similar to Notion, Linear, or Figma branding with soft, muted colors.
    """

    try:
        print("🎨 Generating KidBrowser logo...")
        
        response = client.images.generate(
            model="gpt-image-1",
            prompt=logo_prompt,
            size="1024x1024",
            quality="hd",
            style="natural",
            n=1
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Create assets directory if it doesn't exist
            os.makedirs("assets", exist_ok=True)
            
            # Save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"assets/kidbrowser_logo_{timestamp}.png"
            
            with open(filename, "wb") as f:
                f.write(image_response.content)
            
            print(f"✅ Logo saved as: {filename}")
            
            # Also save as the main logo file
            main_logo_path = "assets/kidbrowser_logo.png"
            with open(main_logo_path, "wb") as f:
                f.write(image_response.content)
            
            print(f"✅ Main logo saved as: {main_logo_path}")
            return main_logo_path
            
        else:
            print(f"❌ Failed to download image: HTTP {image_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating logo: {e}")
        return None

def main():
    """Main function to generate the KidBrowser logo."""
    print("🚀 KidBrowser Logo Generator")
    print("=" * 40)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set the OPENAI_API_KEY environment variable")
        return
    
    # Generate the logo
    logo_path = generate_logo()
    
    if logo_path:
        print("\n🎉 Logo generation complete!")
        print(f"📁 Logo saved to: {logo_path}")
        print("\n📝 Next steps:")
        print("1. Review the generated logo")
        print("2. Update HTML files to use the new logo")
        print("3. Consider generating additional sizes if needed")
    else:
        print("\n❌ Logo generation failed. Please check your API key and try again.")

if __name__ == "__main__":
    main() 