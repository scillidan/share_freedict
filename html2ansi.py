# Write by GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python html2ansi.py <input_file> <output_file>

import sys

html_to_ansi = {
    '<font color="gray">': "\033[38;5;245m",
    '<font class="grammar" color="green">': "\033[32m",
    "</font>": "\033[0m",
    "<br />": r"\n",
}

def convert_html_to_ansi(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            for html_tag, ansi_code in html_to_ansi.items():
                content = content.replace(html_tag, ansi_code)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html2ansi.py input_file output_file", file=sys.stderr)
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_html_to_ansi(input_file, output_file)