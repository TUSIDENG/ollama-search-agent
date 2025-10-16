# search_engines/factory.py
from typing import Dict, Type, Optional, List, Any
import importlib
import inspect
import os
from .base_search import BaseSearch
from config import SEARCH_ENGINES


class SearchEngineFactory:
    """Factory class for dynamically creating search engine instances."""
    
    _engines: Dict[str, Dict[str, Any]] = {}
    _search_engines_path = "search_engines"
    
    @classmethod
    def _discover_engines(cls):
        """Dynamically discover all search engine classes in the search_engines directory."""
        if cls._engines:
            return
            
        # Get all Python files in the search_engines directory
        try:
            search_engines_dir = os.path.join(os.path.dirname(__file__))
            for filename in os.listdir(search_engines_dir):
                if filename.endswith('.py') and filename != '__init__.py' and filename != 'factory.py' and filename != 'base_search.py':
                    module_name = filename[:-3]  # Remove .py extension
                    
                    try:
                        # Dynamically import the module
                        module = importlib.import_module(f".{module_name}", package="search_engines")
                        
                        # Find all classes in the module that inherit from BaseSearch
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if (issubclass(obj, BaseSearch) and 
                                obj != BaseSearch and 
                                obj.__module__ == module.__name__):
                                
                                # Use class name without 'Search' suffix as engine name
                                engine_name = name.lower().replace('search', '')
                                if engine_name.endswith('_'):
                                    engine_name = engine_name[:-1]
                                
                                # Store module and class information
                                cls._engines[engine_name] = {
                                    'module': module_name,
                                    'class_name': name,
                                    'class': obj
                                }
                                
                    except ImportError as e:
                        print(f"Warning: Failed to import module {module_name}: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error discovering search engines: {e}")
    
    @classmethod
    def register_engine(cls, engine_name: str, module_path: str, class_name: str):
        """
        Register a new search engine by module path and class name.
        
        Args:
            engine_name: Name to register the engine under
            module_path: Python module path (e.g., "search_engines.google_search")
            class_name: Name of the search engine class
        """
        try:
            module = importlib.import_module(module_path)
            engine_class = getattr(module, class_name)
            
            if not issubclass(engine_class, BaseSearch):
                raise ValueError(f"Class {class_name} must inherit from BaseSearch")
            
            cls._engines[engine_name.lower()] = {
                'module': module_path,
                'class_name': class_name,
                'class': engine_class
            }
            
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to register engine {engine_name}: {e}")
    
    @classmethod
    def create(cls, engine_name: str, **kwargs) -> BaseSearch:
        """
        Create a search engine instance.
        
        Args:
            engine_name: Name of the search engine
            **kwargs: Additional arguments to pass to the search engine constructor
            
        Returns:
            BaseSearch: Instance of the requested search engine
            
        Raises:
            ValueError: If the engine name is not supported
        """
        cls._discover_engines()
        engine_name = engine_name.lower()
        
        if engine_name not in cls._engines:
            available_engines = ", ".join(cls.get_available_engines())
            raise ValueError(
                f"Unsupported search engine: '{engine_name}'. "
                f"Available engines: {available_engines}"
            )
        
        engine_info = cls._engines[engine_name]
        engine_class = engine_info['class']
        
        try:
            return engine_class(**kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Failed to create search engine '{engine_name}': {str(e)}"
            ) from e
    
    @classmethod
    def create_from_config(cls, engine_name: str) -> BaseSearch:
        """
        Create a search engine instance using configuration from config.py.
        
        Args:
            engine_name: Name of the search engine
            
        Returns:
            BaseSearch: Instance of the requested search engine
        """
        return cls.create(engine_name)
    
    @classmethod
    def get_available_engines(cls) -> List[str]:
        """Get list of available search engine names."""
        cls._discover_engines()
        return list(cls._engines.keys())
    
    @classmethod
    def get_engine_config_status(cls, engine_name: str) -> Dict[str, bool]:
        """
        Check if the required configuration for a search engine is available.
        
        Args:
            engine_name: Name of the search engine
            
        Returns:
            Dict[str, bool]: Dictionary with configuration status for each required key
        """
        cls._discover_engines()
        engine_name = engine_name.lower()
        
        if engine_name not in cls._engines:
            print(f"DEBUG: Engine '{engine_name}' not in _engines.")
            return {}
        
        config = SEARCH_ENGINES.get(engine_name, {})
        status = {}
        
        print(f"DEBUG: Checking config status for '{engine_name}'. Config: {config}")
        # Check each required configuration key
        for key, value in config.items():
            status[key] = value is not None and value != ""
            print(f"DEBUG:   Key '{key}': Value present = {status[key]}")
        
        return status
    
    @classmethod
    def is_engine_available(cls, engine_name: str) -> bool:
        """
        Check if a search engine is available (both registered and configured).
        
        Args:
            engine_name: Name of the search engine
            
        Returns:
            bool: True if the engine is available, False otherwise
        """
        cls._discover_engines()
        engine_name = engine_name.lower()
        
        if engine_name not in cls._engines:
            print(f"DEBUG: is_engine_available: Engine '{engine_name}' not registered.")
            return False
        
        # Placeholder is always available
        if engine_name == "placeholder":
            print(f"DEBUG: is_engine_available: '{engine_name}' is placeholder, always available.")
            return True
        
        # Check if required configuration is present
        config_status = cls.get_engine_config_status(engine_name)
        is_available = all(config_status.values())
        print(f"DEBUG: is_engine_available: '{engine_name}' config status: {config_status}, all values present: {is_available}")
        return is_available
    
    @classmethod
    def get_default_engine(cls) -> BaseSearch:
        """
        Get the default search engine based on available configuration.
        
        Returns:
            BaseSearch: Instance of the default search engine
            
        Raises:
            RuntimeError: If no search engine is available
        """
        cls._discover_engines()
        
        # Get all available engines (excluding placeholder)
        available_engines = [
            engine_name for engine_name in cls.get_available_engines()
            if cls.is_engine_available(engine_name) and engine_name != "placeholder"
        ]
        
        # Prioritize Custom Google, then Google
        if "customgoogle" in available_engines:
            return cls.create("customgoogle")
        
        if available_engines:
            # Return the first available engine
            return cls.create(available_engines[0])
        
        # Fallback to placeholder if nothing else is available
        return cls.create("placeholder")
    
    @classmethod
    def get_engine_info(cls, engine_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a search engine.
        
        Args:
            engine_name: Name of the search engine
            
        Returns:
            Dict[str, Any]: Dictionary with engine information
        """
        cls._discover_engines()
        engine_name = engine_name.lower()
        
        if engine_name not in cls._engines:
            return {}
        
        engine_info = cls._engines[engine_name].copy()
        # Remove the class object to make it serializable
        if 'class' in engine_info:
            del engine_info['class']
        
        engine_info['available'] = cls.is_engine_available(engine_name)
        engine_info['config_status'] = cls.get_engine_config_status(engine_name)
        
        return engine_info


# Convenience functions
def create_search_engine(engine_name: str, **kwargs) -> BaseSearch:
    """Convenience function to create a search engine instance."""
    return SearchEngineFactory.create(engine_name, **kwargs)


def get_default_search_engine() -> BaseSearch:
    """Convenience function to get the default search engine."""
    return SearchEngineFactory.get_default_engine()


def list_available_engines() -> List[str]:
    """Convenience function to list available search engines."""
    return SearchEngineFactory.get_available_engines()


def check_engine_availability(engine_name: str) -> Dict[str, bool]:
    """Convenience function to check engine configuration status."""
    return SearchEngineFactory.get_engine_config_status(engine_name)


def register_search_engine(engine_name: str, module_path: str, class_name: str):
    """Convenience function to register a new search engine."""
    SearchEngineFactory.register_engine(engine_name, module_path, class_name)


def get_engine_info(engine_name: str) -> Dict[str, Any]:
    """Convenience function to get engine information."""
    return SearchEngineFactory.get_engine_info(engine_name)
