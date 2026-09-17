# Configuring a custom domain

Our custom domain `lunssi.fi` is bought from Domainkeskus and points to the
`lunssi` Cloudflare Pages project.

## Cloudflare Pages

1. Add `lunssi.fi` as a site in Cloudflare (Websites > Add a site) if not
   already done. Cloudflare will show two nameservers to use.
2. Go to **Workers & Pages** > `lunssi` > **Custom domains**.
3. Add `lunssi.fi` and `www.lunssi.fi`. Cloudflare manages DNS and
   certificates for the domain automatically once it's active.

## Domainkeskus

1. Login to Domainkeskus.
2. Navigate to Domains > Manage Domain > Nameservers.
3. Replace the existing nameservers with the ones Cloudflare provided in
   step 1 above.
