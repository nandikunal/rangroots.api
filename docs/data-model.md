# Data Model (initial)

## City
- id, name, country, region, timezone, latitude, longitude

## User
- id, name, email, password_hash, role (visitor/registered/admin), preferred_cities, language

## Event
- id, city_id, title, description, venue_name, venue_address
- start_datetime, end_datetime, organizer_name, organizer_id
- event_category (festival, community, social_cultural, food_market, embassy_official, commercial_promo, other)
- community_state_tag, organizer_type (temple, association, embassy, business, individual)
- is_free, has_entry_fee, price_from, price_to, currency, booking_url
- language, is_family_friendly
- status (draft, submitted, under_review, approved, rejected)
- created_by_user_id, created_at, updated_at, reviewed_by_admin_id, review_notes

## CalendarEntry (Panchang)
- id, date, city_id, tithi, paksha, festival_ids, sunrise, sunset, muhurtas (structured list), metadata

## Festival
- id, name, description, type (fasting, main_festival, jayanti), rule_hints, icon
