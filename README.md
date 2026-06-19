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

## Use

In Codex, ask:

```text
Use $blender-reference-rebuild to reconstruct this indoor reference image in Blender.
```

The skill expects Blender to be available locally. For interactive scene creation, use it with Blender MCP or an equivalent local Blender Python execution path.

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

