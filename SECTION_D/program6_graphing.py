"""
Program 6: Graphing Empirical Timing Results
Reads timing data from timing_results.csv (or generates it via Program 5)
and creates two plots using matplotlib:
1. Performance of all 6 algorithms on random input data.
2. Performance of all 6 algorithms on already-sorted input data.
Saves both plots as PNG files.
"""

import os
import csv
import matplotlib.pyplot as plt


def load_timing_data(csv_path="timing_results.csv"):
    """
    Loads timing data from CSV file into structured dictionary:
    data[input_type][algorithm] = [(n, time_sec), ...]
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file '{csv_path}' not found. Run Program 5 first.")

    data = {}
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            itype = row["Input_Type"]
            algo = row["Algorithm"]
            n = int(row["N"])
            time_ms = float(row["Time_MS"])

            if itype not in data:
                data[itype] = {}
            if algo not in data[itype]:
                data[itype][algo] = []
            data[itype][algo].append((n, time_ms))

    # Sort data points by n
    for itype in data:
        for algo in data[itype]:
            data[itype][algo].sort(key=lambda x: x[0])

    return data


def plot_and_save(data, input_type, title, filename, output_dir):
    """
    Plots timing curves for all algorithms for a specific input type and saves to image.
    """
    plt.figure(figsize=(10, 6))
    
    # Styles and markers for distinct algorithm visualization
    styles = {
        "Bubble Sort": {"color": "#e74c3c", "marker": "o", "linestyle": "-"},
        "Selection Sort": {"color": "#e67e22", "marker": "s", "linestyle": "--"},
        "Insertion Sort": {"color": "#f39c12", "marker": "^", "linestyle": "-."},
        "Merge Sort": {"color": "#2ecc71", "marker": "D", "linestyle": "-"},
        "Quick Sort": {"color": "#9b59b6", "marker": "v", "linestyle": "--"},
        "Heap Sort": {"color": "#3498db", "marker": "P", "linestyle": "-."},
    }

    type_data = data.get(input_type, {})
    for algo, pts in type_data.items():
        xs = [pt[0] for pt in pts]
        ys = [pt[1] for pt in pts]
        style = styles.get(algo, {"marker": "o"})
        plt.plot(xs, ys, label=algo, linewidth=2, markersize=7, **style)

    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Input Size (n)", fontsize=12)
    plt.ylabel("Execution Time (milliseconds)", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(fontsize=10, loc="upper left")
    plt.tight_layout()

    out_path = os.path.join(output_dir, filename)
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Plot saved: {out_path}")
    return out_path


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "timing_results.csv")

    # If CSV doesn't exist, generate it
    if not os.path.exists(csv_path):
        print("[INFO] timing_results.csv not found. Running Program 5 benchmark...")
        from program5_sorting_comparison import run_benchmarks, save_results_csv
        results = run_benchmarks()
        save_results_csv(results, csv_path)

    data = load_timing_data(csv_path)

    # Plot 1: Random Input Data
    plot_and_save(
        data=data,
        input_type="random",
        title="Sorting Algorithm Comparison: Random Order Input",
        filename="timing_random.png",
        output_dir=script_dir,
    )

    # Plot 2: Already-Sorted Input Data
    plot_and_save(
        data=data,
        input_type="sorted",
        title="Sorting Algorithm Comparison: Already-Sorted Input",
        filename="timing_sorted.png",
        output_dir=script_dir,
    )


if __name__ == "__main__":
    main()