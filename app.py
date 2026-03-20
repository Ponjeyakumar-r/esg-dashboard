from src.data_loader import load_data
from src.scoring import calculate_esg_scores
from src.ranking import rank_companies
from src.visualization import plot_esg_scores

def main():
    df = load_data("data/esg_data.csv")
    df = calculate_esg_scores(df)
    df = rank_companies(df)

    print(df[['company', 'ESG_score', 'Rank']])

    plot_esg_scores(df)
    print("\nTop ESG Company:", df.iloc[0]['company'])
    print("Worst ESG Company:", df.iloc[-1]['company'])
    print("Average ESG Score:", round(df['ESG_score'].mean(), 2))

if __name__ == "__main__":
    main()