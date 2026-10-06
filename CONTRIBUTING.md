# Contributing

Start with the [submission template](template/README.md). It includes the skill instructions, website metadata, a license starting point and a guide to the required preview. The pull request description has a separate checklist that GitHub fills in when you open the PR.

Include:

- Complete instructions in `SKILL.md`, with tools, versions and inputs.
- A preview and an HTTPS link to a result people can check.
- Steps to reproduce, known limitations, and what was AI-generated or edited by hand.
- A license for the skill, and permission to show every asset.

Include your public creator credit in `metadata.json`: `creator.github_id` is your permanent numeric GitHub ID as a string, `creator.github_login` is your username, and `creator.name` is your chosen public name. Find your ID in the `id` field at `https://api.github.com/users/YOUR_USERNAME`. Replace every placeholder in the template. A maintainer verifies the ID against the pull request author before publishing; claiming another person's identity is not allowed.

Do not include secrets, private client material, private personal data, other people's work without permission, or anything malicious. Your chosen creator credit and submitted files become public. Obtain permission for any coauthor credit.

Published skills appear on your creator profile at `https://beyondordinary.art/creators/YOUR_NUMERIC_ID`. GitHub sign-in on the site is optional and lets you add a public bio and display name. It does not publish submissions. Deleting a site account removes its custom profile data; separately published credits and public GitHub history remain. Contact the legal mailbox for withdrawal requests.

Leave `reviewed` and `rights_confirmed` as `false`. An authorized maintainer reviews the result, permissions and creator credit before merging. That merge approves publication; the website checks approved merges about every five minutes and records the review flags in its published copy. You do not need a second pull request to change those flags. Invalid entries stay unpublished and the prior catalog remains available. Review is an editorial decision, not a guarantee of originality, rights or safety.

The structure checks reject missing files, invalid dates, oversized fields, broken JPEG previews, and new creator credit that does not match the pull request author. They do not run the skill or prove rights, safety or creative quality. Existing skills can be improved without claiming their creator identity.

By submitting, you give Beyond Ordinary limited permission to display your entry, as set out in the [Terms](https://beyondordinary.art/terms). You keep ownership.

Withdrawals and reports: legal@beyondordinary.art. Do not post private complaints in public issues.
