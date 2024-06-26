import csv
from PIL import ImageFont, ImageDraw, Image

# Function to calculate the width of the text in the specified font
def text_width(text, font):
    # Create a new image with arbitrary size
    image = Image.new('RGB', (1000, 1000))
    # Initialize the Draw object
    draw = ImageDraw.Draw(image)
    # Return the width of the given text using the specified font
    return draw.textlength(text, font=font)

# Function to split address lines
def split_address_line(address, font, max_width):
    # Split the address into parts using ", " as the delimiter
    parts = address.split(', ')
    lines = []  # List to store splitted lines of the address
    current_line = ""  # Variable to store the current line being processed
    
    # Iterate through each part of the address
    for part in parts:
        # Check if adding the current part exceeds the maximum width
        if text_width(current_line + part, font) <= max_width:
            current_line += part + ", "  # Add part to the current line
        else:
            # If the current line exceeds the width, add it to lines and start a new line
            lines.append(current_line.rstrip(', '))
            current_line = part + ", "
    
    # Add any remaining text in the current line to lines
    if current_line:
        lines.append(current_line.rstrip(', '))
    
    return lines

def main():
    import os  # Import os module for file path operations

    # Prompt user for input
    csv_file_path = input("Enter the path to the CSV file: ")
    font_size = int(input("Enter the font size: "))
    max_length_cm = float(input("Enter the maximum length per line (in cm): "))
    address_column_number = int(input("Enter the column number containing the addresses (starting from 0): "))

    # Convert cm to pixels (assuming 96 DPI, you can adjust as necessary)
    # 1 cm is approximately 37.8 pixels at 96 DPI
    max_width_px = int(max_length_cm * 37.8)

    # Load the Arial font. Adjust the font path if necessary.
    font = ImageFont.truetype("arial.ttf", font_size)

    # Prepare the output file path by appending "_modified" to the original file name
    output_file_path = os.path.splitext(csv_file_path)[0] + "_modified.csv"

    # Open the input CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:
         
        reader = csv.reader(infile)  # Initialize CSV reader
        writer = csv.writer(outfile)  # Initialize CSV writer

        # Read and write header row
        headers = next(reader)
        writer.writerow(headers)
        
        # Process each row in the input CSV file
        for row in reader:
            if len(row) > address_column_number:
                # Retrieve the original address from the specified column
                original_address = row[address_column_number]
                
                # Split the address into multiple lines within max width
                split_lines = split_address_line(original_address, font, max_width_px)
                
                # Join the split lines with new line characters
                modified_address = '\n'.join(split_lines)
                
                # Replace the original address with the modified address in the row
                row[address_column_number] = modified_address
            
            # Write the modified row to the output CSV file
            writer.writerow(row)

    # Print a message indicating the output file path
    print(f"Modified addresses saved to {output_file_path}")

if __name__ == "__main__":
    # Execute the main function when the script is run directly
    main()
