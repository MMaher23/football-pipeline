SELECT
    fixture_id,
    date,
    home_team,
    away_team,
    home_goals,
    away_goals,
    status
FROM {{ source('football', 'raw_fixtures') }}