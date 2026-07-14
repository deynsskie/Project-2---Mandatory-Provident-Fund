import streamlit as st

from calculator import calculate
from excel_export import (
    add_result_to_buffer,
    build_buffer_excel_bytes,
    build_excel_bytes,
    get_buffer_count,
)


def main() -> None:
    st.set_page_config(page_title="SSS MPF Calculator", page_icon="💰", layout="wide")
    st.title("SSS Mandatory Provident Fund Calculator")
    st.caption("Estimate the monthly pension, review the contribution schedule, and download Excel results from any browser.")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=59,
            value=30,
        )
    
        msc_option = st.selectbox(
            "Monthly Salary Credit",
            ["Min (20,500)", "Max (35,000)", "Other"],
        )
    
        if msc_option == "Other":
            msc = st.number_input(
                "Enter MSC value",
                min_value=0.0,
                value=20500.0,
                step=100.0,
            )
        elif msc_option == "Min (20,500)":
            msc = 20500.0
        else:
            msc = 35000.0
    
    with col2:
        annuity_option = st.selectbox(
            "Benefit Duration",
            ["5 years", "15 years", "Other"],
        )
    
        if annuity_option == "Other":
            annuity_years = st.number_input(
                "Enter benefit duration",
                min_value=1,
                max_value=50,
                value=5,
            )
        else:
            annuity_years = 5 if annuity_option == "5 years" else 15
    
    submitted = st.button("Calculate")
    # with st.form("calculator_form"):
    #     col1, col2 = st.columns(2)

    #     with col1:
    #         age = st.number_input("Age", min_value=18, max_value=59, value=30, step=1)
    #         msc_option = st.selectbox("Monthly Salary Credit", ["Min (20,500)", "Max (35,000)", "Other"])
    #         msc_custom = 20500.0

    #         if msc_option == "Other":
    #             msc_custom = st.number_input("Custom MSC value", min_value=0.0, value=20500.0, step=100.0)

    #         if msc_option == "Min (20,500)":
    #             msc = 20500.0
    #         elif msc_option == "Max (35,000)":
    #             msc = 35000.0
    #         else:
    #             msc = msc_custom

    #     with col2:
    #         annuity_option = st.selectbox("Benefit Duration", ["5 years", "15 years", "Other"])
    #         if annuity_option == "Other":
    #             annuity_years = st.number_input(
    #                 "Enter benefit duration in years",
    #                 min_value=1,
    #                 max_value=50,
    #                 value=5,
    #                 step=1,
    #             )
    #         else:
    #             annuity_years = 5 if annuity_option == "5 years" else 15

    #     submitted = st.form_submit_button("Calculate")

    # if submitted:
    #     try:
    #         monthly_pension, total_benefits_claimed, taav, df = calculate(
    #             int(age), float(msc), int(annuity_years)
    #         )
    #         add_result_to_buffer(df, age=int(age), msc=float(msc), annuity_years=int(annuity_years))

    #         col_a, col_b, col_c = st.columns(3)
    #         with col_a:
    #             st.metric("Estimated Monthly Pension", f"₱{monthly_pension:,.2f}")
    #         with col_b:
    #             st.metric("Total Benefits Claimed", f"₱{total_benefits_claimed:,.2f}")
    #         with col_c:
    #             st.metric("TAAV at Retirement", f"₱{taav:,.2f}" if taav is not None else "N/A")

    #         st.dataframe(df, use_container_width=True, height=450)

    #         latest_bytes = build_excel_bytes(
    #             df,
    #             age=int(age),
    #             msc=float(msc),
    #             annuity_years=int(annuity_years),
    #         )
    #         buffer_bytes = build_buffer_excel_bytes() if get_buffer_count() >= 1 else None

    #         col_d, col_e, col_f = st.columns(3)
    #         with col_d:
    #             st.download_button(
    #                 "Download Latest Excel",
    #                 data=latest_bytes,
    #                 file_name=f"mpf_results_age_{int(age)}.xlsx",
    #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #                 disabled=latest_bytes is None,
    #             )
    #         with col_e:
    #             st.download_button(
    #                 "Download All Saved Results",
    #                 data=buffer_bytes,
    #                 file_name="mpf_buffered_results.xlsx",
    #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #                 disabled=buffer_bytes is None,
    #             )
    #         with col_f:
    #             st.download_button(
    #                 "Download CSV",
    #                 data=df.to_csv(index=False).encode("utf-8"),
    #                 file_name=f"mpf_results_age_{int(age)}.csv",
    #                 mime="text/csv",
    #             )
    #     except Exception as exc:
    #         st.error(f"Unable to calculate results: {exc}")
    if submitted:

        if annuity_years <= 0:
            st.error("Benefit duration must be at least 1 year.")
            st.stop()
        # Validate inputs first
        if msc < 20500 or msc > 35000:
            st.error("Monthly Salary Credit must be within the range [20500, 35000].")
            st.stop()

    
        try:
            monthly_pension, total_benefits_claimed, taav, df = calculate(
                int(age),
                float(msc),
                int(annuity_years),
            )
    
            add_result_to_buffer(
                df,
                age=int(age),
                msc=float(msc),
                annuity_years=int(annuity_years),
            )
    
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Estimated Monthly Pension", f"₱{monthly_pension:,.2f}")
            with col_b:
                st.metric("Total Benefits Claimed", f"₱{total_benefits_claimed:,.2f}")
            with col_c:
                st.metric(
                    "TAAV at Retirement",
                    f"₱{taav:,.2f}" if taav is not None else "N/A"
                )
    
            st.dataframe(df, use_container_width=True, height=450)
    
            latest_bytes = build_excel_bytes(
                df,
                age=int(age),
                msc=float(msc),
                annuity_years=int(annuity_years),
            )
    
            buffer_bytes = (
                build_buffer_excel_bytes()
                if get_buffer_count() >= 1
                else None
            )
    
            col_d, col_e, col_f = st.columns(3)
    
            with col_d:
                st.download_button(
                    "Download Latest Excel",
                    data=latest_bytes,
                    file_name=f"mpf_results_age_{int(age)}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    
            with col_e:
                st.download_button(
                    "Download All Saved Results",
                    data=buffer_bytes,
                    file_name="mpf_buffered_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    disabled=buffer_bytes is None,
                )
    
            with col_f:
                st.download_button(
                    "Download CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=f"mpf_results_age_{int(age)}.csv",
                    mime="text/csv",
                )
    
        except Exception as exc:
            st.exception(exc)
    else:
        st.info("Fill in the form and click Calculate to see the results.")
if __name__ == "__main__":
    main()
