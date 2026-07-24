# Arı Sürüsü Grafiği Oluşturucu - Excel dosyasındaki verilerden arı sürüsü grafiği oluşturma programı
# Copyright (C) 2026 Taner ÇİN
# taner.ciin@gmail.com
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı (Free Software Foundation) tarafından 
# yayımlanan GNU Genel Kamu Lisansı'nın (GPL) 3. sürümü koşulları altında onu yeniden
# dağıtabilir ve/veya değiştirebilirsiniz.
#
# Bu program, kullanışlı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİSİ YOKTUR;
# hatta satılabilirlik veya belirli bir amaca uygunluk gibi zımni garantisi bile yoktur.
# Ayrıntılar için GNU Genel Kamu Lisansı'na bakınız.
#
# Bu programla birlikte GNU Genel Kamu Lisansı'nın bir kopyasını almış olmalısınız. 
# Eğer almadıysanız, bkz: <http://www.gnu.org/licenses/>.

import customtkinter as ctk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox

class BeeswarmPlotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arı Sürüsü Grafiği Oluşturucu")
        self.geometry("500x750") 
        ctk.set_appearance_mode("System")

        # --- Arayüz Elemanları ---
        
        # 1. Excel Dosya Yolu
        ctk.CTkLabel(self, text="Excel Dosyası:").pack(pady=(20, 0))
        self.entry_path = ctk.CTkEntry(self, width=350)
        self.entry_path.pack(pady=5)
        self.btn_browse = ctk.CTkButton(self, text="Dosya Seç", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        # 2. X ve Y Sütunları
        ctk.CTkLabel(self, text="X Ekseni Sütun Başlığı (Excel'deki başlık):").pack(pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self, width=350)
        self.entry_x.pack(pady=5)

        ctk.CTkLabel(self, text="Y Ekseni Sütun Başlığı (Excel'deki başlık):").pack(pady=(10, 0))
        self.entry_y = ctk.CTkEntry(self, width=350)
        self.entry_y.pack(pady=5)

        # 3. Grafik Başlığı
        ctk.CTkLabel(self, text="Grafik Başlığı (Opsiyonel):").pack(pady=(10, 0))
        self.entry_title = ctk.CTkEntry(self, width=350)
        self.entry_title.pack(pady=5)

        # 4. X Ekseni Gruplama İsimlendirme
        ctk.CTkLabel(self, text="X Ekseni İsimlendirme (örn: 1:Kontrol grubu, 2:Deney grubu):").pack(pady=(10, 0))
        self.entry_x_labels = ctk.CTkEntry(self, width=350)
        self.entry_x_labels.pack(pady=5)

        # 5. Nokta Boyutu Parametresi
        ctk.CTkLabel(self, text="Nokta Boyutu (Point Size - Varsayılan: 5):").pack(pady=(10, 0))
        self.entry_size = ctk.CTkEntry(self, width=350)
        self.entry_size.insert(0, "5") 
        self.entry_size.pack(pady=5)

        # 6. Çalıştır Butonu
        self.btn_plot = ctk.CTkButton(self, text="Grafiği Oluştur ve Kaydet", command=self.generate_plot)
        self.btn_plot.pack(pady=30)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Dosyaları", "*.xlsx *.xls")])
        if filename:
            self.entry_path.delete(0, 'end')
            self.entry_path.insert(0, filename)

    def generate_plot(self):
        path = self.entry_path.get().strip()
        x_col = self.entry_x.get().strip()
        y_col = self.entry_y.get().strip()
        title_val = self.entry_title.get().strip()
        x_labels_input = self.entry_x_labels.get().strip()
        size_val = self.entry_size.get().strip()

        try:
            size_val = float(size_val) if size_val else 5

            df = pd.read_excel(path)

            if x_col not in df.columns or y_col not in df.columns:
                messagebox.showerror("Hata", f"Sütun isimleri bulunamadı!\nMevcut sütunlar: {list(df.columns)}")
                return

            # Grafiği oluştur (Şık bir görünüm için şeffaf bir boxplot üzerine swarmplot çiziyoruz)
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, x=x_col, y=y_col, boxprops=dict(alpha=0.3), showcaps=False, 
                        whiskerprops=dict(alpha=0.3), fliersize=0)
            ax = sns.swarmplot(data=df, x=x_col, y=y_col, size=size_val, palette="deep")
            
            # Başlık ayarı
            if title_val:
                plt.title(title_val)
            else:
                plt.title(f"{y_col} ve {x_col} Arı Sürüsü Grafiği")

            # X Ekseni İsimlendirme (Virgülle ayrılmış format)
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
                    messagebox.showwarning("Uyarı", f"Etiketleme yapılamadı, formatı kontrol edin (Hata: {e})")

            # PDF Olarak Kaydetme
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", 
                filetypes=[("PDF Dosyası", "*.pdf")]
            )
            
            if save_path:
                plt.savefig(save_path, format='pdf')
                messagebox.showinfo("Başarılı", f"Grafik başarıyla kaydedildi:\n{save_path}")

            plt.show()

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{str(e)}")

if __name__ == "__main__":
    app = BeeswarmPlotApp()
    app.mainloop()
