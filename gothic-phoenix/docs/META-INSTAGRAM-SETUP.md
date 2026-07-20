# Gothic Phoenix — Meta/Instagram Publishing Setup

## Goal
Enable approved Gothic Phoenix still images and Reels to publish through n8n, verify the permalink, and retrieve performance metrics.

## Security rules
- Never commit access tokens, app secrets, Instagram passwords, or Page tokens.
- Store secrets only in n8n credentials or protected environment variables.
- Keep the publish node disabled until the test checklist passes.
- Require explicit human approval immediately before publication.

## Recommended authentication path
Use Instagram API with Facebook Login for the first production integration because it supports a linked Instagram Professional account and Facebook Page and has an established Page-token flow.

## Human account setup
1. In Instagram, open Settings and activity > Account type and tools.
2. Confirm the account is Business or Creator. Convert it if it is personal.
3. In Instagram Edit profile > Page, connect the correct Facebook Page.
4. In Meta Business Suite Settings, confirm the same Facebook Page and Instagram account are present and that the owner has full control.
5. Enable two-factor authentication on the owning Facebook and Instagram accounts.

## Meta developer setup
1. Sign in at Meta for Developers using the Facebook account with full control.
2. Create an app intended for business use.
3. Add the Instagram API product and Facebook Login for Business where offered by the current interface.
4. Add the owning Facebook account as an app administrator/developer.
5. During development, keep the app in Development mode and test only with app-role users and the connected professional account.
6. Request only the permissions required by the selected Meta flow. For the Facebook Login flow, verify the current permission names in Meta's dashboard before requesting them. Typical publishing integrations require access to the linked Pages plus Instagram basic/content-publishing capabilities.
7. Generate a user token through the supported OAuth/Graph API Explorer flow, exchange it for a long-lived token when available, and retrieve the Page token and Instagram professional account ID.

## Required n8n secrets
- META_GRAPH_API_VERSION
- META_ACCESS_TOKEN
- META_IG_USER_ID
- META_FACEBOOK_PAGE_ID

Optional:
- META_APP_ID
- META_APP_SECRET

## Still-image publication sequence
1. Ensure the final image is available through a direct public HTTPS URL with no cookies, redirects, or login.
2. POST to `https://graph.facebook.com/${META_GRAPH_API_VERSION}/${META_IG_USER_ID}/media` with:
   - `image_url`
   - `caption`
   - `access_token`
3. Save the returned creation/container ID.
4. Poll container status until ready or failed.
5. After explicit approval, POST to `https://graph.facebook.com/${META_GRAPH_API_VERSION}/${META_IG_USER_ID}/media_publish` with:
   - `creation_id`
   - `access_token`
6. Save the published media ID.
7. GET the media object fields needed for verification, including permalink when supported.
8. Record the media ID, permalink, timestamp, caption version, asset URL, and approval evidence in Notion.

## Test checklist
- [ ] Instagram account is Professional.
- [ ] Correct Facebook Page is linked.
- [ ] Owner has full control of Page, Instagram account, Business Portfolio, and Meta app.
- [ ] n8n can read the four required secrets.
- [ ] Public image URL returns HTTP 200 and image/png or image/jpeg.
- [ ] Test container can be created.
- [ ] Container reaches ready state.
- [ ] Publish node remains blocked before approval.
- [ ] Approved test post publishes successfully.
- [ ] Permalink and media ID are retrieved.
- [ ] Test media metrics can be queried.
- [ ] No secrets appear in workflow exports or Git history.

## Production activation rule
Enable the scheduled workflow only after every test passes. Keep the human approval gate enabled for all posts until an explicit policy change is approved.