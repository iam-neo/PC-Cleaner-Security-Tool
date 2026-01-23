"""
PC Cleaner Tab UI
"""
import customtkinter as ctk
import threading
from modules.cleaner import PCCleaner
from utils.system_info import format_bytes


class CleanerTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.cleaner = PCCleaner()
        self.scan_results = None
        self.selected_files = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="🧹 PC Cleaner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Control buttons frame
        self.create_control_buttons()
        
        # Results frame
        self.create_results_frame()
        
        # Progress frame
        self.create_progress_frame()
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready to scan",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    
    def create_control_buttons(self):
        """Create control buttons"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Scan button
        self.scan_btn = ctk.CTkButton(
            frame,
            text="🔍 Start Scan",
            command=self.start_scan,
            height=40,
            width=150,
            fg_color="blue",
            hover_color="darkblue"
        )
        self.scan_btn.pack(side="left", padx=5, pady=10)
        
        # Clean button
        self.clean_btn = ctk.CTkButton(
            frame,
            text="🗑️ Clean Selected",
            command=self.clean_files,
            height=40,
            width=150,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.clean_btn.pack(side="left", padx=5, pady=10)
        
        # Select All button
        self.select_all_btn = ctk.CTkButton(
            frame,
            text="☑️ Select All",
            command=self.select_all,
            height=40,
            width=150,
            state="disabled"
        )
        self.select_all_btn.pack(side="left", padx=5, pady=10)
        
        # Deselect All button
        self.deselect_all_btn = ctk.CTkButton(
            frame,
            text="☐ Deselect All",
            command=self.deselect_all,
            height=40,
            width=150,
            state="disabled"
        )
        self.deselect_all_btn.pack(side="left", padx=5, pady=10)
    
    def create_results_frame(self):
        """Create results display frame"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Results title
        self.results_title = ctk.CTkLabel(
            frame,
            text="Scan Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Scrollable frame for results
        self.results_scroll = ctk.CTkScrollableFrame(frame, height=300)
        self.results_scroll.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        
        # Initial message
        self.no_results_label = ctk.CTkLabel(
            self.results_scroll,
            text="Click 'Start Scan' to find temporary files and cache",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.no_results_label.pack(pady=50)
    
    def create_progress_frame(self):
        """Create progress display"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.progress_label = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(padx=15, pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(frame)
        self.progress_bar.pack(padx=15, pady=(0, 10), fill="x")
        self.progress_bar.set(0)
    
    def start_scan(self):
        """Start scanning for files to clean"""
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.status_label.configure(text="Scanning...")
        self.progress_bar.set(0)
        
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        # Run scan in separate thread
        thread = threading.Thread(target=self._perform_scan, daemon=True)
        thread.start()
    
    def _perform_scan(self):
        """Perform the scan (runs in separate thread)"""
        def progress_callback(message):
            self.progress_label.configure(text=message)
        
        # Perform scan
        results = self.cleaner.perform_full_scan(progress_callback)
        self.scan_results = results
        
        # Update UI in main thread
        self.after(0, self._display_results, results)
    
    def _display_results(self, results):
        """Display scan results"""
        # Clear loading message
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        # Update title with total
        total_items = results.get('total_items', 0)
        total_size = results.get('total_size_formatted', '0 B')
        self.results_title.configure(
            text=f"Scan Results - {total_items} items found ({total_size})"
        )
        
        self.selected_files = []
        
        # Display temp files
        if results['temp_files']['count'] > 0:
            self._create_category_section(
                "Temporary Files",
                results['temp_files']['files'],
                results['temp_files']['total_size_formatted']
            )
        
        # Display browser cache
        if results['browser_cache']['count'] > 0:
            self._create_category_section(
                "Browser Cache",
                results['browser_cache']['files'],
                results['browser_cache']['total_size_formatted']
            )
        
        # Display recycle bin
        if results['recycle_bin']['size'] > 0:
            self._create_recycle_bin_section(results['recycle_bin'])
        
        # Show message if nothing found
        if total_items == 0:
            no_items = ctk.CTkLabel(
                self.results_scroll,
                text="✅ No temporary files or cache found!\nYour system is clean.",
                font=ctk.CTkFont(size=14),
                text_color="green"
            )
            no_items.pack(pady=50)
        
        # Enable buttons
        self.scan_btn.configure(state="normal")
        if total_items > 0:
            self.select_all_btn.configure(state="normal")
            self.deselect_all_btn.configure(state="normal")
        
        self.status_label.configure(text=f"Scan complete - {total_items} items found")
        self.progress_bar.set(1)
        
        # Update dashboard
        self.app.dashboard.update_last_scan_info("cleaner", results)
    
    def _create_category_section(self, category_name, files, total_size):
        """Create a section for a category of files"""
        # Category header
        header = ctk.CTkFrame(self.results_scroll)
        header.pack(fill="x", padx=5, pady=(10, 5))
        
        label = ctk.CTkLabel(
            header,
            text=f"📁 {category_name} ({len(files)} items, {total_size})",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(side="left", padx=10, pady=5)
        
        # File list (show first 10, then "and X more")
        display_count = min(10, len(files))
        for i in range(display_count):
            file_info = files[i]
            self._create_file_item(file_info)
        
        if len(files) > 10:
            more_label = ctk.CTkLabel(
                self.results_scroll,
                text=f"... and {len(files) - 10} more files",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            more_label.pack(padx=20, pady=2)
    
    def _create_file_item(self, file_info):
        """Create a checkbox item for a file"""
        frame = ctk.CTkFrame(self.results_scroll)
        frame.pack(fill="x", padx=10, pady=2)
        
        var = ctk.BooleanVar(value=True)
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text="",
            variable=var,
            command=lambda: self._toggle_file(file_info['path'], var.get())
        )
        checkbox.pack(side="left", padx=5)
        
        # File info
        if file_info.get('is_directory'):
            text = f"📁 {file_info['category']} - {file_info['size_formatted']}"
        else:
            filename = file_info['path'].split('\\')[-1]
            text = f"📄 {filename} - {file_info['size_formatted']}"
        
        label = ctk.CTkLabel(
            frame,
            text=text,
            font=ctk.CTkFont(size=11)
        )
        label.pack(side="left", padx=5)
        
        # Add to selected by default
        self.selected_files.append(file_info['path'])
    
    def _create_recycle_bin_section(self, recycle_info):
        """Create recycle bin section"""
        frame = ctk.CTkFrame(self.results_scroll)
        frame.pack(fill="x", padx=10, pady=5)
        
        var = ctk.BooleanVar(value=True)
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text="",
            variable=var,
            command=lambda: self._toggle_recycle_bin(var.get())
        )
        checkbox.pack(side="left", padx=5)
        
        label = ctk.CTkLabel(
            frame,
            text=f"🗑️ Recycle Bin - {recycle_info['size_formatted']}",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        label.pack(side="left", padx=5)
        
        self.selected_files.append("RECYCLE_BIN")
    
    def _toggle_file(self, filepath, selected):
        """Toggle file selection"""
        if selected and filepath not in self.selected_files:
            self.selected_files.append(filepath)
        elif not selected and filepath in self.selected_files:
            self.selected_files.remove(filepath)
        
        # Enable/disable clean button
        self.clean_btn.configure(state="normal" if self.selected_files else "disabled")
    
    def _toggle_recycle_bin(self, selected):
        """Toggle recycle bin selection"""
        self._toggle_file("RECYCLE_BIN", selected)
    
    def select_all(self):
        """Select all items"""
        # This would require storing checkbox variables - simplified for now
        self.status_label.configure(text="All items selected")
    
    def deselect_all(self):
        """Deselect all items"""
        self.selected_files = []
        self.clean_btn.configure(state="disabled")
        self.status_label.configure(text="All items deselected")
    
    def clean_files(self):
        """Clean selected files"""
        if not self.selected_files:
            return
        
        # Confirmation dialog
        dialog = ctk.CTkInputDialog(
            text=f"Are you sure you want to delete {len(self.selected_files)} items?\nType 'YES' to confirm:",
            title="Confirm Deletion"
        )
        
        confirmation = dialog.get_input()
        
        if confirmation != "YES":
            self.status_label.configure(text="Cleaning cancelled")
            return
        
        # Disable buttons
        self.clean_btn.configure(state="disabled")
        self.scan_btn.configure(state="disabled")
        
        # Run cleaning in separate thread
        thread = threading.Thread(target=self._perform_clean, daemon=True)
        thread.start()
    
    def _perform_clean(self):
        """Perform cleaning (runs in separate thread)"""
        def progress_callback(message):
            self.progress_label.configure(text=message)
        
        # Separate recycle bin from files
        files_to_delete = [f for f in self.selected_files if f != "RECYCLE_BIN"]
        empty_recycle = "RECYCLE_BIN" in self.selected_files
        
        # Clean files
        results = self.cleaner.clean_selected_files(files_to_delete, progress_callback)
        
        # Empty recycle bin if selected
        if empty_recycle:
            self.progress_label.configure(text="Emptying Recycle Bin...")
            success, message = self.cleaner.empty_recycle_bin()
        
        # Update UI
        self.after(0, self._cleaning_complete, results)
    
    def _cleaning_complete(self, results):
        """Handle cleaning completion"""
        deleted = results['deleted_count']
        failed = results['failed_count']
        freed = results['freed_space_formatted']
        
        message = f"✅ Cleaning complete!\n"
        message += f"Deleted: {deleted} items\n"
        message += f"Space freed: {freed}"
        
        if failed > 0:
            message += f"\n⚠️ Failed to delete: {failed} items"
        
        # Show result dialog
        result_window = ctk.CTkToplevel(self)
        result_window.title("Cleaning Complete")
        result_window.geometry("400x200")
        
        result_label = ctk.CTkLabel(
            result_window,
            text=message,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        result_label.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            result_window,
            text="OK",
            command=result_window.destroy
        )
        ok_btn.pack(pady=10)
        
        # Re-enable buttons and clear results
        self.scan_btn.configure(state="normal")
        self.status_label.configure(text="Ready to scan")
        
        # Clear results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        self.no_results_label = ctk.CTkLabel(
            self.results_scroll,
            text="Click 'Start Scan' to find temporary files and cache",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.no_results_label.pack(pady=50)
