---
name: blender-reference-rebuild
description: Rebuild indoor reference images as editable Blender scenes through Blender MCP or a local Blender Python workflow. Use when Codex needs to reconstruct an interior room from a reference image, match the final camera render to the reference, create screen-space and world-space contracts, iterate camera/layout/geometry/materials, produce layered validation reports, or organize Blender reconstruction deliverables.
---

# Blender Reference Rebuild

## Overview

Use this skill to reconstruct an indoor reference image as an editable Blender scene where the final camera render is the primary target. Prioritize screen-space match first, then tighten world-space geometry so the scene remains physically credible.

The guiding rule is:

```text
Lock screen-space first, then reconcile geometry.
```

## Workflow

1. Inspect the reference image and identify the room type, camera viewpoint, major furniture, architectural features, visible openings, crop edges, and dominant perspective lines.
2. Create a screen-space contract before building. Record normalized `[x0, y0, x1, y1]` target boxes, crop rules, visible area proportions, object ordering, occlusion, and perspective-line directions.
3. Create a world-space contract. Record room axes, camera intent, walls/floor/ceiling, object support relationships, allowed contacts, forbidden collisions, and any camera-visible proxy geometry.
4. Build a coarse proxy scene first: floor, walls, ceiling or roof planes, openings, and major furniture blocks. Avoid detailed materials until composition is close.
5. Use Blender MCP or local Blender Python to search camera position, focal length, crop, and large-object dimensions until the camera render matches the screen-space contract.
6. Run a blocking geometry preflight before deep refinement. Fix only hard failures such as missing key objects, severe intersections, floating tabletop objects, impossible support, or wrong floor height.
7. Re-check screen-space targets. If the render is not close, adjust camera, focal length, crop, and large proxy shapes before spending effort on materials.
8. Tighten world geometry only after screen-space is stable. Preserve the camera match while fixing orientation, support, wall adjacency, spacing, and non-blocking collisions.
9. Add soft furnishings, props, materials, lighting, texture density, and final details in separate passes.
10. Produce a layered validation report and archive the latest `.blend`, render, comparison image, top view, screen-space report, geometry report, and perceptual report.

Read `references/rebuild-method.md` for the detailed contract, validation, iteration, and archive standards.

## Required Validation Layers

Keep validation layers separate. Do not collapse them into one vague quality score.

- `blocking_geometry_status`: hard gate for missing objects, severe intersections, floating objects, and impossible support.
- `screen_space_status`: main acceptance layer for camera render similarity, including bbox, crop, proportions, perspective lines, and relative positions.
- `world_geometry_status`: 3D plausibility after the camera view is mostly locked.
- `perceptual_status`: image-difference or LPIPS-style evidence used to choose the next refinement target.
- `final_status`: pass only when the current stage requirements are satisfied.

If screen-space and world-space conflict, favor screen-space, then solve the 3D credibility problem explicitly through adjusted geometry or a named visual proxy. Never hide a proxy or geometry compromise.

## Scripts

Use scripts when their automation fits the task:

- `scripts/init_rebuild_workspace.py`: create the standard `REFERENCE/`, `LATEST_RESULTS/`, and `ITERATION_ARCHIVE/` folders and seed contract/report templates.
- `scripts/validate_rebuild_report.py`: validate that a layered report JSON includes the required statuses, evidence fields, and artifact references.

Run scripts from the skill directory or pass absolute paths. They are intentionally lightweight and do not require Blender.

## Deliverables

For a complete reconstruction, deliver:

- Latest `.blend` file.
- Final camera render.
- Reference/render comparison image.
- Screen-space contract and report.
- World-space contract and geometry report.
- Blocking geometry preflight result.
- Perceptual or LPIPS-style report, heatmap, or region ranking when available.
- Top-view validation image.
- Organized output folders with latest results easy to find.

## Guardrails

- Do not polish materials while the camera composition is wrong.
- Do not treat a plausible 3D layout as success if the final camera view does not match the reference.
- Do not let non-blocking geometry concerns derail early camera/layout alignment.
- Do not claim final success without a layered validation report.
- Do not silently create fake geometry; name visual proxies and state which screen-space goal they serve.

