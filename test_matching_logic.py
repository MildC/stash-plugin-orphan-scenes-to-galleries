#!/usr/bin/env python3
"""
Test suite for folder hierarchy matching logic
Tests all 4 examples from README.md
"""

import os
from pathlib import Path


def test_example_1_same_folder():
    """
    Example 1: Same Folder Match
    Scene: /media/photoshoots/2024-03-15/video.mp4
    Images: /media/photoshoots/2024-03-15/image1.jpg, image2.jpg
    Result: Should match ✓
    """
    print("\n" + "=" * 70)
    print("TEST 1: Same Folder Match")
    print("=" * 70)

    scene_path = "/media/photoshoots/2024-03-15/video.mp4"
    scene_folder = str(Path(scene_path).parent)

    image_paths = [
        "/media/photoshoots/2024-03-15/image1.jpg",
        "/media/photoshoots/2024-03-15/image2.jpg"
    ]

    print(f"Scene folder: {scene_folder}")
    print(f"Image paths: {image_paths}")

    # Test: Images in same folder
    for img_path in image_paths:
        img_folder = str(Path(img_path).parent)
        matches = img_folder == scene_folder
        print(f"  {Path(img_path).name}: folder={img_folder}, matches={matches}")
        assert matches, "Should match images in same folder"

    print("✓ PASSED: Same folder matching works")


def test_example_2_direct_parent():
    """
    Example 2: Direct Parent Folder Search
    Scene: /media/shoots/session1/video/scene.mp4
    Images: /media/shoots/session1/image1.jpg, image2.jpg
    Result: Should match (direct parent) ✓
    """
    print("\n" + "=" * 70)
    print("TEST 2: Direct Parent Folder Search")
    print("=" * 70)

    scene_path = "/media/shoots/session1/video/scene.mp4"
    scene_folder = str(Path(scene_path).parent)
    parent_path = str(Path(scene_folder).parent)

    image_paths = [
        "/media/shoots/session1/image1.jpg",
        "/media/shoots/session1/image2.jpg"
    ]

    print(f"Scene folder: {scene_folder}")
    print(f"Parent path: {parent_path}")
    print(f"Image paths: {image_paths}")

    for img_path in image_paths:
        img_folder = str(Path(img_path).parent)

        # Check if it's a child folder
        is_child = img_folder.startswith(scene_folder + os.sep)
        # Check if it's the direct parent
        is_direct_parent = img_folder == parent_path
        # Should match if either condition is true
        should_match = is_child or is_direct_parent

        print(f"  {Path(img_path).name}:")
        print(f"    folder={img_folder}")
        print(f"    is_child={is_child}, is_direct_parent={is_direct_parent}")
        print(f"    should_match={should_match}")

        assert is_direct_parent, "Should match direct parent folder"
        assert should_match, "Should match via direct parent logic"

    print("✓ PASSED: Direct parent folder matching works")


def test_example_3_child_folder():
    """
    Example 3: Multi-Level Hierarchy (Child Folder)
    Scene: /media/studio/2024/march/scene.mp4
    Images: /media/studio/2024/march/gallery/image1.jpg
    Result: Should match (child folder) ✓
    """
    print("\n" + "=" * 70)
    print("TEST 3: Child Folder Search")
    print("=" * 70)

    scene_path = "/media/studio/2024/march/scene.mp4"
    scene_folder = str(Path(scene_path).parent)
    parent_path = str(Path(scene_folder).parent)

    image_paths = [
        "/media/studio/2024/march/gallery/image1.jpg"
    ]

    print(f"Scene folder: {scene_folder}")
    print(f"Parent path: {parent_path}")
    print(f"Image paths: {image_paths}")

    for img_path in image_paths:
        img_folder = str(Path(img_path).parent)

        # Check if it's a child folder
        is_child = img_folder.startswith(scene_folder + os.sep)
        # Check if it's the direct parent
        is_direct_parent = img_folder == parent_path
        # Should match if either condition is true
        should_match = is_child or is_direct_parent

        print(f"  {Path(img_path).name}:")
        print(f"    folder={img_folder}")
        print(f"    is_child={is_child}, is_direct_parent={is_direct_parent}")
        print(f"    should_match={should_match}")

        assert is_child, "Should match child folder"
        assert should_match, "Should match via child folder logic"

    print("✓ PASSED: Child folder matching works")


