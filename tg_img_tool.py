import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def adjust_image_size(directory):
    # Erstellt einen neuen Unterordner im ausgewählten Ordner mit dem Namen DAM_Tagesdatum
    today = datetime.today().strftime('%Y-%m-%d')
    output_directory = os.path.join(directory, f"DAM_{today}")
    os.makedirs(output_directory, exist_ok=True)
    
    processed_files = 0
    for file in os.listdir(directory):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp', '.svg')):
            image_path = os.path.join(directory, file)
            output_path = os.path.join(output_directory, file)
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    new_size = max(width, height, 800)
                    new_img = Image.new("RGB", (new_size, new_size), "white")
                    new_img.paste(img, ((new_size - width) // 2, (new_size - height) // 2))
                    new_img.save(output_path, "JPEG", quality=100, subsampling=0)
                processed_files += 1
            except Exception as e:
                messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")
    messagebox.showinfo("Erledigt", f"{processed_files} Bilder wurden erfolgreich im Ordner '{output_directory}' gespeichert.")

def load_image_info(directory):
    global selected_directory
    selected_directory = directory
    image_info = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp', '.svg')):
            image_path = os.path.join(directory, file)
            with Image.open(image_path) as img:
                width, height = img.size
                image_info.append((file, width, height))
    return image_info

def main_window():
    def load_images():
        global selected_directory
        directory = filedialog.askdirectory()
        if directory:
            selected_directory = directory
            image_info = load_image_info(directory)
            update_image_list(image_info)

    def start_processing():
        global selected_directory
        if selected_directory:
            adjust_image_size(selected_directory)
        else:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst einen Quellordner aus.")

    window = tk.Tk()
    window.title("IMG-Resizer | Powered by KostjaX®")
    window.geometry("415x400")
    window.configure(bg='brown3')

    logo_path = resource_path("logo_tgx.png")
    logo = Image.open(logo_path)
    logo_width, logo_height = 300, int(300 * (logo.height / logo.width))
    logo = logo.resize((logo_width, logo_height))
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(window, image=logo_img, bg='lightblue')
    logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    load_button = tk.Button(window, text="Quellordner & Auflistung", command=load_images)
    load_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    start_button = tk.Button(window, text="Start", command=start_processing)
    start_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    image_frame = tk.Frame(window, bg='lightblue')
    image_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    columns = ('file_name', 'dimensions', 'rating')
    image_tree = ttk.Treeview(image_frame, columns=columns, show='headings')
    image_tree.heading('file_name', text='Bildbezeichnung')
    image_tree.heading('dimensions', text='Abmessungen')
    image_tree.heading('rating', text='Bewertung')
    image_tree.column('file_name', width=200)
    image_tree.column('dimensions', width=100)
    image_tree.column('rating', width=80)
    image_tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(image_frame, orient="vertical", command=image_tree.yview)
    image_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def update_image_list(image_info):
        image_tree.delete(*image_tree.get_children())
        for image_name, width, height in image_info:
            rating = "OK" if width >= 800 and height >= 800 else "Zu klein"
            tag = 'ok' if rating == "OK" else 'small'
            image_tree.insert('', tk.END, values=(image_name, f"{width}x{height}", rating), tags=(tag,))
            image_tree.tag_configure('ok', foreground='green')
            image_tree.tag_configure('small', foreground='red')

    window.mainloop()

if __name__ == "__main__":
    main_window()
