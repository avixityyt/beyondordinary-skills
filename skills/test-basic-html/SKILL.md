---
name: test-basic-html
description: Create a plain HTML page from a supplied title and sentence for testing the Beyond Ordinary submission workflow.
---

# Basic HTML test

Take the user's title and one sentence. Return a complete HTML5 document in a single HTML code block.

Use `lang="en"`, UTF-8, a viewport meta tag, and the supplied title in `<title>`. In `<main>`, put the title in one `<h1>` and the sentence in one `<p>`. Escape the supplied text as HTML. Use browser defaults: no CSS, JavaScript, images, fonts, or external resources.

If the title or sentence is missing, ask for it. Do not add other content or write files unless asked.
