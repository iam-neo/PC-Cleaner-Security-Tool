"""
Dashboard UI for PC Cleaner & Security Tool
"""
import customtkinter as ctk
from utils.system_info import get_disk_usage, get_system_info, format_bytes, is_admin
from datetime import datetime


class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self, 
            text="System Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # Admin status warning
        if not is_admin():
            warning = ctk.CTkLabel(
                self,
                text="⚠️ Not running as Administrator - Some features may be limited",
                font=ctk.CTkFont(size=12),
                text_color="orange"
            )
            warning.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")
        
        # System Info Frame
        self.create_system_info_frame()
        
        # Disk Usage Frame
        self.create_disk_usage_frame()
        
        # Quick Actions Frame
        self.create_quick_actions_frame()
        
        # Last Scan Info Frame
        self.create_last_scan_frame()
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Refresh Dashboard",
            command=self.refresh_dashboard,
            height=40
        )
        refresh_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
    
    def create_system_info_frame(self):
        """Create system information display"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        title = ctk.CTkLabel(
            frame,
            text="💻 System Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Get system info
        sys_info = get_system_info()
        
        info_text = f"""
OS: {sys_info.get('os', 'Unknown')} {sys_info.get('os_release', '')}
Version: {sys_info.get('os_version', 'Unknown')}
Processor: {sys_info.get('processor', 'Unknown')}
Machine: {sys_info.get('machine', 'Unknown')}
        """.strip()
        
        info_label = ctk.CTkLabel(
            frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=15, pady=(0, 15), anchor="w")
    
    def create_disk_usage_frame(self):
        """Create disk usage display"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        
        title = ctk.CTkLabel(
            frame,
            text="💾 Disk Usage (C:)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Get disk usage
        disk = get_disk_usage()
        
        # Progress bar
        progress = ctk.CTkProgressBar(frame, width=300)
        progress.pack(padx=15, pady=10)
        progress.set(disk.get('percent', 0) / 100)
        
        # Disk info
        disk_text = f"""
Total: {disk.get('total_gb', 0)} GB
Used: {disk.get('used_gb', 0)} GB ({disk.get('percent', 0)}%)
Free: {disk.get('free_gb', 0)} GB
        """.strip()
        
        disk_label = ctk.CTkLabel(
            frame,
            text=disk_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        disk_label.pack(padx=15, pady=(0, 15), anchor="w")
    
    def create_quick_actions_frame(self):
        """Create quick action buttons"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        
        title = ctk.CTkLabel(
            frame,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Quick Clean button
        clean_btn = ctk.CTkButton(
            frame,
            text="🧹 Quick Clean",
            command=self.quick_clean,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        clean_btn.pack(padx=15, pady=5, fill="x")
        
        # Quick Scan button
        scan_btn = ctk.CTkButton(
            frame,
            text="🔍 Quick Scan",
            command=self.quick_scan,
            height=40,
            fg_color="blue",
            hover_color="darkblue"
        )
        scan_btn.pack(padx=15, pady=(5, 15), fill="x")
    
    def create_last_scan_frame(self):
        """Create last scan information display"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")
        
        title = ctk.CTkLabel(
            frame,
            text="📊 Last Scan Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(padx=15, pady=(15, 10), anchor="w")
        
        self.last_scan_label = ctk.CTkLabel(
            frame,
            text="No scans performed yet",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.last_scan_label.pack(padx=15, pady=(0, 15), anchor="w")
    
    def quick_clean(self):
        """Switch to cleaner tab and start quick scan"""
        self.app.switch_to_cleaner()
    
    def quick_scan(self):
        """Switch to scanner tab and start quick scan"""
        self.app.switch_to_scanner()
    
    def refresh_dashboard(self):
        """Refresh all dashboard information"""
        # Recreate frames with updated info
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        
        self.create_system_info_frame()
        self.create_disk_usage_frame()
        self.create_quick_actions_frame()
        self.create_last_scan_frame()
    
    def update_last_scan_info(self, scan_type: str, results: dict):
        """Update last scan information"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if scan_type == "cleaner":
            info_text = f"""
Last Clean: {timestamp}
Files Found: {results.get('total_items', 0)}
Space to Free: {results.get('total_size_formatted', '0 B')}
            """.strip()
        else:  # scanner
            info_text = f"""
Last Scan: {timestamp}
Threats Found: {results.get('threat_count', 0)}
Files Scanned: {results.get('files_scanned', 0)}
            """.strip()
        
        self.last_scan_label.configure(text=info_text)
