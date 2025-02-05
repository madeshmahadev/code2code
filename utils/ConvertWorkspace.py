"""
Module to convert all files in a project from source language to target language
"""
import os
import logging
from code2code.utils.CodeMemory import CodeMemory
from code2code.utils.CodeConverter import CodeConverter

class ConvertWorkspace:
    def __init__(self, model_path: str):
        self.memory = CodeMemory()
        self.converter = CodeConverter(model_path, self.memory)

    def convert_workspace(
        self, source_dir: str, target_dir: str, source_language: str, target_language: str
    ):
        """Convert all files in a project from source language to target language"""
        
        logging.debug(f"Starting conversion from {source_language} to {target_language}")

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Process each source file
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(f".{source_language}"):
                    source_path = os.path.join(root, file)
                    logging.debug(f"Processing file: {source_path}")
                    relative_path = os.path.relpath(source_path, source_dir)
                    target_path = os.path.join(
                        target_dir,
                        relative_path.replace(f".{source_language}", f".{target_language}")
                    )
                    
                    # Parse the source file into code units
                    units = self.converter.parse_source_file(source_path, source_language)
                    
                    # Convert each unit
                    converted_code = []
                    for unit in units:
                        converted = self.converter.convert_code(unit, target_language)
                        converted_code.append(converted)
                    
                    # Write converted code to target file
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'w') as f:
                        f.write('\n\n'.join(converted_code))

        # Clear Redis data
        self.memory.redis_client.flushdb()
        logging.debug("Cleared Redis data")