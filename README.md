# Beyond Ordinary Skills

Creative AI skills for [beyondordinary.art](https://beyondordinary.art).

## Submit

1. Fork this repository.
2. Copy `template/` to `skills/<your-slug>/` and fill in `metadata.json` and `SKILL.md`.
3. Add a JPEG preview at `previews/<your-slug>.jpg` (under 2 MB).
4. Open a pull request.

A maintainer reviews every submission. Nothing is published until it is approved. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

- `skills/<slug>/metadata.json` and `SKILL.md`
- `previews/<slug>.jpg`
- `template/`: starting point
- `tools/validate.py`: checks structure only. It never runs a skill.

## License

Tooling and docs: MIT. Each skill declares its own license in `metadata.json`.
