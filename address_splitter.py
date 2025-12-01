#!/usr/bin/env python3
"""
Address Formatter for CSV Files

Splits long address fields in a CSV file into multiple lines based on
a maximum pixel width, useful for label printing or fixed-width displays.

Author: okdarnoc
License: MIT
Repository: https://github.com/okdarnoc/Address-Formatter-for-CSV-Files
"""

import csv
import sys
from pathlib import Path

try:
    from PIL import ImageFont, ImageDraw, Image
except ImportError:
    print("Error: Pillow library is required.")
    print("Install it with: pip install Pillow")
    sys.exit(1)


# =============================================================================
# Constants
# =============================================================================

DEFAULT_DPI = 96
DEFAULT_FONT = "arial"
DEFAULT_FONT_SIZE = 12


# =============================================================================
# Font Handling
# =============================================================================

def get_system_font(font_name: str = DEFAULT_FONT, font_size: int = DEFAULT_FONT_SIZE) -> ImageFont.FreeTypeFont:
    """
    Load a font with cross-platform support.
    
    Searches common font directories on Windows, macOS, and Linux.
    Falls back to default font if specified font is not found.
    
    Args:
        font_name: Name of the font (e.g., 'arial') or full path to .ttf file
        font_size: Font size in points
        
    Returns:
        Loaded FreeTypeFont object
    """
    font_paths = [
        # Windows
        f"C:/Windows/Fonts/{font_name}.ttf",
        f"C:/Windows/Fonts/{font_name.lower()}.ttf",
        f"C:/Windows/Fonts/{font_name.upper()}.ttf",
        # macOS
        f"/Library/Fonts/{font_name}.ttf",
        f"/Library/Fonts/{font_name}.ttc",
        f"/System/Library/Fonts/{font_name}.ttf",
        f"/System/Library/Fonts/{font_name}.ttc",
        f"/System/Library/Fonts/Supplemental/{font_name}.ttf",
        # Linux
        f"/usr/share/fonts/truetype/{font_name.lower()}/{font_name}.ttf",
        f"/usr/share/fonts/truetype/{font_name.lower()}/{font_name.lower()}.ttf",
        f"/usr/share/fonts/TTF/{font_name}.ttf",
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Common fallback
        # Current directory
        f"{font_name}.ttf",
        f"{font_name}",
    ]
    
    # Try each potential path
    for path in font_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    
    # Try loading by name directly (works on some systems)
    try:
        return ImageFont.truetype(font_name, font_size)
    except OSError:
        pass
    
    # Last resort: use default font
    print(f"Warning: Could not load '{font_name}' font. Using default font.")
    print("         Text width calculations may be less accurate.")
    return ImageFont.load_default()


# =============================================================================
# Text Measurement
# =============================================================================

def calculate_text_width(text: str, font: ImageFont.FreeTypeFont) -> float:
    """
    Calculate the pixel width of text using the specified font.
    
    Args:
        text: The text string to measure
        font: The font to use for measurement
        
    Returns:
        Width of the text in pixels
    """
    dummy_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    return draw.textlength(text, font=font)


# =============================================================================
# Address Processing
# =============================================================================

def split_address_line(
    address: str,
    font: ImageFont.FreeTypeFont,
    max_width: float,
    delimiter: str = ", "
) -> list:
    """
    Split an address into multiple lines that fit within max_width.
    
    Intelligently breaks at delimiter positions (typically ", ") to keep
    address components together. Handles edge cases like empty addresses
    and overly long single components.
    
    Args:
        address: The full address string to split
        font: The font used for width calculation
        max_width: Maximum width in pixels for each line
        delimiter: The delimiter used between address parts (default: ", ")
        
    Returns:
        List of address lines, each fitting within max_width
    """
    # Handle empty or whitespace-only addresses
    if not address or not address.strip():
        return [address]
    
    parts = address.split(delimiter)
    lines = []
    current_line = ""
    
    for i, part in enumerate(parts):
        # Determine what to add (include delimiter except for last part)
        is_last_part = (i == len(parts) - 1)
        addition = part + ("" if is_last_part else delimiter)
        test_line = current_line + addition
        
        if calculate_text_width(test_line, font) <= max_width:
            # Part fits on current line
            current_line = test_line
        else:
            # Current line is full, save it and start new line
            if current_line:
                lines.append(current_line.rstrip(delimiter + " "))
            
            # Check if the part itself is too long for a single line
            if calculate_text_width(addition, font) > max_width:
                # Split long parts by word as fallback
                words = part.split()
                current_line = ""
                for j, word in enumerate(words):
                    test_word = current_line + word + " "
                    if calculate_text_width(test_word, font) <= max_width:
                        current_line = test_word
                    else:
                        if current_line:
                            lines.append(current_line.strip())
                        current_line = word + " "
                
                # Add delimiter back if not last part
                if not is_last_part:
                    current_line = current_line.rstrip() + delimiter
            else:
                current_line = addition
    
    # Add any remaining text
    if current_line:
        lines.append(current_line.rstrip(delimiter + " "))
    
    return lines if lines else [address]


