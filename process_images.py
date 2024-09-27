import os
from tkinter import Tk, Canvas, Button, filedialog, HORIZONTAL, Scale, Label, Checkbutton, IntVar, messagebox, ttk, Frame, Scrollbar, VERTICAL, BOTH, NW
from PIL import Image, ImageTk, ImageDraw

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper and Processor")

        # Create a frame that will contain the canvas and scrollbar
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=1)

        # Create a canvas for scrollable content
        self.canvas = Canvas(main_frame)
        self.canvas.pack(side="left", fill=BOTH, expand=1)

        # Add a scrollbar to the canvas
        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the canvas (for scrollable content)
        self.scrollable_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Create tab control for personal and group photos
        self.tab_control = ttk.Notebook(self.scrollable_frame)
        self.personal_tab = ttk.Frame(self.tab_control)
        self.group_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.personal_tab, text='Personal Photos')
        self.tab_control.add(self.group_tab, text='Group Photos')

        self.tab_control.grid(row=0, column=0, columnspan=3)

        # Setup for personal photos
        self.setup_personal_tab()

        # Setup for group photos
        self.setup_group_tab()

    def setup_personal_tab(self):
        """Setup the interface for personal photos."""
        # Output image size
        self.output_width = 400
        self.output_height = 265

        # Display canvas size
        self.canvas_width = 400
        self.canvas_height = 265

        # Variables for image manipulation
        self.scale_factor = 1.0
        self.image = None
        self.img_tk = None
        self.image_id = None
        self.img_x = 0
        self.img_y = 0

        # Canvas for displaying the image
        self.canvas_personal = Canvas(self.personal_tab, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas_personal.grid(row=0, column=0, columnspan=4)

        # Load and save buttons
        Button(self.personal_tab, text="Load Image", command=self.load_image).grid(row=1, column=0)
        Button(self.personal_tab, text="Save Image", command=self.process_image).grid(row=1, column=3)

        # Slider for resizing the image (zoom in/out)
        Label(self.personal_tab, text="Resize Image").grid(row=2, column=0)
        Button(self.personal_tab, text="–", command=lambda: self.update_slider(-0.05)).grid(row=2, column=1)
        self.scale = Scale(self.personal_tab, from_=0.05, to=2.0, resolution=0.05, orient=HORIZONTAL, command=self.update_scale)
        self.scale.set(self.scale_factor)
        self.scale.grid(row=2, column=2)
        Button(self.personal_tab, text="+", command=lambda: self.update_slider(0.05)).grid(row=2, column=3)

        # Metadata and Round Corners options (checked by default)
        self.metadata_var = IntVar(value=1)
        self.round_var = IntVar(value=1)
        Checkbutton(self.personal_tab, text="Remove Metadata", variable=self.metadata_var).grid(row=3, column=0, pady=5)
        Checkbutton(self.personal_tab, text="Round Corners", variable=self.round_var).grid(row=3, column=3, pady=5)

        # Bind the dragging events
        self.canvas_personal.bind("<ButtonPress-1>", self.start_drag)
        self.canvas_personal.bind("<B1-Motion>", self.drag_image)

    def setup_group_tab(self):
        """Setup the interface for group photos."""
        # Output image size
        self.output_width_group = 1280
        self.output_height_group = 960

        # Display canvas size
        self.canvas_width_group = 640
        self.canvas_height_group = 480

        # Variables for image manipulation
        self.scale_factor_group = 1.0
        self.group_image = None
        self.group_img_tk = None
        self.group_image_id = None
        self.img_x_group = 0
        self.img_y_group = 0

        # Canvas for displaying the group image
        self.group_canvas = Canvas(self.group_tab, width=self.canvas_width_group, height=self.canvas_height_group, bg="white", highlightthickness=2, highlightbackground="black")
        self.group_canvas.grid(row=0, column=0, columnspan=4)

        # Load and save buttons
        Button(self.group_tab, text="Load Image", command=self.load_group_image).grid(row=1, column=0)
        Button(self.group_tab, text="Save Image", command=self.process_group_image).grid(row=1, column=3)

        # Slider for resizing the image (zoom in/out)
        Label(self.group_tab, text="Resize Image").grid(row=2, column=0)
        Button(self.group_tab, text="–", command=lambda: self.update_group_slider(-0.05)).grid(row=2, column=1)
        self.group_scale = Scale(self.group_tab, from_=0.05, to=2.0, resolution=0.05, orient=HORIZONTAL, command=self.update_group_scale)
        self.group_scale.set(self.scale_factor_group)
        self.group_scale.grid(row=2, column=2)
        Button(self.group_tab, text="+", command=lambda: self.update_group_slider(0.05)).grid(row=2, column=3)

        # Metadata and Round Corners options (checked by default)
        self.metadata_var_group = IntVar(value=1)
        self.round_var_group = IntVar(value=1)
        Checkbutton(self.group_tab, text="Remove Metadata", variable=self.metadata_var_group).grid(row=3, column=0, pady=5)
        Checkbutton(self.group_tab, text="Round Corners", variable=self.round_var_group).grid(row=3, column=3, pady=5)

        # Bind the dragging events for group photos
        self.group_canvas.bind("<ButtonPress-1>", self.start_group_drag)
        self.group_canvas.bind("<B1-Motion>", self.drag_group_image)

    def load_image(self):
        """Load a personal image from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if not file_path:
            return
        self.image = Image.open(file_path).convert("RGB")  # Ensure RGB mode
        self.image_original = self.image.copy()  # Keep a copy of the original image

        # Extract the filename (without extension) from the file path
        self.image_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Reset scaling and position
        self.img_x = 0
        self.img_y = 0

        # Adjust the scale factor to fit the height of the image to the canvas height
        image_height = self.image.height
        self.scale_factor = min(self.canvas_height / image_height, 2.0)  # Constrain to max scale factor
        self.scale.set(self.scale_factor)  # Update the slider value

        self.update_image()

    def process_group_image(self):
        """Process and save the group image with correct DPI."""
        if not self.group_image:
            messagebox.showerror("Error", "No group image loaded!")
            return

        # Use the original image to prevent cumulative resizing
        original_image = self.group_image_original.copy()

        # If scaling is applied, resize the original image accordingly
        if self.scale_factor_group != 1.0:
            img_width = int(original_image.width * self.scale_factor_group)
            img_height = int(original_image.height * self.scale_factor_group)
            resized_img = original_image.resize((img_width, img_height), Image.LANCZOS)
        else:
            resized_img = original_image

        # Create a blank output image
        output_image = Image.new("RGB", (self.output_width_group, self.output_height_group), "white")

        # Paste the resized image onto the output image at the calculated position
        output_image.paste(resized_img, (int(self.img_x_group), int(self.img_y_group)))

        if self.metadata_var_group.get():
            output_image = self.remove_metadata(output_image)

        if self.round_var_group.get():
            output_image = self.round_corners(output_image, radius=100)

        # Pre-fill the save dialog with the original filename and ".webp" extension
        default_filename = f"{self.group_image_filename}.webp"
        save_path = filedialog.asksaveasfilename(defaultextension=".webp", initialfile=default_filename, filetypes=[("WEBP", "*.webp")])

        if save_path:
            output_image.save(save_path, "WEBP", quality=95)
            messagebox.showinfo("Saved", f"Group image saved to {save_path}")



    def load_group_image(self):
        """Load a group image from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if not file_path:
            return
        self.group_image = Image.open(file_path).convert("RGB")  # Ensure RGB mode
        self.group_image_original = self.group_image.copy()

        # Extract the filename (without extension) from the file path
        self.group_image_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Reset scaling and position
        self.scale_factor_group = 1.0
        self.group_scale.set(self.scale_factor_group)
        self.img_x_group = 0
        self.img_y_group = 0

        self.update_group_image()

    def update_image(self):
        """Update the displayed image based on the current scale and position."""
        if self.image:
            # Calculate the scaling factor between the output size and the canvas size
            display_scale_x = self.canvas_width / self.output_width
            display_scale_y = self.canvas_height / self.output_height
            display_scale = min(display_scale_x, display_scale_y)

            # Scale the image for display, maintaining aspect ratio
            img_display_width = int(self.image.width * self.scale_factor * display_scale)
            img_display_height = int(self.image.height * self.scale_factor * display_scale)
            resized_image = self.image.resize((img_display_width, img_display_height), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(resized_image)

            # Clear the canvas and draw the background rectangle
            self.canvas_personal.delete("all")
            self.canvas_personal.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="white", outline="black")

            # Adjust position for display scale
            display_x = self.img_x * display_scale
            display_y = self.img_y * display_scale

            # Display the image
            self.image_id = self.canvas_personal.create_image(display_x, display_y, anchor="nw", image=self.img_tk)

    def update_group_image(self):
        """Update the displayed group image based on the current scale and position."""
        if self.group_image:
            # Calculate the scaling factor between the output size and the canvas size
            display_scale_x = self.canvas_width_group / self.output_width_group
            display_scale_y = self.canvas_height_group / self.output_height_group
            display_scale = min(display_scale_x, display_scale_y)

            # Scale the image for display, maintaining aspect ratio
            img_display_width = int(self.group_image.width * self.scale_factor_group * display_scale)
            img_display_height = int(self.group_image.height * self.scale_factor_group * display_scale)
            resized_image = self.group_image.resize((img_display_width, img_display_height), Image.LANCZOS)
            self.group_img_tk = ImageTk.PhotoImage(resized_image)

            # Clear the canvas and draw the background rectangle
            self.group_canvas.delete("all")
            self.group_canvas.create_rectangle(0, 0, self.canvas_width_group, self.canvas_height_group, fill="white", outline="black")

            # Adjust position for display scale
            display_x = self.img_x_group * display_scale
            display_y = self.img_y_group * display_scale

            # Display the image
            self.group_image_id = self.group_canvas.create_image(display_x, display_y, anchor="nw", image=self.group_img_tk)

    def update_slider(self, step):
        """Increase or decrease the slider value for personal image resizing."""
        new_value = self.scale.get() + step
        new_value = max(0.05, min(2.0, new_value))
        self.scale.set(new_value)
        self.update_scale(new_value)

    def update_group_slider(self, step):
        """Increase or decrease the slider value for group image resizing."""
        new_value = self.group_scale.get() + step
        new_value = max(0.05, min(2.0, new_value))
        self.group_scale.set(new_value)
        self.update_group_scale(new_value)

    def update_scale(self, scale_value):
        """Update the scale factor and redraw the personal image."""
        self.scale_factor = float(scale_value)
        self.update_image()

    def update_group_scale(self, scale_value):
        """Update the scale factor and redraw the group image."""
        self.scale_factor_group = float(scale_value)
        self.update_group_image()

    def start_drag(self, event):
        """Start dragging the image."""
        self.start_x = event.x
        self.start_y = event.y

    def start_group_drag(self, event):
        """Start dragging the group image."""
        self.start_x = event.x
        self.start_y = event.y

    def drag_image(self, event):
        """Handle the dragging of the personal image."""
        # Calculate the scaling factor between the output size and the canvas size
        display_scale_x = self.canvas_width / self.output_width
        display_scale_y = self.canvas_height / self.output_height
        display_scale = min(display_scale_x, display_scale_y)

        dx = (event.x - self.start_x) / display_scale
        dy = (event.y - self.start_y) / display_scale
        self.img_x += dx
        self.img_y += dy
        self.update_image()
        self.start_x = event.x
        self.start_y = event.y

    def drag_group_image(self, event):
        """Handle the dragging of the group image."""
        # Calculate the scaling factor between the output size and the canvas size
        display_scale_x = self.canvas_width_group / self.output_width_group
        display_scale_y = self.canvas_height_group / self.output_height_group
        display_scale = min(display_scale_x, display_scale_y)

        dx = (event.x - self.start_x) / display_scale
        dy = (event.y - self.start_y) / display_scale
        self.img_x_group += dx
        self.img_y_group += dy
        self.update_group_image()
        self.start_x = event.x
        self.start_y = event.y

    def process_image(self):
        """Process and save the personal image with correct DPI."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        # Use the original image to prevent cumulative resizing
        original_image = self.image_original.copy()

        # If scaling is applied, resize the original image accordingly
        if self.scale_factor != 1.0:
            img_width = int(original_image.width * self.scale_factor)
            img_height = int(original_image.height * self.scale_factor)
            resized_img = original_image.resize((img_width, img_height), Image.LANCZOS)
        else:
            resized_img = original_image

        # Create a blank output image
        output_image = Image.new("RGB", (self.output_width, self.output_height), "white")

        # Paste the resized image onto the output image at the calculated position
        output_image.paste(resized_img, (int(self.img_x), int(self.img_y)))

        if self.metadata_var.get():
            output_image = self.remove_metadata(output_image)

        if self.round_var.get():
            output_image = self.round_corners(output_image)

        # Pre-fill the save dialog with the original filename and ".webp" extension
        default_filename = f"{self.image_filename}.webp"
        save_path = filedialog.asksaveasfilename(defaultextension=".webp", initialfile=default_filename, filetypes=[("WEBP", "*.webp")])

        if save_path:
            output_image.save(save_path, "WEBP", quality=95, dpi=(96, 96))
            messagebox.showinfo("Saved", f"Image saved to {save_path}")


    def load_group_image(self):
        """Load a group image from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if not file_path:
            return
        self.group_image = Image.open(file_path).convert("RGB")  # Ensure RGB mode
        self.group_image_original = self.group_image.copy()  # Keep a copy of the original image

        # Extract the filename (without extension) from the file path
        self.group_image_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Reset scaling and position
        self.img_x_group = 0
        self.img_y_group = 0

        # Adjust the scale factor to fit the height of the image to the canvas height
        image_height = self.group_image.height
        self.scale_factor_group = min(self.canvas_height_group / image_height, 2.0)  # Constrain to max scale factor
        self.group_scale.set(self.scale_factor_group)  # Update the slider value

        self.update_group_image()


    def remove_metadata(self, img):
        """Remove metadata from the image."""
        img_no_meta = Image.new(img.mode, img.size)
        img_no_meta.putdata(list(img.getdata()))
        return img_no_meta

    def round_corners(self, img, radius=50):
        """Make the image have rounded corners with a white background."""
        img = img.convert("RGB")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius, fill=255)

        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        white_bg.paste(img, mask=mask)

        return white_bg

# Initialize and run the application
root = Tk()
app = ImageCropper(root)
root.mainloop()
