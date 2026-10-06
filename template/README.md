# Fill in your submission

Copy `SKILL.md`, `metadata.json` and `LICENSE` into `skills/<your-skill-slug>/` in your fork. This README is a guide; it does not need to be copied. Replace every placeholder, then add your own preview and result.

Your finished submission should look like this:

```text
skills/your-skill-slug/
  SKILL.md
  metadata.json
  LICENSE
  example.html       # Optional: source files for your result
previews/
  your-skill-slug.jpg
```

## Fill in the files

1. Choose a slug using lowercase letters, numbers and single hyphens, such as `layered-paper-hero`. Use the same slug for the folder, metadata, SKILL.md `name`, and preview filename.
2. Write the instructions in `SKILL.md`. Include the inputs, tested tools, output format and instructions that produce your particular result. Remove the author guidance and placeholder text.
3. Fill in `metadata.json`. Find your permanent GitHub ID in the `id` field at `https://api.github.com/users/YOUR_USERNAME`. Keep it inside quotes. Use your own GitHub username and chosen public name.
4. Set `published` to the submission date in `YYYY-MM-DD` format. Choose `Web design`, `Motion`, `Video` or `Creative coding` for `category`.
5. Give `demo` an HTTPS link to the actual result. A public page, video or committed example is fine. The reviewer must be able to inspect it without requesting private access. A link to your general portfolio is not enough.
6. Add a JPEG preview under 2,000,000 bytes and no larger than 20 million pixels at `previews/<your-skill-slug>.jpg`. Use a screenshot or frame of the submitted result. Do not rename a PNG to `.jpg`.
7. Choose a license you can grant. The supplied `LICENSE` is an MIT starting point: replace its year and public name if you choose MIT. Otherwise replace the file and update `metadata.json` to match. Explain any separate licenses for assets.

Leave `reviewed` and `rights_confirmed` as `false`. These are publication fields, not boxes you check yourself.

## Keep it within the limits

| Field | Limit |
| --- | --- |
| `slug` | 80 characters |
| `title`, `author`, creator `name` | 100 characters each |
| `summary` | 280 characters |
| `distinctive`, `limitations`, `proof_note` | 600 characters each |
| `tools` | 1–8 items, 60 characters per item |
| `requirements` | 1–12 items, 200 characters per item |
| `steps` | 2–12 items, 500 characters per item |
| `metadata.json` | 50,000 bytes |
| `SKILL.md` | 100,000 bytes |

Put the full instructions in `SKILL.md`; the metadata is the short version shown on the website. JSON does not allow comments or trailing commas.

## Open the pull request

Commit the files to a branch in your fork. Open a pull request to `avixityyt/beyondordinary-skills`, with `main` as the base branch. GitHub fills in the submission checklist automatically; replace its prompts and complete only the boxes you can confirm. Suggested title: `Add skill: Your skill title`.

Include the exact inputs used for your proof, tool versions, manual edits and known limitations. A maintainer reviews the result and permissions before merging. A successful check alone does not publish the entry. An authorized admin merge normally publishes it on the next website check, about every five minutes.

Your files, creator credit and PR description are public. Keep secrets and private client or personal data out of the submission. Read [CONTRIBUTING.md](../CONTRIBUTING.md) before sending it.
