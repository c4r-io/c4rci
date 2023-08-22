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
    ipynb_content = md_to_ipynb_conversion_test(cmd, "test1.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert "Test 1: Simple Conversion" in nb.cells[0].source

def test_embedding_urls(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "test2.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'markdown'
    assert "Test 2: Embedding URLs" in nb.cells[0].source
    assert nb.cells[1].cell_type == 'code'
    assert "iframe" in nb.cells[1].source

def test_multiple_sections(cmd):
    ipynb_content = md_to_ipynb_conversion_test(cmd, "test3.md")
    nb = nbformat.reads(ipynb_content, as_version=4)
    
    assert len(nb.cells) == 3
    assert all(cell.cell_type == 'markdown' for cell in nb.cells)
    assert "Test 3: Multiple Sections" in nb.cells[0].source
    assert "Introduction" in nb.cells[1].source
    assert "Another Section" in nb.cells[2].source

# ... Add more tests as needed
