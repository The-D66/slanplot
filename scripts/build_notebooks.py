import os
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

def create_notebook(title, description, scripts, out_path):
    nb = new_notebook()
    nb.cells.append(new_markdown_cell(f"# {title}\n\n{description}"))
    
    for script_name in scripts:
        with open(os.path.join('examples', script_name), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove Agg backend line and savefig logic for notebook friendliness
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            if "matplotlib.use('Agg')" in line: continue
            if "savefig" in line: continue
            if "print(\"Saved" in line: continue
            if "print(\"Updated" in line: continue
            clean_lines.append(line)
        
        cell_content = "\n".join(clean_lines)
        nb.cells.append(new_markdown_cell(f"### Example from `{script_name}`"))
        nb.cells.append(new_code_cell(cell_content))
        
    with open(out_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    os.makedirs('examples/notebooks', exist_ok=True)
    
    create_notebook(
        "Relational Plots", 
        "Demonstrating Chord Diagrams, Sankey, and hierarchical Tree diagrams.",
        ["demo_chord.py", "demo_sankey.py", "demo_stree.py", "demo_pitree.py", "demo_circ_tree.py"],
        "examples/notebooks/01_Relational_Plots.ipynb"
    )
    
    create_notebook(
        "Distribution Plots", 
        "Demonstrating Heatmaps, JoyPlots, Hatched Charts, Venn Diagrams, and Marginal Layouts.",
        ["demo_joyplot.py", "demo_marginal.py", "demo_sheatmap.py", "demo_calendar.py", "demo_hatched.py", "demo_venn.py", "demo_upset.py"],
        "examples/notebooks/02_Distribution_Plots.ipynb"
    )
    
    create_notebook(
        "Advanced Scientific Visualization", 
        "Recreating complex biological multi-axis illustrations from slandarer.",
        ["scientific_viz_1.py", "scientific_viz_2.py", "demo_marginal_errorbar.py"],
        "examples/notebooks/03_Scientific_Visualization.ipynb"
    )
    
    print("Notebooks built successfully.")
