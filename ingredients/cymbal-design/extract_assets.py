import os
import argparse
from PIL import Image

# Output paths
BASE_DIR = "/Users/sanchitalekh/Documents/Code/agy-scratchpad/cloud-summit-dach/genmedia/cymbal-design"
PAGES_DIR = os.path.join(BASE_DIR, "pages")
LOGOS_DIR = os.path.join(BASE_DIR, "logos")
SAMPLES_DIR = os.path.join(BASE_DIR, "brand_samples")

def analyze_page(page_num, min_pixels=500):
    img_path = os.path.join(PAGES_DIR, f"page_{page_num:03d}.png")
    if not os.path.exists(img_path):
        print(f"Page image {img_path} not found.")
        return []
    
    img = Image.open(img_path)
    width, height = img.size
    pixels = img.load()
    
    # Identify non-white pixels (distance from white background #FFFFFF)
    # Background in Google Slides might have very subtle shades, so let's check threshold
    non_white = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            # If pixel is not very close to white/off-white (e.g. at least one channel is < 248)
            if r < 248 or g < 248 or b < 248:
                non_white[y][x] = 1
                
    # BFS to find connected components
    visited = [[False for _ in range(width)] for _ in range(height)]
    components = []
    
    for y in range(height):
        for x in range(width):
            if non_white[y][x] == 1 and not visited[y][x]:
                # Start BFS
                queue = [(x, y)]
                visited[y][x] = True
                min_x, max_x = x, x
                min_y, max_y = y, y
                count = 0
                
                head = 0
                while head < len(queue):
                    cx, cy = queue[head]
                    head += 1
                    count += 1
                    
                    if cx < min_x: min_x = cx
                    if cx > max_x: max_x = cx
                    if cy < min_y: min_y = cy
                    if cy > max_y: max_y = cy
                    
                    # 8-neighbors
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if non_white[ny][nx] == 1 and not visited[ny][nx]:
                                visited[ny][nx] = True
                                queue.append((nx, ny))
                                
                if count >= min_pixels:
                    components.append({
                        "bbox": (min_x, min_y, max_x, max_y),
                        "size": count
                    })
                    
    # Sort components by Y coordinate, then X coordinate
    components.sort(key=lambda c: (c["bbox"][1], c["bbox"][0]))
    return components

def crop_and_save(src_page_num, bbox, dest_path, padding=10):
    img_path = os.path.join(PAGES_DIR, f"page_{src_page_num:03d}.png")
    img = Image.open(img_path)
    width, height = img.size
    
    x1, y1, x2, y2 = bbox
    # Apply padding
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(width - 1, x2 + padding)
    y2 = min(height - 1, y2 + padding)
    
    cropped = img.crop((x1, y1, x2 + 1, y2 + 1))
    cropped.save(dest_path, "PNG")
    print(f"Cropped page {src_page_num} {bbox} -> {dest_path} (size: {cropped.size})")

