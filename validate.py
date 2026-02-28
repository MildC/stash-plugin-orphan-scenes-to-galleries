#!/usr/bin/env python3
"""
Plugin Validator - Checks plugin structure and configuration
"""

import sys
import json
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def validate_plugin():
    """Validate the plugin structure and files."""
    errors = []
    warnings = []

    # Check required files exist
    required_files = [
        'orphan_scenes_to_galleries.yml',
        'orphan_scenes_to_galleries.py',
        'requirements.txt',
        'README.md'
    ]

    for filename in required_files:
        if not Path(filename).exists():
            errors.append(f"Missing required file: {filename}")

    if errors:
        print("❌ Validation failed!")
        for error in errors:
            print(f"  ERROR: {error}")
        return False

    # Validate YAML structure
    if not HAS_YAML:
        warnings.append("PyYAML not installed - skipping YAML validation. Install with: pip install pyyaml")
        config = None
    else:
        try:
            with open('orphan_scenes_to_galleries.yml', 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML: {e}")
            config = None
        except Exception as e:
            errors.append(f"Error reading YAML: {e}")
            config = None

    if config:
        try:
            # Check required fields
            required_fields = ['name', 'description', 'version', 'exec', 'interface']
            for field in required_fields:
                if field not in config:
                    errors.append(f"Missing required field in YAML: {field}")

            # Check exec command
            if 'exec' in config and isinstance(config['exec'], list):
                if 'python' not in config['exec'][0].lower():
                    warnings.append("Exec command doesn't use Python")

            # Validate settings structure
            if 'settings' in config:
                for setting_name, setting_config in config['settings'].items():
                    if 'displayName' not in setting_config:
                        warnings.append(f"Setting '{setting_name}' missing displayName")
                    if 'description' not in setting_config:
                        warnings.append(f"Setting '{setting_name}' missing description")
                    if 'type' not in setting_config:
                        errors.append(f"Setting '{setting_name}' missing type")

            # Validate tasks
            if 'tasks' in config:
                for task in config['tasks']:
                    if 'name' not in task:
                        errors.append("Task missing 'name' field")
                    if 'description' not in task:
                        warnings.append(f"Task '{task.get('name', 'unknown')}' missing description")

        except Exception as e:
            errors.append(f"Error validating YAML structure: {e}")

    # Try to import Python file
    try:
        import ast
        with open('orphan_scenes_to_galleries.py', 'r') as f:
            code = f.read()
            ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Python syntax error: {e}")
    except Exception as e:
        warnings.append(f"Could not validate Python file: {e}")

    # Print results
    if errors:
        print("❌ Validation failed!")
        for error in errors:
            print(f"  ERROR: {error}")
        return False

    print("✅ Plugin validation passed!")

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  WARNING: {warning}")

    # Print summary
    print("\n📦 Plugin Summary:")
    if HAS_YAML and config:
        try:
            print(f"  Name: {config.get('name')}")
            print(f"  Version: {config.get('version')}")
            print(f"  Description: {config.get('description')}")

            if 'settings' in config:
                print(f"  Settings: {len(config['settings'])}")
            if 'tasks' in config:
                print(f"  Tasks: {len(config['tasks'])}")
            if 'hooks' in config:
                print(f"  Hooks: {len(config['hooks'])}")
        except:
            pass

    return True


if __name__ == '__main__':
    success = validate_plugin()
    sys.exit(0 if success else 1)
