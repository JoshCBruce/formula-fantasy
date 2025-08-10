# F1 Fantasy Complete Data Scraper

A comprehensive web scraper for extracting F1 Fantasy driver data from the official Formula 1 Fantasy website. This tool handles all drivers including complex team swap scenarios and provides detailed race-by-race breakdowns.

## ✨ Features

- **Complete Driver Coverage**: Extracts data for all 21+ F1 drivers
- **Team Swap Handling**: Automatically merges data for drivers who switched teams mid-season (Tsunoda, Lawson)
- **Rich Data Extraction**: 
  - Race and sprint session breakdowns
  - Fantasy points by category (position, qualifying, overtakes, etc.)
  - Percentage picked by fantasy players
  - Team information, positions, and costs
  - Driver of the Day awards
- **Smart File Organization**: Saves individual files as `{ABBREVIATION}.json` (e.g., `NOR.json`, `TSU.json`)
- **Comprehensive Summaries**: Multiple summary files for different analysis needs
- **Dynamic Race Detection**: Automatically determines race order from the website
- **Error Handling**: Robust error handling with popup management and retry logic

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- npm

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
npm install
```

### Usage

Run the scraper:
```bash
node fantasy_scraper_V3.1.js
```

The scraper will:
1. Open a browser window (headless mode can be enabled in config)
2. Navigate to the F1 Fantasy website
3. Handle cookie consent automatically
4. Extract data for all drivers including team swaps
5. Save results to a versioned folder named after the most recent race (e.g., `15-Netherlands/`)

## 📁 Output Structure

All output files are saved in a versioned folder named after the most recent race (e.g., `15-Netherlands/`) and duplicated in a `latest/` folder for easy access.

### Directory Structure
```
15-Netherlands/                    # Versioned folder (historical data)
├── driver_data/
│   ├── NOR.json
│   ├── TSU.json (merged team swap data)
│   ├── LAW.json (merged team swap data)
│   └── ... (21 total driver files)
├── constructor_data/
│   ├── MCL.json
│   ├── FER.json
│   └── ... (10 total constructor files)  
└── summary_data/
    ├── weekend_summary.json
    ├── extraction_summary.json
    ├── team_summary.json
    └── percentage_picked_ranking.json

latest/                           # Always current data (overwrites each run)
├── driver_data/
│   ├── NOR.json
│   ├── TSU.json (merged team swap data)
│   └── ... (identical to versioned folder)
├── constructor_data/
│   ├── MCL.json
│   └── ... (identical to versioned folder)
└── summary_data/
    └── ... (identical to versioned folder)
