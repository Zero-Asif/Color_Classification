# Color Recognition App

A Python application that allows users to recognize colors from images, simulate color blindness conditions, and interact with images in a user-friendly way. The app provides features such as copying color values to the clipboard, simulating different types of color blindness, and adjusting images to fit the screen while considering the taskbar.

## Table of Contents

- [Color Recognition App](#color-recognition-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [Interacting with the Application](#interacting-with-the-application)
      - [Selecting a Color](#selecting-a-color)
      - [Copying Color Information](#copying-color-information)
      - [Color Blindness Simulation Modes](#color-blindness-simulation-modes)
      - [Exiting the Application](#exiting-the-application)
  - [Dependencies](#dependencies)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

---

## Features

- **Color Recognition**: Double-click on any point in an image to recognize the color at that pixel. The app displays the color name, RGB values, and HEX code.

- **Copy to Clipboard**: Press the 'c' key after selecting a color to copy its information to the clipboard.

- **Color Blindness Simulation**: Simulate how the image appears to individuals with different types of color blindness:
  - Normal Vision
  - Protanopia (red color blindness)
  - Deuteranopia (green color blindness)
  - Tritanopia (blue color blindness)

- **Image Resizing**: Automatically resizes large images to fit within the screen dimensions while maintaining the aspect ratio.

- **Taskbar Adjustment**: Considers the taskbar height to ensure the application window fits entirely within the visible screen area.

- **Simulation Mode Display**: Shows the current color blindness simulation mode at the bottom-left corner of the image.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/color-recognition-app.git
   cd color-recognition-app
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If you don't have a `requirements.txt`, you can install the packages individually:

   ```bash
   pip install numpy pandas opencv-python pyperclip
   ```

---

## Usage

### Running the Application

1. **Prepare the Color Data CSV**

   Ensure you have a `colors.csv` file containing color names and their RGB and HEX values. The CSV should have the following columns:

   ```
   color_name, hex_value, R, G, B
   ```

   You can download a sample `colors.csv` or create your own.

2. **Run the Script**

   ```bash
   python color_recognition_app.py
   ```

   - Upon running, a file dialog will appear prompting you to select an image file.
   - Select an image (e.g., `.jpg`, `.png`, `.bmp`, `.tiff`).

### Interacting with the Application

#### Selecting a Color

- **Double-Click** on any point in the image to select a color.
- The app will display the color name, RGB values, and HEX code at the top of the image.

#### Copying Color Information

- After selecting a color, **press the 'c' key** to copy the color information to your clipboard.
- The information includes:
  - Color Name
  - RGB Values
  - HEX Code

#### Color Blindness Simulation Modes

- **Press 'n'**: Switch to **Normal Vision** mode.
- **Press 'p'**: Switch to **Protanopia Simulation** mode.
- **Press 'd'**: Switch to **Deuteranopia Simulation** mode.
- **Press 't'**: Switch to **Tritanopia Simulation** mode.
- The current simulation mode is displayed at the bottom-left corner of the image.

#### Exiting the Application

- **Press the 'Esc' key** to exit the application at any time.

---

## Dependencies

- **Python 3.x**

- **Libraries**:

  - `numpy`
  - `pandas`
  - `opencv-python`
  - `pyperclip`
  - `tkinter` (usually included with Python)

- **Additional Notes**:

  - **Windows Users**: The application uses `ctypes` to adjust for the taskbar height.
  - **Linux Users**: May need to install `xclip` or `xsel` for `pyperclip` to function properly.

    ```bash
    sudo apt-get install xclip
    ```

---

## Project Structure

```
color-recognition-app/
├── color_recognition_app.py  # Main application script
├── colors.csv                # CSV file containing color data
├── requirements.txt          # List of dependencies
├── README.md                 # Documentation
└── images/                   # Directory for sample images (optional)
```

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Description of your changes"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software as per the license terms.

---

## Acknowledgements

- **OpenCV**: For providing powerful computer vision tools.
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical computations.
- **Pyperclip**: For clipboard functionality.
- **Color Data**: The color names and values are sourced from various public datasets.

---

**Disclaimer**: This application is intended for educational purposes. While efforts have been made to ensure accuracy, the color recognition and simulations may not be perfect. For professional applications, further validation is recommended.

---

**Contact Information**

If you have any questions or suggestions, please feel free to contact:

- **Email**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

**Screenshots**

*(Optional: Include screenshots of the application in use, showing the color recognition and simulation modes.)*

---

**Version History**

- **v1.0**:
  - Initial release with core features.

---