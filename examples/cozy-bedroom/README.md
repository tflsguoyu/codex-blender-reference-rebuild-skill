# Cozy Bedroom Example

This example shows how to test `blender-reference-rebuild` with a single indoor reference image.

## Input

Reference image:

```text
examples/cozy-bedroom/cozy-bedroom-interior-scene-006-02.jpg
```

The image is a cozy bedroom interior reference. It should be used as the visual target for the final Blender camera render.

## Before You Start

Make sure:

1. The skill is installed with `bash tools/install.sh`.
2. Blender is installed and open.
3. Blender MCP, Blender Lab MCP, or another local Blender Python execution path is available to Codex.
4. Codex can access this repository folder and the example image.

## Recommended First Prompt

Start with contracts only:

```text
Use $blender-reference-rebuild with examples/cozy-bedroom/cozy-bedroom-interior-scene-006-02.jpg.

First, do not model yet. Analyze the image and create:
1. A screen-space contract with normalized bboxes, crop rules, area proportions, and perspective-line notes.
2. A world-space contract with room axes, camera intent, main objects, support relationships, and forbidden geometry relationships.

Create a project workspace at ./examples/cozy-bedroom/output and save the contracts there.
```

## Full Reconstruction Prompt

After reviewing the contracts, continue with:

```text
Use $blender-reference-rebuild to reconstruct examples/cozy-bedroom/cozy-bedroom-interior-scene-006-02.jpg as an editable Blender scene.

Use ./examples/cozy-bedroom/output as the project workspace. Build the coarse room shell and main furniture first, align the camera to the screen-space contract, run blocking geometry preflight, then refine world geometry, soft furnishings, materials, and lighting. Save the latest .blend, render, comparison image, top view, and layered validation report in LATEST_RESULTS.
```

## Expected Output

A complete run should create or update:

```text
examples/cozy-bedroom/output/
  REFERENCE/
    cozy-bedroom-interior-scene-006-02.jpg
    scene_contract.json
  LATEST_RESULTS/
    scene.blend
    final_render.png
    reference_vs_render.png
    top_view.png
    validation_report.json
    perceptual_report.json
    heatmap.png
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

The exact filenames may vary, but `LATEST_RESULTS/validation_report.json` should include:

- `blocking_geometry_status`
- `screen_space_status`
- `world_geometry_status`
- `perceptual_status`
- `final_status`
- artifact paths for the latest Blender file, render, comparison, top view, and reports

## Validate The Report

Run:

```bash
python3 skills/blender-reference-rebuild/scripts/validate_rebuild_report.py \
  examples/cozy-bedroom/output/LATEST_RESULTS/validation_report.json
```

This checks the report shape. It does not judge whether the render looks good; Codex should still compare the reference and render visually and use the layered validation evidence.

