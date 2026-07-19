# from io import BytesIO

# import pandas as pd

# try:
#     from tkinter import filedialog, messagebox
# except ImportError:  # pragma: no cover - Streamlit/CI environments
#     filedialog = None
#     messagebox = None

# results_buffer = []


# def get_buffer_count():
#     """Return the number of currently buffered calculation sheets."""
#     return len(results_buffer)


# def _build_export_filename(age=None, msc=None, annuity_years=None):
#     """Build a default filename from the current calculation inputs."""
#     age_text = age if age is not None else "Unknown"
#     msc_text = int(msc) if msc is not None else "Unknown"
#     years_text = annuity_years if annuity_years is not None else "Unknown"
#     return f"Age_{age_text}__MSC_{msc_text}__Years_{years_text}.xlsx"


# def _format_sheet_name(index, age=None, msc=None, annuity_years=None):
#     age_text = f"Age_{age}" if age is not None else f"Age_{index}"
#     msc_text = f"MSC_{int(msc)}" if msc is not None else f"MSC_{index}"
#     years_text = f"Years_{annuity_years}" if annuity_years is not None else f"Years_{index}"
#     return f"{age_text}_{msc_text}_{years_text}"


# def _safe_notify(kind, title, message):
#     if messagebox is None:
#         return None
#     if kind == "info":
#         messagebox.showinfo(title, message)
#     elif kind == "warning":
#         messagebox.showwarning(title, message)
#     elif kind == "error":
#         messagebox.showerror(title, message)


# def add_result_to_buffer(df, age=None, msc=None, annuity_years=None):
#     """Store the current dataframe in memory so multiple calculations can be exported together later."""
#     if df is None or df.empty:
#         return False

#     sheet_name = _format_sheet_name(len(results_buffer) + 1, age=age, msc=msc, annuity_years=annuity_years)
#     results_buffer.append((sheet_name, df.copy()))
#     _safe_notify(
#         "info",
#         "Info",
#         f"Calculation saved to current workbook as sheet '{sheet_name}'. You can export all buffered calculations later.",
#     )
#     return True


# def _build_export_writer(target):
#     """Use xlsxwriter when available, otherwise fall back to pandas default Excel writing."""
#     try:
#         return pd.ExcelWriter(target, engine="xlsxwriter")
#     except ModuleNotFoundError:
#         return pd.ExcelWriter(target)


# def _apply_column_widths(writer, df, sheet_name):
#     """Applies auto-fit column width only when the xlsxwriter engine is available."""
#     try:
#         worksheet = writer.sheets[sheet_name]
#         for idx, col in enumerate(df.columns):
#             series = df[col]
#             max_len = max(series.astype(str).map(len).max(), len(str(col))) + 2
#             worksheet.set_column(idx, idx, max_len)
#     except Exception:
#         pass


# def build_excel_bytes(df, age=None, msc=None, annuity_years=None, sheet_name="Sheet1"):
#     """Create an Excel workbook in memory for a single dataframe."""
#     if df is None or df.empty:
#         return None

#     output = BytesIO()
#     with _build_export_writer(output) as writer:
#         df.to_excel(writer, sheet_name=sheet_name, index=False)
#         _apply_column_widths(writer, df, sheet_name)
#     output.seek(0)
#     return output.getvalue()


# def build_buffer_excel_bytes():
#     """Create an Excel workbook in memory containing all buffered calculations."""
#     if not results_buffer:
#         return None

#     output = BytesIO()
#     with _build_export_writer(output) as writer:
#         for sheet_name, df in results_buffer:
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#             _apply_column_widths(writer, df, sheet_name)
#     output.seek(0)
#     return output.getvalue()


# def export_buffer_to_excel():
#     """Export all buffered calculations into a single workbook, one sheet per calculation."""
#     if not results_buffer:
#         _safe_notify("warning", "Warning", "No calculations have been saved yet.")
#         return None

#     if filedialog is not None and messagebox is not None:
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".xlsx",
#             filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
#             title="Save Calculation Workbook",
#         )

#         if file_path:
#             try:
#                 with _build_export_writer(file_path) as writer:
#                     for sheet_name, df in results_buffer:
#                         df.to_excel(writer, sheet_name=sheet_name, index=False)
#                         _apply_column_widths(writer, df, sheet_name)

#                 _safe_notify(
#                     "info",
#                     "Success",
#                     f"Workbook successfully exported to:\n{file_path}\n\nSaved {len(results_buffer)} sheet(s) to the current workbook.",
#                 )
#             except Exception as e:
#                 _safe_notify("error", "Error", f"Failed to save file:\n{str(e)}")
#         return None

