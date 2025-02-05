"""
Module for storing and retrieving code units in Redis
"""
import logging
from typing import Optional
from pathlib import Path
import json
import redis
import torch
import yaml
from sentence_transformers import SentenceTransformer
from code2code.utils.CodeUnit import CodeUnit

# Load configuration from config.yaml
config_path = Path(__file__).resolve().parent.parent / "config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

class CodeMemory:
    def __init__(self, redis_host=config['redis']['host'], redis_port=config['redis']['port']):
        # Initialize Redis client
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        # Load the sentence transformer model for generating embeddings
        self.embedding_model = SentenceTransformer(config['sentence_transformer_model']['name'])
        
    def store_code_unit(self, unit: CodeUnit):
        """Store a code unit in Redis with its embeddings"""
        # Create a unique key based on unit properties
        key = f"{unit.language}:{unit.unit_type}:{unit.name}"

        logging.debug(f"Storing code unit in Redis with key: {key}")
        
        # Generate embeddings for the code content
        embeddings = self.embedding_model.encode(unit.content)
        
        # Prepare the code unit data for storage
        unit_data = {
            "content": unit.content,
            "file_path": unit.file_path,
            "language": unit.language,
            "unit_type": unit.unit_type,
            "name": unit.name,
            "dependencies": json.dumps(unit.dependencies),
            "embeddings": json.dumps(embeddings.tolist())
        }
        
        # Convert the dictionary to a format that Redis accepts
        unit_data_str = {k: str(v) for k, v in unit_data.items()}
        
        # Store the code unit data in Redis
        self.redis_client.hset(key, mapping=unit_data_str)
    
    def find_similar_unit(self, content: str, threshold: float = 0.8) -> Optional[CodeUnit]:
        """Find a similar code unit in Redis based on content similarity"""
        # Generate embeddings for the query content
        query_embedding = self.embedding_model.encode(content)
        
        # Search through stored units in Redis
        for key in self.redis_client.keys("*"):
            stored_unit = self.redis_client.hgetall(key)
            if not stored_unit:
                continue
                
            # Retrieve stored embeddings and calculate similarity
            stored_embedding = torch.tensor(json.loads(stored_unit[b'embeddings']))
            similarity = torch.cosine_similarity(
                torch.tensor(query_embedding), 
                stored_embedding, 
                dim=0
            )
            
            # If similarity exceeds the threshold, return the stored code unit
            if similarity > threshold:
                return CodeUnit(
                    content=stored_unit[b'content'].decode(),
                    file_path=stored_unit[b'file_path'].decode(),
                    language=stored_unit[b'language'].decode(),
                    unit_type=stored_unit[b'unit_type'].decode(),
                    name=stored_unit[b'name'].decode(),
                    dependencies=json.loads(stored_unit[b'dependencies'])
                )
        return None