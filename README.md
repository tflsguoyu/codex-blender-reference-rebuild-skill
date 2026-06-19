# Codex Blender Reference Rebuild Skill

`blender-reference-rebuild` is a Codex skill for rebuilding indoor reference images as editable Blender scenes.

It is designed for Blender MCP or local Blender Python workflows where the final camera render must match the reference image. The skill emphasizes:

- Screen-space contracts before modeling.
- World-space constraints after composition is close.
- Blocking geometry preflight.
- Layered validation reports.
- Perceptual or LPIPS-style difference evidence.
- Clean reconstruction project archives.

## Install

Clone the repository:

```bash
git clone https://github.com/tflsguoyu/codex-blender-reference-rebuild-skill.git
cd codex-blender-reference-rebuild-skill
```

Install into Codex:

```bash
bash tools/install.sh
```

Or copy manually:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/blender-reference-rebuild "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Prepare Your Environment

Before using the skill, make sure you have:

1. Codex installed and able to load local skills from `${CODEX_HOME:-$HOME/.codex}/skills`.
2. Blender installed locally.
3. Blender open when you want Codex to create or inspect a scene.
4. A working Blender control path:
   - Blender MCP / Blender Lab MCP, recommended for interactive scene control.
   - Or another local Blender Python execution workflow that Codex can use.
5. An indoor reference image ready to provide to Codex.

This skill does not install Blender or Blender MCP for you. It teaches Codex the reconstruction workflow once Blender access is already available.

## Use

In Codex, ask:

```text
Use $blender-reference-rebuild to reconstruct this indoor reference image in Blender.
```

The skill expects Blender to be available locally. For interactive scene creation, use it with Blender MCP or an equivalent local Blender Python execution path.

For a first run, ask Codex to start by creating the contracts instead of modeling immediately:

```text
Use $blender-reference-rebuild to analyze this indoor reference image first. Create the screen-space and world-space contracts before building the Blender scene.
```

## Example: Cozy Bedroom

This repository includes a sample indoor reference image:

```text
examples/cozy-bedroom/reference.jpg
```

It also includes two example outputs:

```text
examples/cozy-bedroom/camera-render.png
examples/cozy-bedroom/topdown-render.png
```

Use it to test the skill end to end. First, create the project workspace and contracts:

```text
Use $blender-reference-rebuild with examples/cozy-bedroom/reference.jpg.

First, do not model yet. Analyze the image and create:
1. A screen-space contract with normalized bboxes, crop rules, area proportions, and perspective-line notes.
2. A world-space contract with room axes, camera intent, main objects, support relationships, and forbidden geometry relationships.

Create a project workspace at ./examples/cozy-bedroom/output and save the contracts there.
```

Then continue with scene creation:

```text
Use $blender-reference-rebuild to reconstruct examples/cozy-bedroom/reference.jpg as an editable Blender scene.

Use ./examples/cozy-bedroom/output as the project workspace. Build the coarse room shell and main furniture first, align the camera to the screen-space contract, run blocking geometry preflight, then refine world geometry, soft furnishings, materials, and lighting. Save the latest .blend, render, comparison image, top view, and layered validation report in LATEST_RESULTS.
```

Expected output:

```text
examples/cozy-bedroom/output/
  REFERENCE/
    reference.jpg
    scene_contract.json
  LATEST_RESULTS/
    scene.blend
    camera-render.png
    reference_vs_render.png
    topdown-render.png
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

For more detail, see `examples/cozy-bedroom/README.md`.

## Repository Layout

```text
skills/blender-reference-rebuild/
  SKILL.md
  agents/openai.yaml
  references/rebuild-method.md
  scripts/init_rebuild_workspace.py
  scripts/validate_rebuild_report.py
  assets/contracts/scene_contract.template.json
  assets/reports/validation_report.template.json
examples/cozy-bedroom/
  README.md
  reference.jpg
  camera-render.png
  topdown-render.png
examples/example-prompts.md
tools/install.sh
tools/validate_skill.py
```

## Helper Scripts

Create a standard reconstruction workspace:

```bash
python3 skills/blender-reference-rebuild/scripts/init_rebuild_workspace.py ./my-bedroom-rebuild
```

Validate a layered report:

```bash
python3 skills/blender-reference-rebuild/scripts/validate_rebuild_report.py ./my-bedroom-rebuild/LATEST_RESULTS/validation_report.json
```

Validate the skill repository:

```bash
python3 tools/validate_skill.py skills/blender-reference-rebuild
```

## License

MIT
