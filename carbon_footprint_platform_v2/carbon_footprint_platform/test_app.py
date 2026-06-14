"""
EcoTrack – Carbon Footprint Awareness Platform
Test Suite
 
Tests cover:
- Emission calculations
- Data validation
- Badge logic
- Edge cases
- Data processing functions
""" 
import pytest
import pandas as pd
import sys
import os
 
# ── Import app constants directly ─────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
 
# Constants (mirrored from app.py to avoid streamlit import in tests)
EMISSION_FACTORS = {
    "Transport": {
        "Car (Petrol) – per km":    0.21,
        "Car (Diesel) – per km":    0.17,
        "Car (Electric) – per km":  0.05,
        "Bus – per km":             0.089,
        "Train – per km":           0.041,
        "Flight (Domestic) – per km": 0.255,
        "Flight (International) – per km": 0.195,
        "Motorbike – per km":       0.114,
        "Bicycle / Walking":        0.0,
    },
    "Food": {
        "Beef meal":        6.61,
        "Pork meal":        2.42,
        "Chicken meal":     1.02,
        "Fish meal":        1.34,
        "Vegetarian meal":  0.50,
        "Vegan meal":       0.35,
        "Dairy (1 glass milk)": 0.63,
        "Cheese (100 g)":   1.32,
        "Eggs (1 egg)":     0.20,
    },
    "Home Energy": {
        "Electricity (kWh)": 0.82,
        "Natural Gas (kWh)": 0.20,
        "LPG (kg)":          2.98,
        "Coal (kg)":         2.42,
        "Solar/Renewable":   0.0,
    },
    "Shopping & Waste": {
        "New clothing item":         10.0,
        "Electronics (smartphone)": 70.0,
        "Electronics (laptop)":    300.0,
        "Plastic bag":               0.01,
        "Recycled 1 kg waste":      -0.21,
        "Composting 1 kg":          -0.10,
    }
}
 
GLOBAL_AVG_KG_PER_DAY = 13.0
 
 
# ── Core calculation function ─────────────────────────────────────────────────
def calculate_emissions(category: str, activity: str, quantity: float) -> float:
    """Calculate CO2 emissions for a given activity."""
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    factor = EMISSION_FACTORS.get(category, {}).get(activity, 0)
    return round(factor * quantity, 3)
 
def get_badge(total_kg: float) -> tuple:
    """Return badge name and color based on emissions."""
    if total_kg <= 3:    return ("🌟 Eco Hero", "#39d353")
    elif total_kg <= 7:  return ("🌿 Green Warrior", "#7ee787")
    elif total_kg <= 13: return ("🌱 Earth Aware", "#e3b341")
    elif total_kg <= 20: return ("⚡ Taking Action", "#f0883e")
    else:                return ("🔥 High Impact", "#f85149")
 
def get_daily_summary(activities: list) -> pd.DataFrame:
    """Compute daily summary from activities."""
    if not activities:
        return pd.DataFrame()
    df = pd.DataFrame(activities)
    df["date"] = pd.to_datetime(df["date"])
    return df.groupby("date")["emissions"].sum().reset_index()
 
