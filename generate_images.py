#!/usr/bin/env python3
"""
Image Generation Script for KidBrowser Landing Page
Uses OpenAI's latest gpt-image-1 model (2025)
"""

import os
import sys
import base64
import requests
from datetime import datetime
from pathlib import Path

# You'll need to install the openai package
# pip install openai requests

try:
    from openai import OpenAI
except ImportError:
    print("Please install the OpenAI package: pip install openai")
    sys.exit(1)

class ImageGenerator:
    def __init__(self, api_key=None):
        """Initialize the image generator with OpenAI API key"""
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("Please provide an API key or set the OPENAI_API_KEY environment variable")
            self.client = OpenAI(api_key=api_key)
    
    def generate_image(self, 
                      prompt, 
                      model="gpt-image-1",
                      size="1024x1024", 
                      quality="high",
                      output_format="png",
                      background="auto",
                      output_compression=100,
                      moderation="auto",
                      save_path="assets/"):
        """
        Generate an image using OpenAI's gpt-image-1 model
        
        Args:
            prompt (str): Description of the image to generate (up to 32,000 characters)
            model (str): Model to use (gpt-image-1, dall-e-3, or dall-e-2)
            size (str): Image size - for gpt-image-1: 1024x1024, 1536x1024, 1024x1536, or auto
            quality (str): Image quality - for gpt-image-1: high, medium, low, or auto
            output_format (str): Output format - png, jpeg, or webp (gpt-image-1 only)
            background (str): Background transparency - transparent, opaque, or auto (gpt-image-1 only)
            output_compression (int): Compression level 0-100% (gpt-image-1 only)
            moderation (str): Content moderation level - low or auto (gpt-image-1 only)
            save_path (str): Directory to save the image
        """
        
        print(f"Generating image with prompt: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}'")
        print(f"Using model: {model}")
        print(f"Settings: {size}, {quality} quality, {output_format} format")
        
        # Prepare request parameters
        request_params = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": 1,  # gpt-image-1 supports 1-10 images
        }
        
        # Add gpt-image-1 specific parameters
        if model == "gpt-image-1":
            request_params.update({
                "output_format": output_format,
                "background": background,
                "output_compression": output_compression,
                "moderation": moderation,
            })
        elif model == "dall-e-3":
            # DALL-E 3 specific parameters
            request_params.update({
                "response_format": "b64_json",  # or "url"
                "style": "vivid"  # or "natural"
            })
        
        try:
            # Make the API request
            response = self.client.images.generate(**request_params)
            
            # Create save directory if it doesn't exist
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"{safe_prompt}_{timestamp}.{output_format}"
            filepath = Path(save_path) / filename
            
            # Handle the response based on model
            if model == "gpt-image-1":
                # gpt-image-1 always returns base64 encoded images
                image_data = response.data[0].b64_json
                if image_data:
                    # Decode and save the image
                    image_bytes = base64.b64decode(image_data)
                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)
                    print(f"✅ Image saved as: {filepath}")
                else:
                    print("❌ No image data received")
                    return None
            else:
                # DALL-E models might return URL or base64
                if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                    # Base64 format
                    image_data = response.data[0].b64_json
                    image_bytes = base64.b64decode(image_data)
                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)
                    print(f"✅ Image saved as: {filepath}")
                elif hasattr(response.data[0], 'url') and response.data[0].url:
                    # URL format - download the image
                    image_url = response.data[0].url
                    img_response = requests.get(image_url)
                    img_response.raise_for_status()
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"✅ Image downloaded and saved as: {filepath}")
            
            # Print usage information if available
            if hasattr(response, 'usage') and response.usage:
                print(f"Token usage: {response.usage}")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None

def generate_kidbrowser_images(api_key):
    """Generate images specifically for the KidBrowser landing page"""
    
    generator = ImageGenerator(api_key)
    
    # Define prompts for KidBrowser imagery
    prompts = [
        {
            "prompt": "A clean, modern icon representing AI-powered content filtering for children. Show a shield with a brain symbol inside, surrounded by gentle, protective elements. Use soft blues and greens. Minimalist style, suitable for a tech website.",
            "filename_prefix": "ai_shield_icon",
            "size": "1024x1024",
            "quality": "high"
        },
        {
            "prompt": "A friendly, cartoon-style illustration of children safely browsing YouTube with a protective AI watching over them. Show kids with happy expressions looking at a screen with safe, educational content. Warm, inviting colors. Family-friendly illustration style.",
            "filename_prefix": "safe_browsing_illustration", 
            "size": "1536x1024",
            "quality": "high"
        },
        {
            "prompt": "A modern, technical icon representing real-time video analysis. Show flowing data streams, video thumbnails being scanned, and checkmarks indicating approval. Clean, professional design with blue and white colors. Suitable for a software interface.",
            "filename_prefix": "video_analysis_icon",
            "size": "1024x1024", 
            "quality": "high"
        },
        {
            "prompt": "A search interface icon showing filtered search results for kids. Display a search bar with child-friendly results appearing, and harmful content being blocked with a gentle red X. Clean, modern UI design with soft colors.",
            "filename_prefix": "search_filter_icon",
            "size": "1024x1024",
            "quality": "medium"
        },
        {
            "prompt": "A family-centric logo design for KidBrowser. Show a stylized browser window with a heart shape and shield combined, representing love and protection. Modern, trustworthy design with gradient blues and soft corners.",
            "filename_prefix": "kidbrowser_logo_concept",
            "size": "1024x1024",
            "quality": "high",
            "background": "transparent"
        }
    ]
    
    print("🎨 Generating images for KidBrowser landing page...")
    print("=" * 60)
    
    successful_generations = []
    
    for i, prompt_config in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Generating: {prompt_config['filename_prefix']}")
        
        filepath = generator.generate_image(
            prompt=prompt_config["prompt"],
            size=prompt_config.get("size", "1024x1024"),
            quality=prompt_config.get("quality", "high"),
            background=prompt_config.get("background", "auto"),
            output_format="png"
        )
        
        if filepath:
            successful_generations.append(filepath)
        
        print("-" * 40)
    
    print(f"\n✅ Successfully generated {len(successful_generations)} images!")
    print("Generated images:")
    for img_path in successful_generations:
        print(f"  📸 {img_path}")
    
    return successful_generations

def main():
    """Main function to run the image generator"""
    print("🎨 KidBrowser Image Generator")
    print("Using OpenAI's gpt-image-1 model (2025)")
    print("=" * 50)
    
    # Get API key
    api_key = input("Please enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    try:
        # Generate images for KidBrowser
        generate_kidbrowser_images(api_key)
        
        print("\n🎉 Image generation complete!")
        print("You can now use these images in your KidBrowser landing page.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 