#     return build_buffer_excel_bytes()


# def export_to_excel(df, age=None, msc=None, annuity_years=None):
#     """Backward-compatible single-export helper for a single dataframe."""
#     if df is None or df.empty:
#         _safe_notify("warning", "Warning", "No data available to export.")
#         return None

#     if filedialog is not None and messagebox is not None:
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".xlsx",
#             initialfile=_build_export_filename(age=age, msc=msc, annuity_years=annuity_years),
#             filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
#             title="Save Calculation Results",
#         )

#         if file_path:
#             try:
#                 with _build_export_writer(file_path) as writer:
#                     df.to_excel(writer, sheet_name="Sheet1", index=False)
#                     _apply_column_widths(writer, df, "Sheet1")

#                 _safe_notify("info", "Success", f"Data successfully exported to:\n{file_path}")
#             except Exception as e:
#                 _safe_notify("error", "Error", f"Failed to save file:\n{str(e)}")
#         return None

#     return build_excel_bytes(df, age=age, msc=msc, annuity_years=annuity_years)




from io import BytesIO
import pandas as pd

results_buffer = []


def get_buffer_count():
    """Return the number of currently buffered calculation sheets."""
    return len(results_buffer)


def _build_export_filename(age=None, msc=None, annuity_years=None):
    age_text = age if age is not None else "Unknown"
    msc_text = int(msc) if msc is not None else "Unknown"
    years_text = annuity_years if annuity_years is not None else "Unknown"
    return f"Age_{age_text}__MSC_{msc_text}__Years_{years_text}.xlsx"


def _format_sheet_name(index, age=None, msc=None, annuity_years=None):
    age_text = f"Age_{age}" if age is not None else f"Age_{index}"
    msc_text = f"MSC_{int(msc)}" if msc is not None else f"MSC_{index}"
    years_text = (
        f"Years_{annuity_years}"
        if annuity_years is not None
        else f"Years_{index}"
    )
    return f"{age_text}_{msc_text}_{years_text}"
    

def add_result_to_buffer(df, metadata, age=None, msc=None, annuity_years=None):
    """Store a calculation in memory."""
    if df is None or df.empty:
        return False

    sheet_name = _format_sheet_name(
        len(results_buffer) + 1,
        age=age,
        msc=msc,
        annuity_years=annuity_years,
    )

    # Make sheet name unique if it already exists
    existing = {name for name, _, _ in results_buffer}

    base = sheet_name
    counter = 2

    while sheet_name in existing:
        sheet_name = f"{base}_{counter}"
        counter += 1

    results_buffer.append(
        (
            sheet_name,
            df.copy(),
            metadata.copy(),
        )
    )

    return True

def _build_export_writer(target):
    try:
        return pd.ExcelWriter(target, engine="xlsxwriter")
    except ModuleNotFoundError:
        return pd.ExcelWriter(target)


def _write_sheet_with_metadata(writer, df, metadata, sheet_name):
    metrics = pd.DataFrame({
        "Summary Metric": list(metadata.keys()),
        "Value": list(metadata.values()),
    })

    metrics.to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=0,
        startcol=4,
        index=False,
    )

    df.to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=10,
        startcol=0,
        index=False,
    )

    worksheet = writer.sheets[sheet_name]

def _apply_column_widths(writer, df, sheet_name):
    try:
        worksheet = writer.sheets[sheet_name]

        for i, column in enumerate(df.columns):
            width = max(
                df[column].astype(str).map(len).max(),
                len(str(column)),
            ) + 2

            worksheet.set_column(i, i, width)

    except Exception:
        pass


def build_excel_bytes(
    df,
    metadata,
    age=None,
    msc=None,
    annuity_years=None,
    sheet_name="Sheet1",
):
    """Create a single-sheet Excel workbook."""

    if df is None or df.empty:
        return None

    output = BytesIO()

    with _build_export_writer(output) as writer:
        _write_sheet_with_metadata(
            writer,
            df,
            metadata,
            sheet_name,
        )

        _apply_column_widths(
            writer,
            df,
            sheet_name,
        )

    output.seek(0)
    return output.getvalue()


def build_buffer_excel_bytes():
    """Create an Excel workbook containing every saved calculation."""

    if not results_buffer:
        return None

    output = BytesIO()

    with _build_export_writer(output) as writer:

        for sheet_name, df, metadata in results_buffer:

            _write_sheet_with_metadata(
                writer,
                df,
                metadata,
                sheet_name,
            )

            _apply_column_widths(
                writer,
                df,
                sheet_name,
            )

    output.seek(0)
    return output.getvalue()


def clear_buffer():
    """Remove all saved calculations."""
    results_buffer.clear()
