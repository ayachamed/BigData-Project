"""
YouTube Gaza Data Collection - Complete GUI Application
Includes pipeline execution, progress tracking, and image gallery
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import threading
import time
import os
import sys
import glob

# Palestinian flag colors
COLORS = {
    'bg': '#FFFFFF',
    'fg': '#1A1A1A',
    'primary': '#00732F',
    'secondary': '#CE1126',
    'accent': '#2C2C2C',
    'border': '#E0E0E0',
    'input_bg': '#F8F8F8',
}


class PipelineExecutor:
    """Executes the data collection pipeline in separate thread."""
    
    def __init__(self, config, progress_callback, complete_callback):
        self.config = config
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        
    def run(self):
        """Run the complete pipeline."""
        try:
            # Stage 1: Data Collection
            self.progress_callback("Initializing...", 0)
            time.sleep(0.5)
            
            self.progress_callback("Collecting videos...", 10)
            success = self.run_collector()
            if not success:
                self.complete_callback(False, "Collection failed")
                return
            
            # Stage 2: Analysis
            self.progress_callback("Analyzing data with PySpark...", 40)
            success = self.run_analyzer()
            if not success:
                self.complete_callback(False, "Analysis failed")
                return
            
            # Stage 3: Visualization
            self.progress_callback("Creating visualizations...", 70)
            success = self.run_visualizer()
            if not success:
                self.complete_callback(False, "Visualization failed")
                return
            
            self.progress_callback("Complete!", 100)
            time.sleep(0.5)
            self.complete_callback(True, "Pipeline completed successfully!")
            
        except Exception as e:
            self.complete_callback(False, f"Error: {str(e)}")
    
    def run_collector(self):
        """Execute data collector."""
        try:
            from data_collector import YouTubeCollector, collect_videos_split_window
            import config as api_config
            
            collector = YouTubeCollector(api_config.API_KEY)
            all_videos = []
            
            queries = self.config['queries']
            start_iso = f"{self.config['start_date']}T00:00:00Z"
            end_iso = f"{self.config['end_date']}T23:59:59Z"
            
            for i, query in enumerate(queries):
                progress = 10 + (i / len(queries)) * 25
                self.progress_callback(f"Collecting: {query[:30]}...", progress)
                
                videos = collect_videos_split_window(
                    collector, query, target=self.config['videos_per_query']
                )
                
                for video in videos:
                    video['comments'] = collector.get_comments(video['videoId'], max_comments=30)
                    video['commentsCount'] = len(video['comments'])
                    all_videos.append(video)
                    time.sleep(0.3)
            
            collector.save_to_files(all_videos, output_dir="data")
            return True
            
        except Exception as e:
            print(f"Collector error: {e}")
            return False
    
    def run_analyzer(self):
        """Execute PySpark analyzer."""
        try:
            import subprocess
            result = subprocess.run(
                ['python3', 'src/data_analyzer.py'],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Analyzer error: {e}")
            return False
    
    def run_visualizer(self):
        """Execute visualizer."""
        try:
            import subprocess
            result = subprocess.run(
                ['python3', 'src/data_visualizer.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Visualizer error: {e}")
            return False


class ImageGallery(tk.Frame):
    """Image gallery viewer for browsing generated charts."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg'], **kwargs)
        self.images = []
        self.current_index = 0
        self.create_widgets()
        
    def create_widgets(self):
        """Build gallery UI."""
        # Title
        title = tk.Label(
            self,
            text="Generated Charts",
            font=('Arial', 16, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg']
        )
        title.pack(pady=20)
        
        # Image display area
        self.image_frame = tk.Frame(self, bg=COLORS['bg'], relief='solid', borderwidth=2)
        self.image_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.image_label = tk.Label(self.image_frame, bg=COLORS['bg'])
        self.image_label.pack(expand=True)
        
        # Image counter
        self.counter_label = tk.Label(
            self,
            text="No images",
            font=('Arial', 10),
            fg='#666666',
            bg=COLORS['bg']
        )
        self.counter_label.pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self, bg=COLORS['bg'])
        nav_frame.pack(pady=15)
        
        self.prev_btn = tk.Button(
            nav_frame,
            text="◀ Previous",
            font=('Arial', 11),
            bg=COLORS['primary'],
            fg=COLORS['bg'],
            activebackground='#005A25',
            relief='flat',
            padx=20,
            pady=10,
            command=self.prev_image,
            state='disabled'
        )
        self.prev_btn.pack(side='left', padx=10)
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Next ▶",
            font=('Arial', 11),
            bg=COLORS['primary'],
            fg=COLORS['bg'],
            activebackground='#005A25',
            relief='flat',
            padx=20,
            pady=10,
            command=self.next_image,
            state='disabled'
        )
        self.next_btn.pack(side='left', padx=10)
        
    def load_images(self):
        """Load all images from outputs directory."""
        image_files = glob.glob('outputs/*.png')
        image_files.sort()
        
        self.images = []
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                # Resize to fit
                img.thumbnail((700, 500), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.images.append({
                    'path': img_path,
                    'photo': photo,
                    'name': os.path.basename(img_path)
                })
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
        
        if self.images:
            self.current_index = 0
            self.show_current_image()
            self.prev_btn.config(state='normal')
            self.next_btn.config(state='normal')
        
    def show_current_image(self):
        """Display current image."""
        if not self.images:
            return
        
        img_data = self.images[self.current_index]
        self.image_label.config(image=img_data['photo'])
        self.counter_label.config(
            text=f"{self.current_index + 1} of {len(self.images)} - {img_data['name']}"
        )
        
    def prev_image(self):
        """Show previous image."""
        if self.images and self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()
            
    def next_image(self):
        """Show next image."""
        if self.images and self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_current_image()


class YouTubeDataCollectorGUI:
    """Complete GUI application with pipeline execution and gallery."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Gaza Data Collector - Complete")
        self.root.geometry("800x700")
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(False, False)
        
        # State
        self.current_view = 'config'  # 'config' or 'gallery'
        
        # Main container
        self.container = tk.Frame(root, bg=COLORS['bg'])
        self.container.pack(fill='both', expand=True)
        
        # Create views
        self.create_config_view()
        self.create_progress_view()
        self.create_gallery_view()
        
        # Show config initially
        self.show_view('config')
        
    def create_config_view(self):
        """Create configuration input view."""
        self.config_frame = tk.Frame(self.container, bg=COLORS['bg'])
        
        # Header
        header = tk.Frame(self.config_frame, bg=COLORS['primary'], height=80)
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
        
        # Main form
        main_frame = tk.Frame(self.config_frame, bg=COLORS['bg'], padx=40, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Queries
        self.create_section_header(main_frame, "Search Queries", row=0)
        tk.Label(
            main_frame,
            text="Enter exactly 5 queries in English, separated by commas",
            font=('Arial', 9, 'italic'),
            fg='#666666',
            bg=COLORS['bg']
        ).grid(row=1, column=0, sticky='w', pady=(0, 5))
        
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
        
        # Date range
        self.create_section_header(main_frame, "Time Period", row=3)
        date_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        date_frame.grid(row=4, column=0, sticky='ew', pady=(5, 20))
        
        tk.Label(date_frame, text="Start:", font=('Arial', 10), bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.start_date_picker = DateEntry(date_frame, width=15, background=COLORS['primary'], foreground=COLORS['bg'], borderwidth=2, year=2023, month=10, day=6, mindate=datetime(2023, 10, 1), maxdate=datetime(2025, 10, 31), date_pattern='yyyy-mm-dd')
        self.start_date_picker.grid(row=0, column=1, padx=(0, 30))
        
        tk.Label(date_frame, text="End:", font=('Arial', 10), bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.end_date_picker = DateEntry(date_frame, width=15, background=COLORS['primary'], foreground=COLORS['bg'], borderwidth=2, year=2025, month=10, day=11, mindate=datetime(2023, 10, 1), maxdate=datetime(2025, 10, 31), date_pattern='yyyy-mm-dd')
        self.end_date_picker.grid(row=0, column=3)
        
        # Videos per query
        self.create_section_header(main_frame, "Videos per Query", row=5)
        video_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        video_frame.grid(row=6, column=0, sticky='w', pady=(5, 30))
        
        tk.Label(video_frame, text="Number of videos:", font=('Arial', 10), bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.videos_per_query_var = tk.IntVar(value=100)
        self.video_spinbox = tk.Spinbox(video_frame, from_=10, to=100, textvariable=self.videos_per_query_var, width=10, font=('Arial', 10), bg=COLORS['input_bg'], fg=COLORS['fg'])
        self.video_spinbox.grid(row=0, column=1)
        tk.Label(video_frame, text="(Max: 100)", font=('Arial', 9, 'italic'), fg='#666666', bg=COLORS['bg']).grid(row=0, column=2, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.grid(row=7, column=0, sticky='ew')
        
        self.start_button = tk.Button(
            button_frame,
            text="Start Processing",
            font=('Arial', 12, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['bg'],
            activebackground='#005A25',
            relief='flat',
            padx=30,
            pady=12,
            command=self.start_pipeline
        )
        self.start_button.pack(fill='x', pady=(0, 10))
        
        tk.Button(
            button_frame,
            text="Exit",
            font=('Arial', 11),
            bg='#CCCCCC',
            fg=COLORS['fg'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.root.quit
        ).pack(fill='x')
        
        main_frame.columnconfigure(0, weight=1)
        
    def create_progress_view(self):
        """Create progress display view."""
        self.progress_frame = tk.Frame(self.container, bg=COLORS['bg'])
        
        # Center content
        center = tk.Frame(self.progress_frame, bg=COLORS['bg'])
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(
            center,
            text="Processing Pipeline",
            font=('Arial', 18, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg']
        ).pack(pady=(0, 20))
        
        self.progress_label = tk.Label(
            center,
            text="Initializing...",
            font=('Arial', 12),
            fg=COLORS['fg'],
            bg=COLORS['bg']
        )
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(
            center,
            length=400,
            mode='determinate',
            style='Palestinian.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=20)
        
        self.progress_percent = tk.Label(
            center,
            text="0%",
            font=('Arial', 14, 'bold'),
            fg=COLORS['primary'],
            bg=COLORS['bg']
        )
        self.progress_percent.pack()
        
        # Style the progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Palestinian.Horizontal.TProgressbar',
            troughcolor=COLORS['input_bg'],
            background=COLORS['primary'],
            thickness=25
        )
        
    def create_gallery_view(self):
        """Create image gallery view."""
        self.gallery_frame = tk.Frame(self.container, bg=COLORS['bg'])
        
        # Header
        header = tk.Frame(self.gallery_frame, bg=COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Results Gallery",
            font=('Arial', 18, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['bg']
        ).pack(pady=20)
        
        # Gallery
        self.gallery = ImageGallery(self.gallery_frame)
        self.gallery.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Back button
        tk.Button(
            self.gallery_frame,
            text="← Back to Start",
            font=('Arial', 11),
            bg='#CCCCCC',
            fg=COLORS['fg'],
            relief='flat',
            padx=30,
            pady=10,
            command=lambda: self.show_view('config')
        ).pack(pady=10)
        
    def create_section_header(self, parent, text, row):
        """Create styled section header."""
        tk.Label(
            parent,
            text=text,
            font=('Arial', 11, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg']
        ).grid(row=row, column=0, sticky='w', pady=(0, 5))
        
    def show_view(self, view_name):
        """Switch between views."""
        # Hide all
        self.config_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.gallery_frame.pack_forget()
        
        # Show requested
        if view_name == 'config':
            self.config_frame.pack(fill='both', expand=True)
        elif view_name == 'progress':
            self.progress_frame.pack(fill='both', expand=True)
        elif view_name == 'gallery':
            self.gallery_frame.pack(fill='both', expand=True)
            
        self.current_view = view_name
        
    def validate_inputs(self):
        """Validate all inputs."""
        # Queries
        queries_text = self.query_entry.get('1.0', 'end-1c').strip()
        queries = [q.strip() for q in queries_text.split(',')]
        
        if len(queries) != 5:
            messagebox.showerror("Invalid Input", f"Expected 5 queries, found {len(queries)}")
            return None
        
        if any(not q for q in queries):
            messagebox.showerror("Invalid Input", "All queries must be non-empty")
            return None
        
        # Dates
        start = self.start_date_picker.get_date()
        end = self.end_date_picker.get_date()
        
        if start >= end:
            messagebox.showerror("Invalid Input", "Start date must be before end date")
            return None
        
        # Video count
        try:
            count = self.videos_per_query_var.get()
            if count < 1 or count > 100:
                messagebox.showerror("Invalid Input", "Video count must be 1-100")
                return None
        except:
            messagebox.showerror("Invalid Input", "Invalid video count")
            return None
        
        return {
            'queries': queries,
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d'),
            'videos_per_query': count
        }
        
    def start_pipeline(self):
        """Validate and start pipeline execution."""
        config = self.validate_inputs()
        if not config:
            return
        
        # Confirm
        confirm = messagebox.askyesno(
            "Start Processing",
            f"Ready to process:\n\n"
            f"• {len(config['queries'])} queries\n"
            f"• {config['start_date']} to {config['end_date']}\n"
            f"• {config['videos_per_query']} videos per query\n"
            f"• Target: {len(config['queries']) * config['videos_per_query']} videos\n\n"
            f"This may take several minutes. Continue?"
        )
        
        if not confirm:
            return
        
        # Show progress view
        self.show_view('progress')
        self.progress_bar['value'] = 0
        
        # Run pipeline in thread
        executor = PipelineExecutor(
            config,
            self.update_progress,
            self.pipeline_complete
        )
        
        thread = threading.Thread(target=executor.run, daemon=True)
        thread.start()
        
    def update_progress(self, message, percent):
        """Update progress display (thread-safe)."""
        self.root.after(0, lambda: self._update_progress_ui(message, percent))
        
    def _update_progress_ui(self, message, percent):
        """Update progress UI elements."""
        self.progress_label.config(text=message)
        self.progress_bar['value'] = percent
        self.progress_percent.config(text=f"{int(percent)}%")
        
    def pipeline_complete(self, success, message):
        """Handle pipeline completion (thread-safe)."""
        self.root.after(0, lambda: self._show_completion(success, message))
        
    def _show_completion(self, success, message):
        """Show completion and switch to gallery."""
        if success:
            messagebox.showinfo("Success", message)
            self.gallery.load_images()
            self.show_view('gallery')
        else:
            messagebox.showerror("Error", message)
            self.show_view('config')


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = YouTubeDataCollectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
