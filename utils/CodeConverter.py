"""
Module to convert code from one language to another using a language model.
"""
import os
import logging
import re
from typing import List
from pathlib import Path
import ollama

from code2code.utils.CodeMemory import CodeMemory
from code2code.utils.CodeUnit import CodeUnit

class CodeConverter:
    def __init__(self, model_name: str, memory: CodeMemory):
        self.model = model_name  # Model name for the language model
        self.memory = memory  # Memory object to store and retrieve code units
        
    def parse_source_file(self, file_path: str, source_language: str) -> List[CodeUnit]:
        """Parse source file into code units (classes, interfaces, etc.)"""
        with open(file_path, 'r') as f:
            content = f.read()

        # Simple heuristic to determine unit type based on file content
        if 'class ' in content:
            unit_type = 'class'
        elif 'function ' in content or 'def ' in content:
            unit_type = 'function'
        elif 'interface ' in content:
            unit_type = 'interface'
        elif 'enum ' in content:
            unit_type = 'enum'
        else:
            unit_type = 'unknown'
            
        # This is a simplified parser - in practice, you'd want to use a proper
        # parser for the source language (e.g., babel for JavaScript)
        # For now, I have just created a single unit per file
        return [CodeUnit(
            content=content,
            file_path=file_path,
            language=source_language,
            unit_type='unknown',  
            name=Path(file_path).stem,
            dependencies=[]  
        )]
    
    def convert_code(self, unit: CodeUnit, target_language: str) -> str:
        """Convert a code unit to target language using the LLM"""
        # First check if we have a similar conversion in memory
        logging.debug(f"Checking for similar unit in memory for: {unit.name}")

        similar_unit = self.memory.find_similar_unit(unit.content)
        if similar_unit:
            return similar_unit.content
            
        # Prepare prompt for the model
        prompt = f"""Convert this {unit.language} code to {target_language}. Output only the code without any explanations or descriptions.
        Input code:
        {unit.content}

        Output code:"""

        # For main files:
        if unit.name.lower() == 'main':
            prompt = f"""Convert this {unit.language} code to {target_language}. Output only the code without any explanations or descriptions.
        Input code:
        {unit.content}

        Output code:"""

        # Generate conversion using the model
        logging.info(f"Starting code conversion for {unit.name}")
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "max_tokens": 2048
            }
        )

        converted_code = response['response'] 
        converted_code = self.process_converted_code(converted_code, unit.unit_type)

        logging.info(f"Completed code conversion for {unit.name}")
        
        # Store the conversion in memory
        converted_unit = CodeUnit(
            content=converted_code,
            file_path=unit.file_path.replace(unit.language, target_language),
            language=target_language,
            unit_type=unit.unit_type,
            name=unit.name,
            dependencies=unit.dependencies
        )
        logging.debug(f"Storing converted unit: {converted_unit}")
        self.memory.store_code_unit(converted_unit)
        logging.debug("Code unit stored in memory")
        
        return converted_code

    def process_converted_code(self, response, unit_type) -> str:
        """Extract code from the response which could be in markdown format"""
        # Define a regex pattern to match code blocks in markdown
        code_block_pattern = re.compile(r'```(?:\w+)?\s*([\s\S]*?)\s*```')

        # Search for code blocks in the response
        match = code_block_pattern.search(response)
        if match:
            # Extract the code from the first matched code block
            code = match.group(1).strip()
        else:
            # If no code block is found, return the original response
            code = response.strip()

        return code