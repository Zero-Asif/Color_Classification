Feature Details and Usage Instructions
1. Drag and Drop Image Loading

Description: The application now allows users to drag and drop an image file onto the Tkinter window to load it.

Implementation:

    Integrated the tkinterdnd2 package to enable drag-and-drop functionality in Tkinter.
    Created a Tkinter window with a label instructing the user to drag and drop an image.
    The drop method handles the event when an image is dropped onto the window, loads the image, and starts the main application loop.

Usage:

    Run the script.
    A Tkinter window titled "Drag and Drop Image" will appear.
    Drag an image file (e.g., .jpg, .png) onto the window.
    The application will load the image and proceed to the main functionality.

2. Copy Color Values to Clipboard

Description: After selecting a color by double-clicking on the image, pressing the 'c' key copies the color's name, RGB, and HEX values to the clipboard.

Implementation:

    Added the pyperclip library to handle clipboard operations.
    Implemented the handle_key_press method to detect key presses.
    When 'c' is pressed, and a color is selected, the color information is copied to the clipboard.

Usage:

    Double-click on any point in the image to select a color.
    Press the 'c' key on your keyboard.
    The color information is copied to the clipboard, and a message is printed in the console.

3. Color Blindness Simulation

Description: The application can simulate how the image appears to individuals with different types of color blindness (protanopia, deuteranopia, tritanopia). Users can toggle between simulations.

Implementation:

    Defined color transformation matrices for each type of color blindness.
    Implemented the apply_color_blindness_simulation method to transform the image.
    Updated the handle_key_press method to change the simulation mode based on key presses ('n', 'p', 'd', 't').

Usage:

    Normal Vision: Press 'n' to view the image in normal color vision.
    Protanopia Simulation: Press 'p' to simulate protanopia.
    Deuteranopia Simulation: Press 'd' to simulate deuteranopia.
    Tritanopia Simulation: Press 't' to simulate tritanopia.