```

### Individual Driver Files (`{ROUND}-{RACE}/driver_data/`)

Each driver gets a file named `{ABBREVIATION}.json`:
- `NOR.json` - Lando Norris
- `TSU.json` - Yuki Tsunoda (merged team swap data)
- `LAW.json` - Liam Lawson (merged team swap data)
- etc.

### Summary Files (`{ROUND}-{RACE}/summary_data/`)

1. **`weekend_summary.json`** - Points by race for all drivers
2. **`extraction_summary.json`** - Overall statistics and driver list
3. **`team_summary.json`** - Data grouped by team
4. **`percentage_picked_ranking.json`** - Drivers ranked by popularity

## 📊 Data Format

### Individual Driver File Structure

```json
{
  "driverId": "landonorrisdriver",
  "name": "landonorrisdriver",
  "displayName": "landonorris",
  "abbreviation": "NOR",
  "team": "McLaren",
  "position": 1,
  "value": "31.4M",
  "seasonTotalPoints": 500,
  "percentagePicked": 23,
  "teamSwap": false,
  "races": [
    {
      "round": "1",
      "raceName": "Australia",
      "totalPoints": 59,
      "race": {
        "dotd": 10,
        "position": 25,
        "qualifyingPosition": 10,
        "fastestLap": -10,
        "overtakeBonus": 24
      },
      "sprint": {
        "position": 0,
        "qualifyingPosition": 0,
        "fastestLap": 0,
        "overtakeBonus": 0
      }
    }
  ],
  "extractedAt": "2025-08-08T03:11:36.789Z"
}
```

### Team Swap Driver Format

For drivers who switched teams (Tsunoda, Lawson), additional fields are included:

```json
{
  "teamSwap": true,
  "teams": ["Red Bull Racing", "Racing Bulls"],
  "teamSwapDetails": [
    {
      "team": "Red Bull Racing",
      "position": 13,
      "value": "11.2M",
      "points": 74
    },
    {
      "team": "Racing Bulls",
      "position": 20,
      "value": "8.4M", 
      "points": 6
    }
  ],
  "versions": 2,
  "races": [
    {
      "round": "1",
      "raceName": "Australia",
      "totalPoints": 0,
      "race": { /* race data */ },
      "team": "Racing Bulls",
      "source": "single"
    }
  ]
}
```

### Weekend Summary Format

```json
{
  "1": {
    "raceName": "Australia",
    "drivers": {
      "NOR": 59,
      "PIA": 10,
      "VER": 29,
      "TSU": 0,
      "LAW": -17
    }
  }
}
```

### Percentage Picked Ranking Format

```json
{
  "HAD": 54,
  "BEA": 44,
  "PIA": 40,
  "SAI": 39,
  "ALO": 37,
  "HUL": 34,
  "ALB": 29,
  "BOR": 25,
  "OCO": 24,
  "NOR": 23,
  "TSU": 5
}
```

## 🔧 Configuration

Edit the `CONFIG` object in `fantasy_scraper_V3.1.js`:

```javascript
const CONFIG = {
    BASE_URL: 'https://fantasy.formula1.com/en/statistics/details?tab=driver&filter=fPoints',
    BROWSER_HEADLESS: false, // Set to true for headless mode
    PROCESS_ALL_DRIVERS: true,
    DELAYS: {
        PAGE_LOAD: 5000,
        POPUP_WAIT: 3000,
        BETWEEN_DRIVERS: 2000,
        POPUP_CLOSE: 1000
    }
};

// Output directories are now automatically created as versioned folders
// based on the most recent race (e.g., "15-Netherlands/driver_data/")
```

## 🏎️ Team Swap Handling

The scraper automatically detects and handles drivers who switched teams mid-season:

### Current Team Swap Drivers (2025 Season)
- **Yuki Tsunoda**: Red Bull Racing → Racing Bulls
- **Liam Lawson**: Racing Bulls → Red Bull Racing

### How It Works
1. **Detection**: Identifies multiple entries for the same driver with different teams
2. **Collection**: Gathers race data from both team periods
3. **Merging**: Combines data into a single comprehensive driver record
4. **Conflict Resolution**: When the same race has different data, chooses the version with more points
5. **Metadata**: Includes team swap details and version tracking

## 📈 Points Breakdown

Fantasy points are broken down by category:

### Race Points
- **Position Points**: Based on finishing position
- **Qualifying Points**: Based on qualifying position  
- **Driver of the Day**: 10 points bonus
- **Fastest Lap**: Points for fastest lap
- **Overtake Bonus**: Points for positions gained/lost

### Sprint Points (Sprint weekends only)
- **Sprint Position**: Based on sprint finishing position
- **Sprint Qualifying**: Based on sprint qualifying position
- **Sprint Fastest Lap**: Points for sprint fastest lap
- **Sprint Overtake Bonus**: Points for sprint positions gained/lost

## 🛠️ Technical Details

### Dependencies
- **Playwright**: Browser automation for web scraping
- **Node.js fs/promises**: File system operations
- **Path**: File path handling

### Architecture
1. **Main Controller**: Orchestrates the scraping process
2. **Data Extraction**: Handles popup navigation and data parsing
3. **Team Swap Logic**: Merges multiple driver versions
4. **File Generation**: Creates JSON outputs with proper formatting

### Error Handling
- Cookie consent automation
- Popup management with fallback escape keys
- Element waiting with timeouts
- Graceful error recovery between drivers

## 🏁 Race Coverage

The scraper dynamically determines race order from the website and typically covers:

- **15 Regular Races**: Full season calendar
- **6 Sprint Weekends**: Races with both sprint and main sessions
- **All Sessions**: Qualifying, race, sprint qualifying, sprint race

### 2025 Season Races Covered
1. Australia
2. China (Sprint)
3. Japan
4. Bahrain
5. Saudi Arabia
6. United States (Sprint)
7. Italy
8. Monaco
9. Spain
10. Canada
11. Austria (Sprint)
12. United Kingdom
13. Belgium (Sprint)
14. Hungary
15. Netherlands

## 📊 Analysis Use Cases

The extracted data enables various analyses:

### Driver Performance
- Points progression over the season
- Race vs qualifying performance comparison
- Consistency analysis (standard deviation of points)

### Team Analysis  
- Team total points and driver comparisons
- Team development through the season
- Cost vs performance analysis

### Fantasy Strategy
- Percentage picked trends
- Value for money calculations (points per cost)
- Popular vs contrarian pick identification

### Team Swap Impact
- Before/after team switch performance
- Team environment effects on driver performance

## 🐍 Python Data Visualization Example

The scraped data is automatically available via GitHub raw URLs, making it easy to analyze and visualize using Python. Here's a comprehensive example that demonstrates various types of analysis:

### Installation Requirements

```bash
pip install requests matplotlib pandas seaborn
```

### Example Code

```python
#!/usr/bin/env python3
"""
F1 Fantasy Data Visualization Example

Demonstrates how to fetch and visualize F1 Fantasy data directly from 
GitHub using raw URLs with the 'latest' folder for always-current data.
"""

