import tkinter as tk
from tkinter import ttk, messagebox

class CalculatorApp:
    def __init__(self, master, on_submit_callback):
        self.master = master
        self.master.title("SSS Mandatory Provident Fund Calculator")
        self.master.geometry("450x500")
        self.on_submit_callback = on_submit_callback

        style = ttk.Style()
        style.theme_use("aqua") #clam #aqua #default #vista #xpnative #winnative

        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        user_info_frame = tk.LabelFrame(main_frame, text=" Input Member Information ", padx=15, pady=15)
        user_info_frame.pack(fill="x", pady=10)

        # 1. Age Input
        ttk.Label(user_info_frame, text="Age:").pack(anchor="w", pady=(5, 2))
        self.age_spinbox = tk.Spinbox(user_info_frame, from_=18, to=59, width=28)
        self.age_spinbox.pack(fill="x", pady=(0, 10))

        # 2. Monthly Salary Credit Input
        ttk.Label(user_info_frame, text="Monthly Salary Credit:").pack(anchor="w", pady=(5, 2))
        self.MSC_combobox = ttk.Combobox(user_info_frame, values=["Min (20,500)", "Max (35,000)", "Other"], state="readonly")
        self.MSC_combobox.pack(fill="x", pady=(0, 10))
        self.MSC_combobox.bind("<<ComboboxSelected>>", self.toggle_msc_entry)
        self.MSC_other_entry = ttk.Entry(user_info_frame)

        # 3. Benefit Duration Input
        self.benefit_label = ttk.Label(user_info_frame, text="Benefit Duration:")
        self.benefit_label.pack(anchor="w", pady=(5, 2))
        self.benefit_combobox = ttk.Combobox(user_info_frame, values=["5 years", "15 years", "Other"], state="readonly")
        self.benefit_combobox.pack(fill="x", pady=(0, 10))
        self.benefit_combobox.bind("<<ComboboxSelected>>", self.toggle_benefit_entry)
        self.benefit_other_entry = ttk.Entry(user_info_frame)

        # Action Button
        submit_button = ttk.Button(main_frame, text="Calculate / Enter Data", command=self.enter_data)
        submit_button.pack(fill="x", pady=15)

        # Results Presentation Area
        results_frame = tk.LabelFrame(main_frame, text=" Summary Results ", padx=15, pady=15)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        self.pension_display_label = ttk.Label(results_frame, text="Est. Monthly Pension: ₱0.00", font=("Arial", 12, "bold"))
        self.pension_display_label.pack(pady=10)

        # Export Button (Disabled by default until calculations exist)
        self.export_button = ttk.Button(results_frame, text="Export Table to Excel", state="disabled")
        self.export_button.pack(fill="x", pady=5)

        # Tracking variables
        self.results_window = None
        self.results_tree = None

    def toggle_msc_entry(self, event):
        if self.MSC_combobox.get() == "Other":
            self.MSC_other_entry.pack(fill="x", pady=(0, 10), before=self.benefit_label)
        else:
            self.MSC_other_entry.pack_forget()

    def toggle_benefit_entry(self, event):
        if self.benefit_combobox.get() == "Other":
            self.benefit_other_entry.pack(fill="x", pady=(0, 10))
        else:
            self.benefit_other_entry.pack_forget()

    def enter_data(self):
        try:
            age = int(self.age_spinbox.get())
            if age >= 60:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid age (must be under retirement age 60).")
            return

        if self.MSC_combobox.get() == "Min (20,500)":
            MSC = 20500
        elif self.MSC_combobox.get() == "Max (35,000)":
            MSC = 35000
        else:
            try:
                MSC = float(self.MSC_other_entry.get())
                if MSC < 20500 or MSC > 35000:
                    raise Exception
            except ValueError:
                messagebox.showerror("Error", "Enter a valid MSC price format.")
                return
            except Exception:
                messagebox.showerror("Error", "Enter a valid MSC value between 20,500 and 35,000.")
                return

        if self.benefit_combobox.get() == "5 years":
            annuity_years = 5
        elif self.benefit_combobox.get() == "15 years":
            annuity_years = 15
        else:
            try:
                annuity_years = int(self.benefit_other_entry.get())
                if annuity_years <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Enter a valid benefit duration integer.")
                return
            
        # Instead of doing calculation here, throw data to main.py
        self.on_submit_callback(age, MSC, annuity_years)

    def show_results_table(self, df):
        """Show or refresh the calculation results in a table window."""
        
        # Check if there exists a table window, if none it creates one, if it exists it reuses it
        if self.results_window is None or not self.results_window.winfo_exists(): 
            self.results_window = tk.Toplevel(self.master) # Creates a new top-level window
            self.results_window.title("MPF Calculation Results") 
            self.results_window.geometry("1400x800") 

            # Table creation
            self.results_tree = ttk.Treeview(self.results_window, show="headings")
            y_scrollbar = ttk.Scrollbar(self.results_window, orient=tk.VERTICAL, command=self.results_tree.yview)
            x_scrollbar = ttk.Scrollbar(self.results_window, orient=tk.HORIZONTAL, command=self.results_tree.xview)
            self.results_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set) 

            self.results_tree.grid(row=0, column=0, sticky="nsew")
            y_scrollbar.grid(row=0, column=1, sticky="ns")
            x_scrollbar.grid(row=1, column=0, sticky="ew")

            self.results_window.grid_rowconfigure(0, weight=1)
            self.results_window.grid_columnconfigure(0, weight=1)

        columns = list(df.columns) 
        self.results_tree.configure(columns=columns) 

        # Column settings
        # for col in columns:
        #     self.results_tree.heading(col, text=col)
        #     self.results_tree.column(col, anchor=tk.CENTER, width=110, stretch=True)
        column_widths = {
            "#": 50,
            "Year": 50,
            "Month": 50,
            "Age": 50,
            "MSC Attributed to MPF (₱)": 180,
            "MPF Contribution (₱)": 170,
            "Investment Income (₱)": 170,
            "Management Fee (₱)": 150,
            "Accumulated Value (₱)": 170,
            "Monthly Pension (₱)": 160,
            "Investment Income (Annuity) (₱)": 210,
            "Management Fee (Annuity) (₱)": 200,
            "Final Accumulated Value (₱)": 200,
        }

        for col in columns:
            self.results_tree.heading(col, text=col)
            width = column_widths.get(col, 120)
            self.results_tree.column(col, anchor=tk.CENTER, width=width, stretch=True)

        # Deletes old data in the table before inserting new data
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Inserts the new data in the table
        for _, row in df.iterrows():
            self.results_tree.insert("", tk.END, values=[row[col] for col in columns])
            self.results_window.lift()
            self.results_window.focus_force()

    def update_results_ui(self, monthly_pension, export_command):
        """Updates UI display with calculated metrics and hooks the export trigger."""
        self.pension_display_label.config(text=f"Est. Monthly Pension: ₱{monthly_pension:,.2f}")
        self.export_button.config(state="normal", command=export_command)

def main_tk(on_submit_callback):
    window = tk.Tk()
    app = CalculatorApp(window, on_submit_callback)
    return window, app