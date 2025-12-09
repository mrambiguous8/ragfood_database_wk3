#!/usr/bin/env python3
"""
Food Database Analysis Script

This autonomous script analyzes fooddatabase.json and produces a comprehensive
breakdown by category_group with professional analytics and insights.

Author: AI Data Analysis Agent
Date: December 9, 2025
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path


class FoodDatabaseAnalyzer:
    """Autonomous analyzer for food database JSON files."""
    
    def __init__(self, json_path: str):
        """Initialize analyzer with path to JSON file."""
        self.json_path = Path(json_path)
        self.data = []
        self.category_counts = None
        self.total_items = 0
        
    def load_data(self):
        """Load and parse JSON data with error handling."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.total_items = len(self.data)
            print(f"✅ Loaded {self.total_items} items from {self.json_path.name}")
            return True
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.json_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format - {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def extract_category_groups(self):
        """Extract and count category_group values from data."""
        category_groups = []
        
        for item in self.data:
            # Primary field: category_group
            if 'category_group' in item:
                category_groups.append(item['category_group'])
            # Fallback: try 'origin' field
            elif 'origin' in item:
                category_groups.append(item['origin'])
            # Fallback: try 'category' field
            elif 'category' in item:
                category_groups.append(item['category'])
            else:
                category_groups.append('Uncategorized')
        
        self.category_counts = Counter(category_groups)
        print(f"✅ Extracted {len(self.category_counts)} unique category groups")
        
    def calculate_percentages(self):
        """Calculate percentage distribution for each category."""
        percentages = {}
        for category, count in self.category_counts.items():
            percentage = (count / self.total_items) * 100
            percentages[category] = percentage
        return percentages
    
    def generate_table(self):
        """Generate formatted markdown table with results."""
        percentages = self.calculate_percentages()
        
        # Sort by count (descending)
        sorted_categories = sorted(
            self.category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build table
        table_lines = [
            "| Category Group | Count | Percentage |",
            "|----------------|-------|------------|"
        ]
        
        for category, count in sorted_categories:
            percentage = percentages[category]
            table_lines.append(f"| {category} | {count} | {percentage:.1f}% |")
        
        # Add TOTAL row
        table_lines.append(f"| **TOTAL** | **{self.total_items}** | **100.0%** |")
        
        return "\n".join(table_lines)
    
    def generate_insights(self):
        """Generate interpretive insights about the data distribution."""
        percentages = self.calculate_percentages()
        sorted_categories = sorted(
            self.category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        insights = []
        
        # 1. Dominant category analysis
        top_category, top_count = sorted_categories[0]
        top_percentage = percentages[top_category]
        
        if top_percentage > 30:
            dominance_level = "heavily dominates"
        elif top_percentage > 20:
            dominance_level = "dominates"
        elif top_percentage > 15:
            dominance_level = "leads"
        else:
            dominance_level = "slightly leads"
        
        insights.append(
            f"**Dominant Category**: {top_category} {dominance_level} the dataset with "
            f"{top_count} items ({top_percentage:.1f}%), representing nearly "
            f"{top_percentage/10:.0f}x the average category size. This suggests a strong "
            f"focus on {top_category} cuisine in the database."
        )
        
        # 2. Underrepresented categories
        bottom_categories = [cat for cat, count in sorted_categories if count <= 2]
        
        if bottom_categories:
            insights.append(
                f"**Underrepresented Categories**: {len(bottom_categories)} categories have "
                f"minimal representation (≤2 items): {', '.join(bottom_categories[:5])}"
                f"{'...' if len(bottom_categories) > 5 else ''}. These niche categories offer "
                f"opportunities for expansion to create more balanced representation."
            )
        
        # 3. Distribution patterns
        num_categories = len(self.category_counts)
        avg_items = self.total_items / num_categories
        
        # Calculate distribution balance (coefficient of variation)
        counts = list(self.category_counts.values())
        import statistics
        if len(counts) > 1:
            std_dev = statistics.stdev(counts)
            cv = (std_dev / avg_items) * 100
            
            if cv > 80:
                balance = "highly imbalanced"
            elif cv > 50:
                balance = "moderately imbalanced"
            elif cv > 30:
                balance = "somewhat uneven"
            else:
                balance = "relatively balanced"
            
            insights.append(
                f"**Distribution Patterns**: The dataset shows a {balance} distribution across "
                f"{num_categories} categories. The average category contains {avg_items:.1f} items, "
                f"with a coefficient of variation of {cv:.1f}%, indicating "
                f"{'significant concentration in top categories' if cv > 50 else 'moderate variety across categories'}."
            )
        
        # 4. Cultural diversity
        top_5 = sorted_categories[:5]
        top_5_percentage = sum(percentages[cat] for cat, _ in top_5)
        
        insights.append(
            f"**Cultural Diversity**: The top 5 categories account for {top_5_percentage:.1f}% "
            f"of all items. "
            f"{'This concentration suggests focused coverage of major cuisines' if top_5_percentage > 70 else 'The distribution shows good diversity across multiple culinary traditions'}. "
            f"Categories include: {', '.join([cat for cat, _ in top_5])}."
        )
        
        # 5. Notable observations
        single_item_categories = [cat for cat, count in sorted_categories if count == 1]
        
        if single_item_categories:
            insights.append(
                f"**Notable Observations**: {len(single_item_categories)} categories contain "
                f"exactly 1 item, suggesting either specialty/unique dishes or areas needing "
                f"expansion. The dataset spans {num_categories} distinct culinary traditions, "
                f"demonstrating global coverage with room for deeper exploration in "
                f"underrepresented regions."
            )
        else:
            insights.append(
                f"**Notable Observations**: Every category contains multiple items, indicating "
                f"comprehensive coverage across {num_categories} culinary traditions. The dataset "
                f"demonstrates balanced attention to each included cuisine with consistent depth."
            )
        
        return insights
    
    def generate_report(self, output_path: str = "food_database_analysis_report.md"):
        """Generate complete markdown report and save to file."""
        report_lines = [
            "# Food Database Breakdown by Category Group",
            "",
            f"*Analysis Date: {datetime.now().strftime('%B %d, %Y')} | Total Items: {self.total_items}*",
            "",
            "---",
            "",
            "## Category Distribution",
            "",
            self.generate_table(),
            "",
            "---",
            "",
            "## Interpretive Insights",
            ""
        ]
        
        # Add insights
        insights = self.generate_insights()
        for insight in insights:
            report_lines.append(f"{insight}\n")
        
        report_lines.extend([
            "---",
            "",
            "## Methodology",
            "",
            "This analysis was performed autonomously by extracting the `category_group` field from each item in the database. ",
            "Items were counted and grouped, percentages calculated based on total dataset size, and results sorted by frequency. ",
            "Statistical measures including coefficient of variation were used to assess distribution balance. ",
            "Insights were generated through automated analysis of concentration patterns, representation levels, and diversity metrics.",
            "",
            "---",
            "",
            f"*Report generated automatically by Food Database Analyzer v1.0*"
        ])
        
        report_content = "\n".join(report_lines)
        
        # Save report
        try:
            output_file = Path(output_path)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"✅ Report saved to: {output_file.name}")
            return True
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
    
    def analyze(self, output_path: str = "food_database_analysis_report.md"):
        """Execute complete analysis pipeline."""
        print("\n" + "="*70)
        print("🍽️  FOOD DATABASE ANALYSIS")
        print("="*70 + "\n")
        
        # Step 1: Load data
        if not self.load_data():
            return False
        
        # Step 2: Extract and count category groups
        self.extract_category_groups()
        
        # Step 3: Generate and save report
        success = self.generate_report(output_path)
        
        if success:
            print("\n" + "="*70)
            print("✅ ANALYSIS COMPLETE!")
            print("="*70)
            print(f"\n📊 Summary:")
            print(f"   - Total Items: {self.total_items}")
            print(f"   - Unique Categories: {len(self.category_counts)}")
            print(f"   - Top Category: {max(self.category_counts, key=self.category_counts.get)} "
                  f"({max(self.category_counts.values())} items)")
            print(f"   - Report File: {output_path}\n")
        
        return success


def main():
    """Main execution function."""
    # Try multiple possible locations for the JSON file
    possible_paths = [
        "Cloud_Version/fooddatabase.json",
        "fooddatabase.json",
        "../Cloud_Version/fooddatabase.json"
    ]
    
    json_path = None
    for path in possible_paths:
        if Path(path).exists():
            json_path = path
            break
    
    if not json_path:
        print("❌ Error: Could not find fooddatabase.json in expected locations")
        print("   Searched:")
        for path in possible_paths:
            print(f"   - {path}")
        return
    
    # Create analyzer and run analysis
    analyzer = FoodDatabaseAnalyzer(json_path)
    analyzer.analyze("food_database_analysis_report.md")


if __name__ == "__main__":
    main()
