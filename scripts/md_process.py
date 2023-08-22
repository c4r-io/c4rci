import os
import re
import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

def md_to_notebook(md_content):
    # Start with an empty notebook
    notebook = new_notebook()

    # Split the markdown content into "cells" at every double newline
    # This is just a basic approach; you might want to refine this
    cells = md_content.split('\n\n')

    for cell in cells:
        # Replace links with iframes if they match the pattern
        cell = replace_links_with_iframes(cell)
        
        # Add the markdown cell to the notebook
        notebook.cells.append(new_markdown_cell(cell))

    return notebook

def replace_links_with_iframes(content):
    # This is a simple example. Replace the regex pattern with whatever you need.
    pattern = r'https://www\.example\.com/[\w/]+'
    replacement = r'<iframe src="\g<0>" width="600" height="400"></iframe>'

    return re.sub(pattern, replacement, content)

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r') as f:
                    md_content = f.read()

                notebook = md_to_notebook(md_content)

                # Save as .ipynb
                with open(os.path.join(root, file.replace('.md', '.ipynb')), 'w') as f:
                    f.write(nbformat.writes(notebook))

if __name__ == '__main__':
    main()
