"""
YouTube Gaza Data Collection - GUI Interface
Color scheme: Palestinian Flag (Black, White, Green, Red)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import sys
import os

# Palestinian flag colors (professional/muted versions)
COLORS = {
    'bg': '#FFFFFF',           # White background
    'fg': '#1A1A1A',           # Almost black for text
    'primary': '#00732F',      # Palestinian green
    'secondary': '#CE1126',    # Palestinian red
    'accent': '#2C2C2C',       # Black accent
    'border': '#E0E0E0',       # Light gray borders
    'input_bg': '#F8F8F8',     # Very light gray for inputs
}


class YouTubeDataCollectorGUI:
    """Modern GUI for YouTube data collection configuration."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Gaza Data Collector")
        self.root.geometry("600x550")
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(False, False)
        
        # Variables
        self.queries_var = tk.StringVar()
        self.videos_per_query_var = tk.IntVar(value=100)
        self.start_date_var = tk.StringVar(value="2023-10-06")
        self.end_date_var = tk.StringVar(value="2025-10-11")
        
        self.create_widgets()
        
    def create_widgets(self):
        """Build the GUI layout."""
        
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="YouTube Data Collector",
            font=('Arial', 20, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['bg']
        )
        title.pack(pady=25)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg'], padx=40, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # === QUERY INPUT ===
        self.create_section_header(main_frame, "Search Queries", row=0)
        
        query_hint = tk.Label(
            main_frame,
            text="Enter exactly 5 queries in English, separated by commas",
            font=('Arial', 9, 'italic'),
            fg='#666666',
            bg=COLORS['bg']
        )
        query_hint.grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        self.query_entry = tk.Text(
            main_frame,
            height=3,
            font=('Arial', 10),
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            relief='solid',
            borderwidth=1,
            wrap='word'
        )
        self.query_entry.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        self.query_entry.insert('1.0', 'Gaza war, Israel Palestine conflict, Gaza humanitarian crisis, Palestine news, Israel Hamas war')
        
        # === DATE RANGE ===
        self.create_section_header(main_frame, "Time Period", row=3)
        
        date_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        date_frame.grid(row=4, column=0, sticky='ew', pady=(5, 20))
        
        # Start date
        tk.Label(
            date_frame,
            text="Start Date:",
            font=('Arial', 10),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.start_date_picker = DateEntry(
            date_frame,
            width=15,
            background=COLORS['primary'],
            foreground=COLORS['bg'],
            borderwidth=2,
            year=2023,
            month=10,
            day=6,
            mindate=datetime(2023, 10, 1),
            maxdate=datetime(2025, 10, 31),
            date_pattern='yyyy-mm-dd'
        )
        self.start_date_picker.grid(row=0, column=1, padx=(0, 30))
        
        # End date
        tk.Label(
            date_frame,
            text="End Date:",
            font=('Arial', 10),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        ).grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.end_date_picker = DateEntry(
            date_frame,
            width=15,
            background=COLORS['primary'],
            foreground=COLORS['bg'],
            borderwidth=2,
            year=2025,
            month=10,
            day=11,
            mindate=datetime(2023, 10, 1),
            maxdate=datetime(2025, 10, 31),
            date_pattern='yyyy-mm-dd'
        )
        self.end_date_picker.grid(row=0, column=3)
        
        # === VIDEOS PER QUERY ===
        self.create_section_header(main_frame, "Videos per Query", row=5)
        
        video_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        video_frame.grid(row=6, column=0, sticky='w', pady=(5, 30))
        
        tk.Label(
            video_frame,
            text="Number of videos:",
            font=('Arial', 10),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.video_spinbox = tk.Spinbox(
            video_frame,
            from_=10,
            to=100,
            textvariable=self.videos_per_query_var,
            width=10,
            font=('Arial', 10),
            bg=COLORS['input_bg'],
            fg=COLORS['fg'],
            buttonbackground=COLORS['primary']
        )
        self.video_spinbox.grid(row=0, column=1)
        
        tk.Label(
            video_frame,
            text="(Max: 100)",
            font=('Arial', 9, 'italic'),
            fg='#666666',
            bg=COLORS['bg']
        ).grid(row=0, column=2, padx=(10, 0))
        
        # === ACTION BUTTONS ===
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.grid(row=7, column=0, sticky='ew')
        
        self.start_button = tk.Button(
            button_frame,
            text="Start Collection",
            font=('Arial', 12, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['bg'],
            activebackground='#005A25',
            activeforeground=COLORS['bg'],
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=self.start_collection
        )
        self.start_button.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 12),
            bg='#CCCCCC',
            fg=COLORS['fg'],
            activebackground='#999999',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=self.root.quit
        )
        cancel_button.pack(side='right', expand=True, fill='x')
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        
    def create_section_header(self, parent, text, row):
        """Create a styled section header."""
        label = tk.Label(
            parent,
            text=text,
            font=('Arial', 11, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg']
        )
        label.grid(row=row, column=0, sticky='w', pady=(0, 5))
        
    def validate_queries(self, queries_text):
        """Validate query input."""
        queries = [q.strip() for q in queries_text.split(',')]
        
        # Check count
        if len(queries) != 5:
            return False, f"Expected exactly 5 queries, but found {len(queries)}"
        
        # Check non-empty
        if any(not q for q in queries):
            return False, "All queries must be non-empty"
        
        # Check English (basic check for ASCII)
        for q in queries:
            if not all(ord(c) < 128 or c.isspace() for c in q):
                return False, f"Queries must be in English only: '{q}'"
        
        return True, queries
    
    def validate_dates(self):
        """Validate date range."""
        start = self.start_date_picker.get_date()
        end = self.end_date_picker.get_date()
        
        # Check order
        if start >= end:
            return False, "Start date must be before end date"
        
        # Check range limits
        min_date = datetime(2023, 10, 1).date()
        max_date = datetime(2025, 10, 31).date()
        
        if start < min_date or end > max_date:
            return False, "Dates must be within October 2023 to October 2025"
        
        return True, (start, end)
    
    def validate_video_count(self):
        """Validate video count."""
        try:
            count = self.videos_per_query_var.get()
            if count < 1 or count > 100:
                return False, "Video count must be between 1 and 100"
            return True, count
        except:
            return False, "Invalid video count"
    
    def start_collection(self):
        """Validate all inputs and start data collection."""
        
        # Validate queries
        queries_text = self.query_entry.get('1.0', 'end-1c').strip()
        valid, result = self.validate_queries(queries_text)
        if not valid:
            messagebox.showerror("Invalid Queries", result)
            return
        queries = result
        
        # Validate dates
        valid, result = self.validate_dates()
        if not valid:
            messagebox.showerror("Invalid Date Range", result)
            return
        start_date, end_date = result
        
        # Validate video count
        valid, result = self.validate_video_count()
        if not valid:
            messagebox.showerror("Invalid Video Count", result)
            return
        video_count = result
        
        # Confirm
        confirm_msg = f"Ready to collect data:\n\n"
        confirm_msg += f"Queries: {len(queries)}\n"
        confirm_msg += f"Period: {start_date} to {end_date}\n"
        confirm_msg += f"Videos per query: {video_count}\n\n"
        confirm_msg += f"Total target: {len(queries) * video_count} videos\n\n"
        confirm_msg += "Start collection?"
        
        if not messagebox.askyesno("Confirm Collection", confirm_msg):
            return
        
        # Save configuration and close
        self.config = {
            'queries': queries,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'videos_per_query': video_count
        }
        
        messagebox.showinfo("Starting...", "Data collection will begin.\nPlease wait...")
        self.root.quit()
        

def launch_gui():
    """Launch the GUI and return configuration."""
    root = tk.Tk()
    app = YouTubeDataCollectorGUI(root)
    root.mainloop()
    
    # Return configuration if available
    if hasattr(app, 'config'):
        root.destroy()
        return app.config
    else:
        root.destroy()
        return None


if __name__ == "__main__":
    config = launch_gui()
    if config:
        print("\n=== Configuration ===")
        print(f"Queries: {config['queries']}")
        print(f"Date Range: {config['start_date']} to {config['end_date']}")
        print(f"Videos per query: {config['videos_per_query']}")
    else:
        print("Collection cancelled.")
