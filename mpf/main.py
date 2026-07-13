# MAIN CODE
import tkinter as tk
from gui import main_tk
from calculator import calculate
from excel_export import export_to_excel

# Global storage placeholder for tracking the current session's output dataframe
current_dataframe = None

def handle_calculation_pipeline(age, msc, annuity_years):
    """
    Coordinates data processing: pipeline passes parameters from UI to the calculator engine,
    prints outputs to the terminal, and links the resulting dataset to the Excel export feature.
    """
    global current_dataframe
    
    # 1. Run Core Calculations
    monthly_pension, df = calculate(age, msc, annuity_years)
    current_dataframe = df
    
    # 2. Print output to Terminal (Optional)
    # print("\n" + "="*50)
    # print(f"Calculated Monthly Pension: ${monthly_pension:,.2f}")
    # print("="*50)
    # print(df.to_string(index=False))
    # print("="*50 + "\n")
    
    # 3. Inform GUI that output metrics are processed and setup the Excel trigger
    app_instance.update_results_ui(
        monthly_pension=monthly_pension, 
        export_command=lambda: export_to_excel(current_dataframe)
    )

    # 4. CALL THE NEW WINDOW TABLE HERE 
    app_instance.show_results_table(df)

if __name__ == "__main__":
    # Boot the system passing our workflow pipeline function as the listener
    root_window, app_instance = main_tk(on_submit_callback=handle_calculation_pipeline)
    root_window.mainloop()