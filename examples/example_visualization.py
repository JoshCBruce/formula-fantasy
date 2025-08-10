#!/usr/bin/env python3
"""
Formula Fantasy Data Visualization Example

A comprehensive demonstration of the Formula Fantasy Python library's capabilities
with interactive data visualizations and analysis tools.

This example showcases:
- Driver performance comparisons
- Race-by-race analysis 
- Team comparisons and strategies
- Fantasy value analysis
- Popular vs contrarian picks
- Season progression trends

Requirements:
    pip install formula-fantasy matplotlib pandas seaborn numpy

Usage:
    python example_visualization.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from formula_fantasy import (
    get_driver_points, get_constructor_points,
    get_driver_breakdown, get_constructor_breakdown,
    get_driver_info, get_constructor_info,
    list_drivers, list_constructors, get_latest_round
)

# Set up matplotlib style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class FormulaFantasyAnalyzer:
    """Main class for Formula Fantasy data analysis and visualization"""
    
    def __init__(self):
        self.drivers = list_drivers()
        self.constructors = list_constructors()
        self.latest_round = get_latest_round()
        print(f"🏎️ Formula Fantasy Analyzer initialized")
        print(f"📊 Found {len(self.drivers)} drivers, {len(self.constructors)} constructors")
        print(f"📅 Latest round: {self.latest_round}\n")

    def driver_performance_comparison(self, driver_list=None, rounds_to_analyze=5):
        """Compare driver performance over recent rounds"""
        if not driver_list:
            # Use top-picked drivers based on common fantasy picks
            driver_list = ['NOR', 'VER', 'RUS', 'PIA', 'HAM']
        
        print(f"📈 Analyzing driver performance for: {', '.join(driver_list)}")
        
        # Collect data
        performance_data = {}
        latest_round_num = int(self.latest_round)
        rounds = list(range(max(1, latest_round_num - rounds_to_analyze + 1), latest_round_num + 1))
        
        for driver in driver_list:
            driver_points = []
            for round_num in rounds:
                try:
                    points = get_driver_points(driver, str(round_num))
                    driver_points.append(points)
                except:
                    driver_points.append(0)
            performance_data[driver] = driver_points
        
        # Create performance comparison chart
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
        
        # Individual round performance
        x = np.arange(len(rounds))
        width = 0.15
        colors = plt.cm.tab10(np.linspace(0, 1, len(driver_list)))
        
        for i, (driver, points) in enumerate(performance_data.items()):
            ax1.bar(x + i * width, points, width, label=driver, color=colors[i], alpha=0.8)
        
        ax1.set_xlabel('Race Round')
        ax1.set_ylabel('Fantasy Points')
        ax1.set_title(f'Driver Performance Comparison - Last {rounds_to_analyze} Rounds', 
                     fontsize=14, fontweight='bold')
        ax1.set_xticks(x + width * 2)
        ax1.set_xticklabels([f'R{r}' for r in rounds])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Cumulative performance
        cumulative_data = {}
        for driver, points in performance_data.items():
            cumulative_data[driver] = np.cumsum(points)
            ax2.plot(rounds, cumulative_data[driver], marker='o', linewidth=2.5, 
                    markersize=6, label=driver)
        
        ax2.set_xlabel('Race Round')
        ax2.set_ylabel('Cumulative Fantasy Points')
        ax2.set_title('Cumulative Points Progression', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return performance_data

    def race_breakdown_analysis(self, driver='NOR', round_num=None):
        """Detailed analysis of a specific driver's performance in a race"""
        if not round_num:
            round_num = self.latest_round
            
        print(f"🔍 Analyzing {driver} breakdown for round {round_num}")
        
        try:
            # Get detailed breakdown
            race_breakdown = get_driver_breakdown(driver, round_num, "race")
            qualifying_breakdown = get_driver_breakdown(driver, round_num, "qualifying") 
            driver_info = get_driver_info(driver)
            
            # Create breakdown visualization
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # Race points breakdown pie chart
            race_points = {k: v for k, v in race_breakdown.items() if v != 0}
            if race_points:
                colors = plt.cm.Set3(np.linspace(0, 1, len(race_points)))
                wedges, texts, autotexts = ax1.pie(race_points.values(), labels=race_points.keys(), 
                                                  autopct='%1.0f pts', colors=colors, startangle=90)
                ax1.set_title(f'{driver} - Race Points Breakdown (R{round_num})', fontweight='bold')
                
                # Enhance text appearance
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                ax1.text(0.5, 0.5, 'No race points\nthis round', ha='center', va='center', 
                        transform=ax1.transAxes, fontsize=14)
                ax1.set_title(f'{driver} - Race Points Breakdown (R{round_num})', fontweight='bold')
            
            # Driver season info bar chart
            season_info = {
                'Season Total': driver_info.get('seasonTotalPoints', 0),
                'Percentage Picked': driver_info.get('percentagePicked', 0),
                'Value (M)': float(driver_info.get('value', '0M').replace('M', ''))
            }
            
            bars = ax2.bar(season_info.keys(), season_info.values(), 
                          color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            ax2.set_title(f'{driver} - Season Stats', fontweight='bold')
            ax2.set_ylabel('Value')
            
            # Add value labels on bars
            for bar, value in zip(bars, season_info.values()):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Points distribution across recent rounds
            recent_rounds = list(range(max(1, int(round_num) - 4), int(round_num) + 1))
            recent_points = []
            for r in recent_rounds:
                try:
                    points = get_driver_points(driver, str(r))
                    recent_points.append(points)
                except:
                    recent_points.append(0)
            
            ax3.plot(recent_rounds, recent_points, marker='o', linewidth=3, markersize=8, 
                    color='#E74C3C', markerfacecolor='#C0392B')
            ax3.fill_between(recent_rounds, recent_points, alpha=0.3, color='#E74C3C')
            ax3.set_xlabel('Round')
            ax3.set_ylabel('Points')
            ax3.set_title(f'{driver} - Recent Performance Trend', fontweight='bold')
            ax3.grid(True, alpha=0.3)
            
            # Qualifying vs Race performance comparison
            try:
                qual_pos = qualifying_breakdown.get('position', 0)
                race_pos = race_breakdown.get('position', 0)
                
                categories = ['Qualifying\nPosition', 'Race\nPosition']
                positions = [qual_pos, race_pos]
                colors = ['#3498DB', '#E67E22']
                
                bars = ax4.bar(categories, positions, color=colors, alpha=0.8)
                ax4.set_ylabel('Fantasy Points')
                ax4.set_title(f'{driver} - Qualifying vs Race Points (R{round_num})', fontweight='bold')
                
                # Add value labels
                for bar, pos in zip(bars, positions):
                    height = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{pos}', ha='center', va='bottom', fontweight='bold', fontsize=12)
                            
            except Exception as e:
                ax4.text(0.5, 0.5, f'Qualifying data\nnot available', ha='center', va='center',
                        transform=ax4.transAxes, fontsize=12)
                ax4.set_title(f'{driver} - Session Comparison (R{round_num})', fontweight='bold')
            
            plt.suptitle(f'🏎️ {driver} ({driver_info.get("team", "Unknown Team")}) - Round {round_num} Analysis', 
                        fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"❌ Error analyzing {driver}: {e}")

    def team_comparison_analysis(self):
        """Compare constructor/team performance and value"""
        print("🏁 Analyzing team performance and value...")
        
        team_data = {}
        for constructor in self.constructors:
            try:
                info = get_constructor_info(constructor)
                points = get_constructor_points(constructor, self.latest_round)
                
                team_data[constructor] = {
                    'latest_points': points,
                    'season_total': info.get('seasonTotalPoints', 0),
                    'value': float(info.get('value', '0M').replace('M', '')),
                    'percentage_picked': info.get('percentagePicked', 0)
                }
            except:
                continue
        
        if not team_data:
            print("❌ No team data available")
            return
            
        # Create team comparison visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
        
        teams = list(team_data.keys())
        
        # Season total points comparison
        season_totals = [team_data[team]['season_total'] for team in teams]
        bars1 = ax1.bar(teams, season_totals, color=plt.cm.viridis(np.linspace(0, 1, len(teams))))
        ax1.set_title('Constructor Season Total Points', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Total Points')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, total in zip(bars1, season_totals):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(total)}', ha='center', va='bottom', fontweight='bold')
        
        # Latest round performance
        latest_points = [team_data[team]['latest_points'] for team in teams]
        bars2 = ax2.bar(teams, latest_points, color=plt.cm.plasma(np.linspace(0, 1, len(teams))))
        ax2.set_title(f'Latest Round ({self.latest_round}) Points', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Points')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, points in zip(bars2, latest_points):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(points)}', ha='center', va='bottom', fontweight='bold')
        
        # Value vs Performance scatter plot
        values = [team_data[team]['value'] for team in teams]
        ax3.scatter(values, season_totals, s=200, alpha=0.7, 
                   c=range(len(teams)), cmap='tab10')
        
        for i, team in enumerate(teams):
            ax3.annotate(team, (values[i], season_totals[i]), 
                        xytext=(5, 5), textcoords='offset points', fontweight='bold')
        
        ax3.set_xlabel('Value (Millions)')
        ax3.set_ylabel('Season Total Points')
        ax3.set_title('Value vs Performance Analysis', fontweight='bold', fontsize=14)
        ax3.grid(True, alpha=0.3)
        
        # Popularity analysis
        popularity = [team_data[team]['percentage_picked'] for team in teams]
        bars4 = ax4.barh(teams, popularity, color=plt.cm.coolwarm(np.linspace(0, 1, len(teams))))
        ax4.set_xlabel('Percentage Picked (%)')
        ax4.set_title('Constructor Popularity', fontweight='bold', fontsize=14)
        
        # Add percentage labels
        for bar, pct in zip(bars4, popularity):
            width = bar.get_width()
            ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                    f'{pct:.1f}%', ha='left', va='center', fontweight='bold')
        
        plt.suptitle('🏁 Constructor/Team Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
        
        return team_data

    def fantasy_strategy_analysis(self):
        """Analyze fantasy strategy metrics: value for money, popularity trends"""
        print("💡 Analyzing fantasy strategy metrics...")
        
        # Collect driver strategy data
        strategy_data = {}
        for driver in self.drivers[:15]:  # Limit to avoid too much data
            try:
                info = get_driver_info(driver)
                latest_points = get_driver_points(driver, self.latest_round)
                
                # Calculate recent performance (last 3 rounds)
                recent_points = []
                for r in range(max(1, int(self.latest_round) - 2), int(self.latest_round) + 1):
                    try:
                        points = get_driver_points(driver, str(r))
                        recent_points.append(points)
                    except:
                        recent_points.append(0)
                
                avg_recent = sum(recent_points) / len(recent_points) if recent_points else 0
                
                strategy_data[driver] = {
                    'season_total': info.get('seasonTotalPoints', 0),
                    'value': float(info.get('value', '0M').replace('M', '')),
                    'percentage_picked': info.get('percentagePicked', 0),
                    'latest_points': latest_points,
                    'avg_recent': avg_recent,
                    'team': info.get('team', 'Unknown')
                }
            except:
                continue
        
        if not strategy_data:
            print("❌ No strategy data available")
            return
            
        # Create strategy analysis dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
        
        drivers = list(strategy_data.keys())
        
        # Value for Money analysis (points per million spent)
        values = [strategy_data[d]['value'] for d in drivers]
        season_points = [strategy_data[d]['season_total'] for d in drivers]
        value_for_money = [pts/val if val > 0 else 0 for pts, val in zip(season_points, values)]
        
        # Create bubble chart
        popularity = [strategy_data[d]['percentage_picked'] for d in drivers]
        scatter = ax1.scatter(values, value_for_money, s=[p*10 for p in popularity], 
                            alpha=0.6, c=range(len(drivers)), cmap='viridis')
        
        for i, driver in enumerate(drivers):
            ax1.annotate(driver, (values[i], value_for_money[i]), 
                        xytext=(3, 3), textcoords='offset points', fontsize=9, fontweight='bold')
        
        ax1.set_xlabel('Value (Millions)')
        ax1.set_ylabel('Points per Million Spent')
        ax1.set_title('Value for Money Analysis\n(Bubble size = Popularity %)', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Popular vs Contrarian picks
        ax2.scatter(popularity, season_points, s=100, alpha=0.7, 
                   c=[strategy_data[d]['latest_points'] for d in drivers], cmap='RdYlGn')
        
        for i, driver in enumerate(drivers):
            ax2.annotate(driver, (popularity[i], season_points[i]), 
                        xytext=(3, 3), textcoords='offset points', fontsize=9, fontweight='bold')
        
        ax2.set_xlabel('Percentage Picked (%)')
        ax2.set_ylabel('Season Total Points')
        ax2.set_title('Popular vs Contrarian Strategy\n(Color = Latest Round Points)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Recent form vs Season performance
        recent_avg = [strategy_data[d]['avg_recent'] for d in drivers]
        ax3.scatter(recent_avg, season_points, s=100, alpha=0.7, 
                   c=values, cmap='plasma')
        
        for i, driver in enumerate(drivers):
            ax3.annotate(driver, (recent_avg[i], season_points[i]), 
                        xytext=(3, 3), textcoords='offset points', fontsize=9, fontweight='bold')
        
        ax3.set_xlabel('Recent Average Points (Last 3 Rounds)')
        ax3.set_ylabel('Season Total Points')
        ax3.set_title('Recent Form vs Season Performance\n(Color = Value)', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Top value picks recommendation
        # Sort by value for money
        sorted_drivers = sorted(drivers, key=lambda d: value_for_money[drivers.index(d)], reverse=True)
        top_10_drivers = sorted_drivers[:10]
        top_10_vfm = [value_for_money[drivers.index(d)] for d in top_10_drivers]
        
        bars = ax4.barh(range(len(top_10_drivers)), top_10_vfm, 
                       color=plt.cm.RdYlGn(np.linspace(0.3, 1, len(top_10_drivers))))
        ax4.set_yticks(range(len(top_10_drivers)))
        ax4.set_yticklabels([f"{d}\n({strategy_data[d]['team'][:8]})" for d in top_10_drivers])
        ax4.set_xlabel('Points per Million')
        ax4.set_title('Top 10 Value for Money Picks', fontweight='bold')
        
        # Add value labels
        for i, (bar, vfm) in enumerate(zip(bars, top_10_vfm)):
            width = bar.get_width()
            ax4.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                    f'{vfm:.1f}', ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.suptitle('💡 Fantasy Strategy Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
        
        # Print top recommendations
        print("\n🏆 TOP VALUE FOR MONEY PICKS:")
        for i, driver in enumerate(top_10_drivers[:5], 1):
            data = strategy_data[driver]
            print(f"{i}. {driver} ({data['team']}) - {top_10_vfm[i-1]:.1f} pts/M, "
                  f"{data['percentage_picked']:.1f}% picked, {data['value']:.1f}M value")
        
        return strategy_data

    def comprehensive_season_overview(self):
        """Create a comprehensive season overview with multiple metrics"""
        print("📊 Creating comprehensive season overview...")
        
        # Get data for top performers
        top_drivers = ['NOR', 'VER', 'RUS', 'PIA', 'HAM', 'LEC', 'SAI', 'ALO']
        available_drivers = [d for d in top_drivers if d in self.drivers]
        
        if len(available_drivers) < 4:
            available_drivers = self.drivers[:8]  # Use first 8 available drivers
        
        # Create multi-metric dashboard
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
        
        # 1. Season points progression (spans 2 columns)
        ax1 = fig.add_subplot(gs[0, :2])
        
        for driver in available_drivers[:6]:  # Top 6 to avoid cluttering
            try:
                info = get_driver_info(driver)
                season_total = info.get('seasonTotalPoints', 0)
                
                # Simulate progression (in real implementation, you'd get round-by-round data)
                rounds = list(range(1, int(self.latest_round) + 1))
                # This is a simplified progression - actual implementation would fetch each round
                progression = [season_total * (r / len(rounds)) for r in rounds]
                
                ax1.plot(rounds, progression, marker='o', linewidth=2, 
                        markersize=4, label=f"{driver} ({info.get('team', '')[:3]})")
            except:
                continue
        
        ax1.set_xlabel('Race Round')
        ax1.set_ylabel('Cumulative Points')
        ax1.set_title('Season Points Progression - Top Drivers', fontweight='bold', fontsize=14)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 2. Current championship standings
        ax2 = fig.add_subplot(gs[0, 2])
        
        standings_data = []
        for driver in available_drivers:
            try:
                info = get_driver_info(driver)
                standings_data.append((driver, info.get('seasonTotalPoints', 0)))
            except:
                continue
        
        standings_data.sort(key=lambda x: x[1], reverse=True)
        top_8 = standings_data[:8]
        
        drivers_standing, points_standing = zip(*top_8)
        bars = ax2.barh(range(len(drivers_standing)), points_standing, 
                       color=plt.cm.viridis(np.linspace(0, 1, len(drivers_standing))))
        ax2.set_yticks(range(len(drivers_standing)))
        ax2.set_yticklabels([f"{i+1}. {d}" for i, d in enumerate(drivers_standing)])
        ax2.set_xlabel('Season Points')
        ax2.set_title('Current Championship\nStandings', fontweight='bold', fontsize=12)
        
        # 3. Latest round performance
        ax3 = fig.add_subplot(gs[1, 0])
        
        latest_performance = []
        for driver in available_drivers:
            try:
                points = get_driver_points(driver, self.latest_round)
                latest_performance.append((driver, points))
            except:
                continue
        
        latest_performance.sort(key=lambda x: x[1], reverse=True)
        latest_drivers, latest_points = zip(*latest_performance[:8])
        
        colors = ['#FFD700', '#C0C0C0', '#CD7F32'] + ['#4472C4'] * 5  # Gold, Silver, Bronze, Blue
        bars = ax3.bar(latest_drivers, latest_points, color=colors[:len(latest_drivers)])
        ax3.set_ylabel('Points')
        ax3.set_title(f'Round {self.latest_round}\nPerformance', fontweight='bold', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Value analysis
        ax4 = fig.add_subplot(gs[1, 1])
        
        value_data = []
        for driver in available_drivers:
            try:
                info = get_driver_info(driver)
                value = float(info.get('value', '0M').replace('M', ''))
                points = info.get('seasonTotalPoints', 0)
                value_data.append((driver, value, points))
            except:
                continue
        
        if value_data:
            drivers_val, values_val, points_val = zip(*value_data)
            scatter = ax4.scatter(values_val, points_val, s=100, alpha=0.7, 
                                c=range(len(drivers_val)), cmap='tab10')
            
            for i, driver in enumerate(drivers_val):
                ax4.annotate(driver, (values_val[i], points_val[i]), 
                           xytext=(3, 3), textcoords='offset points', fontsize=9)
            
            ax4.set_xlabel('Value (Millions)')
            ax4.set_ylabel('Season Points')
            ax4.set_title('Value vs Performance', fontweight='bold', fontsize=12)
            ax4.grid(True, alpha=0.3)
        
        # 5. Popularity analysis
        ax5 = fig.add_subplot(gs[1, 2])
        
        popularity_data = []
        for driver in available_drivers:
            try:
                info = get_driver_info(driver)
                popularity = info.get('percentagePicked', 0)
                popularity_data.append((driver, popularity))
            except:
                continue
        
        popularity_data.sort(key=lambda x: x[1], reverse=True)
        pop_drivers, pop_percentages = zip(*popularity_data[:8])
        
        bars = ax5.barh(range(len(pop_drivers)), pop_percentages, 
                       color=plt.cm.coolwarm(np.linspace(0, 1, len(pop_drivers))))
        ax5.set_yticks(range(len(pop_drivers)))
        ax5.set_yticklabels(pop_drivers)
        ax5.set_xlabel('% Picked')
        ax5.set_title('Driver Popularity', fontweight='bold', fontsize=12)
        
        # 6-8. Constructor analysis (spans bottom row)
        ax6 = fig.add_subplot(gs[2:, :])
        
        # Constructor season totals
        constructor_data = []
        for constructor in self.constructors:
            try:
                info = get_constructor_info(constructor)
                points = info.get('seasonTotalPoints', 0)
                value = float(info.get('value', '0M').replace('M', ''))
                popularity = info.get('percentagePicked', 0)
                constructor_data.append((constructor, points, value, popularity))
            except:
                continue
        
        constructor_data.sort(key=lambda x: x[1], reverse=True)
        
        if constructor_data:
            constructors, c_points, c_values, c_popularity = zip(*constructor_data)
            
            x = np.arange(len(constructors))
            width = 0.25
            
            bars1 = ax6.bar(x - width, c_points, width, label='Season Points', alpha=0.8)
            bars2 = ax6.bar(x, [v*10 for v in c_values], width, label='Value (x10M)', alpha=0.8)
            bars3 = ax6.bar(x + width, [p*5 for p in c_popularity], width, label='Popularity (x5%)', alpha=0.8)
            
            ax6.set_xlabel('Constructor')
            ax6.set_ylabel('Value (Scaled)')
            ax6.set_title('Constructor Comprehensive Analysis', fontweight='bold', fontsize=14)
            ax6.set_xticks(x)
            ax6.set_xticklabels(constructors, rotation=45)
            ax6.legend()
            ax6.grid(True, alpha=0.3)
        
        plt.suptitle('🏎️ Formula Fantasy - Season Overview Dashboard', 
                    fontsize=18, fontweight='bold', y=0.98)
        plt.show()

def main():
    """Main function to run the Formula Fantasy analysis examples"""
    print("🏁 Formula Fantasy Data Visualization Demo")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = FormulaFantasyAnalyzer()
    
    try:
        print("\n1️⃣ Driver Performance Comparison")
        print("-" * 30)
        performance_data = analyzer.driver_performance_comparison()
        
        print("\n2️⃣ Detailed Race Breakdown Analysis")
        print("-" * 35)
        analyzer.race_breakdown_analysis('VER')  # Analyze Verstappen's latest race
        
        print("\n3️⃣ Team Comparison Analysis")
        print("-" * 28)
        team_data = analyzer.team_comparison_analysis()
        
        print("\n4️⃣ Fantasy Strategy Analysis")
        print("-" * 30)
        strategy_data = analyzer.fantasy_strategy_analysis()
        
        print("\n5️⃣ Comprehensive Season Overview")
        print("-" * 33)
        analyzer.comprehensive_season_overview()
        
        print("\n🎉 Formula Fantasy Analysis Complete!")
        print("\nKey insights:")
        print(f"📊 Latest round analyzed: {analyzer.latest_round}")
        print(f"🏎️ Total drivers tracked: {len(analyzer.drivers)}")
        print(f"🏁 Total constructors: {len(analyzer.constructors)}")
        print("\n💡 This demo showcases the Formula Fantasy library's capabilities for:")
        print("   • Driver and constructor performance tracking")
        print("   • Race-by-race detailed analysis") 
        print("   • Fantasy strategy optimization")
        print("   • Value for money calculations")
        print("   • Popularity and contrarian pick analysis")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install matplotlib pandas seaborn numpy")

if __name__ == "__main__":
    main()