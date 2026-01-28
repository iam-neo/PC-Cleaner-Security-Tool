"""
PC Cleaner & Security Tool
Main Application
"""
import customtkinter as ctk
import sys
from ui.dashboard import DashboardTab
from ui.cleaner_tab import CleanerTab
from ui.scanner_tab import ScannerTab
from ui.security_tab import SecurityTab
from utils.system_info import is_admin
import config


class PCCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Set theme
        ctk.set_appearance_mode(config.THEME_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create tabs
        self.dashboard = DashboardTab(self.main_frame, self)
        self.cleaner_tab = CleanerTab(self.main_frame, self)
        self.scanner_tab = ScannerTab(self.main_frame, self)
        self.security_tab = SecurityTab(self.main_frame, self)
        
        # Show dashboard by default
        self.current_tab = None
        self.show_dashboard()
        
        # Check admin status
        if not is_admin():
            self.show_admin_warning()
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        logo_label = ctk.CTkLabel(
            sidebar,
            text="🛡️ PC Cleaner",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        version_label = ctk.CTkLabel(
            sidebar,
            text=f"v{config.APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        version_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            sidebar,
            text="📊 Dashboard",
            command=self.show_dashboard,
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        self.dashboard_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.cleaner_btn = ctk.CTkButton(
            sidebar,
            text="🧹 PC Cleaner",
            command=self.show_cleaner,
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        self.cleaner_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.scanner_btn = ctk.CTkButton(
            sidebar,
            text="🛡️ Malware Scanner",
            command=self.show_scanner,
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        self.scanner_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.security_btn = ctk.CTkButton(
            sidebar,
            text="🔒 Security Guard",
            command=self.show_security,
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        self.security_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Theme toggle
        self.theme_label = ctk.CTkLabel(
            sidebar,
            text="Appearance Mode:",
            font=ctk.CTkFont(size=12)
        )
        self.theme_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.theme_switch = ctk.CTkSegmentedButton(
            sidebar,
            values=["Light", "Dark", "System"],
            command=self.change_theme
        )
        self.theme_switch.grid(row=8, column=0, padx=20, pady=10)
        self.theme_switch.set("Dark" if config.THEME_MODE == "dark" else "Light")
        
        # About button
        about_btn = ctk.CTkButton(
            sidebar,
            text="ℹ️ About",
            command=self.show_about,
            height=30,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        about_btn.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="ew")
    
    def show_dashboard(self):
        """Show dashboard tab"""
        self.hide_all_tabs()
        self.dashboard.grid(row=0, column=0, sticky="nsew")
        self.current_tab = "dashboard"
        self.highlight_button(self.dashboard_btn)
    
    def show_cleaner(self):
        """Show PC cleaner tab"""
        self.hide_all_tabs()
        self.cleaner_tab.grid(row=0, column=0, sticky="nsew")
        self.current_tab = "cleaner"
        self.highlight_button(self.cleaner_btn)
    
    def show_scanner(self):
        """Show malware scanner tab"""
        self.hide_all_tabs()
        self.scanner_tab.grid(row=0, column=0, sticky="nsew")
        self.current_tab = "scanner"
        self.highlight_button(self.scanner_btn)

    def show_security(self):
        """Show security hardening tab"""
        self.hide_all_tabs()
        self.security_tab.grid(row=0, column=0, sticky="nsew")
        self.current_tab = "security"
        self.highlight_button(self.security_btn)
    
    def hide_all_tabs(self):
        """Hide all tabs"""
        self.dashboard.grid_forget()
        self.cleaner_tab.grid_forget()
        self.scanner_tab.grid_forget()
        self.security_tab.grid_forget()
        
        # Reset button colors
        self.dashboard_btn.configure(fg_color="transparent")
        self.cleaner_btn.configure(fg_color="transparent")
        self.scanner_btn.configure(fg_color="transparent")
        self.security_btn.configure(fg_color="transparent")
    
    def highlight_button(self, button):
        """Highlight the active navigation button"""
        button.configure(fg_color=("gray75", "gray25"))
    
    def switch_to_cleaner(self):
        """Switch to cleaner tab (called from dashboard)"""
        self.show_cleaner()
    
    def switch_to_scanner(self):
        """Switch to scanner tab (called from dashboard)"""
        self.show_scanner()
    
    def change_theme(self, value):
        """Change application theme"""
        ctk.set_appearance_mode(value.lower())
    
    def show_about(self):
        """Show about dialog"""
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("500x400")
        
        # Make it modal
        about_window.transient(self)
        about_window.grab_set()
        
        # Content
        title = ctk.CTkLabel(
            about_window,
            text=f"🛡️ {config.APP_NAME}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(30, 10))
        
        version = ctk.CTkLabel(
            about_window,
            text=f"Version {config.APP_VERSION}",
            font=ctk.CTkFont(size=14)
        )
        version.pack(pady=5)
        
        description = ctk.CTkLabel(
            about_window,
            text="A powerful tool to clean temporary files,\ncache, and scan for malware on your PC.",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        description.pack(pady=20)
        
        features_frame = ctk.CTkFrame(about_window)
        features_frame.pack(padx=40, pady=20, fill="both", expand=True)
        
        features_title = ctk.CTkLabel(
            features_frame,
            text="Features:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        features_title.pack(pady=(10, 5))
        
        features_text = """
• Clean temporary files and system cache
• Remove browser cache (Chrome, Edge, Firefox, Opera)
• Empty Recycle Bin
• Scan for malware and suspicious files
• Detect suspicious running processes
• Quarantine or remove threats
• Real-time system monitoring
        """.strip()
        
        features_label = ctk.CTkLabel(
            features_frame,
            text=features_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        features_label.pack(pady=10, padx=20)
        
        close_btn = ctk.CTkButton(
            about_window,
            text="Close",
            command=about_window.destroy,
            width=100
        )
        close_btn.pack(pady=20)
    
    def show_admin_warning(self):
        """Show warning if not running as administrator"""
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("Administrator Privileges Required")
        warning_window.geometry("500x250")
        
        # Make it modal
        warning_window.transient(self)
        warning_window.grab_set()
        
        warning_label = ctk.CTkLabel(
            warning_window,
            text="⚠️ Administrator Privileges Required",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="orange"
        )
        warning_label.pack(pady=(30, 20))
        
        message = ctk.CTkLabel(
            warning_window,
            text="This application is not running with administrator privileges.\n\n"
                 "Some features may be limited:\n"
                 "• Cannot access all system directories\n"
                 "• Cannot delete protected files\n"
                 "• Cannot terminate system processes\n\n"
                 "For full functionality, please run as administrator.",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        message.pack(pady=20, padx=30)
        
        btn_frame = ctk.CTkFrame(warning_window, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        continue_btn = ctk.CTkButton(
            btn_frame,
            text="Continue Anyway",
            command=warning_window.destroy,
            width=150
        )
        continue_btn.pack(side="left", padx=10)
        
        exit_btn = ctk.CTkButton(
            btn_frame,
            text="Exit",
            command=self.quit,
            width=150,
            fg_color="red",
            hover_color="darkred"
        )
        exit_btn.pack(side="left", padx=10)


def main():
    """Main entry point"""
    app = PCCleanerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