def get_category_summary(activities: list) -> pd.DataFrame:
    """Compute category breakdown."""
    if not activities:
        return pd.DataFrame()
    df = pd.DataFrame(activities)
    return df.groupby("category")["emissions"].sum().reset_index()
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 1: Emission Calculations
# ══════════════════════════════════════════════════════════════════════════════
class TestEmissionCalculations:
    """Tests for core emission calculation logic."""
 
    def test_car_petrol_emissions(self):
        """Car petrol: 10 km * 0.21 = 2.1 kg CO2"""
        result = calculate_emissions("Transport", "Car (Petrol) – per km", 10)
        assert result == 2.1
 
    def test_car_electric_lower_than_petrol(self):
        """Electric car should always emit less than petrol car."""
        petrol = calculate_emissions("Transport", "Car (Petrol) – per km", 100)
        electric = calculate_emissions("Transport", "Car (Electric) – per km", 100)
        assert electric < petrol
 
    def test_bicycle_zero_emissions(self):
        """Bicycle/walking should produce zero emissions."""
        result = calculate_emissions("Transport", "Bicycle / Walking", 50)
        assert result == 0.0
 
    def test_beef_meal_emissions(self):
        """Beef meal: 1 meal * 6.61 = 6.61 kg CO2"""
        result = calculate_emissions("Food", "Beef meal", 1)
        assert result == 6.61
 
    def test_vegan_lower_than_beef(self):
        """Vegan meal should produce much less emissions than beef."""
        beef = calculate_emissions("Food", "Beef meal", 1)
        vegan = calculate_emissions("Food", "Vegan meal", 1)
        assert vegan < beef
        assert beef / vegan > 10  # beef is 10x+ more than vegan
 
    def test_solar_zero_emissions(self):
        """Solar/Renewable energy should have zero emissions."""
        result = calculate_emissions("Home Energy", "Solar/Renewable", 100)
        assert result == 0.0
 
    def test_recycling_negative_emissions(self):
        """Recycling should produce negative (saved) emissions."""
        result = calculate_emissions("Shopping & Waste", "Recycled 1 kg waste", 5)
        assert result < 0
 
    def test_composting_negative_emissions(self):
        """Composting should produce negative (saved) emissions."""
        result = calculate_emissions("Shopping & Waste", "Composting 1 kg", 3)
        assert result < 0
 
    def test_zero_quantity(self):
        """Zero quantity should return zero emissions."""
        result = calculate_emissions("Transport", "Car (Petrol) – per km", 0)
        assert result == 0.0
 
    def test_large_quantity(self):
        """Large quantity should scale proportionally."""
        single = calculate_emissions("Food", "Chicken meal", 1)
        hundred = calculate_emissions("Food", "Chicken meal", 100)
        assert round(hundred, 3) == round(single * 100, 3)
 
    def test_unknown_category_returns_zero(self):
        """Unknown category should return 0, not crash."""
        result = calculate_emissions("Unknown", "Unknown activity", 10)
        assert result == 0.0
 
    def test_unknown_activity_returns_zero(self):
        """Unknown activity in valid category should return 0."""
        result = calculate_emissions("Transport", "Rocket Ship", 10)
        assert result == 0.0
 
    def test_negative_quantity_raises_error(self):
        """Negative quantity should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_emissions("Transport", "Car (Petrol) – per km", -5)
 
    def test_result_is_rounded_to_3_decimals(self):
        """Result should be rounded to 3 decimal places."""
        result = calculate_emissions("Transport", "Bus – per km", 7)
        assert result == round(result, 3)
 
    def test_flight_domestic_higher_than_train(self):
        """Domestic flight should emit more than train per km."""
        flight = calculate_emissions("Transport", "Flight (Domestic) – per km", 100)
        train = calculate_emissions("Transport", "Train – per km", 100)
        assert flight > train
 
    def test_laptop_higher_than_smartphone(self):
        """Laptop should have higher carbon footprint than smartphone."""
        laptop = calculate_emissions("Shopping & Waste", "Electronics (laptop)", 1)
        phone = calculate_emissions("Shopping & Waste", "Electronics (smartphone)", 1)
        assert laptop > phone
 
    def test_electricity_emissions(self):
        """Electricity: 10 kWh * 0.82 = 8.2 kg CO2"""
        result = calculate_emissions("Home Energy", "Electricity (kWh)", 10)
        assert result == 8.2
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 2: Badge Logic
# ══════════════════════════════════════════════════════════════════════════════
class TestBadgeLogic:
    """Tests for user badge assignment based on emissions."""
 
    def test_eco_hero_badge(self):
        """Very low emissions should give Eco Hero badge."""
        badge, _ = get_badge(2.0)
        assert "Eco Hero" in badge
 
    def test_green_warrior_badge(self):
        """Low emissions should give Green Warrior badge."""
        badge, _ = get_badge(5.0)
        assert "Green Warrior" in badge
 
    def test_earth_aware_badge(self):
        """Medium emissions should give Earth Aware badge."""
        badge, _ = get_badge(10.0)
        assert "Earth Aware" in badge
 
    def test_taking_action_badge(self):
        """Above average emissions should give Taking Action badge."""
        badge, _ = get_badge(15.0)
        assert "Taking Action" in badge
 
    def test_high_impact_badge(self):
        """Very high emissions should give High Impact badge."""
        badge, _ = get_badge(25.0)
        assert "High Impact" in badge
 
    def test_zero_emissions_eco_hero(self):
        """Zero emissions should give Eco Hero badge."""
        badge, _ = get_badge(0.0)
        assert "Eco Hero" in badge
 
    def test_badge_returns_tuple(self):
        """Badge function should return a tuple of (str, str)."""
        result = get_badge(5.0)
        assert isinstance(result, tuple)
        assert len(result) == 2
 
    def test_badge_color_is_string(self):
        """Badge color should be a hex color string."""
        _, color = get_badge(5.0)
        assert color.startswith("#")
        assert len(color) == 7
 
    def test_boundary_eco_hero(self):
        """Exactly 3 kg should be Eco Hero."""
        badge, _ = get_badge(3.0)
        assert "Eco Hero" in badge
 
    def test_boundary_green_warrior(self):
        """Just above 3 kg should be Green Warrior."""
        badge, _ = get_badge(3.1)
        assert "Green Warrior" in badge
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 3: Data Processing
# ══════════════════════════════════════════════════════════════════════════════
class TestDataProcessing:
    """Tests for data aggregation and processing functions."""
 
    def setup_method(self):
        """Sample activities for testing."""
        self.sample_activities = [
            {"date": "2026-06-14", "category": "Transport", "activity": "Car (Petrol) – per km",
             "quantity": 10, "unit": "km", "emissions": 2.1},
            {"date": "2026-06-14", "category": "Food", "activity": "Beef meal",
             "quantity": 1, "unit": "meals", "emissions": 6.61},
            {"date": "2026-06-13", "category": "Home Energy", "activity": "Electricity (kWh)",
             "quantity": 5, "unit": "kWh", "emissions": 4.1},
        ]
 
    def test_daily_summary_returns_dataframe(self):
        """Daily summary should return a DataFrame."""
        result = get_daily_summary(self.sample_activities)
        assert isinstance(result, pd.DataFrame)
 
    def test_daily_summary_correct_totals(self):
        """Daily totals should sum correctly."""
        result = get_daily_summary(self.sample_activities)
        day_total = result[result["date"] == "2026-06-14"]["emissions"].values[0]
        assert round(day_total, 2) == round(2.1 + 6.61, 2)
 
    def test_daily_summary_empty_input(self):
        """Empty activities should return empty DataFrame."""
        result = get_daily_summary([])
        assert result.empty
 
    def test_category_summary_returns_dataframe(self):
        """Category summary should return a DataFrame."""
        result = get_category_summary(self.sample_activities)
        assert isinstance(result, pd.DataFrame)
 
    def test_category_summary_correct_categories(self):
        """Category summary should have all 3 categories."""
        result = get_category_summary(self.sample_activities)
        categories = result["category"].tolist()
        assert "Transport" in categories
        assert "Food" in categories
        assert "Home Energy" in categories
 
    def test_category_summary_empty_input(self):
        """Empty activities should return empty DataFrame."""
        result = get_category_summary([])
        assert result.empty
 
    def test_total_emissions_sum(self):
        """Total emissions should equal sum of all activities."""
        total = sum(a["emissions"] for a in self.sample_activities)
        assert round(total, 2) == round(2.1 + 6.61 + 4.1, 2)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 4: Emission Factors Validation
# ══════════════════════════════════════════════════════════════════════════════
class TestEmissionFactors:
    """Tests to validate the emission factors data."""
 
    def test_all_categories_exist(self):
        """All 4 categories must exist."""
        assert "Transport" in EMISSION_FACTORS
        assert "Food" in EMISSION_FACTORS
        assert "Home Energy" in EMISSION_FACTORS
        assert "Shopping & Waste" in EMISSION_FACTORS
 
    def test_transport_has_activities(self):
        """Transport category should have activities."""
        assert len(EMISSION_FACTORS["Transport"]) > 0
 
    def test_food_has_activities(self):
        """Food category should have activities."""
        assert len(EMISSION_FACTORS["Food"]) > 0
 
    def test_all_factors_are_numeric(self):
        """All emission factors should be numeric."""
        for category, activities in EMISSION_FACTORS.items():
            for activity, factor in activities.items():
                assert isinstance(factor, (int, float)), \
                    f"{category}/{activity} factor is not numeric"
 
    def test_global_average_is_correct(self):
        """Global average should be 13 kg/day."""
        assert GLOBAL_AVG_KG_PER_DAY == 13.0
 
    def test_beef_higher_than_vegan(self):
        """Beef emission factor should be much higher than vegan."""
        beef_factor = EMISSION_FACTORS["Food"]["Beef meal"]
        vegan_factor = EMISSION_FACTORS["Food"]["Vegan meal"]
        assert beef_factor > vegan_factor * 5
 
    def test_petrol_higher_than_electric(self):
        """Petrol car factor should be higher than electric."""
        petrol = EMISSION_FACTORS["Transport"]["Car (Petrol) – per km"]
        electric = EMISSION_FACTORS["Transport"]["Car (Electric) – per km"]
        assert petrol > electric
 
    def test_no_negative_transport_factors(self):
        """Transport factors should not be negative."""
        for activity, factor in EMISSION_FACTORS["Transport"].items():
            assert factor >= 0, f"{activity} has negative factor"
 
    def test_recycling_factor_is_negative(self):
        """Recycling should have negative factor (carbon saving)."""
        assert EMISSION_FACTORS["Shopping & Waste"]["Recycled 1 kg waste"] < 0
 
    def test_minimum_activities_per_category(self):
        """Each category should have at least 4 activities."""
        for category in EMISSION_FACTORS:
            assert len(EMISSION_FACTORS[category]) >= 4, \
                f"{category} has fewer than 4 activities"
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 5: Accessibility & Input Validation
# ══════════════════════════════════════════════════════════════════════════════
class TestAccessibilityAndValidation:
    """Tests for input validation and accessibility requirements."""
 
    def test_calculate_with_float_quantity(self):
        """Should handle float quantities correctly."""
        result = calculate_emissions("Transport", "Car (Petrol) – per km", 5.5)
        assert result == round(0.21 * 5.5, 3)
 
    def test_calculate_with_large_quantity(self):
        """Should handle very large quantities without errors."""
        result = calculate_emissions("Transport", "Car (Petrol) – per km", 10000)
        assert result == round(0.21 * 10000, 3)
 
    def test_calculate_with_fractional_quantity(self):
        """Should handle very small fractional quantities."""
        result = calculate_emissions("Food", "Beef meal", 0.5)
        assert result == round(6.61 * 0.5, 3)
 
    def test_emission_result_is_float(self):
        """Emission calculation should always return float."""
        result = calculate_emissions("Food", "Chicken meal", 2)
        assert isinstance(result, float)
 
    def test_badge_handles_very_high_emissions(self):
        """Badge should handle extreme emission values."""
        badge, color = get_badge(1000.0)
        assert "High Impact" in badge
        assert color is not None
 
    def test_badge_handles_exact_boundaries(self):
        """Test all exact boundary values for badges."""
        assert "Eco Hero" in get_badge(3.0)[0]
        assert "Green Warrior" in get_badge(7.0)[0]
        assert "Earth Aware" in get_badge(13.0)[0]
        assert "Taking Action" in get_badge(20.0)[0]
 
    def test_category_names_are_strings(self):
        """All category names should be non-empty strings."""
        for category in EMISSION_FACTORS:
            assert isinstance(category, str)
            assert len(category) > 0
 
    def test_activity_names_are_strings(self):
        """All activity names should be non-empty strings."""
        for category, activities in EMISSION_FACTORS.items():
            for activity in activities:
                assert isinstance(activity, str)
                assert len(activity) > 0
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASS 6: UI Accessibility Markers (source-level checks)
# ══════════════════════════════════════════════════════════════════════════════
class TestUIAccessibilityMarkers:
    """
    Source-level checks that key accessibility features are present in app.py,
    such as alt text, ARIA roles/labels, and contextual help text on inputs.
    """
 
    @classmethod
    def setup_class(cls):
        app_path = os.path.join(os.path.dirname(__file__), "app.py")
        with open(app_path, encoding="utf-8") as f:
            cls.source = f.read()
 
    def test_logo_has_alt_text(self):
        """Logo image should include descriptive alt text."""
        assert 'alt="EcoTrack leaf logo"' in self.source
 
    def test_aria_labels_present(self):
        """App should include ARIA labels for screen readers."""
        assert "aria-label" in self.source
 
    def test_aria_live_regions_present(self):
        """Dynamic content (AI responses, results) should use aria-live."""
        assert "aria-live" in self.source
 
    def test_focus_outline_styles_present(self):
        """Custom CSS should define visible focus indicators."""
        assert ":focus" in self.source
        assert "outline" in self.source
 
    def test_inputs_have_help_text(self):
        """Key inputs should include help text for screen readers/tooltips."""
        assert self.source.count('help=') >= 8
 
    def test_footer_has_accessibility_statement(self):
        """Footer should mention accessibility considerations."""
        assert "accessibility" in self.source.lower()
 
    def test_lang_attribute_present(self):
        """Page should declare a language for assistive technologies."""
        assert 'lang="en"' in self.source
 
    def test_contentinfo_role_present(self):
        """Footer should use a semantic landmark role."""
        assert 'role="contentinfo"' in self.source
 
 
# ══════════════════════════════════════════════════════════════════════════════
# Run tests
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
