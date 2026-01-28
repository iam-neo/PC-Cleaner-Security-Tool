"""
Security Posture Check - CLI Tool
"""
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from modules.security_hardening import SecurityHardener
from utils.cli_renderer import render_posture_table, render_audit_table

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="Windows Security Hardening CLI")
    parser.add_argument("--audit", action="store_true", help="Audit startup items")
    parser.add_argument("--posture", action="store_true", help="Check system security posture")
    parser.add_argument("--apply", action="store_true", help="Apply security best practices (Admin required)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate changes (default)")
    parser.add_argument("--force", action="store_false", dest="dry_run", help="Actually apply changes")
    
    args = parser.parse_args()
    hardener = SecurityHardener()
    
    console.print(Panel.fit("[bold blue]Windows Security Hardening[/bold blue]", border_style="blue"))
    
    if not hardener.check_os():
        console.print("[red]Error: This tool supports Windows only.[/red]")
        sys.exit(1)

    # 1. Posture Check
    if args.posture or (not args.audit and not args.apply):
        console.print("\n[bold]System Security Posture[/bold]")
        posture = hardener.check_posture()
        table = render_posture_table(posture)
        console.print(table)

    # 2. Audit
    if args.audit:
        console.print("\n[bold]Startup Items Audit[/bold]")
        items = hardener.audit_startup()
        
        if not items:
            console.print("[yellow]No startup items found.[/yellow]")
        else:
            table = render_audit_table(items)
            console.print(table)

    # 3. Apply Hardening
    if args.apply:
        mode = "DRY RUN" if args.dry_run else "LIVE EXECUTION"
        style = "yellow" if args.dry_run else "red"
        console.print(f"\n[bold {style}]Applying Hardening ({mode})...[/bold {style}]")
        
        logs = hardener.apply_security_best_practices(dry_run=args.dry_run)
        
        for log in logs:
            console.print(f" > {log}")

if __name__ == "__main__":
    main()
