import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json

def create_monte_carlo_figure(json_path, output_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    episodes = data['episodes']
    
    b1_top1 = [ep['baseline_1_flat']['accuracy_top1'] for ep in episodes]
    b2_top1 = [ep['baseline_2_rigid_13species']['accuracy_top1'] for ep in episodes]
    mp_top1 = [ep['morphopath_edge']['accuracy_top1'] for ep in episodes]

    b1_top2 = [ep['baseline_1_flat']['accuracy_top2'] for ep in episodes]
    b2_top2 = [ep['baseline_2_rigid_13species']['accuracy_top2'] for ep in episodes]
    mp_top2 = [ep['morphopath_edge']['accuracy_top2'] for ep in episodes]

    b1_fpr = [ep['baseline_1_flat']['fpr'] for ep in episodes]
    b2_fpr = [ep['baseline_2_rigid_13species']['fpr'] for ep in episodes]
    mp_fpr = [ep['morphopath_edge']['fpr'] for ep in episodes]

    b2_router = [ep['baseline_2_rigid_13species']['router_top1_accuracy'] for ep in episodes]
    mp_router = [ep['morphopath_edge']['router_top1_accuracy'] for ep in episodes]

    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.8), dpi=300)
    plt.subplots_adjust(wspace=0.28, bottom=0.20, top=0.84, left=0.06, right=0.98)

    colors = ['#7F8C8D', '#E74C3C', '#27AE60']
    models_3 = ['Flat Metric\n(Baseline 1)', 'Rigid Router\n(Baseline 2)', 'MorphoPath\n(Proposed)']
    
    np.random.seed(42)

    def style_box(ax, data_list, labels, palette, ylabel, title, y_lim=None):
        bp = ax.boxplot(data_list, patch_artist=True, tick_labels=labels, widths=0.55,
                        showmeans=True, meanline=False,
                        meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='white', markersize=6),
                        medianprops=dict(color='black', linewidth=1.8),
                        whiskerprops=dict(color='#555555', linewidth=1.2),
                        capprops=dict(color='#555555', linewidth=1.2),
                        flierprops=dict(marker='o', markersize=3, alpha=0.5))
        
        for patch, color in zip(bp['boxes'], palette):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_edgecolor('black')
            patch.set_linewidth(1.2)

        # Overlay jittered points
        for i, d in enumerate(data_list):
            x = np.random.normal(i + 1, 0.04, size=len(d))
            ax.plot(x, d, 'k.', alpha=0.35, markersize=4.5)

        ax.set_ylabel(ylabel, fontsize=9.5, fontweight='bold', color='#2C3E50')
        ax.set_title(title, fontsize=10, fontweight='bold', color='#2C3E50', pad=10)
        ax.grid(axis='y', linestyle='--', alpha=0.45)
        if y_lim:
            ax.set_ylim(y_lim)
        ax.tick_params(axis='x', labelsize=8.5)
        ax.tick_params(axis='y', labelsize=8.5)

    def draw_bracket(ax, x1, x2, y, h, text):
        ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.2, c='#2C3E50')
        ax.text((x1 + x2) * 0.5, y + h + 0.3, text, ha='center', va='bottom',
                color='#1B2631', fontsize=7.5, fontweight='bold')

    # 1. Top-1 Accuracy
    style_box(axes[0], [b1_top1, b2_top1, mp_top1], models_3, colors,
              "Top-1 Diagnostic Accuracy (%)", "(a) In-the-Wild Top-1 Accuracy", y_lim=[42, 69])
    draw_bracket(axes[0], 2, 3, 63.8, 0.8, r"+11.84% ($p < 10^{-20}$)")
    draw_bracket(axes[0], 1, 3, 66.2, 0.8, r"+6.42% ($p < 10^{-14}$)")

    # 2. Top-2 Accuracy
    style_box(axes[1], [b1_top2, b2_top2, mp_top2], models_3, colors,
              "Top-2 Differential Triage (%)", "(b) Top-2 Differential Triage", y_lim=[58, 87])
    draw_bracket(axes[1], 2, 3, 82.2, 0.8, r"+11.52% ($p < 10^{-20}$)")
    draw_bracket(axes[1], 1, 3, 84.4, 0.8, r"+6.48% ($p < 10^{-18}$)")

    # 3. Clinical FPR (Healthy misdiagnosed as diseased)
    style_box(axes[2], [b2_fpr, b1_fpr, mp_fpr],
              ['Rigid Router\n(Baseline 2)', 'Flat Metric\n(Baseline 1)', 'MorphoPath\n(Proposed)'],
              ['#E74C3C', '#7F8C8D', '#27AE60'],
              "False Positive Rate (FPR, %)", "(c) Chemical Mis-Spray Risk (FPR)", y_lim=[6, 32])
    draw_bracket(axes[2], 1, 3, 28.5, 0.8, r"-38.1% Sprayed FPR ($p < 10^{-13}$)")

    # 4. Upstream Router Accuracy
    style_box(axes[3], [b2_router, mp_router],
              ['13-Species Router\n(Hierarchical)', '4-Archetype Router\n(MorphoPath)'],
              ['#E74C3C', '#27AE60'],
              "Upstream Routing Accuracy (%)", "(d) Upstream Routing Precision", y_lim=[75, 96])
    draw_bracket(axes[3], 1, 2, 93.3, 0.6, r"+12.04% Gain ($p < 10^{-29}$)")

    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print(f"Monte Carlo figure generated successfully at: {output_path}")

if __name__ == '__main__':
    create_monte_carlo_figure(
        'experiments/phase3_morphopath/monte_carlo_30ep_results.json',
        'paper_morphopath/figures/fig_monte_carlo.png'
    )
