#!/usr/bin/env python3
"""
Generate professional framework diagrams for the Gnosis LIF Framework.
Uses the established LIF Slate color palette for visual consistency.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ============================================================================
# COLOR PALETTE (LIF Slate Theme)
# ============================================================================
COLORS = {
    'bg': '#F8FAFC',           # Slate 50 - Background
    'primary': '#475569',       # Dark Slate - Text
    'secondary': '#9AA6B2',     # Slate 400
    'light_blue': '#D9EAFD',    # Light Blue - Boxes
    'accent': '#3B82F6',        # Blue 500 - Accent
    'level1': '#EF4444',        # Red - Nuclear
    'level2': '#F59E0B',        # Amber
    'level3': '#FBBF24',        # Yellow
    'level4': '#10B981',        # Emerald
    'level5': '#06B6D4',        # Cyan - Surgical
    'white': '#FFFFFF',
    'border': '#CBD5E1',        # Slate 300
}

# Get the absolute path to the directory where this script resides
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Determine the project root (one level up from 'scripts')
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# DIAGRAM 1: Hierarchy of Precision (Funnel/Levels)
# ============================================================================
def create_hierarchy_diagram():
    """Create a layered funnel showing intervention scope levels."""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'HIERARCHY OF PRECISION', fontsize=20, fontweight='bold',
            ha='center', va='top', color=COLORS['primary'])
    ax.text(5, 8.9, 'Graduated Intervention Levels', fontsize=12,
            ha='center', va='top', color=COLORS['secondary'])
    
    # Define levels (widest at top, narrowest at bottom = inverted funnel logic)
    levels = [
        ('LEVEL 1', 'NETWORK SCOPE', 'Chain Halt ("Nuclear Option")', 'Berachain Nov 2025', COLORS['level1'], 0.9),
        ('LEVEL 2', 'ASSET SCOPE', 'Token Freeze', 'Sui Cetus, USDC', COLORS['level2'], 0.8),
        ('LEVEL 3', 'PROTOCOL SCOPE', 'dApp Pause', 'Balancer pool pause', COLORS['level3'], 0.7),
        ('LEVEL 4', 'MODULE SCOPE', 'Feature Pause', 'Swap disabled only', COLORS['level4'], 0.6),
        ('LEVEL 5', 'ACCOUNT SCOPE', 'Targeted Intervention', 'Attacker wallet block', COLORS['level5'], 0.5),
    ]
    
    y_start = 8.2
    y_step = 1.5
    
    for i, (level, scope, action, example, color, width_factor) in enumerate(levels):
        y = y_start - i * y_step
        width = 8 * width_factor
        x_left = 5 - width / 2
        
        # Main box
        box = FancyBboxPatch((x_left, y - 0.5), width, 1.0,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor=COLORS['white'],
                             linewidth=2, alpha=0.9)
        ax.add_patch(box)
        
        # Level number (left side in a small badge)
        ax.text(x_left + 0.5, y + 0.2, level, fontsize=9, fontweight='bold',
                ha='left', va='center', color=COLORS['white'])
        
        # Scope name (centered, larger)
        ax.text(5, y + 0.2, scope, fontsize=13, fontweight='bold',
                ha='center', va='center', color=COLORS['white'])
        
        # Action and example on separate line
        ax.text(5, y - 0.2, f'{action}  |  {example}', fontsize=9,
                ha='center', va='center', color=COLORS['white'], alpha=0.95)
    
    # Arrow indicating "More Surgical" direction
    ax.annotate('', xy=(9.2, 1.2), xytext=(9.2, 7.7),
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=2))
    ax.text(9.4, 4.5, 'MORE\nSURGICAL', fontsize=9, ha='left', va='center',
            color=COLORS['secondary'], rotation=0)
    
    # Principle box at bottom
    principle_box = FancyBboxPatch((1.5, 0.3), 7, 0.8,
                                   boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=COLORS['light_blue'], edgecolor=COLORS['border'],
                                   linewidth=1)
    ax.add_patch(principle_box)
    ax.text(5, 0.7, 'PRINCIPLE: Use the least restrictive intervention that achieves the security objective',
            fontsize=10, ha='center', va='center', color=COLORS['primary'], style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/lif_hierarchy_of_precision.png', dpi=150, 
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ Created: lif_hierarchy_of_precision.png")


# ============================================================================
# DIAGRAM 2: Pre-Incident Flow
# ============================================================================
def create_pre_incident_flow():
    """Create a simple left-to-right flow for pre-incident phase."""
    fig, ax = plt.subplots(figsize=(12, 4), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Title
    ax.text(6, 3.6, 'PRE-INCIDENT PHASE', fontsize=16, fontweight='bold',
            ha='center', va='top', color=COLORS['primary'])
    ax.text(6, 3.2, 'Establish Rules Before the Crisis', fontsize=11,
            ha='center', va='top', color=COLORS['secondary'])
    
    # Boxes
    boxes = [
        (1.5, 'Define\nCriteria'),
        (4.5, 'Publish\nFramework'),
        (7.5, 'Community\nRatification'),
        (10.5, 'GIP\nApproval'),
    ]
    
    for x, label in boxes:
        box = FancyBboxPatch((x - 1, 1), 2, 1.5,
                             boxstyle="round,pad=0.05,rounding_size=0.15",
                             facecolor=COLORS['light_blue'], edgecolor=COLORS['accent'],
                             linewidth=2)
        ax.add_patch(box)
        ax.text(x, 1.75, label, fontsize=11, fontweight='bold',
                ha='center', va='center', color=COLORS['primary'])
    
    # Arrows between boxes
    for i in range(len(boxes) - 1):
        x_start = boxes[i][0] + 1.1
        x_end = boxes[i + 1][0] - 1.1
        ax.annotate('', xy=(x_end, 1.75), xytext=(x_start, 1.75),
                    arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=2))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/lif_pre_incident_flow.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ Created: lif_pre_incident_flow.png")


# ============================================================================
# DIAGRAM 3: Optimistic Freeze Flow
# ============================================================================
def create_optimistic_freeze_flow():
    """Create the main Optimistic Freeze process diagram."""
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.6, 'OPTIMISTIC FREEZE MODEL', fontsize=18, fontweight='bold',
            ha='center', va='top', color=COLORS['primary'])
    ax.text(7, 7.1, 'Fast Action with DAO Ratification', fontsize=12,
            ha='center', va='top', color=COLORS['secondary'])
    
    # Define box positions
    def draw_box(x, y, w, h, text, subtext=None, color=COLORS['light_blue'], border=COLORS['accent']):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.05,rounding_size=0.15",
                             facecolor=color, edgecolor=border, linewidth=2)
        ax.add_patch(box)
        if subtext:
            ax.text(x, y + 0.15, text, fontsize=11, fontweight='bold',
                    ha='center', va='center', color=COLORS['primary'])
            ax.text(x, y - 0.25, subtext, fontsize=9,
                    ha='center', va='center', color=COLORS['secondary'])
        else:
            ax.text(x, y, text, fontsize=11, fontweight='bold',
                    ha='center', va='center', color=COLORS['primary'])
    
    # Top row: Detection → Council → Pause
    draw_box(2.5, 5.5, 2.5, 1.2, 'Anomaly', 'Detected', COLORS['level1'], COLORS['level1'])
    draw_box(7, 5.5, 3, 1.2, 'Emergency Council', '(Multisig)', COLORS['light_blue'], COLORS['accent'])
    draw_box(11.5, 5.5, 2.8, 1.2, 'Immediate Pause', '(Optimistic)', COLORS['level2'], COLORS['level2'])
    
    # Arrows for top row
    ax.annotate('', xy=(5.3, 5.5), xytext=(3.8, 5.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
    ax.annotate('', xy=(9.9, 5.5), xytext=(8.6, 5.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
    
    # Down arrow from Pause
    ax.annotate('', xy=(11.5, 4.0), xytext=(11.5, 4.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
    
    # 24-48h Window box
    draw_box(11.5, 3.3, 2.5, 0.9, '24-48h Window', color='#FEF3C7', border=COLORS['level2'])
    
    # Arrow from window to DAO Vote
    ax.annotate('', xy=(8.6, 3.3), xytext=(10.1, 3.3),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
    
    # DAO Vote box (larger, central)
    draw_box(7, 3.3, 3, 1.4, 'DAO Vote', 'Ratify or Revert', COLORS['accent'], COLORS['accent'])
    ax.patches[-1].set_facecolor('#DBEAFE')  # Light blue fill
    
    # Three outcome arrows
    ax.annotate('', xy=(4.5, 1.5), xytext=(6, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['level4'], lw=2))
    ax.annotate('', xy=(7, 1.5), xytext=(7, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['level1'], lw=2))
    ax.annotate('', xy=(9.5, 1.5), xytext=(8, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['level2'], lw=2))
    
    # Outcome boxes
    draw_box(4.5, 1, 2, 0.9, 'CONFIRM', color='#D1FAE5', border=COLORS['level4'])
    draw_box(7, 1, 2, 0.9, 'REVERT', color='#FEE2E2', border=COLORS['level1'])
    draw_box(9.5, 1, 2, 0.9, 'MODIFY', color='#FEF3C7', border=COLORS['level2'])
    
    # Legend/Note at bottom
    legend_box = FancyBboxPatch((2, 0.1), 10, 0.5,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=COLORS['light_blue'], edgecolor=COLORS['border'],
                                linewidth=1, alpha=0.7)
    ax.add_patch(legend_box)
    ax.text(7, 0.35, 'If reverted: Council members face review  •  If confirmed: Intervention continues',
            fontsize=9, ha='center', va='center', color=COLORS['primary'], style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/lif_optimistic_freeze_flow.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ Created: lif_optimistic_freeze_flow.png")


# ============================================================================
# DIAGRAM 4: LIF Legitimacy Pillars (4-Column Grid)
# ============================================================================
def create_legitimacy_pillars():
    """Create a 4-column grid showing the legitimacy conditions."""
    fig, ax = plt.subplots(figsize=(14, 6), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(7, 5.6, 'LEGITIMACY CONDITIONS', fontsize=18, fontweight='bold',
            ha='center', va='top', color=COLORS['primary'])
    ax.text(7, 5.1, 'Four Requirements for Valid Intervention', fontsize=11,
            ha='center', va='top', color=COLORS['secondary'])
    
    pillars = [
        ('TRANSPARENCY', '[1]', 'Criteria documented\nbefore use', '#3B82F6'),
        ('PROPORTIONALITY', '[2]', 'Scope matches\nseverity', '#10B981'),
        ('ACCOUNTABILITY', '[3]', 'Clear authority,\npenalties for misuse', '#F59E0B'),
        ('DUE PROCESS', '[4]', 'Appeals mechanism\nexists', '#8B5CF6'),
    ]
    
    x_positions = [2, 5, 8, 11]
    
    for i, (title, number, desc, color) in enumerate(pillars):
        x = x_positions[i]
        
        # Main pillar box
        box = FancyBboxPatch((x - 1.3, 1), 2.6, 3.5,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=COLORS['white'], edgecolor=color,
                             linewidth=3)
        ax.add_patch(box)
        
        # Color header bar
        header = FancyBboxPatch((x - 1.3, 3.8), 2.6, 0.7,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=color, edgecolor=color,
                                linewidth=1)
        ax.add_patch(header)
        
        # Number in circle
        circle = plt.Circle((x, 3.0), 0.4, facecolor=color, edgecolor=COLORS['white'], linewidth=2)
        ax.add_patch(circle)
        ax.text(x, 3.0, str(i+1), fontsize=20, fontweight='bold', ha='center', va='center', color=COLORS['white'])
        
        # Title
        ax.text(x, 4.15, title, fontsize=9, fontweight='bold',
                ha='center', va='center', color=COLORS['white'])
        
        # Description
        ax.text(x, 2.0, desc, fontsize=10, ha='center', va='center',
                color=COLORS['primary'], linespacing=1.3)
    
    # Bottom note
    note_box = FancyBboxPatch((2, 0.2), 10, 0.5,
                              boxstyle="round,pad=0.02,rounding_size=0.05",
                              facecolor=COLORS['light_blue'], edgecolor=COLORS['border'],
                              linewidth=1, alpha=0.7)
    ax.add_patch(note_box)
    ax.text(7, 0.45, 'All four conditions must be satisfied for intervention to be considered legitimate',
            fontsize=9, ha='center', va='center', color=COLORS['primary'], style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/lif_legitimacy_pillars.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ Created: lif_legitimacy_pillars.png")


# ============================================================================
# DIAGRAM 5: Resilience Stack (Layered Foundation)
# ============================================================================
def create_resilience_stack():
    """Create a layered stack showing human/budget foundation supporting tech."""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.6, 'THE RESILIENCE STACK', fontsize=18, fontweight='bold',
            ha='center', va='top', color=COLORS['primary'])
    ax.text(6, 7.1, 'Human Foundation Supporting Technical Capability', fontsize=11,
            ha='center', va='top', color=COLORS['secondary'])
    
    # Define layers (bottom to top)
    layers = [
        ('BUDGET & RESOURCES', 'Explicit funding for security operations', '#1E3A5F', 0.9),
        ('HEADCOUNT & DEPTH', 'Roster with rotation capacity', '#2563EB', 0.85),
        ('TRAINING & EXERCISES', 'Regular drills, runbooks, fatigue protocols', '#3B82F6', 0.8),
        ('SURGE CAPACITY', 'Retainers, partnerships (e.g., SEAL 911)', '#60A5FA', 0.75),
        ('RECOVERY TIME', 'Decompression between incidents', '#93C5FD', 0.7),
        ('TECHNICAL CAPABILITY', 'Intervention tools & processes', '#DBEAFE', 0.65),
    ]
    
    y_start = 0.8
    layer_height = 0.9
    
    for i, (title, desc, color, width_factor) in enumerate(layers):
        y = y_start + i * layer_height
        width = 10 * width_factor
        x_left = 6 - width / 2
        
        # Layer box
        box = FancyBboxPatch((x_left, y), width, layer_height - 0.1,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor=color, edgecolor=COLORS['white'],
                             linewidth=2)
        ax.add_patch(box)
        
        # Title and description
        text_color = COLORS['white'] if i < 4 else COLORS['primary']
        ax.text(6, y + 0.5, title, fontsize=11, fontweight='bold',
                ha='center', va='center', color=text_color)
        ax.text(6, y + 0.2, desc, fontsize=9, ha='center', va='center',
                color=text_color, alpha=0.9)
    
    # Arrow on the side indicating "Foundation"
    ax.annotate('', xy=(1.2, 1), xytext=(1.2, 6.2),
                arrowprops=dict(arrowstyle='<->', color=COLORS['secondary'], lw=2))
    ax.text(0.5, 2.5, 'HUMAN\nFACTORS', fontsize=9, ha='center', va='center',
            color=COLORS['secondary'], fontweight='bold', rotation=90)
    ax.text(0.5, 5.5, 'TECH\nLAYER', fontsize=9, ha='center', va='center',
            color=COLORS['secondary'], fontweight='bold', rotation=90)
    
    # Key insight box (moved BELOW the stack, not overlapping title)
    insight_box = FancyBboxPatch((1.5, 0.1), 9, 0.5,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor='#FEF3C7', edgecolor=COLORS['level2'],
                                 linewidth=2)
    ax.add_patch(insight_box)
    ax.text(6, 0.35, '"Improvisation is a symptom of under-resourcing" — @mfw78',
            fontsize=10, ha='center', va='center', color=COLORS['primary'], style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/lif_resilience_stack.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ Created: lif_resilience_stack.png")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == '__main__':
    print("\nGenerating LIF Framework Diagrams...")
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    create_hierarchy_diagram()
    create_pre_incident_flow()
    create_optimistic_freeze_flow()
    create_legitimacy_pillars()
    create_resilience_stack()
    
    print("\nAll 5 diagrams generated successfully!")
    print("\nGenerated files:")
    print("  • lif_hierarchy_of_precision.png")
    print("  • lif_pre_incident_flow.png")
    print("  • lif_optimistic_freeze_flow.png")
    print("  • lif_legitimacy_pillars.png")
    print("  • lif_resilience_stack.png")
