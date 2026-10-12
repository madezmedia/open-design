# Deployment

Open Design ships the `apps/web` Next.js app as a **static export** (`apps/web/out/`) in production, served by the daemon from the same process. The containerized workflow builds the web export, bundles the daemon, and produces a single runtime image. For operator-managed production, Vercel and Cloudflare Pages are first-class targets.

---



## 0. What this docs set covers

| Document | Purpose |
|---|---|
| `README.md` | This file — local run, build pipeline, Vercel, Cloudflare Pages, Docker |
| `docker-compose.yml` | Single-image local/production compose |
| `Dockerfile` | Multi-stage build: Next.js static export + daemon runtime |
| `scripts/publish-images.sh` | Docker Hub multi-arch publish + skopeo preload |
| `scripts/prepare-colima-build-swap.sh` | Apple Silicon Colima swap helper for low-RAM hosts |
| `tests/prepare-colima-build-swap.test.ts` | Swap helper unit tests |

---



## 1. Architecture

```
Production
  apps/web/next.config.ts → output: export → apps/web/out/
  daemon serves /api/* + /artifacts/* + /frames/*
  daemon also serves apps/web/out/ as static files
  → single port, single process, same-origin
```

`vercel.json` points `outputDirectory` at `apps/web/out/`, so Vercel gets the exact same bundle the daemon serves locally.

`apps/web/next.config.ts`:

- `NODE_ENV=production` + no `OD_WEB_OUTPUT_MODE` → static export to `apps/web/out/`
- `OD_WEB_OUTPUT_MODE=server|standalone` → server-runtime mode for desktop/E2E
- `OD_WEB_PROD=1` → canonical `out/` dist dir even if `OD_WEB_DIST_DIR` is set

```bash
# canonical build
pnpm --filter @open-design/web build
# output: apps/web/out/{index.html,_next/,assets/...}
```

The daemon's `STATIC_DIR` points at `apps/web/out/` when the export exists, so no separate nginx is required for local or container deployments.

---



## 2. Vercel

