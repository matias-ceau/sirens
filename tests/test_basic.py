#!/usr/bin/env python3
"""Test script to verify sirens functionality without numpy dependency.

This script tests the core functionality by directly importing and checking
the module structure before numpy is required.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def test_imports():
    """Test that modules can be imported."""
    print("Testing imports...")
    try:
        # These should work without numpy
        from sirens.presets import PRESETS, validate_siren_preset, register_custom_siren, get_available_sirens
        print("  ✓ presets module imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_presets_structure():
    """Test that French sirens are properly defined."""
    print("\nTesting French siren presets...")
    from sirens.presets import PRESETS
    
    french_sirens = ["police", "firefighter", "samu"]
    all_ok = True
    
    for siren_name in french_sirens:
        if siren_name in PRESETS:
            preset = PRESETS[siren_name]
            print(f"  ✓ {siren_name}: {preset.get('description', 'No description')}")
            print(f"    Frequencies: {preset['freqs']}")
        else:
            print(f"  ✗ {siren_name} not found in PRESETS")
            all_ok = False
    
    return all_ok


def test_validation():
    """Test preset validation."""
    print("\nTesting preset validation...")
    from sirens.presets import validate_siren_preset
    
    # Valid preset
    valid_preset = {
        "freqs": (400, 500),
        "tone_duration": 0.5,
        "attack": 0.05,
        "decay": 0.05,
        "volume": 0.9,
        "max_db": 110
    }
    
    is_valid, error = validate_siren_preset(valid_preset)
    if is_valid:
        print("  ✓ Valid preset accepted")
    else:
        print(f"  ✗ Valid preset rejected: {error}")
        return False
    
    # Invalid preset (missing fields)
    invalid_preset = {
        "freqs": (400, 500),
        "tone_duration": 0.5
    }
    
    is_valid, error = validate_siren_preset(invalid_preset)
    if not is_valid:
        print(f"  ✓ Invalid preset correctly rejected: {error}")
    else:
        print("  ✗ Invalid preset was incorrectly accepted")
        return False
    
    return True


def test_custom_registration():
    """Test custom siren registration."""
    print("\nTesting custom siren registration...")
    from sirens.presets import register_custom_siren, get_available_sirens, PRESETS
    
    # Register a custom siren
    custom_preset = {
        "freqs": (500, 600),
        "tone_duration": 0.4,
        "attack": 0.05,
        "decay": 0.05,
        "volume": 0.85,
        "max_db": 112
    }
    
    try:
        register_custom_siren("test_custom", custom_preset)
        if "test_custom" in PRESETS:
            print("  ✓ Custom siren registered successfully")
        else:
            print("  ✗ Custom siren not found in PRESETS after registration")
            return False
    except Exception as e:
        print(f"  ✗ Registration failed: {e}")
        return False
    
    # Test get_available_sirens
    available = get_available_sirens()
    if "test_custom" in available:
        print(f"  ✓ Custom siren appears in available list: {available['test_custom']}")
    else:
        print("  ✗ Custom siren not in available list")
        return False
    
    # Test that invalid registration fails
    invalid_preset = {"freqs": (400, 500)}  # Missing required fields
    try:
        register_custom_siren("invalid_test", invalid_preset)
        print("  ✗ Invalid preset was accepted (should have failed)")
        return False
    except ValueError:
        print("  ✓ Invalid preset correctly rejected")
    
    return True


def test_cli_structure():
    """Test that CLI module has expected structure."""
    print("\nTesting CLI module structure...")
    try:
        from sirens import cli
        if hasattr(cli, 'main'):
            print("  ✓ CLI main function exists")
        else:
            print("  ✗ CLI main function not found")
            return False
        
        if hasattr(cli, 'list_sirens'):
            print("  ✓ CLI list_sirens function exists")
        else:
            print("  ✗ CLI list_sirens function not found")
            return False
            
        if hasattr(cli, 'print_usage'):
            print("  ✓ CLI print_usage function exists")
        else:
            print("  ✗ CLI print_usage function not found")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ CLI test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=== Sirens Package Test Suite ===\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("French Siren Presets", test_presets_structure),
        ("Preset Validation", test_validation),
        ("Custom Siren Registration", test_custom_registration),
        ("CLI Structure", test_cli_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
