WITH cleaned_fixtures AS (
    SELECT *
    FROM {{ ref('silver_fixtures') }}
    WHERE status = 'FT'
      AND home_goals IS NOT NULL
      AND away_goals IS NOT NULL
),

final AS (
    SELECT
        fixture_id,
        date,
        home_team,
        away_team,
        home_goals,
        away_goals,
        home_goals + away_goals AS total_goals,
        CASE 
            WHEN home_goals > away_goals THEN home_team
            WHEN away_goals > home_goals THEN away_team
            ELSE 'Draw'
        END AS winner,
        CASE
            WHEN home_goals > away_goals THEN 'Home Win'
            WHEN away_goals > home_goals THEN 'Away Win'
            ELSE 'Draw'
        END AS result_type
    FROM cleaned_fixtures
)

SELECT * FROM final