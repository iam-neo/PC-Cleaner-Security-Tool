import customtkinter as ctk
import threading
from tkinter import messagebox
from modules.security_hardening import SecurityHardener

class SecurityTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.hardener = SecurityHardener()
        self.audit_items = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.title = ctk.CTkLabel(
            self.header_frame, 
            text="Windows Security Hardening", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title.pack(side="left")
        
        self.action_btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.action_btn_frame.pack(side="right")

        self.scan_btn = ctk.CTkButton(
            self.action_btn_frame,
            text="Run Audit",
            command=self.run_audit
        )
        self.scan_btn.pack(side="left", padx=5)
        
        self.apply_btn = ctk.CTkButton(
            self.action_btn_frame,
            text="Apply Hardening (Dry Run)",
            command=lambda: self.apply_hardening(dry_run=True),
            fg_color="orange"
        )
        self.apply_btn.pack(side="left", padx=5)

        self.force_apply_btn = ctk.CTkButton(
            self.action_btn_frame,
            text="Apply (Admin)",
            command=lambda: self.apply_hardening(dry_run=False),
            fg_color="red"
        )
        self.force_apply_btn.pack(side="left", padx=5)

        # Content Split: Posture (Top/Left) vs Startup Audit (Bottom/Right)
        # Using tabs or split view? Let's use two frames vertially.
        
        # 1. Posture Dashboard
        self.posture_frame = ctk.CTkFrame(self.main_container)
        self.posture_frame.grid(row=1, column=0, sticky="new", pady=(0, 10))
        self.posture_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.posture_labels = {}
        self.create_posture_widgets()
        
        # 2. Startup Audit List
        self.audit_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Startup Items & Signatures")
        self.audit_frame.grid(row=2, column=0, sticky="nsew")
        
        # Status Bar
        self.status_label = ctk.CTkLabel(self.main_container, text="Ready", anchor="w")
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # Initial quick check
        if self.hardener.check_os():
             self.refresh_posture()
        else:
             self.status_label.configure(text="Module disabled: Non-Windows OS detected.")
             self.scan_btn.configure(state="disabled")
             self.apply_btn.configure(state="disabled")

    def create_posture_widgets(self):
        checks = ["UAC", "Firewall", "Windows Defender"]
        for i, check in enumerate(checks):
            frame = ctk.CTkFrame(self.posture_frame)
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            lbl_title = ctk.CTkLabel(frame, text=check, font=ctk.CTkFont(weight="bold"))
            lbl_title.pack(pady=5)
            
            lbl_status = ctk.CTkLabel(frame, text="Checking...", text_color="gray")
            lbl_status.pack(pady=5)
            
            self.posture_labels[check] = lbl_status

    def refresh_posture(self):
        posture = self.hardener.check_posture()
        for check, (current, recommended, needs_fix) in posture.items():
            lbl = self.posture_labels.get(check)
            if lbl:
                lbl.configure(text=current, text_color="red" if needs_fix else "green")

    def run_audit(self):
        self.status_label.configure(text="Auditing...")
        self.scan_btn.configure(state="disabled")
        
        def _target():
            items = self.hardener.audit_startup()
            self.after(0, lambda: self.display_audit(items))
            self.after(0, lambda: self.status_label.configure(text=f"Audit Complete. Found {len(items)} items."))
            self.after(0, lambda: self.scan_btn.configure(state="normal"))
            
        threading.Thread(target=_target, daemon=True).start()

    def display_audit(self, items):
        # Clear existing
        for widget in self.audit_frame.winfo_children():
            widget.destroy()
            
        if not items:
            ctk.CTkLabel(self.audit_frame, text="No startup items found or error reading.").pack(pady=20)
            return

        for item in items:
            # Color code based on signature
            color = "transparent"
            fg_color = "white" # default text
            border_color = "gray"
            
            signed = item.get("signed", False)
            verified = item.get("verified", False)
            
            if verified:
                status_icon = "✅" 
                detail_color = "green"
            else:
                status_icon = "⚠️"
                detail_color = "orange"
                
            frame = ctk.CTkFrame(self.audit_frame, border_width=1, border_color=border_color)
            frame.pack(fill="x", padx=5, pady=2)
            
            # Row 1: Name + Icon
            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x", px=5, py=2)
            
            ctk.CTkLabel(header, text=f"{status_icon} {item['name']}", font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkLabel(header, text=f"[{item['location']}]", text_color="gray").pack(side="right")
            
            # Row 2: Command + Publisher
            details = ctk.CTkFrame(frame, fg_color="transparent")
            details.pack(fill="x", px=10, py=2)
            
            cmd_trunc = (item['command'][:80] + '..') if len(item['command']) > 80 else item['command']
            ctk.CTkLabel(details, text=f"Cmd: {cmd_trunc}", font=ctk.CTkFont(size=10)).pack(anchor="w")
            
            pub = item.get("publisher", "Unknown")
            ctk.CTkLabel(details, text=f"Publisher: {pub}", text_color=detail_color, font=ctk.CTkFont(size=10)).pack(anchor="w")

    def apply_hardening(self, dry_run=True):
        mode = "Dry Run" if dry_run else "Execute"
        if not dry_run:
            if not messagebox.askyesno("Confirm Hardening", "Are you sure you want to apply security changes? This requires Admin rights."):
                return

        self.status_label.configure(text=f"Applying Hardening ({mode})...")
        
        def _target():
            logs = self.hardener.apply_security_best_practices(dry_run=dry_run)
            msg = "\n".join(logs)
            self.after(0, lambda: self._show_result(msg))
            
        threading.Thread(target=_target, daemon=True).start()

    def _show_result(self, msg):
        self.status_label.configure(text="Hardening task finished.")
        dialog = ctk.CTkToplevel(self)
        dialog.title("Hardening Results")
        dialog.geometry("500x400")
        
        textbox = ctk.CTkTextbox(dialog)
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        textbox.insert("0.0", msg)
