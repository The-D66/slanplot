import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    np.random.seed(123)
    
    families = [
        "Serranidae", "Zoarcidae", "Myctophidae", "Sebastidae", "Liparidae",
        "Carangidae", "Scombridae", "Psychrolutidae", "Nototheniidae", "Macrouridae",
        "Soleidae", "Pleuronectidae", "Paralichthyidae", "Sternoptychidae", "Ophidiidae",
        "Lutjanidae", "Sparidae", "Moridae", "Monacanthidae", "Apogonidae"
    ][::-1]
    
    n = len(families)
    
    # Fake stacked bar data
    shallow = np.random.rand(n)
    intermediate = np.random.rand(n)
    deep = np.random.rand(n)
    total = shallow + intermediate + deep
    shallow /= total
    intermediate /= total
    deep /= total
    
    # Fake dumbbell data
    transitions = np.random.randint(5, 50, n)
    lower_bound = np.maximum(0, transitions - np.random.randint(1, 15, n))
    upper_bound = transitions + np.random.randint(1, 15, n)
    
    status = []
    for i in range(n):
        if transitions[i] < lower_bound[i] + (upper_bound[i] - lower_bound[i])*0.2:
            status.append('Below expectation')
        elif transitions[i] > lower_bound[i] + (upper_bound[i] - lower_bound[i])*0.8:
            status.append('Above expectation')
        else:
            status.append('Within expectation')
            
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=True, gridspec_kw={'width_ratios': [1, 1.2]})
    fig.patch.set_facecolor('white')
    
    # --- Left plot (Stacked Bar) ---
    c_shallow = '#9CE2EC'
    c_inter = '#3393B5'
    c_deep = '#0D3E5E'
    
    y_pos = np.arange(n)
    ax1.barh(y_pos, shallow, color=c_shallow, label='Shallow')
    ax1.barh(y_pos, intermediate, left=shallow, color=c_inter, label='Intermediate')
    ax1.barh(y_pos, deep, left=shallow+intermediate, color=c_deep, label='Deep')
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(families, fontsize=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.set_xticks([])
    
    # legend 1
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=True, edgecolor='black')
    
    # --- Right plot (Dumbbell) ---
    ax2.set_xlabel("Number of Transitions", fontsize=12)
    ax2.grid(True, axis='y', linestyle='-', color='lightgray', alpha=0.5)
    
    c_above = '#00A08A'
    c_within = '#7A7A7A'
    c_below = '#F2A900'
    
    for i in range(n):
        # Background expectation range
        ax2.plot([lower_bound[i], upper_bound[i]], [i, i], color='#EAEAEA', linewidth=8, solid_capstyle='round', zorder=1)
        
        # Connect to zero? No, the line goes from the dot to ... wait, in the image, 
        # it seems like dots are connected to hollow circles. 
        # Let's add a hollow circle at expectation mean
        exp_mean = (lower_bound[i] + upper_bound[i]) / 2
        ax2.plot([transitions[i], exp_mean], [i, i], color='gray', linewidth=1.5, zorder=2)
        
        # Draw expected mean as hollow circle
        ax2.scatter([exp_mean], [i], facecolor='white', edgecolor='gray', s=60, zorder=3)
        
        # Draw actual dot
        if status[i] == 'Above expectation': color = c_above
        elif status[i] == 'Below expectation': color = c_below
        else: color = c_within
        ax2.scatter([transitions[i]], [i], color=color, s=80, zorder=4)
        
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    # Fake legend handles
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=c_above, markersize=10, label='Above expectation'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=c_within, markersize=10, label='Within expectation'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=c_below, markersize=10, label='Below expectation')
    ]
    ax2.legend(handles=handles, loc='lower right', frameon=True, edgecolor='black')
    
    plt.tight_layout()
    plt.savefig('/Users/the-d/.gemini/antigravity/brain/d52f437c-6ca0-4617-8907-efca4c6f0b8c/demo_scientific_viz_1.png', dpi=300, bbox_inches='tight')
    print("Saved demo_scientific_viz_1.png")

if __name__ == "__main__":
    main()
