import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import sys
import os
import argparse
import win32clipboard
from io import BytesIO
import webbrowser


class ImageEditor:
    def __init__(self, master):

        self.master = master
        master.title("SimpleViewer")

        self.file_list = []
        self.current_file_index = None

        master.bind("<Left>", self.load_previous_image)
        master.bind("<Right>", self.load_next_image)

        # Set the focus to the master window
        master.focus_set()

        self.button_frame = tk.Frame(master, bg='white') # Change this line
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.open_button = tk.Button(self.button_frame, text="Open", command=self.open_image)
        self.open_button.pack(side=tk.LEFT)

        self.flip_button = tk.Button(self.button_frame, text="Mirror", command=self.flip_image)
        self.flip_button.pack(side=tk.LEFT)

        self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=self.rotate_image)
        self.rotate_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save as", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        self.contact_button = tk.Button(self.button_frame, text="about", command=self.show_contact_info)
        self.contact_button.pack(side=tk.LEFT)

        self.filename_label = tk.Label(self.button_frame, text="")
        self.filename_label.pack(side=tk.RIGHT)

        self.status_bar = tk.Frame(master)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.pixel_label = tk.Label(self.status_bar, text="")
        self.pixel_label.pack(side=tk.LEFT)
        
        self.filename_label = tk.Label(self.status_bar, text="")
        self.filename_label.pack(side=tk.RIGHT)

        self.canvas_frame = tk.Frame(master, bg='green')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg='grey')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.original_image = None
        self.photo = None

        self.canvas.bind("<MouseWheel>", self.zoom_image)
        self.canvas.bind("<Button-3>", self.show_context_menu) # Change this line

        # Make the window not resizable
        master.resizable(False, False)

        # Check if a command line argument was provided
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            self.original_image = Image.open(file_path)
            self.image = self.original_image.copy()
            self.update_image()

        # Check if a command line argument was provided
        if len(sys.argv) > 1:
            self.open_image(sys.argv[1])
    
    def copy_to_clipboard(self):
        if self.image:
            output = BytesIO()
            self.image.save(output, format='BMP')
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

    def show_context_menu(self, event):
        context_menu = tk.Menu(self.master, tearoff=0)
        context_menu.add_command(label="Copy to Clipboard", command=self.copy_to_clipboard)
        context_menu.tk_popup(event.x_root, event.y_root)

    def load_previous_image(self, event=None):
        print("load_previous_image was called")
        print(f"file_list length: {len(self.file_list)}, current_file_index: {self.current_file_index}")
        if self.file_list:
            self.current_file_index = (self.current_file_index - 1) % len(self.file_list)
            self.open_image(self.file_list[self.current_file_index])
            self.filename_label.config(text=os.path.basename(self.file_list[self.current_file_index]))
            if self.original_image is not None:
                width, height = self.original_image.size
                half_width, half_height = width // 2, height // 2
                self.pixel_label.config(text=f"Pixels: {(half_width, half_height)}")

    def load_next_image(self, event=None):
        print("load_next_image was called")
        print(f"file_list length: {len(self.file_list)}, current_file_index: {self.current_file_index}")
        if self.file_list:
            self.current_file_index = (self.current_file_index + 1) % len(self.file_list)
            self.open_image(self.file_list[self.current_file_index])
            self.filename_label.config(text=os.path.basename(self.file_list[self.current_file_index]))
            if self.original_image is not None:
                width, height = self.original_image.size
                half_width, half_height = width // 2, height // 2
                self.pixel_label.config(text=f"Pixels: {(half_width, half_height)}")


    def open_link(self, event):
        webbrowser.open_new(r"https://github.com/duke0815/SimpleViewer")

    def open_email(self, event):
        webbrowser.open_new(r"mailto:kasser88@outlook.com")

    def show_contact_info(self):
        contact_info = "March 2024 v0.2\n\nI appreciate your feedback!"
        email_link = "kasser88@outlook.com"
        additional_text = "\nVisit the following link for updates:"
        github_link = "https://github.com/duke0815/SimpleViewer"
        popup = tk.Toplevel(self.master)
        popup.resizable(False, False)  # Make the window not resizable
        popup.title("Contact Info:")
        popup.geometry("300x170")  # Set the size of the window
        label = tk.Label(popup, text=contact_info)
        label.pack(padx=10, pady=10)
        email = tk.Label(popup, text=email_link, fg="blue", cursor="hand2")
        email.pack()
        email.bind("<Button-1>", self.open_email)
        additional_label = tk.Label(popup, text=additional_text)
        additional_label.pack()
        link = tk.Label(popup, text=github_link, fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", self.open_link)

    def open_image(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename()
            self.filename_label.config(text=os.path.basename(file_path))
            if self.original_image is not None:
                width, height = self.original_image.size
                half_width, half_height = width // 2, height // 2
                self.pixel_label.config(text=f"Pixels: {(half_width, half_height)}")

        if file_path:
            print(f"file_path: {file_path}")
            self.original_image = Image.open(file_path)
            
            # Get the current size
            width, height = self.original_image.size
            
            # Halve the size
            new_size = (width * 2, height * 2)
            
            # Resize the image
            self.original_image = self.original_image.resize(new_size)
            
            self.image = self.original_image.copy()
            self.update_image()

            # Get the list of files in the same directory
            directory = os.path.dirname(file_path)
            print(f"directory: {directory}")
            
            # Update how we create file_list to match the file_path format
            self.file_list = sorted(os.path.join(directory, f).replace('\\', '/') for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')))
            print(f"file_list: {self.file_list}")

            # Replace backslashes with slashes in the file path
            file_path = file_path.replace('\\', '/')

            self.current_file_index = self.file_list.index(file_path)

    def flip_image(self):
        if self.original_image:
            # Save the current size of the image
            current_size = self.image.size

            # Flip the image
            self.original_image = self.original_image.transpose(Image.FLIP_LEFT_RIGHT)

            # Resize the flipped image to the current size
            self.image = self.original_image.resize(current_size)

            # Update the photo and the canvas
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def zoom_image(self, event):
        if self.original_image:  # Change this line
            # Calculate the new size of the image
            x = self.image.width + (1 if event.delta > 0 else -1) * 100
            y = self.image.height + (1 if event.delta > 0 else -1) * 100

            # Calculate the aspect ratio of the image
            image_ratio = self.original_image.width / self.original_image.height  # Change this line

            # Calculate the new width and height while maintaining the aspect ratio
            if image_ratio > 1:
                new_width = min(max(x, 500), self.master.winfo_screenwidth())
                new_height = int(new_width / image_ratio)
            else:
                new_height = min(max(y, 500), self.master.winfo_screenheight())
                new_width = int(new_height * image_ratio)

            # Resize the image
            self.image = self.original_image.resize((new_width, new_height))  # Change this line

            # Update the photo and the canvas
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

            # Set the size of the window to match the image
            self.master.geometry(f"{new_width+2}x{new_height+28}")

    def save_image(self):
        if self.original_image:  # Change this line
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.original_image.save(file_path, 'PNG')  # Change this line


    def rotate_image(self):
        if self.original_image:
            # Expand the image before rotating
            self.original_image = self.original_image.rotate(-90, expand=True)

            # Get the aspect ratio of the image
            image_ratio = self.original_image.width / self.original_image.height

            # Calculate the new size of the image
            if image_ratio > 1:
                new_width = 400
                new_height = int(400 / image_ratio)
            else:
                new_height = 600
                new_width = int(600 * image_ratio)

            # Resize the image
            self.image = self.original_image.resize((new_width, new_height))

            # Update the photo
            self.photo = ImageTk.PhotoImage(self.image)

            # Update the canvas size and image
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

            # Call zoom_image function
            class Event:
                delta = 1
            self.zoom_image(Event())

    def update_image(self):
        if self.original_image:  # Change this line
            # Get the aspect ratio of the image
            image_ratio = self.original_image.width / self.original_image.height  # Change this line

            # Calculate the new size of the image
            if image_ratio > 1:
                new_width = 400
                new_height = int(400 / image_ratio)
            else:
                new_height = 600
                new_width = int(600 * image_ratio)

            # Resize the image
            self.image = self.original_image.resize((new_width-2, new_height-28))  # Change this line

            # Create the PhotoImage and add it to the canvas
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Set the size of the window to match the image
            self.master.geometry(f"{new_width}x{new_height}")

root = tk.Tk()
my_gui = ImageEditor(root)
root.mainloop()