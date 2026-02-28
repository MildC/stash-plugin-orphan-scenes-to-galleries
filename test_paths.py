#!/usr/bin/env python3
"""
Test the paths field access logic
"""
from pathlib import Path

# Simulate how Stash returns image data
mock_images = [
    {
        'id': '1',
        'title': 'Image 1',
        'paths': [
            {'path': '/media/photoshoot/2024-03-15/image1.jpg'}
        ],
        'galleries': [
            {'id': 'g1', 'title': 'Gallery 1', 'folder': {'path': '/media/photoshoot/2024-03-15'}}
        ]
    },
    {
        'id': '2',
        'title': 'Image 2',
        'paths': [
            {'path': '/media/photoshoot/2024-03-15/subfolder/image2.jpg'}
        ],
        'galleries': []
    },
    {
        'id': '3',
        'title': 'Image 3',
        'paths': [],  # Empty paths array
        'galleries': []
    }
]

def test_path_extraction():
    print("=" * 60)
    print("Testing paths field extraction")
    print("=" * 60)

    target_folder = '/media/photoshoot/2024-03-15'

    for image in mock_images:
        image_id = image['id']
        paths = image.get('paths', [])

        print(f"\nImage {image_id}:")
        print(f"  paths array: {paths}")

        if paths and len(paths) > 0:
            image_path = paths[0].get('path', '')
            print(f"  extracted path: {image_path}")

            if image_path:
                image_folder = str(Path(image_path).parent)
                print(f"  folder: {image_folder}")
                matches = image_folder == target_folder
                print(f"  matches target: {matches}")

                galleries = image.get('galleries', [])
                if galleries:
                    gallery = galleries[0]
                    print(f"  gallery: {gallery['id']} - {gallery['title']}")
        else:
            print(f"  No paths available")

    print("\n" + "=" * 60)
    print("✓ Path extraction test complete")
    print("=" * 60)

if __name__ == "__main__":
    test_path_extraction()
