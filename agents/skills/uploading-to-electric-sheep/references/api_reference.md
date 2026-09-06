# Electric Sheep API notes

Reverse-engineered from validation errors (no OpenAPI spec exists). Verified 2026-08-04 and 2026-09-06.

## Base and auth

- Base: `https://dev-edit.electricsheep.tv/api/v1`
- Header: `Authorization: Bearer <key>`
- Key: 1Password TSE item `iu5v37zthenhj6tucyfoxi6j7e` ("claude-m2-mac - electric-sheep"), password field. Its notes carry the same endpoint map.
- The key has an `sk_live_` prefix but is dev-scoped. Prod (`edit.electricsheep.tv`) rejects it with 401. Dev is the intended target: investor access, dev carries features prod does not. Do not "correct" to prod.
- Anything under `/api/*` that is not `/api/v1/*` returns `{"error":"Not authenticated"}` even for paths that do not exist. That is the playground UI namespace, not a dead key.
- Browser playground (session cookie, not the Bearer key): `https://dev-edit.electricsheep.tv/api`

## Endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/folders` | Tree: `data[]` with `id`, `name`, `path`, `children[]`, `media_count`, `shares[]` |
| POST | `/folders` | JSON `{"path": "name"}`. Returns `id`, `path`, `created[]`. Missing path gives 400 `path is required` |
| GET | `/media?limit=100&cursor=…` | Cursor paging: `data[]`, `next_cursor`, `has_more`. `folder_id` filter is not reliable, so filter client-side on `folder_path` (list of folder ids) |
| GET | `/media/{id}` | Fields: `media_id`, `title`, `status`, `type`, `folder`, `folder_path`, `duration`, `signed_url` |
| POST | `/media/upload` | multipart. `file` or `source_url` required. Optional `folder_id` (uuid) or `folder` (name), `title`. Returns `media_id`, `status: processing` |
| GET | `/media/uploads?id=<uuid>` | per-upload status |
| DELETE | `/media/{id}` | 200 on success |
| DELETE | `/folders/{id}` | Returns `{"deleted": true, "id": …}` |
| GET | `/webhooks` | list |

## Upload behaviour

- Accepted content types: `video/*`, `audio/*`, `image/*`. `text/plain` is rejected with a clear message, so a bogus file is a safe probe.
- A bad `folder_id` returns a bare `Internal Server Error`, not JSON.
- The response `folder` field is `null` when `folder_id` was used, but the item does land in the folder (`folder_path` carries the id). With `folder=<name>` the response echoes the name.
- Status moves `processing` → `splitting` → `transcoding` → `complete`.
- For every video the platform creates a child item titled `<title>_audio`, so a folder's `media_count` is about double the number of uploads.
- A 1GB `.MOV` took about five minutes over home wifi; 2GB of clips took about seven minutes total.
