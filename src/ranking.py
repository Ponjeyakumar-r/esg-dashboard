def rank_companies(df):
    df = df.sort_values(by='ESG_score', ascending=False)
    df['Rank'] = range(1, len(df) + 1)
    return df