# =============================================================================
# Unit Conversion
# =============================================================================

def cm_to_pixels(cm: float, dpi: int = DEFAULT_DPI) -> float:
    """
    Convert centimeters to pixels at the specified DPI.
    
    Args:
        cm: Width in centimeters
        dpi: Dots per inch (default: 96 for screen, use 300 for print)
        
    Returns:
        Width in pixels
    """
    return cm * dpi / 2.54


# =============================================================================
# User Input Helpers
# =============================================================================

def get_input(prompt: str, default=None, converter=str, validator=None):
    """
    Get user input with optional default value, type conversion, and validation.
    
    Args:
        prompt: The prompt to display to the user
        default: Default value if user presses Enter (None = required field)
        converter: Function to convert string input to desired type
        validator: Function that returns True if value is valid
        
    Returns:
        The validated and converted user input
    """
    while True:
        if default is not None:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()
            if not user_input:
                print("This field is required. Please enter a value.")
                continue
        
        try:
            value = converter(user_input)
            if validator:
                is_valid = validator(value)
                if not is_valid:
                    continue
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def get_file_path(prompt: str, must_exist: bool = True) -> Path:
    """
    Get and validate a file path from user input.
    
    Args:
        prompt: The prompt to display
        must_exist: If True, validate that the file exists
        
    Returns:
        Path object for the specified file
    """
    while True:
        path_str = input(f"{prompt}: ").strip()
        if not path_str:
            print("Please enter a file path.")
            continue
        
        # Handle quoted paths (from drag-and-drop)
        path_str = path_str.strip('"\'')
        path = Path(path_str)
        
        if must_exist and not path.exists():
            print(f"File not found: {path}")
            print("Please check the path and try again.")
            continue
        
        return path


# =============================================================================
# CSV Processing
# =============================================================================

def preview_csv_columns(file_path: Path) -> list:
    """
    Read and return the column headers from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List of column header names, or empty list if unable to read
    """
    try:
        with open(file_path, mode='r', encoding='utf-8', newline='') as f:
            # Read sample for dialect detection
            sample = f.read(8192)
            f.seek(0)
            
            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                dialect = csv.excel
            
            reader = csv.reader(f, dialect)
            headers = next(reader, None)
            return headers if headers else []
    except Exception as e:
        print(f"Warning: Could not read CSV headers: {e}")
        return []


def process_csv(
    input_path: Path,
    output_path: Path,
    font: ImageFont.FreeTypeFont,
    max_width_px: float,
    address_column: int,
    delimiter: str = ", "
) -> tuple:
    """
    Process a CSV file, splitting addresses in the specified column.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file
        font: Font for text measurement
        max_width_px: Maximum line width in pixels
        address_column: Column index containing addresses (0-based)
        delimiter: Address part delimiter
        
    Returns:
        Tuple of (rows_processed, rows_modified)
    """
    rows_processed = 0
    rows_modified = 0
    
    with open(input_path, mode='r', encoding='utf-8', newline='') as infile:
        # Detect CSV dialect
        sample = infile.read(8192)
        infile.seek(0)
        
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel
        
        reader = csv.reader(infile, dialect)
        
        with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, dialect)
            
            # Process header row
            try:
                headers = next(reader)
                writer.writerow(headers)
            except StopIteration:
                print("Warning: Empty CSV file.")
                return 0, 0
            
            # Validate column index
            if address_column >= len(headers):
                raise ValueError(
                    f"Column index {address_column} is out of range. "
                    f"CSV has {len(headers)} columns (indices 0-{len(headers)-1})."
                )
            
            # Process data rows
            for row in reader:
                rows_processed += 1
                
                if len(row) > address_column:
                    original = row[address_column]
                    split_lines = split_address_line(original, font, max_width_px, delimiter)
                    modified = '\n'.join(split_lines)
                    
                    if modified != original:
                        rows_modified += 1
                        row[address_column] = modified
                
                writer.writerow(row)
    
    return rows_processed, rows_modified


