#!/usr/bin/env python3
"""
Test script for Search Engine Factory
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from search_engines import (
    SearchEngineFactory,
    create_search_engine,
    get_default_search_engine,
    list_available_engines,
    check_engine_availability,
    get_engine_info
)


def test_factory_functionality():
    """Test the search engine factory functionality."""
    print("=== Search Engine Factory Test ===\n")
    
    # Test 1: List available engines
    print("1. Available Search Engines:")
    engines = list_available_engines()
    for engine in engines:
        print(f"   - {engine}")
    print()
    
    # Test 2: Check engine availability
    print("2. Engine Availability Status:")
    for engine in engines:
        availability = check_engine_availability(engine)
        is_available = SearchEngineFactory.is_engine_available(engine)
        print(f"   - {engine}: Available={is_available}, Config={availability}")
    print()
    
    # Test 3: Get engine information
    print("3. Engine Information:")
    for engine in engines:
        info = get_engine_info(engine)
        print(f"   - {engine}:")
        for key, value in info.items():
            if key != 'class':  # Skip the class object
                print(f"     {key}: {value}")
        print()
    
    # Test 4: Create placeholder search engine (should always work)
    print("4. Testing Placeholder Search Engine:")
    try:
        placeholder = create_search_engine("placeholder")
        results = placeholder.search("test query")
        print(f"   Success! Got {len(results)} results")
        for i, result in enumerate(results[:2]):  # Show first 2 results
            print(f"     Result {i+1}: {result.get('title', 'No title')}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()
    
    # Test 5: Get default engine
    print("5. Default Search Engine:")
    try:
        default_engine = get_default_search_engine()
        engine_type = type(default_engine).__name__
        print(f"   Default engine: {engine_type}")
        print()
    except Exception as e:
        print(f"   Error getting default engine: {e}")
        print()
    
    # Test 6: Test factory methods directly
    print("6. Factory Method Tests:")
    try:
        factory = SearchEngineFactory()
        available_engines = factory.get_available_engines()
        print(f"   Available engines via factory: {available_engines}")
        
        # Test creating each available engine
        for engine_name in available_engines:
            try:
                engine = factory.create(engine_name)
                print(f"   ✓ Successfully created {engine_name}")
            except Exception as e:
                print(f"   ✗ Failed to create {engine_name}: {e}")
        print()
    except Exception as e:
        print(f"   Factory error: {e}")
        print()
    
    print("=== Test Complete ===")


def test_dynamic_registration():
    """Test dynamic engine registration functionality."""
    print("\n=== Dynamic Registration Test ===\n")
    
    # Test registering a new engine (using placeholder as example)
    try:
        SearchEngineFactory.register_engine(
            "test_engine",
            "search_engines.placeholder_search",
            "PlaceholderSearch"
        )
        print("✓ Successfully registered test_engine")
        
        # Verify it's in the list
        engines = list_available_engines()
        if "test_engine" in engines:
            print("✓ test_engine found in available engines")
        else:
            print("✗ test_engine not found in available engines")
            
        # Try to create it
        test_engine = create_search_engine("test_engine")
        results = test_engine.search("dynamic test")
        print(f"✓ Successfully created and used test_engine: {len(results)} results")
        
    except Exception as e:
        print(f"✗ Dynamic registration failed: {e}")
    
    print("\n=== Dynamic Registration Test Complete ===")


if __name__ == "__main__":
    test_factory_functionality()
    test_dynamic_registration()
