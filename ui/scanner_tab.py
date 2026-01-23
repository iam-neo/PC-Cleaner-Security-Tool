"""
Malware Scanner Tab UI
"""
import customtkinter as ctk
import threading
from modules.scanner import MalwareScanner


class ScannerTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.scanner = MalwareScanner()
        self.scan_results = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="🛡️ Malware Scanner",
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
        
        # Quick Scan button
        self.quick_scan_btn = ctk.CTkButton(
            frame,
            text="⚡ Quick Scan",
            command=self.start_quick_scan,
            height=40,
            width=150,
            fg_color="blue",
            hover_color="darkblue"
        )
        self.quick_scan_btn.pack(side="left", padx=5, pady=10)
        
        # Full Scan button
        self.full_scan_btn = ctk.CTkButton(
            frame,
            text="🔍 Full Scan",
            command=self.start_full_scan,
            height=40,
            width=150,
            fg_color="purple",
            hover_color="darkviolet"
        )
        self.full_scan_btn.pack(side="left", padx=5, pady=10)
        
        # Process Scan button
        self.process_scan_btn = ctk.CTkButton(
            frame,
            text="⚙️ Scan Processes",
            command=self.scan_processes,
            height=40,
            width=150,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.process_scan_btn.pack(side="left", padx=5, pady=10)
    
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
            text="Click 'Quick Scan' or 'Full Scan' to check for malware",
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
    
    def start_quick_scan(self):
        """Start quick malware scan"""
        self._start_scan("quick")
    
    def start_full_scan(self):
        """Start full system scan"""
        self._start_scan("full")
    
    def _start_scan(self, scan_type):
        """Start scanning for malware"""
        # Disable buttons
        self.quick_scan_btn.configure(state="disabled")
        self.full_scan_btn.configure(state="disabled")
        self.process_scan_btn.configure(state="disabled")
        
        self.status_label.configure(text=f"Performing {scan_type} scan...")
        self.progress_bar.set(0)
        
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        scanning_label = ctk.CTkLabel(
            self.results_scroll,
            text="🔍 Scanning for threats...",
            font=ctk.CTkFont(size=14)
        )
        scanning_label.pack(pady=50)
        
        # Run scan in separate thread
        thread = threading.Thread(
            target=self._perform_scan,
            args=(scan_type,),
            daemon=True
        )
        thread.start()
    
    def _perform_scan(self, scan_type):
        """Perform the scan (runs in separate thread)"""
        def progress_callback(message):
            self.progress_label.configure(text=message)
            # Animate progress bar
            current = self.progress_bar.get()
            if current < 0.9:
                self.progress_bar.set(current + 0.1)
        
        # Perform scan
        if scan_type == "quick":
            results = self.scanner.perform_quick_scan(progress_callback)
        else:
            results = self.scanner.perform_full_scan(progress_callback)
        
        self.scan_results = results
        
        # Update UI in main thread
        self.after(0, self._display_results, results)
    
    def _display_results(self, results):
        """Display scan results"""
        # Clear loading message
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        threat_count = results.get('threat_count', 0)
        files_scanned = results.get('files_scanned', 0)
        
        # Update title
        self.results_title.configure(
            text=f"Scan Results - {threat_count} threats found ({files_scanned} files scanned)"
        )
        
        if threat_count == 0:
            # No threats found
            clean_label = ctk.CTkLabel(
                self.results_scroll,
                text="✅ No threats detected!\nYour system appears to be clean.",
                font=ctk.CTkFont(size=16),
                text_color="green"
            )
            clean_label.pack(pady=50)
        else:
            # Display threats
            for threat in results['threats']:
                self._create_threat_item(threat)
        
        # Re-enable buttons
        self.quick_scan_btn.configure(state="normal")
        self.full_scan_btn.configure(state="normal")
        self.process_scan_btn.configure(state="normal")
        
        self.status_label.configure(text=f"Scan complete - {threat_count} threats found")
        self.progress_bar.set(1)
        
        # Update dashboard
        self.app.dashboard.update_last_scan_info("scanner", results)
    
    def _create_threat_item(self, threat):
        """Create a threat item display"""
        frame = ctk.CTkFrame(self.results_scroll, fg_color="darkred")
        frame.pack(fill="x", padx=10, pady=5)
        
        # Severity indicator
        severity = threat.get('max_severity', 'Low')
        severity_colors = {
            'Low': 'yellow',
            'Medium': 'orange',
            'High': 'red',
            'Critical': 'darkred'
        }
        
        severity_label = ctk.CTkLabel(
            frame,
            text=f"⚠️ {severity}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=severity_colors.get(severity, 'yellow')
        )
        severity_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # File info
        file_label = ctk.CTkLabel(
            frame,
            text=f"📄 {threat['filename']}",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        file_label.pack(anchor="w", padx=10, pady=2)
        
        path_label = ctk.CTkLabel(
            frame,
            text=f"Path: {threat['path']}",
            font=ctk.CTkFont(size=10),
            text_color="lightgray"
        )
        path_label.pack(anchor="w", padx=10, pady=2)
        
        # Threat details
        for threat_detail in threat['threats']:
            detail_text = f"• {threat_detail['type']}: {threat_detail['description']}"
            detail_label = ctk.CTkLabel(
                frame,
                text=detail_text,
                font=ctk.CTkFont(size=10),
                text_color="white"
            )
            detail_label.pack(anchor="w", padx=20, pady=2)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        quarantine_btn = ctk.CTkButton(
            btn_frame,
            text="🔒 Quarantine",
            command=lambda: self.quarantine_threat(threat['path']),
            height=30,
            width=120,
            fg_color="orange",
            hover_color="darkorange"
        )
        quarantine_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Delete",
            command=lambda: self.delete_threat(threat['path']),
            height=30,
            width=120,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="left", padx=5)
        
        ignore_btn = ctk.CTkButton(
            btn_frame,
            text="✓ Ignore",
            command=lambda: self.ignore_threat(frame),
            height=30,
            width=120,
            fg_color="gray",
            hover_color="darkgray"
        )
        ignore_btn.pack(side="left", padx=5)
    
    def scan_processes(self):
        """Scan running processes"""
        self.process_scan_btn.configure(state="disabled")
        self.status_label.configure(text="Scanning running processes...")
        
        # Clear results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        # Run in thread
        thread = threading.Thread(target=self._scan_processes, daemon=True)
        thread.start()
    
    def _scan_processes(self):
        """Scan processes (runs in separate thread)"""
        suspicious = self.scanner.scan_running_processes()
        
        # Update UI
        self.after(0, self._display_process_results, suspicious)
    
    def _display_process_results(self, suspicious):
        """Display process scan results"""
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        if not suspicious:
            clean_label = ctk.CTkLabel(
                self.results_scroll,
                text="✅ No suspicious processes detected!",
                font=ctk.CTkFont(size=16),
                text_color="green"
            )
            clean_label.pack(pady=50)
        else:
            for proc in suspicious:
                self._create_process_item(proc)
        
        self.process_scan_btn.configure(state="normal")
        self.status_label.configure(text=f"Process scan complete - {len(suspicious)} suspicious processes found")
    
    def _create_process_item(self, proc):
        """Create a suspicious process item"""
        frame = ctk.CTkFrame(self.results_scroll, fg_color="darkred")
        frame.pack(fill="x", padx=10, pady=5)
        
        # Process info
        info_label = ctk.CTkLabel(
            frame,
            text=f"⚙️ {proc['name']} (PID: {proc['pid']})",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        info_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        path_label = ctk.CTkLabel(
            frame,
            text=f"Path: {proc['path']}",
            font=ctk.CTkFont(size=10),
            text_color="lightgray"
        )
        path_label.pack(anchor="w", padx=10, pady=2)
        
        reason_label = ctk.CTkLabel(
            frame,
            text=f"Reason: {proc['reason']}",
            font=ctk.CTkFont(size=10),
            text_color="white"
        )
        reason_label.pack(anchor="w", padx=10, pady=2)
        
        # Terminate button
        terminate_btn = ctk.CTkButton(
            frame,
            text="🛑 Terminate Process",
            command=lambda: self.terminate_process(proc['pid'], frame),
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        terminate_btn.pack(padx=10, pady=10, anchor="w")
    
    def quarantine_threat(self, filepath):
        """Quarantine a threat"""
        success, message = self.scanner.quarantine_threat(filepath)
        
        # Show result
        result_window = ctk.CTkToplevel(self)
        result_window.title("Quarantine Result")
        result_window.geometry("400x150")
        
        result_label = ctk.CTkLabel(
            result_window,
            text=message,
            font=ctk.CTkFont(size=14)
        )
        result_label.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            result_window,
            text="OK",
            command=result_window.destroy
        )
        ok_btn.pack(pady=10)
        
        if success:
            # Refresh results
            self.status_label.configure(text="Threat quarantined successfully")
    
    def delete_threat(self, filepath):
        """Delete a threat"""
        # Confirmation
        dialog = ctk.CTkInputDialog(
            text=f"Permanently delete this file?\nType 'DELETE' to confirm:",
            title="Confirm Deletion"
        )
        
        confirmation = dialog.get_input()
        
        if confirmation != "DELETE":
            return
        
        success, message = self.scanner.remove_threat(filepath)
        
        # Show result
        result_window = ctk.CTkToplevel(self)
        result_window.title("Delete Result")
        result_window.geometry("400x150")
        
        result_label = ctk.CTkLabel(
            result_window,
            text=message,
            font=ctk.CTkFont(size=14)
        )
        result_label.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            result_window,
            text="OK",
            command=result_window.destroy
        )
        ok_btn.pack(pady=10)
        
        if success:
            self.status_label.configure(text="Threat deleted successfully")
    
    def ignore_threat(self, frame):
        """Ignore a threat (remove from display)"""
        frame.destroy()
        self.status_label.configure(text="Threat ignored")
    
    def terminate_process(self, pid, frame):
        """Terminate a suspicious process"""
        # Confirmation
        dialog = ctk.CTkInputDialog(
            text=f"Terminate process {pid}?\nType 'TERMINATE' to confirm:",
            title="Confirm Termination"
        )
        
        confirmation = dialog.get_input()
        
        if confirmation != "TERMINATE":
            return
        
        success, message = self.scanner.terminate_process(pid)
        
        # Show result
        result_window = ctk.CTkToplevel(self)
        result_window.title("Terminate Result")
        result_window.geometry("400x150")
        
        result_label = ctk.CTkLabel(
            result_window,
            text=message,
            font=ctk.CTkFont(size=14)
        )
        result_label.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            result_window,
            text="OK",
            command=result_window.destroy
        )
        ok_btn.pack(pady=10)
        
        if success:
            frame.destroy()
            self.status_label.configure(text="Process terminated successfully")