def run_extraction():
    print("Starting assets extraction...")
    
    # ------------------
    # 1. Sub-brand Logos
    # ------------------
    # Bounding boxes we analyzed for Page 13:
    # Top row:
    # - Health: (57, 423, 331, 700)
    # - Labs: (532, 423, 808, 701)
    # - Superstore: (956, 422, 1144, 700)
    # - Shops: (1416, 425, 1692, 693)
    # - Direct: (1870, 423, 2086, 680)
    # Bottom row:
    # - Bank: (65, 877, 331, 1143)
    # - Investments: (504, 888, 759, 1143)
    # - Insurance: (955, 860, 1237, 1143)
    # - Fintech: (1417, 881, 1634, 1143)
    
    logos_config = {
        "health.png": (57, 423, 331, 700),
        "labs.png": (532, 423, 808, 701),
        "superstore.png": (956, 422, 1144, 700),
        "shops.png": (1416, 425, 1692, 693),
        "direct.png": (1870, 423, 2086, 680),
        "bank.png": (65, 877, 331, 1143),
        "investments.png": (504, 888, 759, 1143),
        "insurance.png": (955, 860, 1237, 1143),
        "fintech.png": (1417, 881, 1634, 1143)
    }
    
    for filename, bbox in logos_config.items():
        dest = os.path.join(LOGOS_DIR, filename)
        crop_and_save(13, bbox, dest, padding=10)
        
    # ------------------
    # 2. Brand Reference Samples
    # ------------------
    # Let's perform smart/content-aware crops or custom cropping box coordinates
    # We want to crop page content, omitting standard slide header (typically 0-150px)
    # and slide footer (typically 1080-1215px).
    # For some slides, we can crop the full central width (x_min = 100, x_max = 2060, y_min = 180, y_max = 1050)
    # or detect active content area.
    
    samples_config = [
        # 1. Cymbal Wordmark (Page 5)
        {"src_page": 5, "name": "01_parent_wordmark.png", "bbox": (67, 155, 921, 718), "pad": 15},
        # 2. Cymbal Monogram (Page 5)
        {"src_page": 5, "name": "02_parent_monogram.png", "bbox": (1085, 0, 2159, 1215), "pad": 0},
        # 3. Icon Grid System (Page 8)
        {"src_page": 8, "name": "03_icon_grid_system.png", "bbox": (68, 155, 2003, 1057), "pad": 15},
        # 4. Shape Library (Page 10)
        {"src_page": 10, "name": "04_shape_library.png", "bbox": (68, 151, 1946, 1092), "pad": 15},
        # 5. Primary Colors (Page 17)
        {"src_page": 17, "name": "05_primary_colors.png", "bbox": (47, 148, 2098, 1150), "pad": 15},
        # 6. Typography Spec (Page 19)
        {"src_page": 19, "name": "06_typography_spec.png", "bbox": (67, 151, 1878, 1007), "pad": 15},
        # 7. Typography Pairings (Page 21)
        {"src_page": 21, "name": "07_typography_pairings.png", "bbox": (67, 151, 2055, 1113), "pad": 15},
        # 8. Typography Scale (Page 22)
        {"src_page": 22, "name": "08_typography_scale.png", "bbox": (70, 152, 1824, 1043), "pad": 15},
        # 9. Layout Spacing (Page 25)
        {"src_page": 25, "name": "09_layout_spacing.png", "bbox": (64, 149, 2114, 1147), "pad": 15},
        # 10. UI Color Shades (Page 28)
        {"src_page": 28, "name": "10_ui_color_shades.png", "bbox": (47, 180, 2098, 1150), "pad": 15},
        # 11. UI Color Application (Page 30)
        {"src_page": 30, "name": "11_ui_color_application.png", "bbox": (67, 148, 1865, 1098), "pad": 15},
        # 12. UI Border Radius (Page 31)
        {"src_page": 31, "name": "12_ui_border_radius.png", "bbox": (68, 154, 2047, 1084), "pad": 15}
    ]
    
    for config in samples_config:
        dest = os.path.join(SAMPLES_DIR, config["name"])
        crop_and_save(config["src_page"], config["bbox"], dest, padding=config["pad"])
        
    print("Assets extraction completed successfully!")

def validate_outputs():
    print("Validating extracted assets...")
    errors = 0
    
    # Validate Logos
    expected_logos = [
        "health.png", "labs.png", "superstore.png", "shops.png", "direct.png",
        "bank.png", "investments.png", "insurance.png", "fintech.png"
    ]
    for logo in expected_logos:
        path = os.path.join(LOGOS_DIR, logo)
        if not os.path.exists(path):
            print(f"Error: Missing logo {logo}")
            errors += 1
        else:
            img = Image.open(path)
            if img.size[0] == 0 or img.size[1] == 0:
                print(f"Error: Logo {logo} has invalid dimensions {img.size}")
                errors += 1
                
    # Validate Samples
    expected_samples = [
        "01_parent_wordmark.png", "02_parent_monogram.png", "03_icon_grid_system.png",
        "04_shape_library.png", "05_primary_colors.png", "06_typography_spec.png",
        "07_typography_pairings.png", "08_typography_scale.png", "09_layout_spacing.png",
        "10_ui_color_shades.png", "11_ui_color_application.png", "12_ui_border_radius.png"
    ]
    for sample in expected_samples:
        path = os.path.join(SAMPLES_DIR, sample)
        if not os.path.exists(path):
            print(f"Error: Missing sample {sample}")
            errors += 1
        else:
            img = Image.open(path)
            if img.size[0] == 0 or img.size[1] == 0:
                print(f"Error: Sample {sample} has invalid dimensions {img.size}")
                errors += 1
                
    if errors == 0:
        print("Validation successful! All files exist, are valid, and have healthy sizes.")
    else:
        print(f"Validation failed with {errors} errors.")
        exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyze", type=int, help="Analyze connected components for a page number")
    parser.add_argument("--run", action="store_true", help="Execute the asset extraction")
    parser.add_argument("--validate", action="store_true", help="Validate extracted assets")
    args = parser.parse_args()
    
    if args.analyze:
        components = analyze_page(args.analyze)
        print(f"\n--- Connected components on page {args.analyze} (found {len(components)}) ---")
        for idx, c in enumerate(components):
            bbox = c["bbox"]
            w = bbox[2] - bbox[0] + 1
            h = bbox[3] - bbox[1] + 1
            print(f"Component {idx}: bbox={bbox}, width={w}, height={h}, size_pixels={c['size']}")
    elif args.run:
        run_extraction()
    elif args.validate:
        validate_outputs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
