import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date


def calculate_net_worth_projection(
    initial_net_worth: float,
    initial_salary: float,
    salary_growth_rate: float,
    asset_growth_rate: float,
    dividend_yield: float,
    tax_rate: float,
    expense_ratio: float,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    """
    Calculate net worth projection based on input parameters.

    Parameters:
    -----------
    initial_net_worth : float
        Starting net worth in dollars
    initial_salary : float
        Starting annual salary in dollars
    salary_growth_rate : float
        Annual salary growth rate as decimal (e.g., 0.03 for 3%)
    asset_growth_rate : float
        Annual asset appreciation rate as decimal (e.g., 0.07 for 7%)
    dividend_yield : float
        Annual dividend yield as decimal (e.g., 0.02 for 2%)
    tax_rate : float
        Effective tax rate as decimal (e.g., 0.25 for 25%)
    expense_ratio : float
        Ratio of total income spent on expenses (e.g., 0.7 for 70%)
    start_year : int
        Starting year for projection
    end_year : int
        Ending year for projection

    Returns:
    --------
    pd.DataFrame
        DataFrame containing yearly projections
    """
    years = list(range(start_year, end_year + 1))
    data = []

    current_net_worth = initial_net_worth
    current_salary = initial_salary

    for year in years:
        # Calculate dividend income (only dividends are taxed)
        dividend_income = current_net_worth * dividend_yield

        # Calculate total income (salary + dividends)
        total_income = current_salary + dividend_income

        # Calculate after-tax income
        after_tax_income = total_income * (1 - tax_rate)

        # Calculate expenses
        expenses = after_tax_income * expense_ratio

        # Calculate savings
        savings = after_tax_income - expenses

        # Store current state before asset growth
        current_state = {
            "Year": year,
            "Net Worth": round(current_net_worth, 2),
            "Salary": round(current_salary, 2),
            "Dividend Income": round(dividend_income, 2),
            "Total Income": round(total_income, 2),
            "After-tax Income": round(after_tax_income, 2),
            "Expenses": round(expenses, 2),
            "Savings": round(savings, 2),
        }

        # Update net worth for next year:
        # 1. Add this year's savings
        # 2. Apply asset growth to the entire portfolio
        current_net_worth += savings
        current_net_worth *= 1 + asset_growth_rate

        # Update salary for next year
        current_salary *= 1 + salary_growth_rate

        data.append(current_state)

    return pd.DataFrame(data)


def main():
    st.title("Net Worth Projection Calculator")
    st.write(
        """
    This calculator helps you project your future net worth based on various financial parameters.
    Adjust the inputs below to see how different factors affect your wealth accumulation.
    """
    )

    # Input parameters
    col1, col2 = st.columns(2)

    with col1:
        initial_net_worth = st.number_input(
            "Initial Net Worth ($)",
            min_value=0.0,
            value=100000.0,
            step=10000.0,
            help="Your current net worth including all assets minus liabilities",
        )

        initial_salary = st.number_input(
            "Initial Annual Salary ($)",
            min_value=0.0,
            value=75000.0,
            step=5000.0,
            help="Your current annual salary before taxes",
        )

        salary_growth = st.slider(
            "Annual Salary Growth Rate (%)",
            min_value=0.0,
            max_value=15.0,
            value=3.0,
            step=0.1,
            help="Expected annual percentage increase in salary",
        )

        asset_growth = st.slider(
            "Annual Asset Growth Rate (%)",
            min_value=-5.0,
            max_value=20.0,
            value=7.0,
            step=0.1,
            help="Expected annual growth rate of your investments (excluding dividends)",
        )

    with col2:
        dividend_yield = st.slider(
            "Expected Dividend Yield (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            help="Expected annual dividend yield on your investments",
        )

        tax_rate = st.slider(
            "Effective Tax Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=25.0,
            step=0.5,
            help="Expected effective tax rate on income (salary + dividends)",
        )

        expense_ratio = st.slider(
            "Expense Ratio (% of after-tax income)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
            help="Percentage of after-tax income spent on expenses",
        )

        current_year = date.today().year
        start_year = st.number_input("Start Year", value=current_year, step=1)

        end_year = st.number_input(
            "End Year",
            min_value=start_year + 1,
            value=min(start_year + 10, current_year + 50),
            step=1,
        )

    # Calculate projections
    df = calculate_net_worth_projection(
        initial_net_worth=initial_net_worth,
        initial_salary=initial_salary,
        salary_growth_rate=salary_growth / 100,
        asset_growth_rate=asset_growth / 100,
        dividend_yield=dividend_yield / 100,
        tax_rate=tax_rate / 100,
        expense_ratio=expense_ratio / 100,
        start_year=start_year,
        end_year=end_year,
    )

    # Display results
    st.subheader("Net Worth Projection")

    # Create and display the chart
    fig = px.line(
        df,
        x="Year",
        y="Net Worth",
        title="Projected Net Worth Over Time",
        labels={"Net Worth": "Net Worth ($)"},
    )
    fig.update_layout(
        xaxis_title="Year", yaxis_title="Net Worth ($)", hovermode="x unified"
    )
    st.plotly_chart(fig)

    # Display detailed results
    st.subheader("Detailed Yearly Projections")
    st.dataframe(
        df.style.format(
            {
                "Net Worth": "${:,.0f}",
                "Salary": "${:,.0f}",
                "Dividend Income": "${:,.0f}",
                "Total Income": "${:,.0f}",
                "After-tax Income": "${:,.0f}",
                "Expenses": "${:,.0f}",
                "Savings": "${:,.0f}",
            }
        )
    )

    # Sensitivity Analysis
    st.subheader("Sensitivity Analysis")
    st.write(
        "Final net worth ($) under different tax rates and asset growth rates:"
    )

    # Generate sensitivity analysis data
    tax_rates = list(range(20, 51, 5))  # 20% to 50% in 5pp increments
    growth_rates = list(range(4, 21, 2))  # 4% to 20% in 2pp increments

    sensitivity_data = []
    for growth in growth_rates:
        row_data = []
        for tax in tax_rates:
            result = calculate_net_worth_projection(
                initial_net_worth=initial_net_worth,
                initial_salary=initial_salary,
                salary_growth_rate=salary_growth / 100,
                asset_growth_rate=growth / 100,
                dividend_yield=dividend_yield / 100,
                tax_rate=tax / 100,
                expense_ratio=expense_ratio / 100,
                start_year=start_year,
                end_year=end_year,
            )
            row_data.append(result.iloc[-1]["Net Worth"])
        sensitivity_data.append(row_data)

    # Create DataFrame for sensitivity table
    sensitivity_df = pd.DataFrame(
        sensitivity_data,
        columns=[f"{tax}%" for tax in tax_rates],
        index=[f"{growth}%" for growth in growth_rates],
    )
    sensitivity_df.index.name = "Asset Growth Rate"

    # Display the table with simple currency formatting
    st.dataframe(sensitivity_df.style.format("${:,.0f}"))

    # Add explanation
    st.caption(
        """
    The table above shows ending net worth for different combinations of tax rate (columns) 
    and asset growth rate (rows). All other parameters remain as specified above.
    """
    )

    # Summary statistics
    st.subheader("Summary Statistics")
    final_year = df.iloc[-1]
    first_year = df.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Net Worth Growth",
            f'${final_year["Net Worth"]:,.0f}',
            f'${final_year["Net Worth"] - first_year["Net Worth"]:,.0f}',
        )

    with col2:
        st.metric(
            "Final Annual Salary",
            f'${final_year["Salary"]:,.0f}',
            f'${final_year["Salary"] - first_year["Salary"]:,.0f}',
        )

    with col3:
        st.metric(
            "Final Annual Dividend Income",
            f'${final_year["Dividend Income"]:,.0f}',
            f'${final_year["Dividend Income"] - first_year["Dividend Income"]:,.0f}',
        )


if __name__ == "__main__":
    main()
