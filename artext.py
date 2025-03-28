#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### BEGIN INIT INFO
# Provides:          artext-banner
# Required-Start:    $network $remote_fs
# Required-Stop:     $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: ArtExt
# Description:       A tool designed for creating multiple banner customizations with ASCII and image processing.
# Author:  
# + LIONMAD <https://github.com/Midohajhouj>
# License:           MIT License - https://opensource.org/licenses/MIT
# Bug-Report:        https://github.com/Midohajhouj/artext-banner/issues
# Depends:           python3, pyfiglet, termcolor, pillow
# Conflicts:         None
# Enhancements:      Support for font customization, image handling with PIL.
# Packaging:         Available on GitHub for manual installation.
### END INIT INFO ###

# =======================================
#      Libraries Used in the Script
# =======================================
import pyfiglet  # Creates ASCII art banners from text.
import os  # Provides tools to interact with the operating system, e.g., file and directory manipulation.
from termcolor import colored  # Adds color and style to terminal output.
import argparse  # Parses command-line arguments for the script.
from PIL import Image, ImageDraw, ImageFont, ImageOps  # Image processing library for creating and manipulating images.
from typing import List, Optional, Literal, Dict, Tuple  # Provides support for type hints in function definitions and variable declarations.
import logging  # Provides a flexible framework for emitting log messages.
from pathlib import Path  # A modern way to handle and manipulate filesystem paths.
import random  # Generates random numbers, selections, or permutations.
import signal  # Handles asynchronous events, such as termination signals.
import sys  # Provides access to system-specific parameters and functions, like manipulating I/O streams.


# Constants
COLORS = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
ALIGNMENTS = ["left", "center", "right"]
TEXT_EFFECTS = ["bold", "underline", "blink", "italic", "strikethrough"]
CUSTOM_FONTS_DIR = "custom_fonts"  # Directory for custom fonts
GRADIENT_COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF"]  # Gradient color options

# Set up logging
logging.basicConfig(filename="banner_generator.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_banner(
    text: str, 
    font: str, 
    color: str, 
    align: Literal["left", "center", "right"] = 'left', 
    attrs: Optional[List[str]] = None,
    gradient: Optional[Tuple[str, str]] = None
) -> str:
    """Generates a banner with the given text, font, color, alignment, and text effects."""
    try:
        banner = pyfiglet.figlet_format(text, font=font, justify=align)
        if gradient:
            # Apply gradient color to the banner
            from colorama import Fore
            gradient_banner = ""
            for i, line in enumerate(banner.splitlines()):
                gradient_banner += Fore.GREEN + line + Fore.RESET + "\n"  # Example gradient (can be improved)
            return gradient_banner
        else:
            colored_banner = colored(banner, color, attrs=attrs)
        logging.info(f"Banner generated: {text}, font: {font}, color: {color}, align: {align}, attrs: {attrs}")
        return colored_banner
    except Exception as e:
        logging.error(f"Error generating banner: {str(e)}")
        return f"Error: {str(e)}"

def list_fonts() -> List[str]:
    """Returns a list of available fonts, including custom fonts."""
    fonts = pyfiglet.FigletFont.getFonts()
    if os.path.exists(CUSTOM_FONTS_DIR):
        custom_fonts = [f for f in os.listdir(CUSTOM_FONTS_DIR) if f.endswith('.flf')]
        fonts.extend(custom_fonts)
    return fonts

def get_user_input(prompt: str, default: Optional[str] = None, validation_func: Optional[callable] = None) -> str:
    """Gets user input with optional validation and default value."""
    while True:
        user_input = input(prompt).strip()
        if not user_input and default is not None:
            return default
        if validation_func is None or validation_func(user_input):
            return user_input
        print("\033[1;31mInvalid input! Try again.\033[0m")

def show_items(items: List[str], page: int = 1, per_page: int = 10) -> None:
    """Displays a paginated list of available items."""
    start = (page - 1) * per_page
    end = start + per_page
    for idx, item in enumerate(items[start:end], start=start + 1):
        print(f"[{idx}] {item}")
    print(f"\nPage {page} of {len(items) // per_page + 1}")
    print("Type 'next' to see more items, 'prev' to go back, or select an item by number or name.")

def color_preview(color: str, text: str = "This is a preview of the color.", font: str = "standard") -> None:
    """Displays a preview of the selected color and font."""
    banner = pyfiglet.figlet_format(text, font=font)
    print(colored(banner, color))

