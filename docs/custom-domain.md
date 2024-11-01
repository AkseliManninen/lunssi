# Configuring a custom domain

Our custom domain `lunssi.fi` is bought from Domainkeskus. The following steps are taken in Fly.io and Domainkeskus to allow traffic to the custom domain.

## Fly.io

1. Navigate to Certificates in the fly website.
2. Add new certificates for `lunssi.fi` and `www.lunssi.fi`.
3. Check that the addresses get verified after adding info to Domainkeskus.

## Domainkeskus

1. Login to Domainkeskus.
2. Navigate to Domains > Manage Domain > Manage DNS.
3. Add A and AAA records for @ and www. The records can be found from fly.io.
4. Add Domain ownership verification CNAME that can also be found from fly.io (this step might not be mandatory).

Using CNAME could be simpler but A / AAA records worked with less effort in this case.
