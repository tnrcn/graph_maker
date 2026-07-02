# Violin Plot Creator - Create violin plots from Excel data
# Copyright (C) 2026 Taner ÇİN
# taner.ciin@gmail.com
#
# This program is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see <http://www.gnu.org/licenses/>.

import customtkinter as ctk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox

class ViolinPlotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Violin Plot Creator")
        self.geometry("500x850") 
        ctk.set_appearance_mode("System")

        # --- UI Elements ---
        
        # 1. Excel Path
        ctk.CTkLabel(self, text="Excel File Path").pack(pady=(20, 0))
        self.entry_path = ctk.CTkEntry(self, width=350)
        self.entry_path.pack(pady=5)
        self.btn_browse = ctk.CTkButton(self, text="Select File", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        # 2. X and Y Columns
        ctk.CTkLabel(self, text="X-Axis Column Name (As in Excel):").pack(pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self, width=350)
        self.entry_x.pack(pady=5)

        ctk.CTkLabel(self, text="Y-Axis Column Name (As in Excel):").pack(pady=(10, 0))
        self.entry_y = ctk.CTkEntry(self, width=350)
        self.entry_y.pack(pady=5)

        # 3. Graph Title
        ctk.CTkLabel(self, text="Graph Title:").pack(pady=(10, 0))
        self.entry_title = ctk.CTkEntry(self, width=350)
        self.entry_title.pack(pady=5)

        # 4. X-Axis Group Labels
        ctk.CTkLabel(self, text="X-Axis Labels (Separate with comma, e.g., 1:Control, 2:Experiment):").pack(pady=(10, 0))
        self.entry_x_labels = ctk.CTkEntry(self, width=350)
        self.entry_x_labels.pack(pady=5)

        # 5. Parameters
        ctk.CTkLabel(self, text="Cut-off parameter (cut):").pack(pady=(10, 0))
        self.entry_cut = ctk.CTkEntry(self, width=350)
        self.entry_cut.insert(0, "0") 
        self.entry_cut.pack(pady=5)

        ctk.CTkLabel(self, text="Smoothing level (bw_adjust):").pack(pady=(10, 0))
        self.entry_bw = ctk.CTkEntry(self, width=350)
        self.entry_bw.insert(0, "0.5") 
        self.entry_bw.pack(pady=5)

        # 6. Run Button
        self.btn_plot = ctk.CTkButton(self, text="Generate and Save Plot", command=self.generate_plot)
        self.btn_plot.pack(pady=30)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if filename:
            self.entry_path.delete(0, 'end')
            self.entry_path.insert(0, filename)

    def generate_plot(self):
        path = self.entry_path.get().strip()
        x_col = self.entry_x.get().strip()
        y_col = self.entry_y.get().strip()
        title_val = self.entry_title.get().strip()
        x_labels_input = self.entry_x_labels.get().strip()
        cut_val = self.entry_cut.get().strip()
        bw_val = self.entry_bw.get().strip()

        try:
            cut_val = float(cut_val) if cut_val else 0
            bw_val = float(bw_val) if bw_val else 0.5

            df = pd.read_excel(path)

            if x_col not in df.columns or y_col not in df.columns:
                messagebox.showerror("Error", f"Column names not found!\nAvailable columns: {list(df.columns)}")
                return

            # Generate Plot
            plt.figure(figsize=(10, 6))
            ax = sns.violinplot(data=df, x=x_col, y=y_col, cut=cut_val, bw_adjust=bw_val)
            
            # Title
            if title_val:
                plt.title(title_val)
            else:
                plt.title(f"{y_col} vs {x_col} Violin Plot")

            # X-Axis Labeling
            if x_labels_input:
                try:
                    mapping = {}
                    pairs = x_labels_input.split(',')
                    for pair in pairs:
                        if ':' in pair:
                            key, val = pair.split(':')
                            mapping[key.strip()] = val.strip()
                    
                    current_labels = [label.get_text() for label in ax.get_xticklabels()]
                    new_labels = [mapping.get(label, label) for label in current_labels]
                    ax.set_xticklabels(new_labels)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Labeling failed, check the format (Error: {e})")

            # Save as PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", 
                filetypes=[("PDF File", "*.pdf")]
            )
            
            if save_path:
                plt.savefig(save_path, format='pdf')
                messagebox.showinfo("Success", f"Graph successfully saved:\n{save_path}")

            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = ViolinPlotApp()
    app.mainloop()
