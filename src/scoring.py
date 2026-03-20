from sklearn.preprocessing import MinMaxScaler

def calculate_esg_scores(df):
    scaler = MinMaxScaler()

    features = [
        'carbon_emissions',
        'energy_usage',
        'employee_satisfaction',
        'diversity_score',
        'board_independence',
        'ethics_score'
    ]

    # Normalize values
    df[features] = scaler.fit_transform(df[features]) * 100

    # Environmental Score (lower is better → invert)
    df['E_score'] = (100 - df['carbon_emissions']) * 0.6 + (100 - df['energy_usage']) * 0.4

    # Social Score
    df['S_score'] = df['employee_satisfaction'] * 0.6 + df['diversity_score'] * 0.4

    # Governance Score
    df['G_score'] = df['board_independence'] * 0.5 + df['ethics_score'] * 0.5

    # Final ESG Score
    df['ESG_score'] = (df['E_score'] + df['S_score'] + df['G_score']) / 3

    # Fix floating issues
    df['ESG_score'] = df['ESG_score'].clip(lower=0)
    df['ESG_score'] = df['ESG_score'].round(2)

    return df