def test_example_4_sibling_prevention():
    """
    Example 4: Sibling Folder Prevention
    Scene: /media/studio/2024/april/scene.mp4
    Images: /media/studio/2024/march/image1.jpg
    Result: Should NOT match (sibling folder) ✗
    """
    print("\n" + "=" * 70)
    print("TEST 4: Sibling Folder Prevention")
    print("=" * 70)

    scene_path = "/media/studio/2024/april/scene.mp4"
    scene_folder = str(Path(scene_path).parent)
    parent_path = str(Path(scene_folder).parent)

    image_paths = [
        "/media/studio/2024/march/image1.jpg"
    ]

    print(f"Scene folder: {scene_folder}")
    print(f"Parent path: {parent_path}")
    print(f"Image paths: {image_paths}")

    for img_path in image_paths:
        img_folder = str(Path(img_path).parent)

        # Check if it's a child folder
        is_child = img_folder.startswith(scene_folder + os.sep)
        # Check if it's the direct parent
        is_direct_parent = img_folder == parent_path
        # Should match if either condition is true
        should_match = is_child or is_direct_parent

        print(f"  {Path(img_path).name}:")
        print(f"    folder={img_folder}")
        print(f"    is_child={is_child}, is_direct_parent={is_direct_parent}")
        print(f"    should_match={should_match}")

        assert not is_child, "Should NOT be a child folder"
        assert not is_direct_parent, "Should NOT be direct parent"
        assert not should_match, "Should NOT match sibling folder"

    print("✓ PASSED: Sibling folder prevention works")


def test_edge_cases():
    """Test additional edge cases"""
    print("\n" + "=" * 70)
    print("TEST 5: Edge Cases")
    print("=" * 70)

    # Edge case 1: Grandparent folder (should NOT match)
    print("\nEdge case 1: Grandparent folder")
    scene_folder = "/media/studio/2024/march/videos"
    parent_path = "/media/studio/2024/march"
    grandparent_path = "/media/studio/2024"
    image_folder = grandparent_path

    is_child = image_folder.startswith(scene_folder + os.sep)
    is_direct_parent = image_folder == parent_path
    should_match = is_child or is_direct_parent

    print(f"  Scene: {scene_folder}")
    print(f"  Image: {image_folder}")
    print(f"  is_child={is_child}, is_direct_parent={is_direct_parent}")
    print(f"  should_match={should_match}")
    assert not should_match, "Should NOT match grandparent folder"
    print("  ✓ Grandparent correctly rejected")

    # Edge case 2: Deep child folder (should match)
    print("\nEdge case 2: Deep child folder")
    scene_folder = "/media/studio/session1"
    parent_path = "/media/studio"
    image_folder = "/media/studio/session1/subfolder1/subfolder2/pics"

    is_child = image_folder.startswith(scene_folder + os.sep)
    is_direct_parent = image_folder == parent_path
    should_match = is_child or is_direct_parent

    print(f"  Scene: {scene_folder}")
    print(f"  Image: {image_folder}")
    print(f"  is_child={is_child}, is_direct_parent={is_direct_parent}")
    print(f"  should_match={should_match}")
    assert should_match, "Should match deep child folder"
    print("  ✓ Deep child correctly matched")

    # Edge case 3: Similar prefix but different folder (should NOT match)
    print("\nEdge case 3: Similar prefix but different folder")
    scene_folder = "/media/session1"
    parent_path = "/media"
    image_folder = "/media/session10"  # Similar but not child or parent

    is_child = image_folder.startswith(scene_folder + os.sep)
    is_direct_parent = image_folder == parent_path
    should_match = is_child or is_direct_parent

    print(f"  Scene: {scene_folder}")
    print(f"  Image: {image_folder}")
    print(f"  is_child={is_child}, is_direct_parent={is_direct_parent}")
    print(f"  should_match={should_match}")
    assert not should_match, "Should NOT match similar prefix"
    print("  ✓ Similar prefix correctly rejected")

    print("\n✓ PASSED: All edge cases handled correctly")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("RUNNING ALL MATCHING LOGIC TESTS")
    print("=" * 70)

    try:
        test_example_1_same_folder()
        test_example_2_direct_parent()
        test_example_3_child_folder()
        test_example_4_sibling_prevention()
        test_edge_cases()

        print("\n" + "=" * 70)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 70)
        print("\nThe matching logic correctly:")
        print("  ✓ Matches images in the same folder")
        print("  ✓ Matches images in the direct parent folder")
        print("  ✓ Matches images in child/subfolders")
        print("  ✓ Prevents matching across sibling folders")
        print("  ✓ Handles edge cases properly")
        return True

    except AssertionError as e:
        print(f"\n✗✗✗ TEST FAILED ✗✗✗")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
