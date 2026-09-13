# ForsatNet Authority Engine

Automation hub for publishing original English authority content that can earn relevant referring domains for ForsatNet.

## Current status

- GitHub repository connected and writable
- ForsatNet target pool configured
- First DEV article prepared
- DEV publishing script added
- Manual-dispatch GitHub Actions workflow added
- External publishing remains locked until `DEVTO_API_KEY` is configured as a GitHub Actions secret

## SEO policy

The engine prioritizes relevant, legitimate referring domains rather than bulk backlink creation.

Core rules:

- Prefer a new relevant referring domain over repeated links from the same domain
- Use one contextual ForsatNet link per article by default
- Avoid repetitive exact-match anchors
- Publish original, useful articles tailored to each platform
- Do not use a target landing page as `canonical_url` unless the external article is actually a republication of that canonical source
- Never claim a link is follow/nofollow/ugc/sponsored until it has been verified on the live page

## Repository structure

- `config/targets.json` — ForsatNet destination pool and strategy rules
- `articles/` — platform-ready English articles
- `queue/` — publication jobs and metadata
- `scripts/publish_dev.py` — DEV publishing client
- `.github/workflows/publish-dev.yml` — safe manual publication workflow

## One-time DEV setup

1. Sign in to DEV Community (`dev.to`).
2. Create an API key in account settings/extensions.
3. In this GitHub repository open `Settings` → `Secrets and variables` → `Actions`.
4. Create a new repository secret named exactly `DEVTO_API_KEY` and paste the DEV API key as its value.
5. Do not put the API key in source files, issues, chat messages, or commits.

After the secret exists, the first queued article can be published using the `Publish queued article to DEV` workflow.

## First queued article

**Title:** Which Business Tasks Should You Delegate to AI? A Practical 2x2 Decision Matrix

**Target:** https://www.forsatnet.ir/ai-management-delegation-matrix.html

The article uses a single natural contextual link to ForsatNet.
