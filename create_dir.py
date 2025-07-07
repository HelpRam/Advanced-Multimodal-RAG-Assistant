import os

# Define the directory structure
structure = {
    "multimodal_rag_assistant": {
        "data": {
            "raw": ["document1.pdf", "image1.png", "report.docx"],
            "processed": [],
        },
        "src": {
            "data_ingestion": ["__init__.py", "data_loader.py", "text_chunker.py", "multimodal_parser.py"],
            "embeddings": ["__init__.py", "embedding_generator.py"],
            "vector_db": ["__init__.py", "vector_store_manager.py"],
            "retrieval": ["__init__.py", "retriever.py"],
            "generation": ["__init__.py", "generator.py"],
            "evaluation": ["__init__.py", "evaluator.py"],
            "core": ["__init__.py", "rag_pipeline.py"],
        },
        "notebooks": ["exploration.ipynb", "prototyping.ipynb"],
        "app": ["__init__.py", "main.py"],
        "config": ["settings.py"],
        ".env": "",
        "requirements.txt": "",
        "README.md": "",
    }
}

def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for item in content:
                item_path = os.path.join(path, item)
                with open(item_path, 'w') as f:
                    f.write("")  # Create an empty file
        elif isinstance(content, str):
            with open(os.path.join(base_path, name), 'w') as f:
                f.write("")  # Create an empty file

# Run the function
create_structure(".", structure)
print("Directory structure created.")
