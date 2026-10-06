# Repository moderation

The normal submission path stays open. The repository limits external contributors to two open PRs and requires workflow approval for all external contributors. Branch protection requires the metadata check and a code-owner review. Review workflow changes before approving any run; do not grant write access merely to bypass a limit.

Inspect the Actions check summary for account-age, automated-account, burst and duplicate-body signals. These are prompts for review, not grounds for an automatic ban. The check has read-only permissions and never posts comments, closes PRs or runs submitted instructions.

## During a spam incident

Open repository **Settings → Moderation options → Interaction limits**. Use a temporary existing-user limit to restrict accounts under 24 hours old, or a prior-contributor limit during a larger incident. Choose a duration and review the effect on legitimate contributors. These restrictions expire automatically; they are not enabled during normal operation.

Blocking or reporting an abusive account is a manual owner decision. Keep private complaints and evidence out of public issues and PR comments. Website reports remain private in the admin library page.

An authorized administrator merge is the final publication decision. Check the result, source of assets, creator identity and instruction safety before merging, even when the checks pass. The website's publisher does not execute repository code.
