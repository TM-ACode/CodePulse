"""
JSON Serialization Diagnostic Tool
===================================

Tests if all objects can be serialized to JSON
"""

import json
import sys


def find_non_serializable(obj, path="root"):
    """Find non-serializable objects in data structure"""
    issues = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}"
            try:
                json.dumps(value)
            except (TypeError, ValueError) as e:
                issues.append({
                    'path': new_path,
                    'type': type(value).__name__,
                    'error': str(e)
                })
                # Recurse to find nested issues
                if isinstance(value, (dict, list)):
                    issues.extend(find_non_serializable(value, new_path))
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_path = f"{path}[{i}]"
            try:
                json.dumps(item)
            except (TypeError, ValueError) as e:
                issues.append({
                    'path': new_path,
                    'type': type(item).__name__,
                    'error': str(e)
                })
                if isinstance(item, (dict, list)):
                    issues.extend(find_non_serializable(item, new_path))
    
    return issues


def make_safe(obj):
    """Convert object to JSON-safe format"""
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    
    if isinstance(obj, dict):
        return {k: make_safe(v) for k, v in obj.items()}
    
    if isinstance(obj, (list, tuple)):
        return [make_safe(item) for item in obj]
    
    if isinstance(obj, set):
        return [make_safe(item) for item in obj]
    
    if str(type(obj)) == "<class 'mappingproxy'>":
        return {k: make_safe(v) for k, v in dict(obj).items()}
    
    if isinstance(obj, (staticmethod, classmethod, property)):
        return f"<{type(obj).__name__}>"
    
    if callable(obj):
        return f"<function {getattr(obj, '__name__', 'unknown')}>"
    
    if isinstance(obj, type):
        return f"<class {obj.__name__}>"
    
    if hasattr(obj, '__dict__'):
        try:
            return make_safe(dict(obj.__dict__))
        except:
            return str(obj)
    
    try:
        return str(obj)
    except:
        return "<unserializable>"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json_diagnostic.py <json_file_or_object>")
        sys.exit(1)
    
    # Test with a file
    import os
    if os.path.isfile(sys.argv[1]):
        try:
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
            print("✅ File is valid JSON")
        except Exception as e:
            print(f"❌ File is not valid JSON: {e}")
    else:
        # Test serialization
        test_objects = {
            'string': 'test',
            'int': 42,
            'float': 3.14,
            'bool': True,
            'none': None,
            'list': [1, 2, 3],
            'dict': {'a': 1, 'b': 2},
            'tuple': (1, 2, 3),
            'set': {1, 2, 3},
        }
        
        print("Testing basic types:")
        for name, obj in test_objects.items():
            try:
                json.dumps(obj)
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
        
        # Test problematic types
        print("\nTesting problematic types:")
        problematic = {
            'staticmethod': staticmethod(lambda: None),
            'classmethod': classmethod(lambda: None),
            'function': lambda x: x,
            'class': str,
        }
        
        for name, obj in problematic.items():
            try:
                json.dumps(obj)
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                # Try to fix
                safe = make_safe(obj)
                try:
                    json.dumps(safe)
                    print(f"     ✅ Fixed: {safe}")
                except:
                    print(f"     ❌ Could not fix")
