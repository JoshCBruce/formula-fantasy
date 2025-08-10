# Formula Fantasy Data Visualization Example 📊🏎️

A comprehensive demonstration of the **Formula Fantasy Python library** with interactive data visualizations and analysis tools.

## 🌟 Features

This example program showcases the full capabilities of the Formula Fantasy library through:

### 📈 Driver Analysis
- **Performance Comparison**: Track multiple drivers across recent rounds
- **Individual Race Breakdown**: Detailed analysis of points by category (overtakes, position, etc.)
- **Season Progression**: Cumulative points tracking and trends
- **Recent Form Analysis**: Performance over last few races

### 🏁 Team/Constructor Analysis  
- **Constructor Standings**: Season totals and latest round performance
- **Value vs Performance**: Scatter plots showing cost efficiency
- **Team Popularity**: Who's being picked by fantasy players

### 💡 Fantasy Strategy Tools
- **Value for Money Analysis**: Points per million spent calculations
- **Popular vs Contrarian**: Identify undervalued picks
- **Popularity Trends**: See which drivers/teams are trending
- **Top Recommendations**: Data-driven pick suggestions

### 📊 Comprehensive Dashboards
- **Season Overview**: Multi-metric dashboard with standings, performance, and value
- **Interactive Visualizations**: Multiple chart types (bar, line, scatter, heatmap, pie)
- **Real-time Data**: Always uses latest available Formula Fantasy data

## 🚀 Quick Start

### Installation

1. **Install Formula Fantasy library:**
   ```bash
   pip install formula-fantasy
   ```

2. **Install visualization dependencies:**
   ```bash
   pip install -r requirements-viz.txt
   ```
   
   Or manually:
   ```bash
   pip install matplotlib pandas seaborn numpy
   ```

### Usage

**Run the complete demo:**
```bash
python3 example_visualization.py
```

**Test components without displaying plots:**
```bash
python3 test_visualization.py
```

## 📊 Example Visualizations

### 1. Driver Performance Comparison
```python
from formula_fantasy import *

# Compare top drivers over recent rounds
analyzer = FormulaFantasyAnalyzer()
performance_data = analyzer.driver_performance_comparison(
    driver_list=['NOR', 'VER', 'RUS', 'PIA', 'HAM'], 
    rounds_to_analyze=5
)
```

**Creates:**
- Bar chart showing individual round performance
- Line chart showing cumulative points progression

### 2. Detailed Race Breakdown
```python
# Analyze a specific driver's latest race
analyzer.race_breakdown_analysis('VER', '14')
```

**Creates:**
- Pie chart of points breakdown by category
- Season stats comparison (total points, value, popularity)
- Recent performance trend line
- Qualifying vs race points comparison

### 3. Team Analysis Dashboard
```python
# Compare all constructors across multiple metrics
team_data = analyzer.team_comparison_analysis()
```

**Creates:**
- Season total points comparison
- Latest round performance bars
- Value vs performance scatter plot
- Constructor popularity ranking

### 4. Fantasy Strategy Analysis
```python
# Find the best value picks and strategy insights
strategy_data = analyzer.fantasy_strategy_analysis()
```

**Creates:**
- Value for money bubble chart (bubble size = popularity)
- Popular vs contrarian strategy scatter
- Recent form vs season performance
- Top 10 value recommendations

### 5. Comprehensive Season Overview
```python
# Complete dashboard with multiple metrics
analyzer.comprehensive_season_overview()
```

**Creates:**
- Season points progression for top drivers
- Current championship standings
- Latest round performance podium
- Value analysis scatter plots
- Driver popularity rankings
- Constructor comprehensive comparison

## 🎯 Key Insights Provided

### Driver Insights
- **Consistency Analysis**: Standard deviation of points across races
- **Value Efficiency**: Points per million spent calculations
- **Popularity Trends**: Percentage picked by fantasy players
- **Recent Form**: Last 3-5 races performance analysis

### Team Insights  
- **Team Development**: Performance progression through season
- **Driver Comparisons**: Teammate performance analysis
- **Cost Effectiveness**: Team value vs points analysis

### Fantasy Strategy
- **Contrarian Picks**: Low-picked drivers with high points potential
- **Value Plays**: Best points per cost ratios
- **Popular Choices**: High-ownership analysis
- **Risk/Reward**: Performance volatility assessment

## 🔧 Customization

### Modify Driver Lists
```python
# Focus on specific drivers
custom_drivers = ['VER', 'HAM', 'ALO', 'SAI', 'LEC']  # Ferrari vs Red Bull vs Mercedes
analyzer.driver_performance_comparison(custom_drivers, rounds_to_analyze=8)
```

### Change Analysis Period
```python
# Analyze more rounds for better trends
analyzer.driver_performance_comparison(rounds_to_analyze=10)

# Focus on specific round
analyzer.race_breakdown_analysis('NOR', '12')  # Austria Sprint weekend
```

