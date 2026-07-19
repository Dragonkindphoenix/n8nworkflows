# Gothic Phoenix AI Artist Automation

This folder contains the implementation scaffold for the Gothic Phoenix autonomous production, critique, publishing, and learning pipeline.

## Current architecture

1. Daily trigger
2. Read Notion command center and content tracker
3. Select deliverable type
4. Retrieve approved references from Google Drive
5. Generate production brief and prompts
6. Generate or ingest image/video candidates
7. Run technical QA and multi-role creative critique
8. Stop at human approval gate
9. Publish through the official Instagram Graph API when credentials are configured
10. Verify the post and collect 24h, 72h, and 7d metrics
11. Update the Art Review Registry, Tool Registry, Improvement Log, prompt library, and failure library

## Security

Never commit API keys, Meta tokens, vendor secrets, or private asset URLs. Use n8n credentials or environment secrets. Publishing remains disabled until the Meta connection passes its verification test.

## Required credentials

- NOTION_TOKEN
- GOOGLE_DRIVE credentials
- META_ACCESS_TOKEN
- META_IG_USER_ID
- META_FACEBOOK_PAGE_ID
- optional RUNWAY_API_KEY
- optional ELEVENLABS_API_KEY
- optional object-storage credentials

## Folders

- `workflows/` n8n workflow exports
- `config/` brand and folder identifiers without secrets
- `scripts/` FFmpeg and QA utilities
- `schemas/` production and review data contracts
- `docs/` setup and verification instructions

## Initial state

Drive and Notion structures are active. Direct Instagram publishing and cinematic video generation remain credential-blocked.