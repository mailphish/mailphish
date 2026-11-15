# Email templates

Keep one `.html` file per fictional training example. The file contains the formatted message body. Keep the exercise title and email subject as separate fields when the scenario library is added. A matching `.txt` file can provide a plain-text alternative. [Email message bodies in Python](https://docs.python.org/3/library/email.examples.html)

Use simple HTML with inline styles for email-client compatibility. Use fictional names and content in examples. Keep the directory outside `frontend/src/` so the development server serves only the training interface files as public assets.

The starter does not load templates yet. This directory is the planned source for the exercise scenario picker.

## Draft scenario set

The draft library deliberately keeps few **message types** (the situation/pretext) and instead varies the **brand** being impersonated, since recognizable brands are what make a lure convincing in practice. Each file is self-contained inline-styled HTML and opens with an HTML comment (invisible to recipients) documenting the subject line, sender, the psychological trigger it relies on, the real-brand visual details it was checked against, and the red flags to cover in the post-exercise debrief. See [`RESEARCH.md`](RESEARCH.md) for the reasoning and source notes.

| Type | File | Brand impersonated |
| --- | --- | --- |
| Account / security alert | `01-microsoft-account-alert.html` | Microsoft 365 |
| Account / security alert | `02-google-account-alert.html` | Google |
| Parcel delivery notification | `03-zasilkovna-delivery.html` | Zásilkovna / Packeta |
| Parcel delivery notification | `04-dhl-delivery.html` | DHL |
| Shared document | `05-google-drive-shared-file.html` | Google Drive |
| Shared document | `06-onedrive-shared-file.html` | Microsoft OneDrive |

All scenarios send from a fictional `*.example` domain (reserved by RFC 2606, never resolvable) styled as a realistic look-alike of the impersonated brand's real domain (e.g. `micr0soft-verify.example`, `accounts-google-security.example`) — the gap between the look-alike and the real domain is itself one of the red flags for the debrief. No official logo artwork is used anywhere; brand marks are approximated with plain CSS (colored shapes/text) using each brand's public color palette, checked against the brands' current public web presence. Each template accepts simple merge fields such as `{{recipient_name}}`, `{{recipient_email}}`, and `{{tracking_url}}`, which the backend will substitute once the exercise/scenario feature lands; until then they are plain placeholders.

These are **training materials for a controlled, consented exercise only** — see the *Etika a hranice použití* section in [`RESEARCH.md`](RESEARCH.md) before reusing them outside this project.

## Reference (legitimate) email

[`07-figma.html`](07-figma.html) is **not a phishing scenario**. It is a sanitized recreation of a genuine Figma transactional e-mail ("your request to edit a file was approved"), kept as a reference for debrief — to show what a real e-mail from that brand actually looks like, alongside the brand-impersonation scenarios above. It keeps the real layout, copy, and the CAN-SPAM-mandated physical address, but strips every element that was tied to the original recipient or to Figma's own assets — real `click.figma.com` tracking links, the Gmail message/thread identifiers, the hosted logo images, and the hidden tracking pixel are all gone, replaced with plain placeholders or a CSS-only logo approximation like the rest of this library. See the file's own header comment for the full rationale.