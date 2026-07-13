import pandas as pd
from tkinter import filedialog, messagebox
# import xlsxwriter

def export_to_excel(df):
    """Prompts the user for a location and saves the dataframe as an Excel file with column widths fitted to content."""
    if df is None or df.empty:
        messagebox.showwarning("Warning", "No data available to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
        title="Save Calculation Results"
    )

    if file_path:
        try:
            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Sheet1", index=False)
                worksheet = writer.sheets["Sheet1"]

                for idx, col in enumerate(df.columns):
                    series = df[col]
                    max_len = max(series.astype(str).map(len).max(), len(str(col))) + 2
                    worksheet.set_column(idx, idx, max_len)

            messagebox.showinfo("Success", f"Data successfully exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")