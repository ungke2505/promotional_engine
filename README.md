# Promotional Engine for ERPNext v14 + POSAwesome

`promotional_engine` is a custom Frappe app that centralizes all promotional logic in one place for ERPNext v14 with POSAwesome as the POS frontend.

With this app, business users can manage:

- discount campaigns and offers
- coupon validation rules
- loyalty earning and redemption
- points-to-cashback conversion
- promotion usage logging
- POS-specific targeting and rule priority

## Current scope

This repository is now structured as a portable Frappe app and is ready to be pushed to GitHub. It includes:

- standard app packaging
- DocTypes for core promotion entities
- a console page and workspace
- a backend rule engine with modular services
- unit tests for core promo scenarios
- installation guidance for a development server

Bench-compatible packaging files also live at the repository root, so `bench get-app` can install the app directly from GitHub.
The top-level `promotional_engine` package also exposes Frappe-compatible entry points for bench and app discovery.

## App structure

- `promotional_engine/promotional_engine/api.py`: whitelisted API for POSAwesome
- `promotional_engine/promotional_engine/services/`: promotion engine modules
- `promotional_engine/promotional_engine/promotional_engine/doctype/`: ERPNext/Frappe DocTypes
- `promotional_engine/promotional_engine/promotional_engine/page/`: central console page
- `promotional_engine/tests/`: pure Python unit tests
- `promotional_engine/docs/architecture.md`: architecture notes

## Core entities

- `Promotion Campaign`
- `Promotion Rule`
- `Promotion Condition`
- `Coupon Batch`
- `Loyalty Policy`
- `Promotion Redemption`

## Features implemented

- cart discount and item discount evaluation
- buy X get Y free-item output
- coupon validation hook
- points earning
- points redemption as discount
- points redemption as cashback
- priority-based rule execution
- stackability toggle
- dynamic conditions through child table rules
- fallback loading from Frappe DB when payload is not injected manually

## Local test command

From the repo root:

1. `.\.venv\Scripts\python.exe -m unittest discover promotional_engine\tests`

## Development server install guide

These steps are intended for an ERPNext v14 bench on your development server.

1. Push this repository to GitHub.
2. On the server, go to your bench folder.
3. Run `bench get-app <your-github-repo-url>`.
4. Run `bench --site <your-site> install-app promotional_engine`.
5. Run `bench --site <your-site> migrate`.
6. Run `bench build`.
7. Restart bench services if needed.

If POSAwesome is already installed, the next integration step is wiring the POS cart payload to `promotional_engine.promotional_engine.api.get_applicable_promotions`.

## Notes

- This local workspace still does not contain a full Bench / ERPNext / POSAwesome source tree, so actual installation has not been executed from here.
- The backend engine is testable without Frappe by passing cart, campaigns, rules, and loyalty policy as payload.
