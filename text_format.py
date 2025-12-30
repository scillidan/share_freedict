# Authors: DeepSeek🧙‍♂️, scillidan🤡
# Usage: python text_format.py <input_file> <output_file>

import re
import sys

def process_line(line):
    # Step 1: Remove all <div> and </div> tags
    line = re.sub(r'<div>|</div>', '', line)

    # Step 2: Convert /<font color="gray"> to <small> and </font>/ to </small>
    line = re.sub(r'/<font color="gray">', '<small>', line)
    line = re.sub(r'</font>/', '</small>', line)

    # Step 3: Convert \n, <br> to <br />, remove repeated
    line = line.replace('\\n', '<br />')
    line = line.replace('<br>', '<br />')
    line = re.sub(r'(<br\s*/?>\s*)+', '<br />', line)

    # Step 4: Remove class="grammar" from <font class="grammar" color="green">
    line = re.sub(r'<font class="grammar" color="green">', '<font color="green">', line)

    # Step 5: Add <br /> after specific elements
    # Add <br /> after pronunciation (</small>)
    line = re.sub(r'(</small>)(?=\s*[^<])', r'\1<br />', line)
    line = re.sub(r'</small><br />, <small>', '</small>, <small>', line)

    # Add <br /> after grammar tag
    line = re.sub(r'(</font>)(?=\s*[A-Z(])', r'\1<br />', line)

    # Add <br /> before English definition (starts with capital letter or parenthesis)
    line = re.sub(r'(?<=[>])(?=\s*[A-Z(])', '<br />', line)

    # Add <br /> after English definition (before Chinese translation)
    line = re.sub(r'(?<=[a-z.])(?=\s*[\u4e00-\u9fff])', '<br />', line)

    # Clean up: remove extra spaces and fix multiple <br />
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'(<br />\s*)+', '<br />', line)
    line = line.strip()

    return line

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            # Split by tab to separate word from definition, but keep the tab
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                word, definition = parts
                processed_definition = process_line(definition)
                # Keep the tab between word and definition
                f_out.write(f"{word}\t{processed_definition}\n")
            else:
                f_out.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input output")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)