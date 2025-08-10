#!/usr/bin/env python3
"""
Generate sample Formula Fantasy plots as image files
This creates actual plot images you can view
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from formula_fantasy import get_driver_points, get_driver_info, get_constructor_info, list_drivers, list_constructors

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_driver_comparison_plot():
    """Create driver performance comparison plot"""
    print("📊 Creating driver comparison plot...")
    
    drivers = ['VER', 'NOR', 'RUS', 'PIA', 'HAM']
    rounds = ['11', '12', '13', '14', '15']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Individual round performance
    colors = plt.cm.tab10(np.linspace(0, 1, len(drivers)))
    x = np.arange(len(rounds))
    width = 0.15
    
    for i, driver in enumerate(drivers):
        points = []
        for round_num in rounds:
            try:
                pts = get_driver_points(driver, round_num)
                points.append(pts)
            except:
                points.append(0)
        
        ax1.bar(x + i * width, points, width, label=driver, color=colors[i], alpha=0.8)
    
    ax1.set_xlabel('Race Round')
    ax1.set_ylabel('Fantasy Points')
    ax1.set_title('Driver Performance Comparison - Last 5 Rounds', fontsize=14, fontweight='bold')
    ax1.set_xticks(x + width * 2)
    ax1.set_xticklabels([f'R{r}' for r in rounds])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Season totals comparison
    season_totals = []
    driver_info = {}
    for driver in drivers:
        try:
            info = get_driver_info(driver)
            total = info.get('seasonTotalPoints', 0)
            season_totals.append(total)
            driver_info[driver] = info
        except:
            season_totals.append(0)
    
    bars = ax2.bar(drivers, season_totals, color=colors, alpha=0.8)
    ax2.set_xlabel('Driver')
    ax2.set_ylabel('Season Total Points')
    ax2.set_title('Season Total Points Comparison', fontsize=14, fontweight='bold')
    
    # Add value labels and team info
    for i, (bar, total, driver) in enumerate(zip(bars, season_totals, drivers)):
        height = bar.get_height()
        team = driver_info.get(driver, {}).get('team', 'Unknown')[:8]
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(total)}\n({team})', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('driver_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Saved: driver_comparison.png")

def create_value_analysis_plot():
    """Create value for money analysis plot"""
    print("💰 Creating value analysis plot...")
    
    drivers = list_drivers()[:12]  # Top 12 for good visualization
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Collect data
    driver_data = {}
    for driver in drivers:
        try:
            info = get_driver_info(driver)
            driver_data[driver] = {
                'season_total': info.get('seasonTotalPoints', 0),
                'value': float(info.get('value', '0M').replace('M', '')),
                'percentage_picked': info.get('percentagePicked', 0),
                'team': info.get('team', 'Unknown')
            }
        except:
            continue
    
    if not driver_data:
        print("❌ No driver data available")
        return
    
    drivers_list = list(driver_data.keys())
    
    # 1. Value vs Performance scatter
    values = [driver_data[d]['value'] for d in drivers_list]
    season_points = [driver_data[d]['season_total'] for d in drivers_list]
    popularity = [driver_data[d]['percentage_picked'] for d in drivers_list]
    
    scatter = ax1.scatter(values, season_points, s=[p*8 for p in popularity], 
                         alpha=0.7, c=range(len(drivers_list)), cmap='viridis')
    
    for i, driver in enumerate(drivers_list):
        ax1.annotate(driver, (values[i], season_points[i]), 
                    xytext=(3, 3), textcoords='offset points', fontsize=9, fontweight='bold')
    
    ax1.set_xlabel('Value (Millions)')
    ax1.set_ylabel('Season Total Points')
    ax1.set_title('Value vs Performance\n(Bubble size = Popularity %)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. Value for money ranking
    value_for_money = [pts/val if val > 0 else 0 for pts, val in zip(season_points, values)]
    sorted_indices = sorted(range(len(value_for_money)), key=lambda i: value_for_money[i], reverse=True)
    top_8_indices = sorted_indices[:8]
    
    top_drivers = [drivers_list[i] for i in top_8_indices]
    top_vfm = [value_for_money[i] for i in top_8_indices]
    
    bars = ax2.barh(range(len(top_drivers)), top_vfm, 
                   color=plt.cm.RdYlGn(np.linspace(0.3, 1, len(top_drivers))))
    ax2.set_yticks(range(len(top_drivers)))
    ax2.set_yticklabels([f"{d}\n({driver_data[d]['team'][:6]})" for d in top_drivers])
    ax2.set_xlabel('Points per Million')
    ax2.set_title('Top Value for Money Picks', fontweight='bold')
    
    # Add labels
    for i, (bar, vfm) in enumerate(zip(bars, top_vfm)):
        width = bar.get_width()
        ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{vfm:.1f}', ha='left', va='center', fontweight='bold')
    
    # 3. Popularity vs Performance
    ax3.scatter(popularity, season_points, s=100, alpha=0.7, 
               c=values, cmap='plasma')
    
    for i, driver in enumerate(drivers_list):
        ax3.annotate(driver, (popularity[i], season_points[i]), 
                    xytext=(3, 3), textcoords='offset points', fontsize=9, fontweight='bold')
    
    ax3.set_xlabel('Percentage Picked (%)')
    ax3.set_ylabel('Season Total Points')
    ax3.set_title('Popular vs Contrarian Strategy\n(Color = Value)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. Team distribution pie chart
    team_points = {}
    for driver, data in driver_data.items():
        team = data['team'][:8]  # Shorten team names
        if team not in team_points:
            team_points[team] = 0
        team_points[team] += data['season_total']
    
    teams = list(team_points.keys())[:6]  # Top 6 teams
    team_totals = [team_points[team] for team in teams]
    
    ax4.pie(team_totals, labels=teams, autopct='%1.1f%%', startangle=90)
    ax4.set_title('Points Distribution by Team', fontweight='bold')
    
    plt.suptitle('Formula Fantasy - Value Analysis Dashboard', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('value_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Saved: value_analysis.png")

def create_constructor_analysis_plot():
    """Create constructor analysis plot"""
    print("🏁 Creating constructor analysis plot...")
    
    constructors = list_constructors()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
    
    # Collect constructor data
    constructor_data = {}
    for constructor in constructors:
        try:
            info = get_constructor_info(constructor)
            constructor_data[constructor] = {
                'season_total': info.get('seasonTotalPoints', 0),
                'value': float(info.get('value', '0M').replace('M', '')),
                'percentage_picked': info.get('percentagePicked', 0)
            }
        except:
            continue
    
    if not constructor_data:
        print("❌ No constructor data available")
        return
    
    constructors_list = list(constructor_data.keys())
    
    # 1. Season totals
    season_totals = [constructor_data[c]['season_total'] for c in constructors_list]
    bars1 = ax1.bar(constructors_list, season_totals, 
                   color=plt.cm.viridis(np.linspace(0, 1, len(constructors_list))))
    ax1.set_title('Constructor Season Total Points', fontweight='bold')
    ax1.set_ylabel('Total Points')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, total in zip(bars1, season_totals):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(total)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 2. Value analysis
    values = [constructor_data[c]['value'] for c in constructors_list]
    ax2.scatter(values, season_totals, s=150, alpha=0.7, 
               c=range(len(constructors_list)), cmap='tab10')
    
    for i, constructor in enumerate(constructors_list):
        ax2.annotate(constructor, (values[i], season_totals[i]), 
                    xytext=(5, 5), textcoords='offset points', fontweight='bold')
    
    ax2.set_xlabel('Value (Millions)')
    ax2.set_ylabel('Season Total Points')
    ax2.set_title('Constructor Value vs Performance', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. Popularity ranking
    popularity = [constructor_data[c]['percentage_picked'] for c in constructors_list]
    bars3 = ax3.barh(constructors_list, popularity, 
                    color=plt.cm.coolwarm(np.linspace(0, 1, len(constructors_list))))
    ax3.set_xlabel('Percentage Picked (%)')
    ax3.set_title('Constructor Popularity', fontweight='bold')
    
    # Add percentage labels
    for bar, pct in zip(bars3, popularity):
        width = bar.get_width()
        ax3.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                f'{pct:.1f}%', ha='left', va='center', fontweight='bold', fontsize=9)
    
    # 4. Championship standings (top 6)
    sorted_constructors = sorted(constructors_list, 
                                key=lambda c: constructor_data[c]['season_total'], reverse=True)
    top_6 = sorted_constructors[:6]
    top_6_points = [constructor_data[c]['season_total'] for c in top_6]
    
    colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#4472C4', '#70AD47', '#FFC000']
    bars4 = ax4.barh(range(len(top_6)), top_6_points, color=colors)
    ax4.set_yticks(range(len(top_6)))
    ax4.set_yticklabels([f"{i+1}. {c}" for i, c in enumerate(top_6)])
    ax4.set_xlabel('Season Points')
    ax4.set_title('Constructor Championship Standings', fontweight='bold')
    
    # Add point labels
    for i, (bar, points) in enumerate(zip(bars4, top_6_points)):
        width = bar.get_width()
        ax4.text(width + 10, bar.get_y() + bar.get_height()/2.,
                f'{int(points)}', ha='left', va='center', fontweight='bold')
    
    plt.suptitle('Formula Fantasy - Constructor Analysis Dashboard', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('constructor_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Saved: constructor_analysis.png")

def create_race_breakdown_plot():
    """Create detailed race breakdown visualization"""
    print("🔍 Creating race breakdown plot...")
    
    driver = 'VER'  # Max Verstappen
    round_num = '14'  # Hungary
    
    try:
        from formula_fantasy import get_driver_breakdown
        race_breakdown = get_driver_breakdown(driver, round_num, "race")
        driver_info = get_driver_info(driver)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Race points breakdown pie chart
        race_points = {k: v for k, v in race_breakdown.items() if v != 0}
        if race_points:
            colors = plt.cm.Set3(np.linspace(0, 1, len(race_points)))
            wedges, texts, autotexts = ax1.pie(race_points.values(), labels=race_points.keys(), 
                                              autopct='%1.0f pts', colors=colors, startangle=90)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            ax1.text(0.5, 0.5, 'No race points\nthis round', ha='center', va='center', 
                    transform=ax1.transAxes, fontsize=14)
        
        ax1.set_title(f'{driver} - Race Points Breakdown (Round {round_num})', fontweight='bold')
        
        # 2. Driver season stats
        season_info = {
            'Season Total': driver_info.get('seasonTotalPoints', 0),
            'Percentage Picked': driver_info.get('percentagePicked', 0),
            'Value (M)': float(driver_info.get('value', '0M').replace('M', ''))
        }
        
        bars = ax2.bar(season_info.keys(), season_info.values(), 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax2.set_title(f'{driver} - Season Stats', fontweight='bold')
        ax2.set_ylabel('Value')
        
        for bar, value in zip(bars, season_info.values()):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Points trend over recent rounds
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
        
        # 4. All race points breakdown details
        categories = list(race_breakdown.keys())
        values = list(race_breakdown.values())
        
        # Color code positive/negative points
        colors = ['green' if v > 0 else 'red' if v < 0 else 'gray' for v in values]
        
        bars = ax4.barh(categories, values, color=colors, alpha=0.7)
        ax4.set_xlabel('Points')
        ax4.set_title(f'{driver} - Detailed Points Breakdown (Round {round_num})', fontweight='bold')
        ax4.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, values):
            width = bar.get_width()
            label_x = width + 0.1 if width >= 0 else width - 0.1
            ha = 'left' if width >= 0 else 'right'
            ax4.text(label_x, bar.get_y() + bar.get_height()/2.,
                    f'{int(value)}', ha=ha, va='center', fontweight='bold')
        
        plt.suptitle(f'Formula Fantasy - {driver} ({driver_info.get("team", "Unknown Team")}) Analysis', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('race_breakdown.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print("✅ Saved: race_breakdown.png")
        
    except Exception as e:
        print(f"❌ Error creating race breakdown: {e}")

def main():
    """Create all sample plots"""
    print("🖼️ Creating Formula Fantasy Sample Plots")
    print("=" * 50)
    
    try:
        create_driver_comparison_plot()
        create_value_analysis_plot()
        create_constructor_analysis_plot()
        create_race_breakdown_plot()
        
        print("\n🎉 All plots created successfully!")
        print("\n📁 Generated files:")
        print("   📊 driver_comparison.png - Driver performance comparison")
        print("   💰 value_analysis.png - Value for money analysis")  
        print("   🏁 constructor_analysis.png - Constructor analysis")
        print("   🔍 race_breakdown.png - Detailed race breakdown")
        
        print("\n✅ Your Formula Fantasy library can create stunning visualizations!")
        print("   • Professional-quality charts and graphs")
        print("   • Multi-panel dashboards")
        print("   • Interactive data analysis")
        print("   • Real F1 Fantasy data integration")
        
    except Exception as e:
        print(f"❌ Error creating plots: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()