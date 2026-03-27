# Legacy Inventory

## Systems

- [x] legacy iOS app reviewed
- [x] legacy server reviewed
- [x] legacy utils reviewed
- [x] PRD reviewed

### Source basis

- iOS app: `/Users/josephsanfilippo/Documents/projects/hidden.adventures`
- server: `/Users/josephsanfilippo/Documents/projects/adventureserver`
- utilities: `/Users/josephsanfilippo/Documents/projects/utils`
- PRD: `/Users/josephsanfilippo/Documents/projects/hidden.adventures/output/pdf/hidden-adventures-suite-prd.pdf`

## Auth and Identity

- [x] Cognito user pool details captured
- [x] token and audience details captured
- [x] delete-account behavior documented

### Findings

- The iOS client is configured from `Config/Secrets.xcconfig` into `Info.plist` keys for server host/base path, Cognito client ID, Cognito pool ID, Cognito user pool region, and sign-in provider key.
- The example configuration pins the Cognito region to `us-west-2`.
- The server expects Cognito JWT validation inputs via `.env`: `COGNITO_PUBKEY`, `COGNITO_AUDIENCE`, `COGNITO_ISSUER`, `COGNITO_POOLID`, and `COGNITO_CLIENTID`.
- The server reads a PEM public key from disk and applies `passport-jwt` bearer-token auth to every `/api` route.
- The expected issuer format is `https://cognito-idp.us-west-2.amazonaws.com/<user-pool-id>`.
- The expected audience is the Cognito app client ID.
- If `custom:roles` is missing in the JWT payload, the server defaults the caller role to `user`.
- The iOS app uses Cognito interactive auth for sign-in, sign-up, confirmation, forgot password, confirm forgot password, and device remember flows.
- Delete account is initiated from the iOS app by calling `DELETE /api/users/:username`, then the client signs out locally and clears the cached session.
- The delete-account server controller deletes profiles, adventures, favorites, sidekicks, comments, and the Cognito user, but does not explicitly delete ratings authored by that user unless removed indirectly elsewhere.

## Data Collections

- [x] adventures
- [x] profiles
- [x] sidekicks
- [x] favorites
- [x] comments
- [x] ratings
- [x] messages
- [x] filenames

### Collection notes

#### `adventures`

- Fields: `name`, `desc`, `author`, `access`, `defaultImage`, `category`, `images[]`, `location`, `rating`, `ratingCount`, `acl[]`
- Storage model: Mongo document with GeoJSON `Point` and numeric coordinates
- Important behavior: `access` defaults to `private`

#### `profiles`

- Fields: `username`, `city`, `state`, `email`, `fullName`, `profileImage`, `backgroundImage`, `adventureCount`
- Important behavior: profile image changes are denormalized into sidekick and comment records

#### `sidekicks`

- Fields: `username`, `sidekickName`, `sidekickImage`
- Important behavior: add/remove sidekick mutates the `acl` array on all adventures authored by the requester

#### `favorites`

- Fields: `username`, `adventureID`

#### `comments`

- Fields: `username`, `adventureID`, `text`, `usernameImage`

#### `ratings`

- Fields: `username`, `adventureID`, `rating`
- Important behavior: rating create/update/delete also adjusts aggregate fields on the related adventure

#### `messages`

- Fields: `username`, `msgType`, `body`
- Used for support requests, bug reports, feature requests, and post reports

#### `filenames`

- Fields: `filename`
- Used as an image moderation queue after upload

## Media

- [x] S3 bucket and key patterns documented
- [x] image upload flow documented
- [x] image moderation flow documented

### Findings

- The server stores images in the S3 bucket referenced by `S3_BUCKETNAME`.
- The legacy docs and code confirm `S3_REGION=us-west-2`.
- The literal bucket name is present in local secrets/env files and should be migrated through secure environment management, not copied into rebuild docs.
- The iOS client generates image keys as `<username>_<uuid>.jpg`, lowercased and URL-path encoded.
- The client compresses images to roughly 250 KB JPEG before upload.
- The client uploads images to `POST /api/images` as multipart form data with a single field named `image`.
- The server uses `multer-s3` and stores the object with `file.originalname` as the S3 key.
- After upload, the server inserts the uploaded key into the `Filenames` collection for asynchronous moderation.
- Authenticated image retrieval happens through `GET /api/images/:key`, and the iOS app reads images back through that API rather than directly from S3.
- The image moderation utility polls `Filenames` every 15 minutes, fetches each object from S3, submits it to Sightengine, emails alerts through SES when thresholds are exceeded, and then clears the queue.

## Operations and Deployment

### Findings

- The legacy deployment shape is Bitnami-style and assumes `/home/bitnami/projects/...` for repo locations.
- Startup manifests exist for the API server, message processor, and image-check processor.
- Separate log files are configured for server, messages, and image-check jobs.
- Apache proxy config forwards `/api` and `/public` to the Node server on `127.0.0.1:3000`.
- Public legal pages are served from `htdocs` under `/public/privacy-policy.html` and `/public/terms-conditions.html`.
- The server uses Morgan request logging piped into Winston transports.
- The legacy server README recommends Node `16.x`, npm `8.x`, and MongoDB `4.2.x`.

## Risk Notes

- PRD is approved as feature-floor input only; do not treat it as a requirement to preserve the legacy UI structure.
- Legacy auth configuration sets `ignoreExpiration = true` in JWT validation; this must not carry into the rebuild.
- The iOS API client disables SSL certificate evaluation; this must not carry into the rebuild.
- The legacy backend is tightly coupled to MongoDB document mutation patterns and denormalized fields; those are migration inputs, not rebuild targets.
- The sidekick model mutates adventure ACLs on relationship changes, which is a data-coupled sharing design the rebuild should replace with explicit visibility policy modeling.
- Adventure deletion cascades into favorites and ratings but not comments in the legacy controller behavior.
- Delete-account flow does not explicitly remove user-authored ratings in all cases.
- The image delete handler in the legacy server reads bucket/key from the request body instead of trusting the route param.
- Media moderation is asynchronous and queue-based, which is useful operationally but may create UX gaps around upload success versus later rejection.
