# 📬 Address Formatter for CSV Files

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pillow](https://img.shields.io/badge/Pillow-required-green.svg)](https://pillow.readthedocs.io/)

A Python utility that intelligently splits long address fields in CSV files into multiple lines based on a specified maximum text width. Perfect for formatting addresses to fit within label constraints, mail merge templates, or fixed-width display areas.

![Demo](docs/demo.gif)

---

## ✨ Features

- **Smart Line Breaking**: Splits addresses at natural break points (commas) rather than mid-word
- **Font-Aware Measurement**: Uses actual font metrics for accurate width calculation
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Interactive Mode**: User-friendly prompts guide you through the process
- **Column Preview**: Automatically displays CSV columns to help you select the right one
- **Flexible Units**: Specify width in centimeters with configurable DPI
- **CSV Dialect Detection**: Automatically detects delimiter style (comma, semicolon, tab)
- **Non-Destructive**: Creates a new file, preserving your original data

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Understanding DPI](#-understanding-dpi)
- [Examples](#-examples)
- [Configuration Options](#-configuration-options)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/okdarnoc/Address-Formatter-for-CSV-Files.git
cd Address-Formatter-for-CSV-Files
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install Pillow directly:

```bash
pip install Pillow
```

### Step 3: Verify Installation

```bash
python address_splitter.py --help
```

---

## ⚡ Quick Start

1. Place your CSV file in the same directory as the script (or note its full path)
2. Run the script:
   ```bash
   python address_splitter.py
   ```
3. Follow the prompts:
   ```
   Enter the path to the CSV file: customers.csv
   Enter the column number containing the addresses: 2
   Enter the font name [arial]: 
   Enter the font size [12]: 
   Enter the maximum line width in cm: 5
   Enter the DPI [96]: 
   ```
4. Find your formatted file at `customers_modified.csv`

---

## 📖 Usage Guide

### Running the Script

```bash
python address_splitter.py
```

The script will interactively prompt you for:

| Prompt | Description | Example |
|--------|-------------|---------|
| CSV file path | Location of your input file | `data/addresses.csv` |
| Column number | Zero-based index of address column | `2` |
| Font name | TrueType font to use for measurement | `arial` |
| Font size | Font size in points | `12` |
| Max width (cm) | Maximum line width in centimeters | `5.5` |
| DPI | Dots per inch for conversion | `96` or `300` |
| Output path | Where to save the result | `addresses_formatted.csv` |

### Input File Format

Your CSV should have addresses in a single column:

```csv
Name,Company,Address,Phone
John Doe,Acme Corp,"1234 Elm Street, Springfield, IL, 62704",555-0100
Jane Smith,Tech Inc,"5678 Maple Avenue, Smalltown, TX, 78910",555-0200
```

### Output Format

The script creates a new file with addresses split across multiple lines:

```csv
Name,Company,Address,Phone
John Doe,Acme Corp,"1234 Elm Street,
Springfield, IL,
62704",555-0100
Jane Smith,Tech Inc,"5678 Maple Avenue,
Smalltown, TX,
78910",555-0200
```

---

## 📏 Understanding DPI

DPI (Dots Per Inch) affects how centimeters are converted to pixels. Choose based on your use case:

### Quick Reference

| Use Case | Recommended DPI |
|----------|-----------------|
| Screen display (Windows) | 96 |
| Screen display (Mac/Retina) | 144 |
| Standard printing | 300 |
| High-quality printing | 600 |

### How to Find Your DPI

#### For Label Printing
Check your printer or label software settings. Most label printers (DYMO, Zebra, Brother) use **300 DPI**.

#### For Microsoft Word/Excel
Word uses 96 DPI for screen display. If you're doing a mail merge:
- For **screen preview**: use 96 DPI
- For **print output**: use 300 DPI

#### For Label Software
- **Avery Design & Print**: 300 DPI
- **DYMO Label**: 300 DPI
- **Bartender**: Check document properties

#### Not Sure?
1. Start with **96 DPI**
2. Test with a small sample
3. If lines are too long → increase DPI
4. If lines break too early → decrease DPI

### The Math Behind It

```
pixels = (centimeters × DPI) / 2.54

Example: 5 cm at 300 DPI
pixels = (5 × 300) / 2.54 = 590.5 pixels
```

---

## 💡 Examples

### Example 1: Basic Address Formatting

**Input (`addresses.csv`):**
```csv
ID,Name,Full Address
1,John Doe,"123 Main Street, Apartment 4B, New York, NY, 10001, USA"
2,Jane Smith,"456 Oak Avenue, Suite 100, Los Angeles, CA, 90001, USA"
```

**Run:**
```
Enter the path to the CSV file: addresses.csv

CSV Columns found:
  0: ID
  1: Name
  2: Full Address

Enter the column number containing the addresses: 2
Enter the font name [arial]: 
Enter the font size [12]: 
Enter the maximum line width in cm: 4
Enter the DPI [96]: 
```

**Output (`addresses_modified.csv`):**
```csv
ID,Name,Full Address
1,John Doe,"123 Main Street,
Apartment 4B,
New York, NY, 10001,
USA"
2,Jane Smith,"456 Oak Avenue,
Suite 100,
Los Angeles, CA, 90001,
USA"
```

### Example 2: Label Printing at 300 DPI

For printing on 5cm wide labels:

```
Enter the maximum line width in cm: 5
Enter the DPI [96]: 300
```

### Example 3: Different Font Size

Using larger font for readability:

```
Enter the font name [arial]: arial
Enter the font size [12]: 14
Enter the maximum line width in cm: 6
```

---

## ⚙️ Configuration Options

### Supported Fonts

The script searches for fonts in these locations:

| Platform | Font Locations |
|----------|----------------|
| Windows | `C:/Windows/Fonts/` |
| macOS | `/Library/Fonts/`, `/System/Library/Fonts/` |
| Linux | `/usr/share/fonts/truetype/` |

Common fonts that work well:
- `arial` (Windows default)
- `helvetica` (macOS)
- `DejaVuSans` (Linux)

### CSV Dialect Support

The script automatically detects:
- Comma-separated (`,`)
- Semicolon-separated (`;`)
- Tab-separated (`\t`)
- Custom quote characters

---

## 🔧 Troubleshooting

### "Font not found" Error

**Problem:** The script can't locate the specified font.

**Solutions:**
1. Use the full path to the font file:
   ```
   Enter the font name: C:/Windows/Fonts/arial.ttf
   ```
2. Try a different font:
   ```
   Enter the font name: DejaVuSans
   ```
3. Copy a `.ttf` file to the script directory

### Lines Not Breaking Correctly

**Problem:** Lines are too long or too short.

**Solutions:**
1. **Lines too long**: Increase the DPI value
2. **Lines too short**: Decrease the DPI value
3. **Verify your target application's DPI settings**

### CSV Encoding Issues

**Problem:** Special characters appear corrupted.

**Solutions:**
1. Ensure your CSV is saved as UTF-8
2. In Excel: Save As → CSV UTF-8

### Column Index Out of Range

**Problem:** Error about column index being invalid.

**Solution:** Column numbers start at 0. If your address is in the 3rd column, enter `2`.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Address-Formatter-for-CSV-Files.git
cd Address-Formatter-for-CSV-Files

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Pillow](https://pillow.readthedocs.io/) for image and text processing
- All contributors who have helped improve this project

---

## 📞 Support

- **Bug Reports**: [Open an issue](https://github.com/okdarnoc/Address-Formatter-for-CSV-Files/issues)
- **Feature Requests**: [Open an issue](https://github.com/okdarnoc/Address-Formatter-for-CSV-Files/issues)
- **Questions**: [Start a discussion](https://github.com/okdarnoc/Address-Formatter-for-CSV-Files/discussions)

---

Made with ❤️ for easier address formatting
