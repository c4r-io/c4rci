import os
from subprocess import run
from pytest import fixture
import nbformat

@fixture
def cmd():
    return ["python", "scripts/md_process.py"]

def md_to_ipynb_conversion_test(cmd, md_file):
    # Construct full path for .md and .ipynb files
    md_path = os.path.join("units", md_file)
    ipynb_file = md_file.replace('.md', '.ipynb')
    ipynb_path = os.path.join("units", ipynb_file)

    # Delete the .ipynb file if it exists
    if os.path.exists(ipynb_path):
        os.remove(ipynb_path)
    
    # Run the script to process .md files
    run(cmd)
    
    # Check if the .ipynb file was created
    assert os.path.exists(ipynb_path), f"File {ipynb_path} not generated"

    # Return the content of the generated .ipynb file
    with open(ipynb_path, 'r') as f:
        ipynb_content = f.read()

    return ipynb_content

def test_simple_conversion(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "simple_conversion_test.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert "Simple Conversion Test" in nb.cells[0].source

def test_multiple_sections(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "multiple_sections_test.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 4
    assert all(cell.cell_type == 'markdown' for cell in nb.cells)
    assert "Multiple Sections Test" in nb.cells[0].source
    assert "Introduction" in nb.cells[1].source
    assert "Another Section" in nb.cells[2].source

def test_default_embedding(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "default_embedding_test.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 4
    assert nb.cells[0].cell_type == 'markdown'
    assert "Default Embedding Test" in nb.cells[0].source
    assert '<iframe src="https://jackliddy.github.io/designTest1" width="600" height="400"></iframe>' in nb.cells[2].source

def test_custom_dimension_embedding(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "custom_dimension_embedding_test.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 4
    assert nb.cells[0].cell_type == 'markdown'
    assert "Custom Dimension Embedding Test" in nb.cells[0].source
    assert '<iframe src="https://jackliddy.github.io/designTest1" width="800" height="500"></iframe>' in nb.cells[2].source

def test_regular_link(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "regular_link_test.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 4
    assert nb.cells[0].cell_type == 'markdown'
    assert "Regular Link Test" in nb.cells[0].source
    assert '[This should remain a regular link](https://jackliddy.github.io/designTest1)' in nb.cells[2].source

# ... Add more tests as needed