### Custom Strategy Analysis
```python
# Focus on midfield drivers for value picks
midfield_drivers = ['ALB', 'GAS', 'OCO', 'HUL', 'STR']
# Modify the strategy_analysis method to use these drivers
```

## 📈 Data Sources

This example uses the **Formula Fantasy Python library** which provides access to:

- **Real-time Race Data**: Latest results and points from F1 Fantasy
- **Historical Performance**: Season-long statistics and trends  
- **Financial Data**: Driver/constructor values and costs
- **Popularity Metrics**: Percentage picked by fantasy players
- **Detailed Breakdowns**: Points by category (position, overtakes, etc.)

All data is sourced from the official Formula 1 Fantasy platform via the [fantasy-data repository](https://github.com/JoshCBruce/fantasy-data).

## 🛠️ Technical Details

### Dependencies
- **formula-fantasy**: Core library for F1 Fantasy data access
- **matplotlib**: Primary plotting library
- **seaborn**: Statistical visualization enhancement
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing support

### Architecture
- **FormulaFantasyAnalyzer Class**: Main orchestrator for analysis workflows
- **Modular Methods**: Each visualization type in separate method
- **Error Handling**: Graceful handling of missing data
- **Performance Optimized**: Efficient data fetching and processing

### Plot Types Used
- **Bar Charts**: Driver/constructor comparisons
- **Line Plots**: Performance trends and progressions
- **Scatter Plots**: Value vs performance analysis
- **Pie Charts**: Points breakdown visualization
- **Heatmaps**: Multi-driver race performance matrices
- **Bubble Charts**: Multi-dimensional analysis (value, points, popularity)

## 📝 Example Output

When you run the complete program, you'll see:

```
🏁 Formula Fantasy Data Visualization Demo
==================================================
🏎️ Formula Fantasy Analyzer initialized
📊 Found 21 drivers, 10 constructors  
📅 Latest round: 15

1️⃣ Driver Performance Comparison
------------------------------
📈 Analyzing driver performance for: NOR, VER, RUS, PIA, HAM
[Displays comparative performance charts]

2️⃣ Detailed Race Breakdown Analysis
-----------------------------------
🔍 Analyzing VER breakdown for round 15
[Shows detailed race analysis with pie charts and trends]

3️⃣ Team Comparison Analysis  
----------------------------
🏁 Analyzing team performance and value...
[Displays constructor comparison dashboard]

4️⃣ Fantasy Strategy Analysis
------------------------------
💡 Analyzing fantasy strategy metrics...

🏆 TOP VALUE FOR MONEY PICKS:
1. BEA (Haas) - 11.3 pts/M, 44% picked, 9.5M value
2. ANT (Mercedes) - 7.7 pts/M, 19% picked, 10.1M value  
3. ALB (Williams) - 7.8 pts/M, 29% picked, 12.3M value
[Shows strategy analysis charts and recommendations]

5️⃣ Comprehensive Season Overview
---------------------------------  
📊 Creating comprehensive season overview...
[Displays complete dashboard with multiple metrics]

🎉 Formula Fantasy Analysis Complete!
```

## 🚨 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'formula_fantasy'**
```bash
pip install formula-fantasy
```

**matplotlib backend issues**
- On macOS: May need to install tkinter: `brew install python-tk`
- For headless environments: The program automatically uses 'Agg' backend

**Missing data for certain drivers/rounds**
- This is normal - not all drivers have data for all rounds
- The program handles missing data gracefully with try/catch blocks

**Plots not displaying**
- Make sure you're in an environment that supports GUI display
- For remote/headless: Save plots to files using `plt.savefig()`

### Performance Tips

**For faster analysis:**
- Reduce the number of drivers analyzed: `analyzer.driver_performance_comparison(['VER', 'NOR'])`
- Decrease rounds analyzed: `rounds_to_analyze=3`
- Focus on specific constructors: `self.constructors[:5]`

## 🎉 Next Steps

After running this example, you can:

1. **Customize the Analysis**: Modify driver lists, time periods, or metrics
2. **Add New Visualizations**: Use the Formula Fantasy library to create your own charts
3. **Automate Reports**: Schedule the analysis to run regularly
4. **Share Insights**: Export plots and share with your fantasy league
5. **Build Interactive Apps**: Use Plotly or Streamlit for web interfaces

## 📚 Learn More

- **Formula Fantasy Library Docs**: Check the main README.md
- **Data Format Reference**: See dataformat.md for complete data structure
- **API Reference**: Use `help(formula_fantasy)` in Python for function docs
- **GitHub Repository**: [fantasy-data source](https://github.com/JoshCBruce/fantasy-data)

---

**Happy Formula Fantasy analysis! 🏎️📊**