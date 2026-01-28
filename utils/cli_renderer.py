"""
CLI Rendering Helpers for Security Module
Uses 'rich' library to format output tables.
"""
from rich.console import Console
from rich.table import Table
from typing import List, Dict

def render_posture_table(posture_data: Dict[str, tuple]) -> Table:
    """
    Render system posture check results as a Rich Table.
    
    Args:
        posture_data (dict): Dictionary { CheckName: (Current, Recommended, NeedsFix) }
        
    Returns:
        Table: Formatted Rich table object
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Recommendation")
    
    for name, (current, recommended, needs_fix) in posture_data.items():
        status_style = "red" if needs_fix else "green"
        table.add_row(name, f"[{status_style}]{current}[/{status_style}]", recommended)
        
    return table

def render_audit_table(audit_items: List[Dict]) -> Table:
    """
    Render startup audit items as a Rich Table.
    
    Args:
        audit_items (list): List of dicts containing startup item info.
        
    Returns:
        Table: Formatted Rich table object
    """
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Name")
    table.add_column("Location")
    table.add_column("Signed?")
    table.add_column("Publisher")
    
    if not audit_items:
        # Return empty table or handle outside? 
        # Table with no rows is fine.
        return table
        
    for item in audit_items:
        signed = item.get("signed", False)
        verified = item.get("verified", False)
        
        if verified:
            sign_str = "[green]YES[/green]"
        elif signed:
             sign_str = "[yellow]Unverified[/yellow]"
        else:
            sign_str = "[red]NO[/red]"
            
        pub = item.get("publisher", "Unknown")
        table.add_row(item.get('name', 'Unknown'), item.get('location', 'Unknown'), sign_str, pub)
        
    return table