def show_font_preview(font: str, color: str, attrs: Optional[List[str]] = None) -> None:
    """Displays a preview of the selected font and color."""
    preview = generate_banner("Preview", font, color, attrs=attrs)
    print(preview)

def select_from_list(items: List[str], prompt: str, default: Optional[str] = None) -> Optional[str]:
    """Generic function to select an item from a list."""
    page = 1
    while True:
        print(f"\nAvailable {prompt}:")
        show_items(items, page)
        user_input = get_user_input(f"\nEnter the {prompt} name or number (or press Enter for default '{default}'), 'exit' to quit: ", default=default)
        
        if user_input.lower() == 'exit':
            return None
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(items):
                return items[index]
            else:
                print("\033[1;31mInvalid number! Try again.\033[0m")
        elif user_input.lower() == 'next':
            page += 1
        elif user_input.lower() == 'prev':
            page = max(1, page - 1)
        elif user_input in items:
            return user_input
        else:
            print("\033[1;31mInvalid input! Try again.\033[0m")

def is_valid_hex(color: str) -> bool:
    """Validates a HEX color code."""
    return color.startswith('#') and len(color) == 7 and all(c in '0123456789ABCDEFabcdef' for c in color[1:])

def select_color(font: str = "standard") -> str:
    """Handles color selection with preview."""
    while True:
        color = get_user_input("Enter the color name or HEX code (or press Enter for default 'white'): ", default="white")
        if color in COLORS or is_valid_hex(color):
            color_preview(color, text="This is a preview of the color.", font=font)
            confirm = get_user_input("Is this color okay? (y/n): ", default="y", validation_func=lambda x: x in ["y", "n"])
            if confirm == 'y':
                return color
        else:
            print("\033[1;31mInvalid color! Try again.\033[0m")

def select_text_effects() -> Optional[List[str]]:
    """Handles text effects selection."""
    while True:
        effects = get_user_input("Enter text effects (comma-separated, e.g., bold,underline): ", default="")
        if effects == "":
            return None
        effects_list = [effect.strip() for effect in effects.split(",")]
        if all(effect in TEXT_EFFECTS for effect in effects_list):
            return effects_list
        else:
            print("\033[1;31mInvalid text effects! Try again.\033[0m")

def save_banner(banner: str) -> None:
    """Saves the generated banner to a file."""
    save_option = get_user_input("Do you want to save the banner to a file? (y/n): ", default="n", validation_func=lambda x: x in ["y", "n"])
    if save_option == 'y':
        file_name = get_user_input("Enter the file name (with .txt extension): ", validation_func=lambda x: x.endswith('.txt'))
        try:
            with open(file_name, 'w') as f:
                f.write(banner)
            print(f"\033[1;32mBanner saved as {file_name}\033[0m")
            logging.info(f"Banner saved as {file_name}")
        except Exception as e:
            print(f"\033[1;31mError saving file: {str(e)}\033[0m")
            logging.error(f"Error saving file: {str(e)}")

def save_banner_as_image(banner: str, file_name: str = "banner.png") -> None:
    """Saves the generated banner as an image."""
    save_option = get_user_input("Do you want to save the banner as an image? (y/n): ", default="n", validation_func=lambda x: x in ["y", "n"])
    if save_option == 'y':
        file_name = get_user_input("Enter the file name (with .png extension): ", default="banner.png", validation_func=lambda x: x.endswith('.png'))
        image_width = int(get_user_input("Enter image width (default 800): ", default="800"))
        image_height = int(get_user_input("Enter image height (default 200): ", default="200"))
        font_size = int(get_user_input("Enter font size (default 20): ", default="20"))
        try:
            image = Image.new('RGB', (image_width, image_height), color=(0, 0, 0))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default().font_variant(size=font_size)
            draw.text((10, 10), banner, font=font, fill=(255, 255, 255))
            image.save(file_name)
            print(f"\033[1;32mBanner saved as {file_name}\033[0m")
            logging.info(f"Banner saved as {file_name}")
        except Exception as e:
            print(f"\033[1;31mError saving image: {str(e)}\033[0m")
            logging.error(f"Error saving image: {str(e)}")

