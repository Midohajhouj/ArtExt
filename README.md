
# ArtExt - Customizable Banner Generator

ArtExt is a Python-based command-line tool that allows you to generate customizable ASCII art banners with various fonts, colors, text effects, and alignments. You can also save the generated banners as text files or images.

## Features

- **Multiple Fonts**: Choose from a wide range of built-in fonts or add custom fonts.
- **Text Colors**: Select from predefined colors or use custom HEX color codes.
- **Text Effects**: Apply effects like bold, underline, blink, italic, and strikethrough.
- **Alignment**: Align text to the left, center, or right.
- **Save Options**: Save banners as text files or images (PNG format).
- **Batch Processing**: Generate banners for all available fonts at once.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/artext.git
   cd artext
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.7 or higher installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:
   - `pyfiglet`
   - `termcolor`
   - `Pillow`

3. **Run the Script**:
   ```bash
   python artext.py
   ```

## Usage

### Command-Line Interface

You can run the script directly from the command line and use the interactive menu to generate banners. Alternatively, you can use command-line arguments for quick setup.

#### Interactive Mode
```bash
python artext.py
```

#### Command-Line Arguments
```bash
python artext.py --text "Hello World" --font "slant" --color "blue" --align "center" --effects "bold,underline"
```

### Available Arguments

- `--text`: Text for the banner (required).
- `--font`: Font for the banner (default: "standard").
- `--color`: Color for the banner (default: "white").
- `--align`: Alignment for the banner (default: "left").
- `--effects`: Text effects (comma-separated, e.g., "bold,underline").
- `--width`: Image width for saving as an image (default: 800).
- `--height`: Image height for saving as an image (default: 200).
- `--font-size`: Font size for saving as an image (default: 20).
- `--output`: Output file name (for text or image).
- `--batch`: Batch process multiple banners from a file.

### Main Menu Options

1. Generate Banner: Create a single banner with custom text, font, color, effects, and alignment.
2. Generate Banner for All Fonts: Generate banners for all available fonts with the same text and settings.
3. List Available Fonts: Display a list of all available fonts.
4. Preview Colors: Preview a color with a sample text.
5. Help: Display the help menu with instructions.
6. Exit: Exit the program.

### Saving Banners

After generating a banner, you can choose to save it as a text file or an image (PNG format). The script will prompt you for the file name and other details.

### Custom Fonts

You can add custom fonts to the `custom_fonts` directory. Ensure that the fonts are in `.flf` format (Figlet font format). The script will automatically detect and include them in the font list.

## Examples

#### Generate a Simple Banner
```bash
python3 artext.py
```

#### Generate a Banner with Effects
```bash
python3 artext.py --text "Hello" --font "slant" --color "green" --effects "bold,underline"
```

#### Save Banner as Image
```bash
python3 artext.py --text "Hello" --font "slant" --color "green" --output "banner.png"
```

#### Generate Banners for All Fonts
```bash
python3 artext.py --text "Hello" --color "blue" --batch
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

**<p align="center"> Developed by <a href="https://github.com/Midohajhouj">MIDO</a> </p>**

