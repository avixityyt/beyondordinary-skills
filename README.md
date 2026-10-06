# Beyond Ordinary Skills

Creative AI skills for [beyondordinary.art](https://beyondordinary.art).

Reviewed skills are credited to your permanent GitHub identity and listed on your creator profile. Site sign-in is optional; it lets you edit a public display name and bio. See the creator metadata instructions in [CONTRIBUTING.md](CONTRIBUTING.md).

## Submit

1. Fork this repository.
2. Follow the [submission starter](template/README.md): copy its files to `skills/<your-slug>/` and fill in `metadata.json`, `SKILL.md` and your license.
3. Add a JPEG preview at `previews/<your-slug>.jpg` (under 2 MB).
4. Open a pull request to `main`. GitHub fills in the [submission checklist](.github/pull_request_template.md); add your result, reproduction details and permissions.

A maintainer reviews every submission. An authorized admin merge approves publication, and the site syncs reviewed catalog changes about every five minutes. There is no separate flag-editing or app deployment step. Submissions are validated as data; their instructions and scripts are never executed by the publication worker. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

- `skills/<slug>/metadata.json` and `SKILL.md`
- `previews/<slug>.jpg`
- `template/`: starting point
- `tools/validate.py`: checks structure only. It never runs a skill.

## License

Tooling and docs: MIT. Each skill declares its own license in `metadata.json`.
