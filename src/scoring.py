from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

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

    df_normalized = scaler.fit_transform(df[features])

    df[features] = df_normalized * 100

    df['E_score'] = (100 - df['carbon_emissions']) * 0.6 + (100 - df['energy_usage']) * 0.4

    df['S_score'] = df['employee_satisfaction'] * 0.6 + df['diversity_score'] * 0.4

    df['G_score'] = df['board_independence'] * 0.5 + df['ethics_score'] * 0.5

    df['ESG_score'] = (df['E_score'] + df['S_score'] + df['G_score']) / 3

    df['ESG_score'] = df['ESG_score'].clip(lower=0).round(2)

    return df


def cluster_companies(df, n_clusters=3):
    features = ['E_score', 'S_score', 'G_score']
    X = df[features].values
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)
    
    cluster_labels = {
        0: 'Laggards',
        1: 'Average',
        2: 'Leaders'
    }
    
    cluster_means = df.groupby('Cluster')['ESG_score'].mean().sort_values()
    label_map = {old: new for old, new in zip(cluster_means.index, ['Laggards', 'Average', 'Leaders'][:len(cluster_means)])}
    
    df['Cluster_Label'] = df['Cluster'].map(label_map)
    
    return df