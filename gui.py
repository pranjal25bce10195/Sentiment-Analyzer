import tkinter as tk
from tkinter import ttk, scrolledtext
from logic import get_mood, Mood

class SentimentAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
        # Title
        title_label = tk.Label(
            root,
            text="💬 Sentiment Analysis Tool",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#333"
        )
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        input_label = tk.Label(
            input_frame,
            text="Enter your text:",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#555"
        )
        input_label.pack(anchor="w")
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            width=60,
            height=8,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.text_input.pack(pady=5, fill="both", expand=True)
        
        # Threshold slider
        threshold_frame = tk.Frame(root, bg=self.bg_color)
        threshold_frame.pack(pady=10, padx=20, fill="x")
        
        threshold_label = tk.Label(
            threshold_frame,
            text="Sensitivity Threshold:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#555"
        )
        threshold_label.pack(side="left")
        
        self.threshold_var = tk.DoubleVar(value=0.3)
        self.threshold_slider = ttk.Scale(
            threshold_frame,
            from_=0.1,
            to=0.9,
            orient="horizontal",
            variable=self.threshold_var,
            length=200
        )
        self.threshold_slider.pack(side="left", padx=10)
        
        self.threshold_value_label = tk.Label(
            threshold_frame,
            text="0.3",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#555"
        )
        self.threshold_value_label.pack(side="left")
        
        # Update threshold label
        self.threshold_slider.configure(command=self.update_threshold_label)
        
        # Analyze button
        analyze_btn = tk.Button(
            root,
            text="Analyze Sentiment",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10,
            command=self.analyze_sentiment
        )
        analyze_btn.pack(pady=15)
        
        # Result frame
        result_frame = tk.Frame(root, bg=self.bg_color)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        self.result_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 36),
            bg=self.bg_color
        )
        self.result_label.pack()
        
        self.sentiment_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#666"
        )
        self.sentiment_label.pack()
        
        # Bind Enter key to analyze
        self.root.bind('<Control-Return>', lambda e: self.analyze_sentiment())
        
    def update_threshold_label(self, value):
        self.threshold_value_label.config(text=f"{float(value):.2f}")
    
    def analyze_sentiment(self):
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            self.result_label.config(text="⚠️", fg="#ff9800")
            self.sentiment_label.config(text="Please enter some text!", fg="#ff9800")
            return
        
        threshold = self.threshold_var.get()
        mood = get_mood(text, threshold=threshold)
        
        # Display result
        self.result_label.config(text=mood.emoji)
        
        # Determine sentiment category
        if mood.sentiment >= threshold:
            category = "Positive"
            color = "#4CAF50"
        elif mood.sentiment <= -threshold:
            category = "Negative"
            color = "#f44336"
        else:
            category = "Neutral"
            color = "#757575"
        
        self.sentiment_label.config(
            text=f"{category} | Score: {mood.sentiment:.3f}",
            fg=color
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalyzerGUI(root)
    root.mainloop()
