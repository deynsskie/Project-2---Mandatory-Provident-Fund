import streamlit as st
import pandas as pd
from io import BytesIO


def calculate_mpf(age, MSC, annuity_years):
    retirement_age = 60
    start_year = 2026

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
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    msc_attributed_to_mpf = max(0, min(MSC - 20000, 35000 - 20000))
    mpf_contribution = msc_attributed_to_mpf * 0.15
    accumulated_value = 0.0
    monthly_pension = 0.0
    final_av_prev = 0.0
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

                final_av = grown_balance - this_pension
                accumulated_value = 0.0
                final_av_prev = final_av

            elif current_age == retirement_age and month == 1:
                msc_attributed_to_mpf = 0
                mpf_contribution = 0
                investment_income = accumulated_value * effective_monthly_rate
                management_fee = (accumulated_value + investment_income) * nominal_monthly_rate
                accumulated_value += investment_income - management_fee
                monthly_pension = accumulated_value / (((1 - (1 + nominal_roi) ** (-annuity_years * 12)) / nominal_roi) * (1 + nominal_roi))
                this_pension = monthly_pension
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
                'MSC Attributed to MPF': msc_attributed_to_mpf if current_age < retirement_age else '-',
                'MPF Contribution': round(mpf_contribution, 2) if current_age < retirement_age else '-',
                'Investment Income': round(investment_income, 2) if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Management Fee': round(management_fee, 2) if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Accumulated Value': round(accumulated_value, 2) if current_age <= retirement_age and not (current_age == retirement_age and month > 1) else '-',
                'Monthly Pension': round(this_pension, 2) if current_age >= retirement_age else '-',
                'Remaining AV': (round(remaining_av, 2) if remaining_av is not None else '-'),
                'Investment Income (Annuity)': round(investment_income, 2) if current_age > retirement_age or (current_age == retirement_age and month > 1) else 0,
                'Management Fee (Annuity)': round(management_fee, 2) if current_age > retirement_age or (current_age == retirement_age and month > 1) else 0,
                'Final Accumulated Value': (round(final_av, 2) if final_av is not None else '-'),
            })

        current_year += 1
        current_age += 1

    return pd.DataFrame(data)


@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MPF Result')
    processed_data = output.getvalue()
    return processed_data


st.set_page_config(page_title='MPF Calculator', layout='centered')
st.title('MPF Calculator')
st.write('Enter the member details and calculate projected MPF results.')

age = st.number_input('Age', min_value=18, max_value=100, value=30, step=1)
msc_choice = st.selectbox('Monthly Salary Credit', ['Min (20,500)', 'Max (35,000)', 'Other'])
msc_custom = 20500.0

if msc_choice == 'Other':
    msc_custom = st.number_input('Custom MSC value', min_value=0.0, value=20500.0, step=100.0)

if msc_choice == 'Min (20,500)':
    MSC = 20500.0
elif msc_choice == 'Max (35,000)':
    MSC = 35000.0
else:
    MSC = msc_custom

benefit_choice = st.selectbox('Benefit Duration', ['5 years', '15 years', 'Other'])
if benefit_choice == 'Other':
    annuity_years = st.number_input('Custom benefit duration (years)', min_value=1, max_value=50, value=5, step=1)
elif benefit_choice == '5 years':
    annuity_years = 5
else:
    annuity_years = 15

if st.button('Calculate'):
    df = calculate_mpf(age, MSC, annuity_years)
    st.success('Calculation complete!')
    st.dataframe(df)

    excel_data = to_excel(df)
    st.download_button(
        label='Download results as Excel',
        data=excel_data,
        file_name='MPF_Result.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
