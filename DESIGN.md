---
version: alpha
colors:
  primary: "#b8486a"
  cream: "#fbf6f1"
  paper: "#fffdfb"
  ink: "#2b2024"
  plum: "#4a2a35"
  rose-deep: "#8d2f4d"
  blush: "#f4dde3"
  blush-soft: "#fbebef"
  sand: "#f2e6da"
typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, Times New Roman, serif"
  body:
    fontFamily: "Manrope, Trebuchet MS, Arial, sans-serif"
rounded:
  card: "22px"
  pill: "999px"
omitted:
  - section: spacing
    reason: "Use the existing responsive section-pad and section spacing in styles.css."
  - section: components
    reason: "This static landing page uses shared CSS classes rather than a component-token adapter."
---

# Rose 73 — existing design with sourced content

## Overview
Preserve the original design explicitly preferred by the user after rejecting the previous redesign: warm cream, dusty rose, plum, Cormorant Garamond/Manrope, rounded panels and the original three-photo hero collage. This change adds factual content; it is not a new visual direction.

## Colors
Runtime `:root` in styles.css is canonical (Model B). colors.primary maps to --rose. Other documented colors map to identically named CSS variables. New catalogue, gift, service, photo and review sections reuse these existing variables. New smaller text uses plum for legibility.

## Typography
display → --serif → headings. body → --sans → copy, prices and controls. Keep Cyrillic-capable fonts and existing fallbacks. Product titles are factual, prices clearly visible and not presented as discounts.

## Layout
Keep original section-pad gutters (9vw desktop, 6vw narrow), hero composition, marquee and original sections. Add catalogue after marquee; gifts/services before about; gallery/reviews before contacts. Catalogue grid 3/2/1 columns; gifts 4/2; reviews 3/2/1. Responsive breakpoints extend the existing 1080/860px layout with 540px content rules.

## Elevation & Depth
Reuse original photo shadows, hairline borders and quiet paper surfaces. No change to the original brand or hero.

## Shapes
22px content cards, rounded photo thumbnails and pill-shaped controls match existing occasions and buttons. Keep photography as photography rather than creating illustrations of products.

## Components
Catalogue filters are a mutually exclusive button group with aria-pressed, plus an independent budget checkbox. Show six matching bouquets initially and add six per click. Announce counts and show an actionable empty state. State is deliberately local and transient on this marketing page. With JavaScript unavailable, all static products remain readable.

Photo viewer uses a native dialog for focus trapping, background isolation and Escape. Restore the originating button on close. Arrow keys and visible buttons move within the active visible photo group. Viewer displays the matching product's actual price. Gallery photos have no implied product price.

## Do's and Don'ts
Use the source product's own image with its price; do not pair unrelated gallery photos with priced bouquets. Prices, rating, counts and source links are a dated snapshot checked 2026-11-09, not live inventory. Catalogue source says updated 21 August without a displayed year. Delivery, wedding floristry and wrapping have no published tariff; state that these are agreed separately. Toy prices exclude flowers shown in photos. Reviews are clearly labelled summaries with authentic names, dates, ratings and original-source links. Never invent prices, delivery guarantees or testimonials.
