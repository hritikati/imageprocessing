import cv2
import numpy as np
import easygui
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, Toplevel, StringVar, OptionMenu
import sys

root = tk.Tk()
root.geometry('700x700')
root.title('Photo Effect Converter')
root.configure(background='light green')

# ========== EFFECT FUNCTIONS ==========

def oil_painting_effect(image):
    return cv2.xphoto.oilPainting(image, 7, 1)

def ghibli_art_style(image):
    return cv2.bilateralFilter(image, 9, 300, 300)

def watercolor_effect(image):
    smooth = cv2.bilateralFilter(image, 9, 300, 300)
    gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
    watercolor = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    watercolor = cv2.convertScaleAbs(watercolor, alpha=1.2, beta=30)
    return watercolor

def manga_style(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    manga = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    manga = cv2.bitwise_not(manga)
    return cv2.cvtColor(manga, cv2.COLOR_GRAY2BGR)

def lomo_effect(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def sepia_effect(image):
    sepia_kernel = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    sepia = cv2.transform(image, sepia_kernel)
    return cv2.convertScaleAbs(sepia)

def negative_effect(image):
    return cv2.bitwise_not(image)

def pencil_sketch_effect(image):
    _, sketch_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return cv2.cvtColor(sketch_color, cv2.COLOR_BGR2RGB)

def anime_style(image):
    img_resized = cv2.resize(image, (640, 480))
    img_cartoon = cv2.bilateralFilter(img_resized, 9, 300, 300)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    cartoon_image = cv2.bitwise_and(img_cartoon, img_cartoon, mask=edges)
    return cartoon_image

def retro_comic_effect(image):
    img_resized = cv2.resize(image, (640, 480))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    return cv2.cvtColor(img_invert, cv2.COLOR_GRAY2BGR)

def color_pencil_sketch(image):
    _, color_sketch = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return cv2.cvtColor(color_sketch, cv2.COLOR_BGR2RGB)

def pop_art_effect(image):
    img_resized = cv2.resize(image, (640, 480))
    img_sepia = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_sepia = cv2.convertScaleAbs(img_sepia, alpha=1.2, beta=30)
    return img_sepia

def vivid_effect(image):
    return cv2.convertScaleAbs(image, alpha=2.0, beta=50)

def vintage_film_effect(image):
    sepia = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sepia = cv2.convertScaleAbs(sepia, alpha=1.2, beta=30)
    return sepia

# ========== EFFECTS DICTIONARY ==========

effects = {
    "Oil Painting": oil_painting_effect,
    "Ghibli Art": ghibli_art_style,
    "Watercolor": watercolor_effect,
    "Manga": manga_style,
    "Lomo": lomo_effect,
    "Sepia": sepia_effect,
    "Negative": negative_effect,
    "Pencil Sketch": pencil_sketch_effect,
    "Anime Style": anime_style,
    "Retro Comic": retro_comic_effect,
    "Color Pencil Sketch": color_pencil_sketch,
    "Pop Art": pop_art_effect,
    "Vivid": vivid_effect,
    "Vintage Film": vintage_film_effect
}

# ========== CAPTION GENERATOR ==========
def generate_caption(effect_name):
    base_caption = f"This image has been enhanced with the {effect_name} effect."
    if "Sketch" in effect_name:
        return base_caption + " It now looks like a hand-drawn artwork."
    elif "Cartoon" in effect_name or "Anime" in effect_name:
        return base_caption + " It has a smooth, animated style."
    elif "Sepia" in effect_name or "Vintage" in effect_name:
        return base_caption + " It carries a warm, nostalgic tone."
    elif "Negative" in effect_name:
        return base_caption + " The colors have been inverted for a unique view."
    elif "Watercolor" in effect_name:
        return base_caption + " It resembles a painting with flowing colors."
    elif "Manga" in effect_name:
        return base_caption + " A high contrast, comic-book inspired style."
    else:
        return base_caption + " A unique artistic transformation has been applied."

# ========== MAIN FUNCTION ==========

def choose_and_convert():
    image_path = easygui.fileopenbox()
    if not image_path:
        return

    original = cv2.imread(image_path)
    if original is None:
        messagebox.showerror("Error", "Could not open the image.")
        return

    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    # Effect selection popup
    effect_window = Toplevel(root)
    effect_window.title("Select Effect")
    effect_window.geometry("300x200")
    effect_window.configure(bg="light yellow")

    tk.Label(effect_window, text="Choose an effect:", font=("Arial", 14), bg="light yellow").pack(pady=10)

    selected_effect = StringVar(effect_window)
    selected_effect.set("Oil Painting")

    effect_menu = OptionMenu(effect_window, selected_effect, *effects.keys())
    effect_menu.config(font=("Arial", 12))
    effect_menu.pack(pady=10)

    def apply_effect():
        effect_name = selected_effect.get()
        result = effects[effect_name](original)
        result_resized = cv2.resize(result, (930, 510))
        caption = generate_caption(effect_name)

        fig, ax = plt.subplots()
        ax.imshow(result_resized)
        ax.set_title(f"{effect_name} Effect", fontsize=16)
        ax.axis('off')

        fig.subplots_adjust(bottom=0.2)  # add padding at the bottom
        fig.text(0.5, 0.1, caption, wrap=True, ha='center', fontsize=12, color='darkblue')


        def show_comparison(event):
            original_resized = cv2.resize(original, (930, 510))
            fig2, axs = plt.subplots(1, 2, figsize=(12, 6))
            axs[0].imshow(original_resized)
            axs[0].set_title("Original Image")
            axs[0].axis('off')

            axs[1].imshow(result_resized)
            axs[1].set_title(f"{effect_name} Effect")
            axs[1].axis('off')
            plt.tight_layout()
            plt.show()

        def copy_caption(event):
            root.clipboard_clear()
            root.clipboard_append(caption)
            messagebox.showinfo("Copied", "Caption copied to clipboard.")

        # Buttons
        button_ax = plt.axes([0.3, 0.01, 0.4, 0.05])
        btn = plt.Button(button_ax, 'Show Original vs Converted', color='lightblue', hovercolor='lightgray')
        btn.on_clicked(show_comparison)

        copy_ax = plt.axes([0.7, 0.91, 0.25, 0.05])
        copy_btn = plt.Button(copy_ax, 'Copy Caption', color='lightgreen', hovercolor='lightgray')
        copy_btn.on_clicked(copy_caption)

        plt.show()
        effect_window.destroy()

    tk.Button(effect_window, text="Apply Effect", command=apply_effect,
              font=("Arial", 12, "bold"), bg="black", fg="white").pack(pady=20)

# Button to start the process
tk.Button(root, text="Choose Image & Apply Effect", command=choose_and_convert,
          padx=15, pady=10, bg="black", fg="white", font=("arial", 30, "bold")).pack(side=tk.TOP, pady=100)

root.mainloop()
