import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = 'game_results.csv'
data = pd.read_csv(file_path)

# Filter the data for Random AI vs Minimax AI
random_vs_minimax = data[(data['White Player'] == 'Random AI') & (data['Black Player'] == 'Minimax AI')]

# Calculate Black Turn Time / Number of Moves
random_vs_minimax['Turn Time per Move'] = random_vs_minimax['Black Turn Time'] / random_vs_minimax['Number of Moves']

# Plot 1: Black Turn Time / Number of Moves vs Black Depth
plt.figure(figsize=(12, 6))
sns.boxplot(x='Black Depth', y='Turn Time per Move', data=random_vs_minimax)
plt.title('Random AI vs Minimax AI: Black Turn Time per Move vs Depth')
plt.xlabel('Black Depth')
plt.ylabel('Black Turn Time per Move')
plt.tight_layout()
plt.show()

# Add a blank figure to create space between plots
plt.figure(figsize=(12, 0.5))
plt.show()

# Plot 2: Number of Moves vs Black Depth with points colored by Winning Player
plt.figure(figsize=(12, 6))
sns.boxplot(x='Black Depth', y='Number of Moves', data=random_vs_minimax)
sns.scatterplot(x='Black Depth', y='Number of Moves', hue='Winning Player', data=random_vs_minimax, palette='deep', s=100, edgecolor='k')
plt.title('Random AI vs Minimax AI: Number of Moves vs Depth')
plt.xlabel('Black Depth')
plt.ylabel('Number of Moves')
plt.legend(title='Winning Player')
plt.tight_layout()
plt.show()

# Filter the data for Random AI vs Stockfish
random_vs_stockfish = data[(data['White Player'] == 'Random AI') & (data['Black Player'] == 'Stockfish')]

# Check if data is available for Random AI vs Stockfish
if not random_vs_stockfish.empty:
    # Calculate Black Turn Time / Number of Moves
    random_vs_stockfish['Turn Time per Move'] = random_vs_stockfish['Black Turn Time'] / random_vs_stockfish['Number of Moves']

    # Plot 3: Black Turn Time / Number of Moves vs Black Depth for Random AI vs Stockfish
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Black Depth', y='Turn Time per Move', data=random_vs_stockfish)
    plt.title('Random AI vs Stockfish: Black Turn Time per Move vs Depth')
    plt.xlabel('Black Depth')
    plt.ylabel('Black Turn Time per Move')
    plt.tight_layout()
    plt.show()

    # Add a blank figure to create space between plots
    plt.figure(figsize=(12, 0.5))
    plt.show()

    # Plot 4: Number of Moves vs Black Depth with points colored by Winning Player for Random AI vs Stockfish
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Black Depth', y='Number of Moves', data=random_vs_stockfish)
    sns.scatterplot(x='Black Depth', y='Number of Moves', hue='Winning Player', data=random_vs_stockfish, palette='deep', s=100, edgecolor='k')
    plt.title('Random AI vs Stockfish: Number of Moves vs Depth')
    plt.xlabel('Black Depth')
    plt.ylabel('Number of Moves')
    plt.legend(title='Winning Player')
    plt.tight_layout()
    plt.show()
else:
    print("No data available for Random AI vs Stockfish")