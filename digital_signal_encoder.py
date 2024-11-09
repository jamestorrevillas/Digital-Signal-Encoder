import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class DigitalSignalEncoder:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signal Encoder")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Maximize window
        self.root.state('zoomed')

        # Configure root grid
        root.grid_rowconfigure(0, weight=0)
        root.grid_rowconfigure(1, weight=0)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Create header frame with white background
        header_frame = ttk.Frame(root, style='Header.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)

        # Style configuration
        style = ttk.Style()
        style.configure('Header.TFrame', background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 11), wraplength=800)
        style.configure('Data.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Error.TLabel', font=('Arial', 12, 'bold'), foreground='red')

        # Button styles
        style.configure('Generate.TButton', font=('Arial', 11))
        style.configure('Clear.TButton', font=('Arial', 11))

        # Title and instruction
        title_frame = ttk.Frame(header_frame, style='Header.TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(10, 0))

        ttk.Label(title_frame, text="Digital Signal Encoder",
                  style='Title.TLabel').grid(row=0, column=0, sticky="w")

        ttk.Label(title_frame,
                  text="This application demonstrates various digital signal encoding techniques used in data communication.",
                  style='Info.TLabel').grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Input section
        input_frame = ttk.Frame(header_frame, style='Header.TFrame')
        input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=5)

        ttk.Label(input_frame, text="Enter binary data:",
                  style='Header.TLabel').grid(row=0, column=0, pady=5, padx=(0, 10))

        self.data_entry = ttk.Entry(input_frame, font=('Arial', 12), width=50)
        self.data_entry.grid(row=0, column=1, pady=5, sticky="ew")

        # Button frame for Generate, Clear buttons and Previous Level dropdown
        button_frame = ttk.Frame(input_frame, style='Header.TFrame')
        button_frame.grid(row=0, column=2, pady=5, padx=(10, 0))

        # Previous Level dropdown
        ttk.Label(button_frame, text="Initial Signal Level:",
                  style='Header.TLabel').grid(row=0, column=0, padx=(0, 5))
        self.initial_level_var = tk.StringVar(value="High")
        self.initial_level = ttk.Combobox(button_frame,
                                          textvariable=self.initial_level_var,
                                          values=["High", "Low"],
                                          state="readonly",
                                          width=10)
        self.initial_level.grid(row=0, column=1, padx=(0, 10))

        generate_btn = ttk.Button(button_frame, text="Generate All Signals",
                                  command=self.generate_all_signals,
                                  style='Generate.TButton')
        generate_btn.grid(row=0, column=2, padx=(0, 5))

        clear_btn = ttk.Button(button_frame, text="Clear",
                               command=self.clear_all,
                               style='Clear.TButton')
        clear_btn.grid(row=0, column=3)

        # Instructions
        instructions = (
            "Instructions:\n"
            "1. Enter a sequence of binary digits (0s and 1s) in the input field above\n"
            "2. Select Initial Signal Level (High or Low) to set the signal level before the first bit\n"
            "3. Click 'Generate All Signals' to see the encoding results\n"
            "4. Each plot shows a different encoding technique used in digital communication"
        )
        ttk.Label(input_frame, text=instructions,
                  style='Info.TLabel').grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 5))

        # Separator
        ttk.Separator(root, orient='horizontal').grid(row=1, column=0, sticky="ew")

        # Input data display frame with default message
        self.data_display = ttk.Label(root,
                                      text="Please enter binary data (0s and 1s)",
                                      style='Data.TLabel')
        self.data_display.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 0))

        # Calculate figure size based on screen dimensions
        fig_width = screen_width / 100
        fig_height = (screen_height - 150) / 100

        # Plot frame with adjusted size
        self.fig, self.axs = plt.subplots(3, 2, figsize=(fig_width, fig_height))
        self.axs = self.axs.flatten()

        # Adjust the subplot parameters
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.3, wspace=0.2)

        # Initialize plots with titles
        self.encodings = {
            'NRZ-L': (self.nrz_l, "NRZ-L (Non-Return to Zero Level)"),
            'NRZ-I': (self.nrz_i, "NRZ-I (Non-Return to Zero Inverted)"),
            'Bipolar AMI': (self.bipolar_ami, "Bipolar AMI (Alternate Mark Inversion)"),
            'Pseudoternary': (self.pseudoternary, "Pseudoternary"),
            'Manchester': (self.manchester, "Manchester"),
            'Differential Manchester': (self.differential_manchester, "Differential Manchester")
        }

        # Initialize empty plots with titles and grid
        self.initialize_plots()

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def initialize_plots(self):
        # Set up empty plots with default grid and labels
        for ax, (_, (_, title)) in zip(self.axs, self.encodings.items()):
            ax.clear()
            ax.set_title(title, pad=10, fontsize=12)
            ax.grid(True)
            ax.set_ylabel('Signal')
            ax.set_ylim(-1.5, 1.5)
            ax.set_xticks([])
            self.canvas.draw() if hasattr(self, 'canvas') else None

    def clear_all(self):
        # Reset application to initial state (clear input and plots)
        self.data_entry.delete(0, tk.END)
        self.data_display.config(
            text="Please enter binary data (0s and 1s)",
            style='Data.TLabel'
        )
        self.initialize_plots()
        self.canvas.draw()

    def on_closing(self):
        # Handle window closing event and cleanup
        plt.close('all')
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def get_previous_level(self):
        # Get the level before first bit
        return 1 if self.initial_level_var.get() == "High" else -1

    def nrz_l(self, data):
        # 0 = low (0), 1 = high (1)
        signal = [1 if bit == '1' else 0 for bit in data]
        signal.append(signal[-1])
        return signal

    def nrz_i(self, data):
        # 0 = no transition, 1 = transition at beginning of interval
        prev_level = 1 if self.initial_level_var.get() == "High" else 0
        current_level = prev_level
        signal = []

        for bit in data:
            if bit == '1':
                current_level = 0 if current_level == 1 else 1
            signal.append(current_level)
        signal.append(signal[-1])
        return signal

    def bipolar_ami(self, data):
        # 0 = no line signal (0), 1 = alternating +1/-1 starting opposite to previous level
        signal = []
        prev_level = self.get_previous_level()
        last_one = -prev_level

        for bit in data:
            if bit == '1':
                signal.append(last_one)
                last_one *= -1
            else:
                signal.append(0)
        signal.append(signal[-1])
        return signal

    def pseudoternary(self, data):
        # 0 = alternating +1/-1 starting opposite to previous level, 1 = no line signal (0)
        signal = []
        prev_level = self.get_previous_level()
        last_zero = -prev_level

        for bit in data:
            if bit == '0':
                signal.append(last_zero)
                last_zero *= -1
            else:
                signal.append(0)
        signal.append(signal[-1])
        return signal

    def manchester(self, data):
        # 0 = high to low, 1 = low to high at center of interval
        signal = []
        t = []
        i = 0

        for bit in data:
            if bit == '1':
                # Low to high transition at center
                signal.extend([0, 0, 1, 1])
            else:
                # High to low transition at center
                signal.extend([1, 1, 0, 0])
            t.extend([i, i + 0.5, i + 0.5, i + 1])
            i += 1
        return np.array(t), np.array(signal)

    def differential_manchester(self, data):
        # Always transition at center, 0 = transition at start, 1 = no transition at start
        signal = []
        t = []
        i = 0
        prev_level = 1 if self.initial_level_var.get() == "High" else 0
        last_level = prev_level

        for bit in data:
            if bit == '0':
                # Transition at start and center
                last_level = 1 if last_level == 0 else 0
                signal.extend([last_level, last_level])
                last_level = 1 if last_level == 0 else 0
                signal.extend([last_level, last_level])
            else:
                # No transition at start, only at center
                signal.extend([last_level, last_level])
                last_level = 1 if last_level == 0 else 0
                signal.extend([last_level, last_level])
            t.extend([i, i + 0.5, i + 0.5, i + 1])
            i += 1
        return np.array(t), np.array(signal)

    def plot_signal(self, ax, signal, data, title, encoding_type):
        ax.clear()
        if encoding_type in ['Manchester', 'Differential Manchester']:
            t, s = signal
            ax.plot(t, s, color='#1f77b4', linewidth=2)
            ax.set_xlim(-0.1, len(data))
        else:
            t = np.arange(len(signal))
            ax.step(t, signal, where='post', color='#1f77b4', linewidth=2)
            ax.set_xlim(-0.1, len(data))

        bit_positions = np.arange(len(data))
        ax.set_xticks(bit_positions)
        ax.set_xticklabels(list(data))

        ax.grid(True)
        ax.set_ylabel('Signal')
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(title, pad=10, fontsize=12)

    def generate_all_signals(self):
        data = self.data_entry.get().strip()

        # Check if input is empty
        if not data:
            self.data_display.config(
                text="⚠ Error: No input data! Please enter binary data (0s and 1s)",
                style='Error.TLabel'
            )
            return

        # Check if input contains only 0s and 1s
        if not all(bit in '01' for bit in data):
            self.data_display.config(
                text="⚠ Error: Invalid input! Please enter only 0s and 1s",
                style='Error.TLabel'
            )
            return

        # Valid input - update display and generate signals
        self.data_display.config(
            text=f"Input Digital Data: {data}",
            style='Data.TLabel'
        )

        for (ax, (encoding_type, (encode_func, title))) in zip(self.axs, self.encodings.items()):
            signal = encode_func(data)
            self.plot_signal(ax, signal, data, title, encoding_type)

        self.fig.tight_layout()
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = DigitalSignalEncoder(root)
    root.mainloop()


if __name__ == "__main__":
    main()