import streamlit as st

from calculator import calculate
from excel_export import (
    add_result_to_buffer,
    build_result_excel_bytes,
    build_buffer_excel_bytes,
    get_buffer_count,
)


def main():
    st.set_page_config(
        page_title="SSS Mandatory Provident Fund Calculator",
        page_icon="💰",
        layout="centered",
    )

    st.title("SSS Mandatory Provident Fund Calculator")
    st.write(
        "Enter the member details and calculate the projected Mandatory Provident Fund (MPF) benefits."
    )

    with st.form("calculator_form"):

        # ---------------- Age ----------------
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=59,
            value=30,
            step=1,
        )

        # ---------------- MSC ----------------
        msc_option = st.selectbox(
            "Monthly Salary Credit",
            [
                "Min (20,500)",
                "Max (35,000)",
                "Other",
            ],
        )

        if msc_option == "Min (20,500)":
            msc = 20500.0

        elif msc_option == "Max (35,000)":
            msc = 35000.0

        else:
            msc = st.number_input(
                "Custom MSC Value",
                min_value=0.0,
                value=20500.0,
                step=100.0,
            )

        # ---------------- Benefit Duration ----------------
        benefit_option = st.selectbox(
            "Benefit Duration",
            [
                "5 years",
                "15 years",
                "Other",
            ],
        )

        if benefit_option == "5 years":
            annuity_years = 5

        elif benefit_option == "15 years":
            annuity_years = 15

        else:
            annuity_years = st.number_input(
                "Custom Benefit Duration (Years)",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
            )

        submitted = st.form_submit_button("Calculate")

    # ============================================================
    # Results
    # ============================================================

    if submitted:

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

            st.success("Calculation complete!")

            st.metric(
                "Estimated Monthly Pension",
                f"₱{monthly_pension:,.2f}",
            )

            st.metric(
                "Total Benefits Claimed",
                f"₱{total_benefits_claimed:,.2f}",
            )

            st.metric(
                "TAAV at Retirement",
                f"₱{taav:,.2f}" if taav is not None else "N/A",
            )

            st.dataframe(df, use_container_width=True)

            latest_bytes = build_result_excel_bytes(
                df,
                age=int(age),
                msc=float(msc),
                annuity_years=int(annuity_years),
            )

            buffer_bytes = (
                build_buffer_excel_bytes()
                if get_buffer_count() > 0
                else None
            )

            st.download_button(
                label="Download Latest Excel",
                data=latest_bytes,
                file_name=f"MPF_Result_Age_{age}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.download_button(
                label="Download All Saved Results",
                data=buffer_bytes,
                file_name="MPF_Buffered_Results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                disabled=buffer_bytes is None,
            )

            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"MPF_Result_Age_{age}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Unable to calculate results: {e}")

    else:
        st.info("Enter the required information and click **Calculate**.")


if __name__ == "__main__":
    main()