`vercel.json`:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "pnpm install && pnpm --filter @open-design/web build",
  "installCommand": "pnpm install",
  "outputDirectory": "apps/web/out",
  "framework": null
}
```

The build uses the same Next.js static export that the daemon ships. `trailingSlash: true` from `next.config.ts` means every directory has its own `index.html`, so clean URLs work without extra routing config.

Deploy config is persisted per-provider in `~/.open-design/`:

- Vercel → `~/.open-design/vercel.json`
- Cloudflare Pages → `~/.open-design/cloudflare-pages.json`

Files are `chmod 600`. Tokens are masked on readback (`SAVED_TOKEN_MASK` / `SAVED_CLOUDFLARE_TOKEN_MASK`).

---



## 3. Cloudflare Pages

Cloudflare Pages publishes the same `apps/web/out/` bundle. Project names are auto-derived from the Open Design project id to match Vercel's `od-<projectId>` convention.

Config shape:

```json
{
  "token": "<cloudflare-api-token>",
  "accountId": "<account-id>",
  "cloudflarePages": {
    "lastZoneId": "zone-1",
    "lastZoneName": "example.com",
    "lastDomainPrefix": "demo"
  }
}
```

Limits mirror Cloudflare's hard caps:

```ts
export const CLOUDFLARE_PAGES_ASSET_UPLOAD_MAX_FILES = 100;
export const CLOUDFLARE_PAGES_ASSET_UPLOAD_MAX_BODY_BYTES = 75 * 1024 * 1024;
export const CLOUDFLARE_PAGES_ASSET_MAX_BYTES = 25 * 1024 * 1024;
```

Deployments >100 files or >75MB total body are rejected at the upload boundary.

Custom domains: after upload, the Cloudflare Pages project is bound to the user's zone/domain prefix. DNS record creation is delegated to the user or the operator.

---



## 4. Local compose

```bash
cd deploy
OPEN_DESIGN_IMAGE=docker.io/vanjayak/open-design:latest docker compose pull
OPEN_DESIGN_IMAGE=docker.io/vanjayak/open-design:latest docker compose up -d --no-build
```

Defaults:

- Host port: `127.0.0.1:7456` (`OPEN_DESIGN_PORT=8080` to publish on `127.0.0.1:8080`)
- Runtime data volume: `open_design_data` mounted at `/app/.od`
- Node heap cap: `--max-old-space-size=192`
- Compose memory cap: `384m` (`OPEN_DESIGN_MEM_LIMIT=256m` to override)

Do not publish the daemon directly on a public or shared LAN interface. The API is unauthenticated for non-browser clients, so remote deployments should keep Compose bound to localhost and put an authenticated reverse proxy, SSH tunnel, or VPN in front of it.

When exposing the service through an authenticated public IP, domain, or reverse proxy, set `OPEN_DESIGN_ALLOWED_ORIGINS` to the browser origins that should be allowed to call `/api`:

```bash
OPEN_DESIGN_ALLOWED_ORIGINS=https://od.example.com,http://203.0.113.10:7456 docker compose up -d --no-build
```

Pin a specific published image with a digest instead of the mutable `latest` tag:

```bash
OPEN_DESIGN_IMAGE=docker.io/vanjayak/open-design@sha256:<digest> docker compose up -d --no-build
```

The image does not bundle Claude/Codex/Gemini CLI binaries. Keep those outside the image, or build a separate private runtime layer if a server deployment needs local code-agent CLIs installed in the container.

---



## 5. Publish to Docker Hub

```bash
deploy/scripts/publish-images.sh --image_tag latest
```

Useful overrides:

```bash
IMAGE_NAMESPACE=your-dockerhub-user deploy/scripts/publish-images.sh --arch arm64
deploy/scripts/publish-images.sh --image docker.io/your-user/open-design:0.1.0
```

The script defaults to:

- `docker.io/vanjayak/open-design:<tag>`
- `linux/amd64,linux/arm64`
- `skopeo` push strategy with Docker credentials read from `~/.docker/config.json`
- preloading base images through `skopeo` to reduce Docker Hub pull flakiness

If `127.0.0.1:7890` is available and no proxy is already set, the script uses it for registry access and passes `host.docker.internal:7890` into Docker builds. The host-gateway alias is only added for builds that need this local proxy mapping.

### Colima swap helper for Apple Silicon

`deploy/scripts/prepare-colima-build-swap.sh` is for manual Docker image publishing from an Apple Silicon macOS host that uses Colima as the Docker VM. The helper is intentionally Apple Silicon-only because the failure mode it covers is local arm64 Colima builds exhausting a small Linux VM while preparing multi-arch images. It exits before touching Colima on non-macOS or non-Apple-Silicon hosts.

Low-memory Colima VMs can run out of RAM during multi-arch image builds. The helper checks the VM memory and swap status, then creates and enables a temporary swap file only when the VM has no swap and less than 4 GiB of RAM. The 4 GiB threshold is a conservative default for short-lived manual publishes on small Colima profiles; raise `COLIMA_BUILD_SWAP_MEMORY_THRESHOLD_KIB` if larger builds still OOM, or lower it if you only want swap for very small VMs.

Prefer increasing the Colima VM memory (`colima start --memory <GiB>` or the profile config) when you want a persistent build machine. Use this helper when you need a temporary, reversible boost for one manual publish without resizing or recreating the VM.

Run it before a manual publish if Docker builds fail with out-of-memory errors, or if `status` shows a small Colima VM with no swap. The swap remains active until cleanup or VM restart, so use a shell trap for one-off sessions:

```bash
deploy/scripts/prepare-colima-build-swap.sh status
deploy/scripts/prepare-colima-build-swap.sh
trap 'deploy/scripts/prepare-colima-build-swap.sh cleanup' EXIT
deploy/scripts/publish-images.sh --image_tag latest
```

Useful overrides:

```bash
COLIMA_BUILD_SWAP_SIZE=6G deploy/scripts/prepare-colima-build-swap.sh
COLIMA_BUILD_SWAP_MEMORY_THRESHOLD_KIB=6291456 deploy/scripts/prepare-colima-build-swap.sh
COLIMA_BIN=/opt/homebrew/bin/colima deploy/scripts/prepare-colima-build-swap.sh status
COLIMA_BUILD_SWAP_CLEANUP_FORCE=1 COLIMA_BUILD_SWAPFILE=/custom-swapfile deploy/scripts/prepare-colima-build-swap.sh cleanup
```

`cleanup` removes the default helper path and the old helper path. If you set a custom `COLIMA_BUILD_SWAPFILE`, cleanup refuses to remove it unless `COLIMA_BUILD_SWAP_CLEANUP_FORCE=1` is also set.

---



## 6. Dockerfile and image shape

Multi-stage:

1. `build` — installs workspace deps, builds `@open-design/daemon` and `@open-design/web`, prunes dev/test artifacts
2. `runtime` — `node:24-alpine`, copies built daemon + `apps/web/out/` + bundled skills/design-systems/assets/plugins

The runtime user is `open-design:open-design` (UID/GID 1001). The entrypoint is `tini` + `node apps/daemon/dist/cli.js --no-open`. The daemon exposes `/api/*`, `/artifacts/*`, `/frames/*`, and static file serving for the Next.js export from the same port.

---



## 7. Reverse proxy notes

If you place nginx/caddy in front of the daemon, keep SSE routes unbuffered and uncompressed. A common failure is `net::ERR_INCOMPLETE_CHUNKED_ENCODING 200 (OK)` after 80–90 seconds because nginx `gzip on` buffers chunked SSE responses even when the daemon sends `X-Accel-Buffering: no`.

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:7456;

    proxy_buffering off;
    gzip off;

    proxy_read_timeout 86400s;
    proxy_send_timeout 86400s;
    proxy_http_version 1.1;
    proxy_set_header Connection "";

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
