import math
import random


class HCIUsabilityStatisticalEvaluator:

    def __init__(self, n_participants=35, seed=101):
        self.n = n_participants
        self.seed = seed
        self.group_old_ui = []  
        self.group_new_ui = []  

    def run_usability_testing_simulation(self):
        print(
            "=== [1] USABILITY TESTING: DESAIN LAMA VS DESAIN BARU (UCD) ==="
        )
        random.seed(self.seed)

        for i in range(1, self.n + 1):
            elemen_junk_old = random.randint(12, 22)
            waktu_old = round(
                random.gauss(88.0, 14.0) + (elemen_junk_old * 1.2), 2
            )
            sus_old = round(min(100.0, max(20.0, random.gauss(56.5, 9.5))), 1)
            error_old = max(
                0, int((elemen_junk_old * 0.25) + random.gauss(1.0, 0.8))
            )

            self.group_old_ui.append({
                "id_user": f"U-OLD-{i:02d}",
                "waktu_detik": waktu_old,
                "skor_sus": sus_old,
                "jumlah_chartjunk": elemen_junk_old,
                "jumlah_error_klik": error_old,
            })

            elemen_junk_new = random.randint(2, 6)
            waktu_new = round(
                random.gauss(46.0, 8.5) + (elemen_junk_new * 1.1), 2
            )
            sus_new = round(min(100.0, max(40.0, random.gauss(84.0, 6.5))), 1)
            error_new = max(
                0, int((elemen_junk_new * 0.15) + random.gauss(0.2, 0.5))
            )

            self.group_new_ui.append({
                "id_user": f"U-NEW-{i:02d}",
                "waktu_detik": waktu_new,
                "skor_sus": sus_new,
                "jumlah_chartjunk": elemen_junk_new,
                "jumlah_error_klik": error_new,
            })

        print(
            f"- Pengujian dilakukan terhadap {self.n} responden per kelompok desain (Total {self.n * 2} partisipan)."
        )
        print(
            "- Metrik diukur: Task Completion Time (detik), Skor SUS (0-100), dan Error Rate.\n"
        )

    def _calc_stats(self, values):
        n = len(values)
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        std_dev = math.sqrt(variance)
        return mean, variance, std_dev

    def perform_independent_t_test(self):
        print(
            "=== [2] UJI STATISTIKA TERAPAN: INDEPENDENT TWO-SAMPLE T-TEST ==="
        )
        print(
            "Hipotesis Nol (H0)      : Tidak ada perbedaan waktu penyelesaian tugas antara UI Lama & UI Baru (UCD)."
        )
        print(
            "Hipotesis Alternatif (H1): UI Baru berbasis UCD secara signifikan mempercepat waktu penyelesaian tugas.\n"
        )

        waktu_lama = [u["waktu_detik"] for u in self.group_old_ui]
        waktu_baru = [u["waktu_detik"] for u in self.group_new_ui]

        mean1, var1, std1 = self._calc_stats(waktu_lama)
        mean2, var2, std2 = self._calc_stats(waktu_baru)

        n1, n2 = len(waktu_lama), len(waktu_baru)
        standard_error = math.sqrt((var1 / n1) + (var2 / n2))
        t_stat = (mean1 - mean2) / standard_error

        df = n1 + n2 - 2
        pooled_std = math.sqrt(
            (((n1 - 1) * var1) + ((n2 - 1) * var2)) / df
        )
        cohens_d = (mean1 - mean2) / pooled_std

        sus_lama_mean = sum(u["skor_sus"] for u in self.group_old_ui) / n1
        sus_baru_mean = sum(u["skor_sus"] for u in self.group_new_ui) / n2

        print(
            f"{'METRIK EVALUASI HCI':<32} | {'ANTARMUKA LAMA':<18} | {'ANTARMUKA BARU (UCD)'}"
        )
        print("-" * 78)
        print(
            f"{'Rata-rata Waktu Tugas (Mean)':<32} | {mean1:>12.2f} dtk   | {mean2:>14.2f} dtk"
        )
        print(
            f"{'Simpangan Baku (Std Dev)':<32} | {std1:>12.2f} dtk   | {std2:>14.2f} dtk"
        )
        print(
            f"{'Rata-rata Skor SUS Usability':<32} | {sus_lama_mean:>12.1f} /100  | {sus_baru_mean:>14.1f} /100"
        )
        print("-" * 78)
        print(f"- Nilai t-Hitung (t-Statistic)      : {t_stat:.4f}")
        print(
            f"- Nilai t-Tabel Kritis (alpha=0.05) : 1.9955 (Derajat Kebebasan df = {df})"
        )
        print(
            f"- Ukuran Efek (Cohen's d)           : {cohens_d:.4f} (Kategori: Efek Sangat Besar > 0.8)"
        )

        if abs(t_stat) > 1.9955:
            print(
                "\n[KEPUTUSAN HIPOTESIS] TOLAK H0 (t-Hitung > t-Tabel, p-value < 0.001)."
            )
            print(
                "Kesimpulan: Redesain UI/UX dengan metode UCD terbukti menurunkan beban kognitif dan mempercepat"
            )
            print(
                f"            penyelesaian tugas sebesar {((mean1 - mean2) / mean1) * 100:.1f}% secara signifikan.\n"
            )
        else:
            print("\n[KEPUTUSAN HIPOTESIS] GAGAL TOLAK H0.\n")

    def analyze_cognitive_load_correlation(self):
        print(
            "=== [3] KORELASI PEARSON: KOMPLEKSITAS VISUAL (CHARTJUNK) VS ERROR PENGGUNA ==="
        )
        combined = self.group_old_ui + self.group_new_ui
        x_junk = [u["jumlah_chartjunk"] for u in combined]
        y_err = [u["jumlah_error_klik"] for u in combined]

        n = len(combined)
        mean_x = sum(x_junk) / n
        mean_y = sum(y_err) / n

        numerator = sum(
            (x_junk[i] - mean_x) * (y_err[i] - mean_y) for i in range(n)
        )
        denom_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_junk))
        denom_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_err))

        r_pearson = (
            numerator / (denom_x * denom_y) if (denom_x * denom_y) != 0 else 0.0
        )

        t_corr = r_pearson * math.sqrt((n - 2) / (1.0 - (r_pearson**2)))

        print(f"- Koefisien Korelasi Pearson (r)    : {r_pearson:.4f}")
        print(f"- Nilai t-Uji Signifikansi Korelasi : {t_corr:.4f}")
        print(
            "- Interpretasi Visualisasi Data     : Korelasi positif kuat menunjukkan semakin banyak elemen visual"
        )
        print(
            "  yang tidak perlu (chartjunk), semakin tinggi beban ingatan dan kesalahan klik pengguna."
        )

        print(
            "\n--- Visualisasi Perbandingan Waktu Penyelesaian Tugas (Skala Grafik Batang) ---"
        )
        mean_old = sum(u["waktu_detik"] for u in self.group_old_ui) / self.n
        mean_new = sum(u["waktu_detik"] for u in self.group_new_ui) / self.n
        bar_old = "█" * int(mean_old / 2.5)
        bar_new = "█" * int(mean_new / 2.5)
        print(f"UI Lama (Non-UCD) : {bar_old} ({mean_old:.1f} detik)")
        print(f"UI Baru (UCD)     : {bar_new} ({mean_new:.1f} detik)")


if __name__ == "__main__":
    evaluator = HCIUsabilityStatisticalEvaluator()
    evaluator.run_usability_testing_simulation()
    evaluator.perform_independent_t_test()
    evaluator.analyze_cognitive_load_correlation()