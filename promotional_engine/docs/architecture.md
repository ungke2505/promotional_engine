# Promotional Engine Architecture

## Objective

Provide a single operational surface for configuring promotions across ERPNext v14 and executing them inside POSAwesome.

## Primary building blocks

### 1. Promotion Campaign

Commercial container for a promo period or business objective.

Examples:

- Weekend discount
- Payday coupon
- Buy 2 Get 1 snack
- Ramadan loyalty booster

### 2. Promotion Rule

Atomic rule executed by the engine.

Examples:

- cart discount by amount threshold
- item discount by item or item group
- buy X get Y
- validate coupon
- earn points
- redeem points to discount
- redeem points to cashback

### 3. Coupon Batch

Defines mass coupon generation and coupon validity windows.

### 4. Loyalty Policy

Defines how points are earned and redeemed, including point-to-cashback conversion.

### 5. Promotion Redemption

Audit log for applied promo transactions.

## Single-page operating model

`Promotional Engine Console` is the central page intended for business admins.

The page should eventually provide:

- campaign summary cards
- active promo timeline
- quick create actions
- simulation form for cart testing
- coupon generator
- loyalty policy setup
- applied promo log

## POSAwesome flow

1. POS cart changes
2. POSAwesome calls `promotional_engine.api.get_applicable_promotions`
3. Server gathers active campaigns
4. Rules are evaluated in priority order
5. Conflict rules are resolved
6. POS receives normalized result:
   - line discounts
   - cart discounts
   - free items
   - coupon validation result
   - points earn / redeem / cashback result
7. After invoice submission, the engine writes a `Promotion Redemption` log

## Recommended next implementation slices

1. Add child tables for campaign conditions and stackability rules
2. Implement coupon code generation and validation
3. Add customer segment support
4. Add territory / branch / POS Profile filtering
5. Add cart simulator UI on the console page
6. Inject POSAwesome frontend hook for real-time promo recomputation
