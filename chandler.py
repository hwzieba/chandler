import tkinter as tk
from tkinter import filedialog, messagebox
from bing_image_downloader import downloader
from PIL import Image, ImageTk
import os

# Initialize the Tkinter GUI application
class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector")
        self.current_term = None
        self.terms = []
        self.current_images = []
        self.current_thumbnails = []
        
        # Setting up the frame
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        # Button to open a text file with terms
        self.open_file_button = tk.Button(self.frame, text="Select Text File", command=self.load_file)
        self.open_file_button.pack(pady=10)

        # Label to display current term
        self.term_label = tk.Label(self.frame, text="", font=("Arial", 14))
        self.term_label.pack(pady=5)

        # Canvas for displaying thumbnails
        self.canvas = tk.Canvas(self.frame, width=500, height=500)
        self.canvas.pack()
        
        # Container for image buttons
        self.image_buttons_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_buttons_frame, anchor="nw")
        
        # Save location for downloaded images
        self.save_dir = "selected_images"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def load_file(self):
        """Load a text file containing terms."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                self.terms = [line.strip() for line in f if line.strip()]
            if self.terms:
                self.next_term()
            else:
                messagebox.showinfo("No Terms", "The selected file is empty.")
    
    def next_term(self):
        """Load the next term and display images."""
        if self.terms:
            self.current_term = self.terms.pop(0)
            self.term_label.config(text=f"Select an image for: {self.current_term}")
            self.display_images()
        else:
            messagebox.showinfo("Complete", "All terms have been processed.")
    
    def display_images(self):
        """Fetch and display images for the current term."""
        for widget in self.image_buttons_frame.winfo_children():
            widget.destroy()
        self.current_images = []
        self.current_thumbnails = []

        # Download images for the term
        downloader.download(self.current_term, limit=15, output_dir='.', adult_filter_off=True, force_replace=False, timeout=10, filter="clipart")
        
        # Load and display thumbnails
        for idx, filename in enumerate(os.listdir(os.path.join(".", self.current_term))):
            img_path = os.path.join(self.current_term, filename)
            image = Image.open(img_path).resize((100, 100))
            thumbnail = ImageTk.PhotoImage(image)
            button = tk.Button(self.image_buttons_frame, image=thumbnail, command=lambda path=img_path: self.select_image(path))
            button.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)
            self.current_thumbnails.append(thumbnail)
            self.current_images.append(img_path)
        
    def select_image(self, img_path):
        """Save the selected image and proceed to the next term."""
        dest_path = os.path.join(self.save_dir, f"{self.current_term}.jpg")
        os.rename(img_path, dest_path)
        for filename in self.current_images:
            if filename != img_path and os.path.exists(filename):  # Skip the renamed file
               os.remove(filename)
        os.rmdir(self.current_term)
        self.next_term()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()
