# Keman Grafiği Çizici - Excel dosyasındaki verilerden keman grafiği oluşturma programı
# Copyright (C) 2026 Taner ÇİN
# taner.ciin@gmail.com
#
# Bu program özgür yazılımdır. Özgür Yazılım Vakfı (Free Software Foundation) tarafından 
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

class ViolinPlotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Keman Grafiği Oluşturucu")
        self.geometry("500x850") 
        ctk.set_appearance_mode("System")

        # --- Arayüz Elemanları ---
        
        # 1. Excel Yolu
        ctk.CTkLabel(self, text="Excel Dosyası").pack(pady=(20, 0))
        self.entry_path = ctk.CTkEntry(self, width=350)
        self.entry_path.pack(pady=5)
        self.btn_browse = ctk.CTkButton(self, text="Dosya Seç", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        # 2. X ve Y Sütunları
        ctk.CTkLabel(self, text="X Ekseni Başlığı (Excel dosyasında kullanılan başlık) ").pack(pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self, width=350)
        self.entry_x.pack(pady=5)

        ctk.CTkLabel(self, text="Y Ekseni Başlığı (Excel dosyasında kullanılan başlık):").pack(pady=(10, 0))
        self.entry_y = ctk.CTkEntry(self, width=350)
        self.entry_y.pack(pady=5)

        # 3. Grafik Başlığı
        ctk.CTkLabel(self, text="Grafik Başlığı:").pack(pady=(10, 0))
        self.entry_title = ctk.CTkEntry(self, width=350)
        self.entry_title.pack(pady=5)

        # 4. X Ekseni Gruplama İsimlendirme
        ctk.CTkLabel(self, text="X Ekseni Sütun İsimleri (Virgülle ayırarak örn: 1:A grubu, 2:B grubu):").pack(pady=(10, 0))
        self.entry_x_labels = ctk.CTkEntry(self, width=350)
        self.entry_x_labels.pack(pady=5)

        # 5. Parametreler
        ctk.CTkLabel(self, text="Sonlanım parametresi (cut):").pack(pady=(10, 0))
        self.entry_cut = ctk.CTkEntry(self, width=350)
        self.entry_cut.insert(0, "0") 
        self.entry_cut.pack(pady=5)

        ctk.CTkLabel(self, text="Grafiğin yumuşatma düzeyi (bw_adjust):").pack(pady=(10, 0))
        self.entry_bw = ctk.CTkEntry(self, width=350)
        self.entry_bw.insert(0, "0.5") 
        self.entry_bw.pack(pady=5)

        # 6. Çalıştır Butonu
        self.btn_plot = ctk.CTkButton(self, text="Grafiği Oluştur ve Kaydet", command=self.generate_plot)
        self.btn_plot.pack(pady=30)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Dosyaları", "*.xlsx *.xls")])
        if filename:
            self.entry_path.delete(0, 'end')
            self.entry_path.insert(0, filename)

    def generate_plot(self):
        # Girdileri al ve temizle
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
                messagebox.showerror("Hata", f"Sütun isimleri bulunamadı!\nMevcut sütunlar: {list(df.columns)}")
                return

            # Grafiği oluştur
            plt.figure(figsize=(10, 6))
            ax = sns.violinplot(data=df, x=x_col, y=y_col, cut=cut_val, bw_adjust=bw_val)
            
            # Başlık ayarı
            if title_val:
                plt.title(title_val)
            else:
                plt.title(f"{y_col} ve {x_col} Keman Grafiği")

            # X Ekseni İsimlendirme (Eğer kullanıcı veri girdiyse)
            if x_labels_input:
                try:
                    # '1:A, 2:B' formatını parse et (Virgül ile ayırıyoruz)
                    mapping = {}
                    # Kullanıcı virgülle ayırırsa
                    pairs = x_labels_input.split(',')
                    for pair in pairs:
                        if ':' in pair:
                            key, val = pair.split(':')
                            # strip() ile hem key'in hem value'nun etrafındaki boşlukları temizliyoruz
                            mapping[key.strip()] = val.strip()
                    
                    # Mevcut X etiketlerini al ve eşleşenleri değiştir
                    current_labels = [label.get_text() for label in ax.get_xticklabels()]
                    new_labels = [mapping.get(label, label) for label in current_labels]
                    ax.set_xticklabels(new_labels)
                except Exception as e:
                    messagebox.showwarning("Uyarı", f"Etiketleme yapılamadı, formatı kontrol edin (Hata: {e})")
                    
                    # Mevcut X etiketlerini al ve eşleşenleri değiştir
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
    app = ViolinPlotApp()
    app.mainloop()
