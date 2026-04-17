# Development Server Install Guide

## Prerequisites

- Existing Frappe / ERPNext v14 bench
- A development site already created
- POSAwesome already installed if you want POS integration immediately
- Git access from the server to this repository

## Install steps

1. Open the bench directory on the development server.
2. Fetch the app:
   - `bench get-app <repo-url>`
3. Install the app on your site:
   - `bench --site <site-name> install-app promotional_engine`
4. Apply schema changes:
   - `bench --site <site-name> migrate`
5. Build frontend assets:
   - `bench build`
6. Clear cache:
   - `bench --site <site-name> clear-cache`

## Smoke checks

After install, verify:

- The `Promotional Engine` workspace is visible.
- The page `promotional-engine-console` opens.
- DocTypes are present:
  - `Promotion Campaign`
  - `Promotion Rule`
  - `Promotion Condition`
  - `Coupon Batch`
  - `Loyalty Policy`
  - `Promotion Redemption`
- Whitelisted method is callable:
  - `promotional_engine.promotional_engine.api.get_applicable_promotions`

## First data setup

1. Create one `Promotion Campaign` with status `Active`.
2. Create one `Loyalty Policy` with:
   - point-to-currency rate
   - minimum redeem points
   - maximum cashback percent
3. Create one `Promotion Rule` for cart discount or points redeem.
4. Optional:
   - add `Promotion Condition` rows to target customer groups, POS Profile, subtotal, or available points.

## Known next integration task

To make POSAwesome consume this engine live, connect cart updates in POSAwesome to the whitelisted API and map the response keys:

- `line_discounts`
- `cart_discounts`
- `free_items`
- `coupon_result`
- `points_result`
- `totals_after`
