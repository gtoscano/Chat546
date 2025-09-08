import csv
import os
import re
import sys
# If uses fish, the user can execute all files with
#for file in faculty/txt_files/*.txt
#         python3 read_txt_profiles.py "$file" profiles.csv
#     end

def parse_faculty_file(filename):
    """
    Parses a text file for a single faculty member and returns a dictionary
    with the specified fields.
    """
    # Desired columns (in the order you want them in the CSV)
    columns = [
        "Faculty Profile",
        "Position",
        "Department",
        "School",
        "Email",
        "Phone",
        "Education",
        "Research Interests and Expertise",
        "Biography",
        "Five Selected Papers",
        "Professional Activities"
    ]
    
    # Initialize dictionary with empty strings
    data = {col: "" for col in columns}

    # Define a helper to check if a line starts with a heading
    # that includes a colon (e.g., "Department:", "School:", etc.).
    # We'll handle "Faculty Profile:" separately.
    # For "Professional Activities", we want to match partial text as well
    # because the line might read "Professional Activities (please ...)".
    def get_heading(line):
        # Exact matches with a colon:
        known_headings = [
            "Department:",
            "School:",
            "Email:",
            "Phone:",
            "Education:",
            "Research Interests and Expertise:",
            "Biography:",
            "Five Selected Papers:"
        ]
        # Check partial match for "Professional Activities"
        # e.g. "Professional Activities (please..."
        if line.strip().lower().startswith("professional activities"):
            return "Professional Activities"
        
        for h in known_headings:
            if line.strip().startswith(h):
                # Return the heading without the colon for normal headings
                return h.replace(":", "")
        return None

    # Read the entire file into lines
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    current_heading = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 1) Detect "Faculty Profile:"
        if line.startswith("Faculty Profile:"):
            # Grab everything after "Faculty Profile:"
            # e.g. "Faculty Profile: Arash Massoudieh" -> "Arash Massoudieh"
            profile_value = line.split("Faculty Profile:")[1].strip()
            data["Faculty Profile"] = profile_value

            # Move to next line and check if it might be the Position
            i += 1
            if i < len(lines):
                next_line = lines[i].strip()
                # If next_line is not empty and doesn't match any heading,
                # we treat it as the "Position".
                heading_match = get_heading(next_line)
                if next_line and (not heading_match) and \
                   (not next_line.startswith("Faculty Profile:")):
                    data["Position"] = next_line
                    i += 1
            continue

        # 2) If the line matches any known heading, set current_heading
        heading = get_heading(line)
        if heading:
            current_heading = heading
            # If it's not "Professional Activities", the format is "Heading: value"
            # so let's see if there's a colon we can split on:
            if ":" in line:
                # e.g. "Department: Civil and Environmental Engineering"
                # We'll split on the first colon.
                parts = line.split(":", 1)  # split only on the first colon
                # The key is parts[0], the value is parts[1]
                # (though we've already used heading above).
                value = parts[1].strip()
                data[current_heading] = value
            else:
                # e.g. "Professional Activities ..." (no direct colon to parse right away)
                data[current_heading] = ""
            i += 1
            
            # For headings that can have multi-line content (i.e., all except the basic single-liners):
            # We'll capture everything until the next recognized heading or end of file.
            # But some headings *can* be single line, so let's continue reading carefully.
            
            # Keep reading lines until we detect a new heading or run out of lines.
            multiline_content = []
            while i < len(lines):
                peek_line = lines[i].strip()
                # If this line is a new heading, we break
                if get_heading(peek_line) is not None or \
                   peek_line.startswith("Faculty Profile:"):
                    break
                multiline_content.append(peek_line)
                i += 1
            # Join collected lines (with a space or newline as desired):
            # For nicer formatting, let's join with newlines.
            # If there was a single-line value already, we prepend it:
            existing_val = data[current_heading].strip()
            if existing_val:
                # If we already have something (like after the colon),
                # combine it with new lines
                combined_val = existing_val + "\n" + "\n".join(multiline_content)
            else:
                combined_val = "\n".join(multiline_content)
            data[current_heading] = combined_val.strip()
            
            # Because we did a while loop inside, we continue here
            continue
        
        # If we reach here, we simply move on
        i += 1

    # Return the dictionary
    return data

def append_or_create_csv(output_filename, columns, faculty_data):
    # Check if the file already exists
    file_exists = os.path.isfile(output_filename)
    
    # Use append mode if the file exists; otherwise write mode
    mode = 'a' if file_exists else 'w'
    
    with open(output_filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # If the file doesn't exist, we need to write the header first
        if not file_exists:
            writer.writerow(columns)
        
        # Then write the data row
        writer.writerow([faculty_data[col] for col in columns])

def main(input_filename, output_filename):
    faculty_data = parse_faculty_file(input_filename)
    
    # Define the order of columns
    columns = [
        "Faculty Profile",
        "Position",
        "Department",
        "School",
        "Email",
        "Phone",
        "Education",
        "Research Interests and Expertise",
        "Biography",
        "Five Selected Papers",
        "Professional Activities"
    ]
    
    # Print CSV header + row to stdout
    append_or_create_csv(output_filename, columns, faculty_data)
    #writer = csv.writer(open(output_filename, "w+", newline="", encoding="utf-8"))
    #writer.writerow(columns)
    #writer.writerow([faculty_data[col] for col in columns])
    
    print(f"CSV output written to {output_filename}")

if __name__ == "__main__":
    # Readh input_filename and output_filename from the parameter inputs
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    main(input_filename, output_filename)
