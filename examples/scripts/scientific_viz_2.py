import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def main():
    sns.set_style('white')
    np.random.seed(0)
    days = np.array([0, 7, 14, 21, 28, 35])
    
    # Fake data for 4 groups
    # Non_SMK (blue), SMK (red), Non_SMK+abx (teal), SMK+abx (yellow)
    non_smk = [0, 8, 14, 18, 28, 32]
    smk = [0, 2, 3, 4, 15, 25]
    non_smk_abx = [0, 10, 19, 22, 30, 40]
    smk_abx = [0, 1, 2, 2, 10, 18]
    
    colors = {
        'Non_SMK': '#4A8DCC',
        'SMK': '#FF8A8A',
        'Non_SMK+abx': '#008C8C',
        'SMK+abx': '#F2C94C'
    }
    
    # Convert to arrays and add some noise for standard deviation
    data = {
        'Non_SMK': (np.array(non_smk), np.random.rand(6)*1.5 + 0.5),
        'SMK': (np.array(smk), np.random.rand(6)*1.5 + 0.5),
        'Non_SMK+abx': (np.array(non_smk_abx), np.random.rand(6)*1.5 + 0.5),
        'SMK+abx': (np.array(smk_abx), np.random.rand(6)*1.5 + 0.5)
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Vertical dashed line at Day 21
    ax.axvline(20, color='black', linestyle='--', linewidth=2)
    
    # Plotting main lines with error bars and fill_between (sigma)
    for label, (y_mean, y_std) in data.items():
        color = colors[label]
        # 添加带有透明度的 sigma 背景区域
        ax.fill_between(days, y_mean - y_std, y_mean + y_std, color=color, alpha=0.15, edgecolor='none')
        # 绘制主线和误差棒
        ax.errorbar(days, y_mean, yerr=y_std, fmt='-o', color=color, label=label,
                    linewidth=4, markersize=8, capsize=4, markeredgecolor='black', markeredgewidth=1)
                    
    ax.set_xlabel('Day', fontsize=14, fontweight='bold')
    ax.set_ylabel('Weight change(%)', fontsize=14, fontweight='bold')
    ax.set_ylim(-2, 60)
    ax.set_yticks([0, 20, 40, 60])
    ax.set_xlim(-1, 40)
    
    # Legend at the top
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4, frameon=True, edgecolor='black')
    
    # --- Inset plots (iAUC) ---
    def create_inset(bounds, title, max_val, title_x=0.5):
        ax_in = ax.inset_axes(bounds)
        ax_in.set_title(title, fontsize=12, fontweight='bold', x=title_x)
        # We will make horizontal bar charts with individual points overlaid
        y_pos = np.array([3, 2, 1, 0])
        labels = ['Non_SMK', 'SMK', 'Non_SMK+abx', 'SMK+abx']
        bar_colors = [colors[l] for l in labels]
        
        # Fake iAUC data
        bar_means = np.random.randint(20, max_val, 4)
        ax_in.barh(y_pos, bar_means, color='white', edgecolor='black', height=0.6)
        
        # Overlay points
        for i, (label, color) in enumerate(zip(labels, bar_colors)):
            points_x = bar_means[i] + np.random.randn(8) * (max_val * 0.05)
            points_y = y_pos[i] + np.random.randn(8) * 0.1
            ax_in.scatter(points_x, points_y, color=color, s=20, alpha=0.8, zorder=3)
            
        # Draw significance brackets in the inset
        # Compare Non_SMK vs SMK
        m0, m1 = bar_means[0], bar_means[1]
        line_x = max(m0, m1) + max_val * 0.15
        ax_in.plot([line_x, line_x], [y_pos[0], y_pos[1]], color='black', lw=1)
        ax_in.text(line_x + max_val * 0.02, (y_pos[0] + y_pos[1])/2, '****', va='center', ha='left', rotation=-90)
        
        # Compare Non_SMK+abx vs SMK+abx
        m2, m3 = bar_means[2], bar_means[3]
        line_x2 = max(m2, m3) + max_val * 0.15
        ax_in.plot([line_x2, line_x2], [y_pos[2], y_pos[3]], color='black', lw=1)
        ax_in.text(line_x2 + max_val * 0.02, (y_pos[2] + y_pos[3])/2, '****', va='center', ha='left', rotation=-90)
            
        ax_in.set_yticks([])
        ax_in.set_xlim(0, max_val * 1.3)
        ax_in.spines['top'].set_visible(False)
        ax_in.spines['right'].set_visible(False)
        return ax_in

    # Left inset (Exposure)
    ax_in1 = create_inset([0.05, 0.65, 0.35, 0.3], 'iAUC: Exposure', 400)
    # Right inset (Cessation)
    ax_in2 = create_inset([0.55, 0.65, 0.35, 0.3], 'iAUC: Cessation', 400)
    
    # Fill the right half background with a slightly darker grey
    ax.axvspan(20, 40, facecolor='#DDDDDD', alpha=0.5, zorder=0)

    # Adding significance brackets manually for the main plot
    # Line between top two at the right end
    x_bracket = 36.5
    ax.plot([x_bracket, x_bracket], [data['Non_SMK+abx'][0][-1], data['Non_SMK'][0][-1]], color='black', lw=1.5)
    ax.text(x_bracket+0.5, (data['Non_SMK+abx'][0][-1] + data['Non_SMK'][0][-1])/2, '****', ha='left', va='center', rotation=-90, fontsize=12)
    
    ax.plot([x_bracket, x_bracket], [data['Non_SMK'][0][-1], data['SMK'][0][-1]], color='black', lw=1.5)
    ax.text(x_bracket+0.5, (data['Non_SMK'][0][-1] + data['SMK'][0][-1])/2, '***', ha='left', va='center', rotation=-90, fontsize=12)
    
    ax.plot([x_bracket, x_bracket], [data['SMK'][0][-1], data['SMK+abx'][0][-1]], color='black', lw=1.5)
    ax.text(x_bracket+0.5, (data['SMK'][0][-1] + data['SMK+abx'][0][-1])/2, '****', ha='left', va='center', rotation=-90, fontsize=12)

    plt.tight_layout()
    plt.savefig('/Users/the-d/.gemini/antigravity/brain/d52f437c-6ca0-4617-8907-efca4c6f0b8c/demo_scientific_viz_2.png', dpi=300, bbox_inches='tight')
    print("Saved demo_scientific_viz_2.png")

if __name__ == "__main__":
    main()
