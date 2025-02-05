"""
Main module for the code2code CLI
"""
import logging
import typer
import sys
from pathlib import Path

# Add the parent directory of 'code2code' to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from code2code.utils.ConvertWorkspace import ConvertWorkspace

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a Typer app
app = typer.Typer()

# Define the convert command
@app.command()
def convert(
    source_dir: str, target_dir: str, source_language: str, target_language: str, model_path: str="mistral-nemo:12b"
):
    """Convert all files in a project from source language to target language"""
    workspace = ConvertWorkspace(model_path=model_path)
    workspace.convert_workspace(source_dir, target_dir, source_language, target_language)

if __name__ == "__main__":
    app()