# =============================================================================
# Main Program
# =============================================================================

def main():
    """Main interactive entry point."""
    
    # Display header
    print()
    print("=" * 60)
    print("  📬 Address Formatter for CSV Files")
    print("=" * 60)
    print()
    
    # Get input file
    input_path = get_file_path("Enter the path to the CSV file")
    
    # Preview columns to help user
    headers = preview_csv_columns(input_path)
    if headers:
        print("\n📋 CSV Columns found:")
        for i, header in enumerate(headers):
            print(f"   {i}: {header}")
        print()
    
    # Get column number
    def validate_column(x):
        if x < 0:
            print("Column number must be 0 or greater.")
            return False
        if headers and x >= len(headers):
            print(f"Column {x} doesn't exist. Valid range: 0-{len(headers)-1}")
            return False
        return True
    
    address_column = get_input(
        "Enter the column number containing the addresses",
        converter=int,
        validator=validate_column
    )
    
    # Get font settings
    font_name = get_input("Enter the font name", default=DEFAULT_FONT)
    font_size = get_input(
        "Enter the font size",
        default=DEFAULT_FONT_SIZE,
        converter=int,
        validator=lambda x: x > 0 or print("Font size must be positive.")
    )
    
    # Get max width
    max_width_cm = get_input(
        "Enter the maximum line width in cm",
        converter=float,
        validator=lambda x: x > 0 or print("Width must be greater than 0.")
    )
    
    # Get DPI with helpful context
    print("\n💡 DPI Guide: 96 for screen, 300 for print")
    dpi = get_input(
        "Enter the DPI (dots per inch)",
        default=DEFAULT_DPI,
        converter=int,
        validator=lambda x: x > 0 or print("DPI must be greater than 0.")
    )
    
    # Get output file (optional)
    default_output = input_path.with_stem(input_path.stem + "_modified")
    output_input = input(f"Enter output file path [{default_output}]: ").strip()
    output_path = Path(output_input) if output_input else default_output
    
    # Convert width to pixels
    max_width_px = cm_to_pixels(max_width_cm, dpi)
    
    # Display summary
    print()
    print("-" * 60)
    print("📝 Settings Summary:")
    print(f"   Input file:  {input_path}")
    print(f"   Output file: {output_path}")
    col_name = f" ({headers[address_column]})" if headers and address_column < len(headers) else ""
    print(f"   Column:      {address_column}{col_name}")
    print(f"   Font:        {font_name} at {font_size}pt")
    print(f"   Max width:   {max_width_cm} cm = {max_width_px:.1f} px @ {dpi} DPI")
    print("-" * 60)
    print()
    
    # Confirm before processing
    confirm = input("Proceed with formatting? (y/n) [y]: ").strip().lower()
    if confirm and confirm not in ('y', 'yes'):
        print("Cancelled.")
        return
    
    print()
    print("⏳ Loading font...")
    try:
        font = get_system_font(font_name, font_size)
        print("   ✓ Font loaded successfully")
    except OSError as e:
        print(f"❌ Error loading font: {e}")
        sys.exit(1)
    
    print("⏳ Processing CSV...")
    try:
        rows_processed, rows_modified = process_csv(
            input_path=input_path,
            output_path=output_path,
            font=font,
            max_width_px=max_width_px,
            address_column=address_column
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        sys.exit(1)
    
    # Success message
    print()
    print("=" * 60)
    print("✅ Complete!")
    print(f"   Processed: {rows_processed} rows")
    print(f"   Modified:  {rows_modified} addresses")
    print(f"   Saved to:  {output_path}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
