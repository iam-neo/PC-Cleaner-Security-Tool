
"""
Security Posture Check - CLI Tool
"""
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.security_hardening import SecurityHardener, STARTUP_REGISTRY_KEYS

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
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check")
        table.add_column("Status")
        table.add_column("Recommendation")
        
        for name, (current, recommended, needs_fix) in posture.items():
            status_style = "red" if needs_fix else "green"
            table.add_row(name, f"[{status_style}]{current}[/{status_style}]", recommended)
            
        console.print(table)

    # 2. Audit
    if args.audit:
        console.print("\n[bold]Startup Items Audit[/bold]")
        items = hardener.audit_startup()
        
        if not items:
            console.print("[yellow]No startup items found.[/yellow]")
        else:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Name")
            table.add_column("Location")
            table.add_column("Signed?")
            table.add_column("Publisher")
            
            for item in items:
                signed = item.get("signed", False)
                verified = item.get("verified", False)
                
                if verified:
                    sign_str = "[green]YES[/green]"
                elif signed:
                     sign_str = "[yellow]Unverified[/yellow]"
                else:
                    sign_str = "[red]NO[/red]"
                    
                pub = item.get("publisher", "Unknown")
                table.add_row(item['name'], item['location'], sign_str, pub)
                
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
