"""
Folder matching logic for orphan scenes to galleries plugin.
This module contains the core matching logic extracted for unit testing.
"""

import os


def should_match_folder(image_folder: str, scene_folder: str, parent_path: str) -> bool:
    """
    Determine if an image folder should match with a scene folder.

    Matching rules:
    1. Same folder as scene
    2. Child/subfolder of scene folder (descendants)
    3. Direct parent folder only

    Does NOT match:
    - Sibling folders at the same level
    - Grandparent or higher ancestors
    - Unrelated folders

    Args:
        image_folder: The folder containing the image
        scene_folder: The folder containing the scene
        parent_path: The direct parent folder of scene_folder

    Returns:
        True if the folders should match, False otherwise

    Examples:
        >>> should_match_folder("/media/shoot", "/media/shoot", "/media")
        True  # Same folder

        >>> should_match_folder("/media/shoot/pics", "/media/shoot", "/media")
        True  # Child folder

        >>> should_match_folder("/media", "/media/shoot", "/media")
        True  # Direct parent

        >>> should_match_folder("/media/other", "/media/shoot", "/media")
        False  # Sibling folder
    """
    # Rule 1: Same folder
    if image_folder == scene_folder:
        return True

    # Rule 2: Child folder (descendant of scene_folder)
    is_child = image_folder.startswith(scene_folder + os.sep)

    # Rule 3: Direct parent folder
    is_direct_parent = image_folder == parent_path

    # Match if either child or direct parent
    return is_child or is_direct_parent