def show_help() -> None:
    """Displays a help menu with instructions."""
    print("\033[1;32mHelp Menu:\033[0m")
    print("1. Enter the text for your banner.")
    print("2. Select a font from the list.")
    print("3. Choose a color for your banner.")
    print("4. Optionally, choose text effects (bold, underline, blink, italic, strikethrough).")
    print("5. Set the alignment (left, center, right).")
    print("6. Save the banner to a file or as an image if desired.")
    print("7. Use command-line arguments for quick setup (--text, --font, --color, --align).")
    print("8. Batch process multiple banners from a file using --batch.")

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate a customizable banner.", add_help=True)
    parser.add_argument("--text", type=str, help="Text for the banner")
    parser.add_argument("--font", type=str, help="Font for the banner")
    parser.add_argument("--color", type=str, help="Color for the banner")
    parser.add_argument("--align", type=str, help="Alignment for the banner")
    parser.add_argument("--effects", type=str, help="Text effects (comma-separated, e.g., bold,underline)")
    parser.add_argument("--width", type=int, help="Image width for saving as image")
    parser.add_argument("--height", type=int, help="Image height for saving as image")
    parser.add_argument("--font-size", type=int, help="Font size for saving as image")
    parser.add_argument("--output", type=str, help="Output file name (for text or image)")
    parser.add_argument("--batch", type=str, help="Batch process multiple banners from a file")
    return parser.parse_args()

def generate_banner_flow() -> None:
    """Handles the banner generation flow."""
    args = parse_arguments()
    clear_screen()
    print("\033[1;32mWelcome to the Customizable Banner Generator!\033[0m\n")
    show_help()

    # Get banner text
    text = args.text if args.text else get_user_input("Enter the text for your banner: ", validation_func=lambda x: x != "")
    
    # Select font
    fonts = list_fonts()
    font = args.font if args.font else select_from_list(fonts, "font", "standard")

    # Select color
    color = args.color if args.color else select_color(font)

    # Select text effects
    effects = args.effects.split(",") if args.effects else select_text_effects()

    # Get alignment
    align = args.align if args.align else get_user_input("Enter alignment (left/center/right, or press Enter for default 'left'): ", default="left", validation_func=lambda x: x in ALIGNMENTS)

    # Generate and display banner
    banner = generate_banner(text, font, color, align, effects)
    print("\n\033[1;34mHere is your banner:\033[0m\n")
    print(banner)

    # Save banner to file or image
    save_banner(banner)
    save_banner_as_image(banner)

def generate_all_fonts_banner(text: str, color: str, align: str = "left", effects: Optional[List[str]] = None) -> None:
    """Generates banners for all available fonts with the given text."""
    fonts = list_fonts()
    for font in fonts:
        banner = generate_banner(text, font, color, align, effects)
        print(f"\n\033[1;34mFont: {font}\033[0m\n")
        print(banner)
        save_option = get_user_input("Do you want to save this banner? (y/n): ", default="n", validation_func=lambda x: x in ["y", "n"])
        if save_option == 'y':
            save_banner(banner)
            save_banner_as_image(banner)

def show_menu() -> None:
    """Displays the main menu."""
    print("\033[1;32mMain Menu:\033[0m")
    print("1. Generate Banner")
    print("2. Generate Banner for All Fonts")
    print("3. List Available Fonts")
    print("4. Preview Colors")
    print("5. Help")
    print("6. Exit")

def signal_handler(sig, frame):
    """Handles Ctrl+C (SIGINT) gracefully."""
    print("\n\033[1;31mCtrl+C pressed. Exiting...\033[0m")
    sys.exit(0)

def main_menu() -> None:
    """Handles the main menu navigation."""
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        show_menu()
        choice = get_user_input("Enter your choice (1-6): ", validation_func=lambda x: x in ["1", "2", "3", "4", "5", "6"])
        if choice == "1":
            generate_banner_flow()
        elif choice == "2":
            text = get_user_input("Enter the text for your banner: ", validation_func=lambda x: x != "")
            color = select_color()
            effects = select_text_effects()
            align = get_user_input("Enter alignment (left/center/right, or press Enter for default 'left'): ", default="left", validation_func=lambda x: x in ALIGNMENTS)
            generate_all_fonts_banner(text, color, align, effects)
        elif choice == "3":
            fonts = list_fonts()
            show_fonts(fonts)
        elif choice == "4":
            color = select_color()
            color_preview(color)
        elif choice == "5":
            show_help()
        elif choice == "6":
            print("\033[1;32mExiting...\033[0m")
            break

if __name__ == "__main__":
    main_menu()
