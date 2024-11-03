import numpy as np
import pandas as pd
import cv2
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class ColorInfo:
    name: str
    rgb: Tuple[int, int, int]
    hex: str

class ColorRecognitionApp:
    def __init__(self, image_path: str, colors_csv_path: str):
        """Initialize the Color Recognition App with image and color dataset."""
        self.img = cv2.imread(image_path)
        if self.img is None:
            raise FileNotFoundError(f"Could not load image from {image_path}")
        
        # Load and prepare color dataset
        self.colors_df = pd.read_csv(
            colors_csv_path,
            names=["color", "color_name", "hex", "R", "G", "B"],
            header=None
        )
        
        self.clicked = False
        self.current_color: Optional[ColorInfo] = None
        self.window_name = 'Color Recognition App'

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
            self.clicked = True
            b, g, r = self.img[y, x]
            self.current_color = self.recognize_color(int(r), int(g), int(b))

    def draw_color_info(self):
        """Draw color information on the image."""
        if not self.current_color:
            return

        # Create color display rectangle
        cv2.rectangle(self.img, (20, 20), (750, 60), 
                     self.current_color.rgb[::-1], -1)

        # Prepare display text
        text = (f"{self.current_color.name} "
               f"RGB={self.current_color.rgb} "
               f"HEX={self.current_color.hex}")

        # Choose text color based on background brightness
        brightness = sum(self.current_color.rgb)
        text_color = (0, 0, 0) if brightness >= 600 else (255, 255, 255)

        # Draw text
        cv2.putText(self.img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                   0.8, text_color, 2, cv2.LINE_AA)

    def run(self):
        """Run the application main loop."""
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        while True:
            if self.clicked:
                self.draw_color_info()
                self.clicked = False

            cv2.imshow(self.window_name, self.img)

            # Break loop on 'esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break

        cv2.destroyAllWindows()

# Usage example
if __name__ == "__main__":
    try:
        app = ColorRecognitionApp("img/sample_4.jpg", "colors.csv")
        app.run()
    except Exception as e:
        print(f"Error: {e}")