# Indoor Reference Rebuild Method

This reference condenses the scene generation playbook into the rules Codex should apply while rebuilding indoor reference images in Blender.

## Core Principle

The final camera render is the primary artifact. A reconstruction can be geometrically plausible and still fail if the render does not match the reference. Work in this order:

1. Define what the reference image requires in screen coordinates.
2. Build the minimum credible 3D structure needed to satisfy those targets.
3. Tighten geometry without destroying the camera match.
4. Use perceptual evidence to choose the next local refinement.

## Screen-Space Contract

Create this before modeling. Use normalized image coordinates `[x0, y0, x1, y1]`.

Include:

- Key object boxes: bed, sofa, desk, chair, window, door, cabinet, rug, lights, major wall features.
- Area proportions: floor, walls, ceiling, windows, dominant furniture.
- Relative screen positions: which object appears left/right/above/behind another.
- Crop rules: which objects may be cut by image edges and on which side.
- Perspective lines: bed edges, floor seams, wall corners, window frames, ceiling beams, roof lines.
- Camera intent translated into image targets: low/high viewpoint, wide/telephoto feeling, vanishing directions, subject dominance.

The screen-space contract is the main acceptance target during camera and layout passes.

## World-Space Contract

Use this to keep the reconstruction credible.

Include:

- Room coordinate convention: front/back, left/right, up/down.
- Approximate camera location and look direction.
- Room shell: floor, walls, ceiling/roof, openings.
- Main object orientation: long axis, front direction, wall adjacency, support height.
- Allowed contacts: rug under furniture, pillows on bed, books on desk, objects on shelves.
- Forbidden relationships: severe intersections, floating objects, large furniture embedded in walls, unsupported tabletops.
- Visual proxies: camera-visible surfaces added to satisfy the render, with an explicit note about which screen-space target they serve.

When the two contracts conflict, preserve the render match and make the world-space compromise explicit.

## Iteration Order

Keep each pass focused:

1. Reference annotation: boxes, lines, crop, and scene semantics.
2. Camera/composition: camera pose, lens, crop, shell, and major masses.
3. Large objects: major furniture size, screen position, silhouette, and occlusion.
4. Blocking geometry: severe collisions, missing objects, floating items.
5. World geometry: object orientation, support, spacing, wall contact, top-view logic.
6. Soft furnishing: pillows, curtains, books, lamps, plants, blankets, small props.
7. Materials: wood, fabric, wall paint, floor, glass, metal, texture scale.
8. Lighting: source direction, shadow strength, window brightness, interior/exterior balance.
9. Perceptual difference: heatmap regions, missing forms, material differences, local texture.
10. Final delivery: `.blend` and same-view camera render. Create comparison images, top views, reports, and archives only for local debugging or deeper QA.

If a metric improves but human side-by-side comparison gets worse, trust the visual comparison and update the contract or validation rule.

## Validation Details

### Blocking Geometry

Only catch hard failures:

- Key object is missing.
- Major furniture severely intersects another major object.
- Tabletop or shelf objects float.
- Floor contact is visibly wrong.
- Object is entirely inside another object.

This can interrupt screen-space work because the scene would otherwise be invalid.

### Screen-Space

Report:

- Rendered bbox for each key group.
- Target bbox.
- Center error, width/height error, IoU.
- Crop edge and crop ratio.
- Main line angle error.
- Area proportions.
- Visibility or occlusion mismatches.

When this fails, adjust camera, lens, crop, coarse blocks, and major dimensions first.

### World Geometry

Report after screen-space is close:

- World bounds for each key group.
- Object long axis and front direction.
- Support relationships.
- Wall adjacency.
- Non-allowed collision list.
- Door/window ownership by wall or named proxy.
- Top-view layout plausibility.

If fixing geometry breaks the render, return to camera/layout alignment.

### Perceptual Difference

Use LPIPS or a lighter image-difference fallback when LPIPS is unavailable.

Report:

- Whole-image scalar score.
- Heatmap or overlay.
- Region ranking.
- Top difference tiles.

Interpretation:

- Large silhouette or position heat: return to screen-space.
- Missing-object heat: add or resize visible masses.
- Material/shadow heat: refine material or lighting.
- Fine texture heat: add local detail after structure is stable.

## Optional Debug Archive Standard

For local testing or deeper QA, use this structure in each reconstruction project:

```text
REFERENCE/
LATEST_RESULTS/
ITERATION_ARCHIVE/
  reference_annotation/
  camera_alignment/
  structure/
  blocking_geometry/
  world_geometry/
  soft_furnishing/
  materials/
  lighting/
  perceptual/
```

The latest results folder should make these easy to find during debugging:

- Latest `.blend`.
- Latest render.
- Latest reference/render comparison.
- Latest screen-space report.
- Latest geometry report.
- Latest perceptual report and heatmap.
- Latest top-view validation image.
