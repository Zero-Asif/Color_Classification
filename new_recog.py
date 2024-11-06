import numpy as np
import pandas as pd
import cv2
from typing import Tuple, Optional
from dataclasses import dataclass
import pyperclip
import tkinter as tk
from tkinter import filedialog, messagebox


@dataclass
class ColorInfo:
    name: str
    rgb: Tuple[int, int, int]
    hex: str


# Color blindness matrices
COLOR_BLINDNESS_MATRICES = {
    "Normal": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "Protanopia": np.array(
        [[0.56667, 0.43333, 0.0], [0.55833, 0.44167, 0.0], [0.0, 0.24167, 0.75833]]
    ),
    "Deuteranopia": np.array(
        [[0.625, 0.375, 0.0], [0.70, 0.30, 0.0], [0.0, 0.30, 0.70]]
    ),
    "Tritanopia": np.array(
        [[0.95, 0.05, 0.0], [0.0, 0.43333, 0.56667], [0.0, 0.475, 0.525]]
    ),
}


class ColorRecognitionApp:
    def __init__(self, colors_csv_path: str):
        """Initialize the Color Recognition App with image and color dataset."""
        self.colors_csv_path = colors_csv_path
        self.img = None
        self.img_resized = None  # Store the resized image
        self.img_simulated = None
        self.img_display = None  # Image used for displaying (with annotations)
        self.simulation_mode = "Normal"
        self.current_color: Optional[ColorInfo] = None
        self.window_name = "Color Recognition App"
        self.scale_factor = 1.0  # Scaling factor for image resizing

        # Set fixed window size
        self.window_width = 800  # Adjust as needed
        self.window_height = 600  # Adjust as needed

        # Load and prepare color dataset
        self.colors_df = pd.read_csv(
            colors_csv_path,
            names=["color", "color_name", "hex", "R", "G", "B"],
            header=None,
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
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")],
        )
        if file_path:
            self.img = cv2.imread(file_path)
            if self.img is None:
                messagebox.showerror("Error", f"Could not load image from {file_path}")
                return
            self.resize_image_to_fixed_window()
            self.root.destroy()  # Close the Tkinter window
            # Proceed to run the app
            self.run()
        else:
            messagebox.showinfo("No File Selected", "No image file was selected.")
            self.root.destroy()

    def resize_image_to_fixed_window(self):
        """Resize the image to fit within the fixed window dimensions."""
        img_height, img_width = self.img.shape[:2]

        # Determine the scaling factor
        scale_width = self.window_width / img_width
        scale_height = self.window_height / img_height
        self.scale_factor = min(scale_width, scale_height)

        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        self.img_resized = cv2.resize(
            self.img, (new_width, new_height), interpolation=cv2.INTER_AREA
        )

        # Center the image in the window
        self.x_offset = (self.window_width - new_width) // 2
        self.y_offset = (self.window_height - new_height) // 2

    def recognize_color(self, r: int, g: int, b: int) -> ColorInfo:
        # Existing code (unchanged)
        colors = self.colors_df[["R", "G", "B"]].values
        query_color = np.array([r, g, b])

        # Calculate Euclidean distances
        distances = np.sqrt(np.sum((colors - query_color) ** 2, axis=1))
        min_index = np.argmin(distances)

        return ColorInfo(
            name=self.colors_df.iloc[min_index]["color_name"],
            rgb=(r, g, b),
            hex=self.colors_df.iloc[min_index]["hex"],
        )

    def mouse_callback(self, event, x: int, y: int, flags, param):
        """Handle mouse events."""
        # Adjust x and y to correspond to the image coordinates
        img_x = x - self.x_offset
        img_y = y - self.y_offset

        if event == cv2.EVENT_LBUTTONDBLCLK:
            if (0 <= img_x < self.img_resized.shape[1]) and (
                0 <= img_y < self.img_resized.shape[0]
            ):
                # Map the coordinates back to the original image
                orig_x = int(img_x / self.scale_factor)
                orig_y = int(img_y / self.scale_factor)
                b, g, r = self.img[orig_y, orig_x]
                self.current_color = self.recognize_color(int(r), int(g), int(b))

    def draw_color_info(self):
        # Existing code (adjusted to draw on canvas)
        if not self.current_color:
            return

        # Create color display rectangle on the canvas
        cv2.rectangle(
            self.canvas, (20, 20), (750, 60), self.current_color.rgb[::-1], -1
        )

        # Prepare display text
        text = (
            f"{self.current_color.name} "
            f"RGB={self.current_color.rgb} "
            f"HEX={self.current_color.hex}"
        )

        # Choose text color based on background brightness
        brightness = sum(self.current_color.rgb)
        text_color = (0, 0, 0) if brightness >= 600 else (255, 255, 255)

        # Draw text on the canvas
        cv2.putText(
            self.canvas,
            text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            text_color,
            2,
            cv2.LINE_AA,
        )

    def draw_simulation_mode(self):
        # Existing code (adjusted to draw on canvas)
        # Prepare the text
        mode_text = f"Mode: {self.simulation_mode}"

        # Set position for the text (bottom left)
        text_position = (10, self.window_height - 10)

        # Text properties
        text_color = (255, 255, 255)  # White text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2

        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            mode_text, font, font_scale, thickness
        )

        # Make a filled rectangle as background
        rect_start = (text_position[0], text_position[1] - text_height - baseline)
        rect_end = (text_position[0] + text_width, text_position[1] + baseline)
        cv2.rectangle(self.canvas, rect_start, rect_end, (0, 0, 0), -1)

        # Put the text
        cv2.putText(
            self.canvas,
            mode_text,
            text_position,
            font,
            font_scale,
            text_color,
            thickness,
            cv2.LINE_AA,
        )

    def apply_color_blindness_simulation(self):
        # Existing code (adjusted to work with resized image)
        # Get the transformation matrix
        matrix = COLOR_BLINDNESS_MATRICES.get(
            self.simulation_mode, COLOR_BLINDNESS_MATRICES["Normal"]
        )

        # Apply the matrix to the resized image
        img_float = self.img_resized.astype(np.float32) / 255.0
        img_sim = cv2.transform(img_float, matrix)
        img_sim = np.clip(img_sim, 0, 1) * 255
        self.img_simulated = img_sim.astype(np.uint8)

    def handle_key_press(self):
        # Existing code (unchanged)
        key = cv2.waitKey(20) & 0xFF
        if key == ord("c") and self.current_color:
            # Copy color values to clipboard
            color_text = f"Name: {self.current_color.name}, RGB: {self.current_color.rgb}, HEX: {self.current_color.hex}"
            pyperclip.copy(color_text)
            print(f"Copied to clipboard: {color_text}")
        elif key == ord("n"):
            # Normal vision
            self.simulation_mode = "Normal"
            self.apply_color_blindness_simulation()
        elif key == ord("p"):
            # Protanopia simulation
            self.simulation_mode = "Protanopia"
            self.apply_color_blindness_simulation()
        elif key == ord("d"):
            # Deuteranopia simulation
            self.simulation_mode = "Deuteranopia"
            self.apply_color_blindness_simulation()
        elif key == ord("t"):
            # Tritanopia simulation
            self.simulation_mode = "Tritanopia"
            self.apply_color_blindness_simulation()
        elif key == 27:
            # ESC key to exit
            return False
        return True

    # Add this function inside the ColorRecognitionApp class
    def draw_help_text(self):
        """Draw the help text based on the current simulation mode."""
        # Define the help text for each mode
        help_text = {
            "Normal": [
                "Double click for RGB, Hex value",
                "Press 'p' for Protanopia Simulation",
                "Press 'd' for Deuteranopia Simulation",
                "Press 't' for Tritanopia Simulation",
                "Press 'c' to copy values",
            ],
            "Protanopia": [
                "Press 'n' for Normal Vision",
                "Press 'd' for Deuteranopia Simulation",
                "Press 't' for Tritanopia Simulation",
                "Double click for RGB, Hex value",
                "Press 'c' to copy values",
            ],
            "Deuteranopia": [
                "Press 'n' for Normal Vision",
                "Press 'p' for Protanopia Simulation",
                "Press 't' for Tritanopia Simulation",
                "Double click for RGB, Hex value",
                "Press 'c' to copy values",
            ],
            "Tritanopia": [
                "Press 'n' for Normal Vision",
                "Press 'p' for Protanopia Simulation",
                "Press 'd' for Deuteranopia Simulation",
                "Double click for RGB, Hex value",
                "Press 'c' to copy values",
            ],
        }
        # Get the text for the current mode
        lines = help_text.get(self.simulation_mode, [])
        # Set starting position and font properties
        y_position = self.window_height - 140  # Start from the bottom with an offset
        x_position = 10  # Margin from the left
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5  # Adjust the font scale for size 12 text
        thickness = 1
        line_height = 20  # Vertical spacing between lines
        # Draw each line of text
        for line in lines:
            text_size, _ = cv2.getTextSize(line, font, font_scale, thickness)
            cv2.putText(
                self.canvas,
                line,
                (x_position, y_position),
                font,
                font_scale,
                (255, 255, 255),
                thickness,
                cv2.LINE_AA,
            )
            y_position += line_height

    def run(self):
        """Run the application main loop."""
        # Create a black canvas with fixed window size
        self.canvas = np.zeros(
            (self.window_height, self.window_width, 3), dtype=np.uint8
        )

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        # Apply initial simulation
        self.apply_color_blindness_simulation()

        while True:
            # Reset the canvas
            self.canvas[:] = (0, 0, 0)

            # Place the image on the canvas
            self.canvas[
                self.y_offset : self.y_offset + self.img_resized.shape[0],
                self.x_offset : self.x_offset + self.img_resized.shape[1],
            ] = self.img_simulated

            # Draw color info if a color is selected
            if self.current_color:
                self.draw_color_info()

            # Draw the simulation mode on the image
            self.draw_simulation_mode()

            # Display the help text
            self.draw_help_text()

            # Display the image
            cv2.imshow(self.window_name, self.canvas)

            if not self.handle_key_press():
                break

        cv2.destroyAllWindows()


# Usage example
if __name__ == "__main__":
    try:
        app = ColorRecognitionApp("colors.csv")
    except Exception as e:
        print(f"Error: {e}")
