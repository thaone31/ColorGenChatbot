import gradio as gr
from PIL import Image
import random
from io import BytesIO

# Function to enhance contrast of the image (placeholder for future enhancement)
def enhance_contrast(img):
    return img  # Currently, just returns the original image

# Function to detect dominant colors
def get_dominant_colors(image, n_colors=6):
    image = image.resize((150, 150))  # Resize for faster processing
    result = image.convert('P', palette=Image.ADAPTIVE, colors=n_colors)
    result = result.convert('RGB')
    colors = result.getcolors(150 * 150)
    colors = sorted(colors, reverse=True, key=lambda x: x[0])[:n_colors]
    return [color[1] for color in colors]

# Function to convert RGB to HEX
def rgb_to_hex(color):
    return '#%02x%02x%02x' % color

# Function to generate color harmonies
def generate_harmonies(colors):
    harmonies = {}
    for color in colors:
        r, g, b = color
        comp_color = (255 - r, 255 - g, 255 - b)  # complementary color
        analogous1 = ((r + 30) % 255, (g + 30) % 255, (b + 30) % 255)
        analogous2 = ((r - 30) % 255, (g - 30) % 255, (b - 30) % 255)
        harmonies[rgb_to_hex(color)] = {
            'complementary': rgb_to_hex(comp_color),
            'analogous': (rgb_to_hex(analogous1), rgb_to_hex(analogous2))
        }
    return harmonies

# Function to create a LinkedIn-friendly color palette description
def create_palette_description(colors):
    descriptions = [
        "A vibrant palette for branding and marketing.",
        "A calming and trustworthy color scheme for professional use.",
        "Bold and energetic colors, perfect for grabbing attention.",
        "Soft and neutral tones, ideal for elegant branding."
    ]
    chosen_description = random.choice(descriptions)
    palette_html = f"<h4>{chosen_description}</h4><div style='display:flex; flex-wrap:wrap;'>"
    for color in colors:
        hex_color = rgb_to_hex(color)
        palette_html += f"<div style='width: 100px; height: 50px; background-color: {hex_color}; margin: 5px;'></div>"
        palette_html += f"<div style='padding: 15px;'>HEX: {hex_color}</div>"
    palette_html += "</div>"
    return palette_html

# Function to generate a downloadable palette image
def generate_palette_image(colors):
    img_width = 500
    img_height = 100
    palette_img = Image.new('RGB', (img_width, img_height))
    
    color_width = img_width // len(colors)
    for i, color in enumerate(colors):
        img = Image.new('RGB', (color_width, img_height), color)
        palette_img.paste(img, (i * color_width, 0))
    
    return palette_img  # Return the PIL image directly

# Function to generate the CSS code for the color palette
def generate_css_code(colors):
    css_code = "/* Color Palette CSS */\n"
    for i, color in enumerate(colors):
        hex_color = rgb_to_hex(color)
        css_code += f".color-{i} {{ background-color: {hex_color}; }}\n"
    return css_code

# Main function to generate palette and display LinkedIn-friendly results
def generate_palette(image_path):
    img = Image.open(image_path)

    # Enhance the contrast (optional placeholder)
    img = enhance_contrast(img)

    # Extract dominant colors
    n_colors = 6
    colors = get_dominant_colors(img, n_colors)

    # Convert colors to HEX and create palette description
    palette_html = create_palette_description(colors)

    # Generate palette image for download
    palette_img = generate_palette_image(colors)

    # Generate CSS code for the palette
    css_code = generate_css_code(colors)

    return palette_html, palette_img, css_code

# Gradio Interface
def gradio_interface(image_path):
    palette_html, palette_img, css_code = generate_palette(image_path)

    return palette_html, palette_img, css_code

# Create the Gradio interface
with gr.Blocks() as interface:
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath", label="Upload Image")  # Image Upload
            submit_btn = gr.Button("Submit", elem_id="submit_btn")
            clear_btn = gr.Button("Clear", elem_id="clear_btn")
        
        with gr.Column():
            palette_output = gr.HTML(label="Generated Color Palette")
            palette_image_output = gr.Image(label="Downloadable Palette Image", type="pil")  # Output PIL image
            css_code_output = gr.Textbox(label="Generated CSS Code", lines=6)  # Use Textbox to display CSS code
    
    submit_btn.click(gradio_interface, inputs=[image_input], outputs=[
        palette_output, palette_image_output, css_code_output])

    # The Clear button now resets the image input and clears all outputs
    clear_btn.click(lambda: [None, None, None, None], inputs=[], outputs=[
        image_input, palette_output, palette_image_output, css_code_output])

# Launch the interface
interface.launch()