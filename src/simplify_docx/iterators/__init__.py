"""
Docx Iterators
"""
# generic machinery
from .generic import xml_iter

# iterator definitions (for side effects only):
import importlib 
importlib.import_module(".table",__package__)
importlib.import_module(".run",__package__)
importlib.import_module(".paragraph",__package__)
importlib.import_module(".body",__package__)
importlib.import_module(".document",__package__)
