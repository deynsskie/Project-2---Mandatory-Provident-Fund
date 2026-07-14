"""
Simple SSS Mandatory Provident Fund calculator.
"""
import pandas as pd

def calculate(age, MSC, annuity_years):
    retirement_age = 60     # age at which contributions cease
    start_year = 2026       # calendar year when contributions start

    effective_annual_rate = 0.06
    effective_monthly_rate = (1 + effective_annual_rate) ** (1 / 12) - 1
    nominal_annual_rate = 0.01
    nominal_monthly_rate = nominal_annual_rate / 12
    net_roi = 0.05
    nominal_roi = (1 + net_roi) ** (1 / 12) - 1

    data = []
    transaction_num = 0
    current_year = start_year
    current_age = age
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    msc_attributed_to_mpf = max(0, min(MSC - 20000, 35000 - 20000))
    mpf_contribution = msc_attributed_to_mpf * 0.15

    accumulated_value = 0.0
    monthly_pension = 0.0
    final_av_prev = 0.0
    taav = None
    total_benefits_claimed = 0.0

    last_age = retirement_age + annuity_years - 1

    while current_age < retirement_age + annuity_years:
        for month in range(1, 13):
            transaction_num += 1
            is_last_month = (current_age == last_age and month == 12)

            if current_age > retirement_age or (current_age == retirement_age and month > 1):
                msc_attributed_to_mpf = 0
                mpf_contribution = 0
                investment_income = final_av_prev * effective_monthly_rate
                management_fee = (final_av_prev + investment_income) * nominal_monthly_rate
                grown_balance = final_av_prev + investment_income - management_fee

                if is_last_month:
                    this_pension = grown_balance
                    remaining_av = 0.0
                else:
                    this_pension = monthly_pension
                    remaining_av = final_av_prev - this_pension

                total_benefits_claimed += this_pension
                final_av = grown_balance - this_pension
                accumulated_value = 0.0
                final_av_prev = final_av

            elif current_age == retirement_age and month == 1:
                msc_attributed_to_mpf = 0
                mpf_contribution = 0
                investment_income = accumulated_value * effective_monthly_rate
                management_fee = (accumulated_value + investment_income) * nominal_monthly_rate
                accumulated_value += investment_income - management_fee
                taav = accumulated_value
                monthly_pension = accumulated_value / (
                    ((1 - (1 + nominal_roi) ** (-annuity_years * 12)) / nominal_roi) * (1 + nominal_roi)
                )
                this_pension = monthly_pension
                total_benefits_claimed += this_pension
                remaining_av = accumulated_value - this_pension
                final_av = remaining_av
                final_av_prev = final_av

            else:
                if current_age == age and current_year == start_year and month == 1:
                    investment_income = 0.0
                    management_fee = 0.0
                    accumulated_value = mpf_contribution
                else:
                    investment_income = accumulated_value * effective_monthly_rate
                    management_fee = (accumulated_value + investment_income) * nominal_monthly_rate
                    accumulated_value += mpf_contribution + investment_income - management_fee
                this_pension = 0.0
                remaining_av = None
                final_av = None

            data.append({
                '#': transaction_num,
                'Year': current_year,
                'Month': months[month - 1],
                'Age': current_age,
                'MSC Attributed to MPF (₱)': f"{msc_attributed_to_mpf:,.2f}" if current_age < retirement_age else '-',
                'MPF Contribution (₱)': f"{mpf_contribution:,.2f}" if current_age < retirement_age else '-',
                'Investment Income (₱)': f"{investment_income:,.2f}" if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Management Fee (₱)': f"{management_fee:,.2f}" if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Accumulated Value (₱)': f"{accumulated_value:,.2f}" if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Monthly Pension (₱)': f"{this_pension:,.2f}" if current_age >= retirement_age else '-',
                'Remaining AV (₱)': (f"{remaining_av:,.2f}" if remaining_av is not None else '-'),
                'Investment Income (Annuity) (₱)': f"{investment_income:,.2f}" if current_age > retirement_age or (current_age == retirement_age and month > 1) else '-',
                'Management Fee (Annuity) (₱)': f"{management_fee:,.2f}" if current_age > retirement_age or (current_age == retirement_age and month > 1) else '-',
                'Final Accumulated Value (₱)': (f"{final_av:,.2f}" if final_av is not None else '-')
            })

        current_year += 1
        current_age += 1

    df = pd.DataFrame(data)
    return monthly_pension, total_benefits_claimed, taav, df