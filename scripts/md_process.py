import os
import re
import sys
import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook


def md_to_notebook(md_content):
    # Start with an empty notebook
    notebook = new_notebook()

    # Split the markdown content into "cells" at every double newline
    cells = md_content.split('\n\n')

    for cell in cells:
        # Replace links with iframes if they match the pattern
        cell = replace_links_with_iframes(cell)
        
        # Add the markdown cell to the notebook
        notebook.cells.append(new_markdown_cell(cell))

    return notebook


def replace_links_with_iframes(content):
    # This pattern matches links labeled [Embed] or [Embed-widthxheight]
    pattern = r'\[Embed(?:-(\d+)x(\d+))?\]\((https?://[^\)]+)\)'
    
    def repl(match):
        width = match.group(1) or '600'
        height = match.group(2) or '400'
        url = match.group(3)
        return f'<iframe src="{url}" width="{width}" height="{height}"></iframe>'
    
    return re.sub(pattern, repl, content)


def convert_md_to_ipynb(input_md):
    # Read the markdown content from the provided path
    with open(input_md, 'r') as f:
        md_content = f.read()

    # Convert the markdown content to a notebook
    notebook = md_to_notebook(md_content)

    # Construct the output notebook's path
    output_ipynb = input_md.replace('.md', '.ipynb')

    # Save as .ipynb
    with open(output_ipynb, 'w') as f:
        f.write(nbformat.writes(notebook))

    return output_ipynb


if __name__ == "__main__":
    input_md_path = os.path.abspath(sys.argv[1])
    output_notebook = convert_md_to_ipynb(input_md_path)
    print(output_notebook)  # This is captured in the GitHub action script.