import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Use the 'latest' folder for always up-to-date data
BASE_URL = "https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest"
DRIVER_DATA_URL = f"{BASE_URL}/driver_data"
SUMMARY_DATA_URL = f"{BASE_URL}/summary_data"

def fetch_driver_data(abbreviation):
    """Fetch individual driver data from GitHub raw URL"""
    url = f"{DRIVER_DATA_URL}/{abbreviation}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_summary_data():
    """Fetch weekend summary data from GitHub raw URL"""
    url = f"{SUMMARY_DATA_URL}/weekend_summary.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def plot_cumulative_points_comparison(drivers):
    """Plot cumulative points comparison for multiple drivers"""
    plt.figure(figsize=(15, 8))
    colors = ['#FF1E1E', '#FF8700', '#BF0A30', '#006F62', '#0090FF', '#DC143C']
    
    for i, (abbrev, name) in enumerate(drivers):
        driver_data = fetch_driver_data(abbrev)
        races = sorted(driver_data['races'], key=lambda x: int(x['round']))
        
        rounds = [int(race['round']) for race in races]
        cumulative_points = []
        cumulative = 0
        
        for race in races:
            cumulative += race['totalPoints']
            cumulative_points.append(cumulative)
        
        plt.plot(rounds, cumulative_points, 
                marker='o', linewidth=2, markersize=4,
                color=colors[i % len(colors)], 
                label=f"{name} ({abbrev})")
    
    plt.title('F1 Fantasy Points - Cumulative Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Race Round')
    plt.ylabel('Cumulative Points')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_race_performance_heatmap():
    """Create a heatmap of all drivers' performance across all races"""
    summary_data = fetch_summary_data()
    
    # Build matrix for heatmap
    rounds = sorted(summary_data.keys(), key=int)
    all_drivers = set()
    for round_data in summary_data.values():
        all_drivers.update(round_data.get('drivers', {}).keys())
    
    matrix_data = []
    for driver in sorted(all_drivers):
        driver_row = []
        for round_num in rounds:
            points = summary_data[round_num].get('drivers', {}).get(driver, 0)
            driver_row.append(points)
        matrix_data.append(driver_row)
    
    # Create DataFrame and heatmap
    race_labels = [f"R{r}: {summary_data[r]['raceName'][:6]}" for r in rounds]
    df = pd.DataFrame(matrix_data, index=sorted(all_drivers), columns=race_labels)
    
    plt.figure(figsize=(20, 12))
    sns.heatmap(df, center=0, cmap='RdYlGn', annot=True, fmt='d',
                cbar_kws={'label': 'Fantasy Points'}, 
                linewidths=0.5, linecolor='white')
    
    plt.title('F1 Fantasy Points Heatmap - All Drivers Across All Races', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Race Weekend')
    plt.ylabel('Driver')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Top drivers comparison
    top_drivers = [
        ('NOR', 'Lando Norris'),
        ('PIA', 'Oscar Piastri'), 
        ('VER', 'Max Verstappen'),
        ('RUS', 'George Russell'),
        ('HAM', 'Lewis Hamilton')
    ]
    plot_cumulative_points_comparison(top_drivers)
    
    # Full season heatmap
    plot_race_performance_heatmap()
    
    # Individual driver analysis
    alonso_data = fetch_driver_data('ALO')
    print(f"Fernando Alonso - {alonso_data['team']}")
    print(f"Season Points: {alonso_data['seasonTotalPoints']}")
    print(f"Percentage Picked: {alonso_data['percentagePicked']}%")
```

### Available Data URLs

The `latest` folder always contains the most recent data:

**Individual Drivers:**
```
https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest/driver_data/{DRIVER_ABBREVIATION}.json
```

**Summary Data:**
```
https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest/summary_data/weekend_summary.json
https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest/summary_data/extraction_summary.json
https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest/summary_data/team_summary.json
https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main/latest/summary_data/percentage_picked_ranking.json
```

### Example Visualizations

The complete Python example (`example_visualization.py`) included in this repository demonstrates:

1. **📈 Cumulative Points Comparison** - Track driver performance progression
2. **🏁 Race-by-Race Performance** - Individual driver analysis with positive/negative point highlighting  
3. **🔥 Season Heatmap** - Visual overview of all drivers across all races
4. **🏆 Top Performers Analysis** - Statistical breakdown of season leaders
5. **📊 Driver Information Display** - Complete driver stats and metadata

### Running the Example

```bash
# Clone the repository
git clone https://github.com/JoshCBruce/fantasy-data.git
cd fantasy-data

# Install Python dependencies
pip install requests matplotlib pandas seaborn

# Run the visualization examples
python example_visualization.py
```

The Python example uses the `latest/` folder URLs, ensuring your visualizations always reflect the most current data without needing to update version numbers or race names.

## 🚨 Important Notes

### Ethical Usage
- This scraper is for personal analysis only
- Respect the F1 Fantasy website's terms of service
- Don't overload their servers with rapid requests
- Use reasonable delays between requests

### Browser Requirements
- Chromium-based browser (installed automatically by Playwright)
- JavaScript enabled
- Stable internet connection

### Data Accuracy
- Data reflects the state at the time of scraping
- Fantasy points may change if official results are updated
- Team swap detection is based on current season patterns

## 🔄 Updates and Maintenance

### Updating Team Swap Drivers
If new team swaps occur, update the `TEAM_SWAP_DRIVERS` object:

```javascript
const TEAM_SWAP_DRIVERS = {
    'yukitsunodadriver': {
        name: 'Yuki Tsunoda',
        abbreviation: 'TSU'
    },
    'liamlawsondriver': {
        name: 'Liam Lawson', 
        abbreviation: 'LAW'
    }
    // Add new team swap drivers here
};
```

### Adding New Drivers
Update the `DRIVER_ABBREVIATIONS` mapping for new drivers:

```javascript
const DRIVER_ABBREVIATIONS = {
    // ... existing drivers
    'newdriverdriver': 'NEW'
};
```

## 📝 Version History

### v3.1 (Current)
- ✅ **Versioned Export**: Data exports to folders named after most recent race (e.g., `15-Netherlands/`)
- ✅ Individual files named as `{ABBREVIATION}.json`
- ✅ Percentage picked data extraction
- ✅ Proper team information from main driver list
- ✅ Team swap logic with actual team names
- ✅ Comprehensive summary files including popularity ranking
- ✅ Enhanced error handling and logging
- ✅ Removed duplicate `cost` field - now only uses `value`

### v3.0
- ✅ Team swap driver handling (Tsunoda, Lawson)
- ✅ Comprehensive race and sprint data extraction
- ✅ Dynamic race order detection
- ✅ Multiple summary file generation

### v2.0
- ✅ Enhanced data extraction with session breakdowns
- ✅ Duplicate driver prevention
- ✅ Improved popup handling

### v1.0
- ✅ Basic driver data extraction
- ✅ Race points collection
- ✅ JSON file generation

## 🤝 Contributing

This scraper was developed to solve the specific challenge of team swap drivers in F1 Fantasy data collection. If you encounter issues or have suggestions for improvements, please ensure any changes maintain the robust team swap handling and data accuracy.

## 📜 License

This tool is provided for educational and personal analysis purposes. Please respect the Formula 1 Fantasy website's terms of service and use responsibly.

---

**Happy F1 Fantasy analysis! 🏎️📊**