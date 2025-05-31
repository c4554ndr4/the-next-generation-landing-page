#!/usr/bin/env python3
import os
from generate_images import ImageGenerator

# Use the environment variable
generator = ImageGenerator()

print('🎨 Generating KidBrowser images with DALL-E 3 (fallback until org verified)...')

# Generate a modern logo
print('1/3 Generating logo...')
logo_path = generator.generate_image(
    prompt='A modern, friendly logo for KidBrowser. Clean typography with "KidBrowser" text and a shield-like icon incorporating a play button and protective elements. Blue and white color scheme. Professional but approachable design.',
    model='dall-e-3',
    size='1024x1024',
    quality='hd'
)

# Generate an AI filtering icon  
print('2/3 Generating AI icon...')
ai_icon_path = generator.generate_image(
    prompt='A clean, modern icon representing AI-powered content filtering for children. Show a shield with a brain/AI chip symbol inside, surrounded by gentle protective elements. Soft blue and green colors. Minimalist style suitable for a tech website interface.',
    model='dall-e-3',
    size='1024x1024', 
    quality='hd'
)

# Generate a hero illustration
print('3/3 Generating hero illustration...')
hero_path = generator.generate_image(
    prompt='A warm, family-friendly illustration showing children safely browsing on a computer with protective AI elements around them. Kids with happy expressions, educational content on screen, gentle shield/safety icons floating around. Bright, optimistic colors with blue and green theme.',
    model='dall-e-3',
    size='1792x1024',
    quality='hd'
)

print(f'✅ Generated 3 images successfully!')
print('Images saved in assets/ directory')
print('')
print('Note: Using DALL-E 3 as fallback. Switch back to gpt-image-1 after organization verification.') 