import numpy as np
import pandas as pd
import cv2
from typing import Tuple, Optional
from dataclasses import dataclass
import pyperclip
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes  # For Windows API to get work area


@dataclass
class ColorInfo:
    name: str
    rgb: Tuple[int, int, int]
    hex: str

# Color blindness matrices
COLOR_BLINDNESS_MATRICES = {
    'Normal': np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    'Protanopia': np.array([
        [0.56667, 0.43333, 0.0],
        [0.55833, 0.44167, 0.0],
        [0.0, 0.24167, 0.75833]
    ]),
    'Deuteranopia': np.array([
        [0.625, 0.375, 0.0],
        [0.70, 0.30, 0.0],
        [0.0, 0.30, 0.70]
    ]),
    'Tritanopia': np.array([
        [0.95, 0.05, 0.0],
        [0.0, 0.43333, 0.56667],
        [0.0, 0.475, 0.525]
    ]),
}

class ColorRecognitionApp:
    def __init__(self, colors_csv_path: str):
        """Initialize the Color Recognition App with image and color dataset."""
        self.colors_csv_path = colors_csv_path
        self.img = None
        self.img_resized = None  # Store the resized image
        self.img_simulated = None
        self.img_display = None  # Image used for displaying (with annotations)
        self.simulation_mode = 'Normal'
        self.current_color: Optional[ColorInfo] = None
        self.window_name = 'Color Recognition App'
        self.scale_factor = 1.0  # Scaling factor for image resizing

        # Load and prepare color dataset
        self.colors_df = pd.read_csv(
            colors_csv_path,
            names=["color", "color_name", "hex", "R", "G", "B"],
            header=None
        )

        # Initialize Tkinter root for GUI features
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        # Use file dialog to select an image
        self.load_image_with_dialog()

    def load_image_with_dialog(self):
        """Use a file dialog to select and load an image."""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.img = cv2.imread(file_path)
            if self.img is None:
                messagebox.showerror("Error", f"Could not load image from {file_path}")
                return
            self.resize_image_to_screen()
            self.root.destroy()  # Close the Tkinter window
            # Proceed to run the app
            self.run()
        else:
            messagebox.showinfo("No File Selected", "No image file was selected.")
            self.root.destroy()
    def get_work_area(self):
        """Get the working area of the screen, excluding taskbar (Windows only)."""
        user32 = ctypes.windll.user32
        spi_get_work_area = 0x0030
        class RECT(ctypes.Structure):
            _fields_ = [('left', ctypes.c_long),
                        ('top', ctypes.c_long),
                        ('right', ctypes.c_long),
                        ('bottom', ctypes.c_long)]
        rect = RECT()
        user32.SystemParametersInfoW(spi_get_work_area, 0, ctypes.byref(rect), 0)
        work_width = rect.right - rect.left
        work_height = rect.bottom - rect.top
        return work_width, work_height
    def resize_image_to_screen(self):
            """Resize the image to fit within the screen dimensions, considering taskbar height."""
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Get work area dimensions (excluding taskbar)
            try:
                work_width, work_height = self.get_work_area()
            except Exception as e:
                print(f"Could not get work area dimensions: {e}")
                # If not on Windows or an error occurs, fall back to screen dimensions minus an estimated taskbar height
                work_width, work_height = screen_width, screen_height - 100  # Subtract 100 pixels as a fallback

            img_height, img_width = self.img.shape[:2]

            # Determine the scaling factor
            scale_width = work_width / img_width
            scale_height = work_height / img_height
            self.scale_factor = min(scale_width, scale_height, 1.0)  # Do not upscale smaller images

            if self.scale_factor < 1.0:
                new_width = int(img_width * self.scale_factor)
                new_height = int(img_height * self.scale_factor)
                self.img_resized = cv2.resize(self.img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            else:
                self.img_resized = self.img.copy()

    def recognize_color(self, r: int, g: int, b: int) -> ColorInfo:
        """
        Find the closest matching color name using Euclidean distance.
        Returns ColorInfo object containing color details.
        """
        # Convert to numpy arrays for vectorized operations
        colors = self.colors_df[['R', 'G', 'B']].values
        query_color = np.array([r, g, b])

        # Calculate Euclidean distances
        distances = np.sqrt(np.sum((colors - query_color) ** 2, axis=1))
        min_index = np.argmin(distances)

        return ColorInfo(
            name=self.colors_df.iloc[min_index]['color_name'],
            rgb=(r, g, b),
            hex=self.colors_df.iloc[min_index]['hex']
        )

    def mouse_callback(self, event, x: int, y: int, flags, param):
        """Handle mouse events."""
        if event == cv2.EVENT_LBUTTONDBLCLK:
            if y < self.img_resized.shape[0] and x < self.img_resized.shape[1]:
                # Map the coordinates back to the original image
                orig_x = int(x / self.scale_factor)
                orig_y = int(y / self.scale_factor)
                b, g, r = self.img[orig_y, orig_x]
                self.current_color = self.recognize_color(int(r), int(g), int(b))

    def draw_color_info(self):
        """Draw color information on the image."""
        if not self.current_color:
            return

        # Draw on the display image
        img_to_draw = self.img_display

        # Create color display rectangle
        cv2.rectangle(img_to_draw, (20, 20), (750, 60),
                      self.current_color.rgb[::-1], -1)

        # Prepare display text
        text = (f"{self.current_color.name} "
                f"RGB={self.current_color.rgb} "
                f"HEX={self.current_color.hex}")

        # Choose text color based on background brightness
        brightness = sum(self.current_color.rgb)
        text_color = (0, 0, 0) if brightness >= 600 else (255, 255, 255)

        # Draw text
        cv2.putText(img_to_draw, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, text_color, 2, cv2.LINE_AA)

    def draw_simulation_mode(self):
        """Draw the current simulation mode on the image."""
        # Draw on the display image
        img_to_draw = self.img_display

        # Prepare the text
        mode_text = f"Mode: {self.simulation_mode}"

        # Get image dimensions
        height, width = img_to_draw.shape[:2]

        # Set position for the text (bottom left)
        text_position = (10, height - 10)

        # Text properties
        text_color = (255, 255, 255)  # White text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2

        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(mode_text, font, font_scale, thickness)

        # Make a filled rectangle as background
        rect_start = (text_position[0], text_position[1] - text_height - baseline)
        rect_end = (text_position[0] + text_width, text_position[1] + baseline)
        cv2.rectangle(img_to_draw, rect_start, rect_end, (0, 0, 0), -1)

        # Put the text
        cv2.putText(img_to_draw, mode_text, text_position, font, font_scale, text_color, thickness, cv2.LINE_AA)

    def apply_color_blindness_simulation(self):
        """Apply color blindness simulation to the image."""
        # Get the transformation matrix
        matrix = COLOR_BLINDNESS_MATRICES.get(self.simulation_mode, COLOR_BLINDNESS_MATRICES['Normal'])

        # Apply the matrix to the image
        # Convert image to float32 for accurate matrix multiplication
        img_float = self.img_resized.astype(np.float32) / 255.0
        img_sim = cv2.transform(img_float, matrix)
        # Clip values to [0,1] and convert back to uint8
        img_sim = np.clip(img_sim, 0, 1) * 255
        self.img_simulated = img_sim.astype(np.uint8)

    def handle_key_press(self):
        """Handle key press events."""
        key = cv2.waitKey(20) & 0xFF
        if key == ord('c') and self.current_color:
            # Copy color values to clipboard
            color_text = f"Name: {self.current_color.name}, RGB: {self.current_color.rgb}, HEX: {self.current_color.hex}"
            pyperclip.copy(color_text)
            print(f"Copied to clipboard: {color_text}")
        elif key == ord('n'):
            # Normal vision
            self.simulation_mode = 'Normal'
            self.apply_color_blindness_simulation()
        elif key == ord('p'):
            # Protanopia simulation
            self.simulation_mode = 'Protanopia'
            self.apply_color_blindness_simulation()
        elif key == ord('d'):
            # Deuteranopia simulation
            self.simulation_mode = 'Deuteranopia'
            self.apply_color_blindness_simulation()
        elif key == ord('t'):
            # Tritanopia simulation
            self.simulation_mode = 'Tritanopia'
            self.apply_color_blindness_simulation()
        elif key == 27:
            # ESC key to exit
            return False
        return True

    def run(self):
        """Run the application main loop."""
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        # Apply initial simulation
        self.apply_color_blindness_simulation()

        while True:
            # Copy the simulated image to display image
            self.img_display = self.img_simulated.copy()

            # Draw color info if a color is selected
            if self.current_color:
                self.draw_color_info()

            # Draw the simulation mode on the image
            self.draw_simulation_mode()

            # Display the image
            cv2.imshow(self.window_name, self.img_display)

            if not self.handle_key_press():
                break

        cv2.destroyAllWindows()

# Usage example
if __name__ == "__main__":
    try:
        app = ColorRecognitionApp("colors.csv")
    except Exception as e:
        print(f"Error: {e}")
