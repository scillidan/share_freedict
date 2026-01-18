# Usage: python text_format.py <input_file> <output_file>

import sys
import re
from html import unescape

def match_remove(text):
    # Add <br> before <div> tags if not already preceded by <br>
    text = re.sub(r'(?<!<br>)<div>', '<br><div>', text, flags=re.IGNORECASE)
    # Add <br> after </div> tags if not already preceded by <br>
    text = re.sub(r'(?<!<br>)</div>', '</div><br>', text, flags=re.IGNORECASE)
    # Remove all <div> and </div> tags
    text = re.sub(r'<div>|</div>', '', text, flags=re.IGNORECASE)
    return text

def match_replace(text):
    # Replace /<font color="gray"></font>/... with <small>...</small>
    def replace_prons(match):
        content = match.group(0)
        prons = re.findall(r'/<font\s+color\s*=\s*["\']gray["\']\s*>(.*?)</font>/', 
                          content, flags=re.IGNORECASE)
        if not prons:
            return content
        formatted_prons = []
        for pron in prons:
            if pron.startswith('[') and pron.endswith(']'):
                formatted_prons.append(pron)
            else:
                formatted_prons.append(f'/{pron}/')
        return f'<small>{" ".join(formatted_prons)}</small>'
    text = re.sub(r'(?:/<font\s+color\s*=\s*["\']gray["\']\s*>.*?</font>/\s*[,\s]*)+',
                 replace_prons, text, flags=re.IGNORECASE)
    # Replace <font class="grammar" color="green"> with <span style="color:green;">
    text = re.sub(r'<font class="grammar" color="green">', '<span style="color:green;">', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*<br>\s*<font style="color:green;">', '<span style="color:green;">', text, flags=re.IGNORECASE)
    text = re.sub(r'</font>', '</span>', text, flags=re.IGNORECASE)
    # Make <ol><li></li></ol> compact
    text = text.replace('<ol>', '<ol style="padding-left: 0; margin: 0;list-style: none;">')
    text = text.replace('<li>', '<li style="margin: 0; padding: 0;">')
    text = re.sub(r'</ol>\s*<br>', '</ol>', text, flags=re.IGNORECASE)
    text = re.sub(r'<li\s+style\s*=\s*["\']margin:\s*0;\s*padding:\s*0;["\']>\s*(<br>\s*)+', 
                  '<li style="margin: 0; padding: 0;">', 
                  text, flags=re.IGNORECASE)
    # Replace \n with <br>
    text = text.replace('\\n', '<br>')
    # Replace repeated <br> with <br>
    text = re.sub(r'(<br>\s*)+', '<br>', text)
    # Replace repeated ' ' with ' '
    text = re.sub(r' {2,}', ' ', text)
    return text

def format(line):
    if '\t' not in line:
        return line.strip()
    parts = line.split('\t', 1)
    word = parts[0]
    meaning = parts[1].strip()

    meaning = match_remove(meaning)
    meaning = match_replace(meaning)
    meaning = unescape(meaning)
    meaning = meaning.strip()
    # Remove <br> if it appears at the start of the meaning
    meaning = re.sub(r'^<br>', '', meaning)
    # Remove multiple consecutive <br> tags at the start
    meaning = re.sub(r'^(<br>)+', '', meaning)
    meaning = meaning.strip()

    result = f"{word}\t{meaning}"
    return result

def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Format each line
    results = [format(line) for line in lines]

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

if __name__ == '__main__':
    main()