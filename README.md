# Jongu Apps Ecosystem

Monorepo of Jongu apps and templates. Each app runs and deploys independently (Next.js + Supabase + Vercel).

## Structure

```
jongu-social-media-1/
├── jongu-wellness/                 # Wellness channel app
├── jongu-tool-best-possible-self/  # Best Possible Self tool
├── jongu-mvp-new/                  # MVP channel app
├── jongu-children-watch/           # Children’s media channel
├── jongu-daniel-tiger/             # Daniel Tiger community channel
├── shared-config/                  # Shared types/helpers (local)
└── scripts/                        # Automation scripts
```

## Quick start (Windows PowerShell)

- Install and run per app:
	- Open a new terminal in the app folder
	- Install: `npm install`
	- Copy env: `Copy-Item .env.example .env.local` (if present)
	- Run dev:
		- Wellness: `npm run dev` (http://localhost:3003)
		- BPS Tool: `npm run dev` (http://localhost:3000)
		- Children Watch: `npm run dev` (http://localhost:3010)

Tip: You can run multiple apps at once in separate terminals.

## Supabase & Auth

- Single Supabase project across apps for unified auth
- Passwordless email magic links recommended
- Central callback sets cookies for cross-subdomain SSO

## Deploy

Deploy each app from its folder via Vercel. Ensure environment variables are set in Vercel Project Settings (see each app’s README).

## License

Unless noted otherwise, projects are licensed under Creative Commons Attribution-ShareAlike 4.0. See each app’s `LICENSE` file.