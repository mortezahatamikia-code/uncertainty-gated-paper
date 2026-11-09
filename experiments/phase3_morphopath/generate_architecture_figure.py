import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram(output_path):
    fig = plt.figure(figsize=(15.5, 5.0), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 155)
    ax.set_ylim(0, 52)
    ax.axis('off')

    c_border_group = '#BDC3C7'
    c_in = '#34495E'
    c_dino = '#1E8449'
    c_bio = '#D35400'
    c_trans = '#6C3483'
    c_rect = '#00838F'
    c_arch = '#C0392B'
    c_fisher = '#2471A3'
    c_triage = '#196F3D'
    c_text = '#2C3E50'

    def draw_box(x, y, w, h, bg_color, border_color, title, subtitle="", radius=1.0, lw=1.3, title_color='white', sub_color='#333333', title_fs=9.2, sub_fs=7.5):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                                     facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=2)
        ax.add_patch(box)
        if title:
            ax.text(x + w/2, y + h - (1.6 if subtitle else h/2), title, ha='center', va='center',
                    fontsize=title_fs, fontweight='bold', color=title_color, zorder=3)
        if subtitle:
            ax.text(x + w/2, y + h/2 - 0.7, subtitle, ha='center', va='center',
                    fontsize=sub_fs, color=sub_color, zorder=3, linespacing=1.15)

    def draw_group(x, y, w, h, title, border_c=c_border_group, bg_c='#FAFAFA'):
        grp = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.2",
                                     facecolor=bg_c, edgecolor=border_c, linewidth=1.1, linestyle='--', zorder=1)
        ax.add_patch(grp)
        ax.text(x + 2.0, y + h - 1.0, title, ha='left', va='center',
                fontsize=8.8, fontweight='bold', color='#5D6D7E', zorder=2)

    def draw_arrow(x1, y1, x2, y2, color='#7F8C8D', lw=1.8, style='-|>', rad=0.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                    shrinkA=1, shrinkB=1,
                                    connectionstyle=f"arc3,rad={rad}"), zorder=4)

    # Stage 1: Field Input
    draw_group(2, 3, 18, 46, "Stage 1: Field Input")
    draw_box(4, 25, 14, 20, '#EAEDED', '#95A5A6', "Unconstrained\nField Imagery",
             "• Specular Glare\n• Complex Clutter\n• Compound Leaves\n• Domain Shift",
             radius=0.7, title_color=c_in, sub_color='#2C3E50', title_fs=8.8, sub_fs=7.2)
    
    leaf_patch = patches.Ellipse((11, 14), 7, 12, angle=25, facecolor='#A9DFBF', edgecolor='#27AE60', lw=1.8, zorder=3)
    ax.add_patch(leaf_patch)
    lesion1 = patches.Circle((10.5, 15.5), 1.2, facecolor='#BA4A00', edgecolor='#7E5109', lw=1.0, zorder=4)
    lesion2 = patches.Circle((12, 11.5), 0.9, facecolor='#E67E22', edgecolor='#7E5109', lw=0.9, zorder=4)
    ax.add_patch(lesion1)
    ax.add_patch(lesion2)
    ax.text(11, 5.5, r"$x \in \mathcal{X} \subset \mathbb{R}^{H \times W \times 3}$", ha='center', fontsize=7.8, color=c_text, zorder=4)

    draw_arrow(20, 27, 24, 37, color='#566573', lw=1.8)
    draw_arrow(20, 27, 24, 15, color='#566573', lw=1.8)

    # Stage 2: Dual-Stream Decoupled Models
    draw_group(24, 3, 25, 46, "Stage 2: Decoupled Foundation Models")
    draw_box(26, 27, 21, 19, '#E8F8F5', c_dino, "Frozen DINOv2\n(ViT-S/14 INT8)",
             "Macroscopic Organ Geometry\nVenation & Margin Contours\n$z_{\\mathrm{dino}} \\in \\mathbb{R}^{384}$\n40.7 ms, Zero Tuning",
             radius=0.7, title_color=c_dino, sub_color='#145A32', title_fs=8.8, sub_fs=7.2)
    draw_box(26, 5, 21, 19, '#FEF9E7', c_bio, "Frozen BioCLIP\n(ViT-B/16 INT8)",
             "Microscopic Lesions\nChlorosis & Necrotic Spots\n$z_{\\mathrm{bio}} \\in \\mathbb{R}^{512}$\n71.0 ms, Taxonomic Prior",
             radius=0.7, title_color=c_bio, sub_color='#7E5109', title_fs=8.8, sub_fs=7.2)

    draw_arrow(47, 36.5, 52, 27, color='#566573', lw=1.8)
    draw_arrow(47, 14.5, 52, 23, color='#566573', lw=1.8)
    draw_arrow(47, 41, 83, 42, color=c_dino, lw=2.0, rad=-0.1)
    ax.text(64, 45.5, r"Geometry Features $z_{\mathrm{dino}}$ for Routing", fontsize=7.5, color=c_dino, fontweight='bold', ha='center')

    # Stage 3: Normalization & Rectification
    draw_group(52, 3, 28, 46, "Stage 3: Manifold Rectification")
    draw_box(54, 16, 24, 16, '#F4ECF7', c_trans, "Joint Embedding &\nTukey Power Transform",
             r"$z_{\mathrm{joint}} = [z_{\mathrm{bio}}^\top, z_{\mathrm{dino}}^\top]^\top \in \mathbb{R}^{896}$" + "\n" +
             r"$z_{\mathrm{tukey}} = \mathrm{sign}(z)|z|^{0.5}$" + "\n" +
             r"$\hat{z} = z_{\mathrm{tukey}} / \|z_{\mathrm{tukey}}\|_2 \in \mathbb{S}^{D-1}$",
             radius=0.7, title_color=c_trans, sub_color='#512E5F', title_fs=8.5, sub_fs=7.0)

    draw_box(54, 34, 24, 12, '#E0F7FA', c_rect, "Test-Time Centering (ADR-005)",
             r"$\tilde{z} = (\hat{z} - \mu) / \|\hat{z} - \mu\|_2$" + "\n" +
             r"$\mathbb{E}[\tilde{z}_q] - \mathbb{E}[\tilde{z}_s] = \mathbf{0}$" + "\n" +
             r"Cancels $\|\Delta\|_2 \approx 0.30$ in 0.04 ms",
             radius=0.7, title_color=c_rect, sub_color='#006064', title_fs=8.3, sub_fs=6.8)
    draw_arrow(66, 32, 66, 34, color=c_trans, lw=1.6)

    draw_box(54, 5, 24, 9, '#FFFFFF', '#BDC3C7', "Online Streaming Buffer",
             r"$\mu_q^{(t)} = (1-\gamma)\mu_q^{(t-1)} + \gamma \hat{z}_q^{(t)}$" + "\n" +
             r"Zero backprop | RAM: 66.9 MB",
             radius=0.5, title_color='#5D6D7E', sub_color='#333333', title_fs=7.8, sub_fs=6.8)
    draw_arrow(66, 16, 66, 14, color='#BDC3C7', lw=1.4)
    draw_arrow(78, 40, 83, 28, color=c_rect, lw=1.8)

    # Stage 4: 4 Archetypes & Shrunk Metric
    draw_group(83, 3, 38, 46, "Stage 4: Archetype Routing & Conditioned Fisher Metric")
    draw_box(85, 34, 34, 13, '#FDEDEC', c_arch, "4 Macro-Botanical Archetypes Router",
             r"$P(A_k \mid x) = \frac{\exp(T \cdot \cos(\mathrm{norm}(z_{\mathrm{dino}}), \mu_{A_k}))}{\sum_j \exp(T \cdot \cos(\dots))}$" + "\n" +
             r"$\mathbf{A_0}$: Solanoid | $\mathbf{A_1}$: Vitoid | $\mathbf{A_2}$: Pooid | $\mathbf{A_3}$: Rosoid" + "\n" +
             r"Routing Accuracy: $\mathbf{93.25\%}$ (100% Top-2 Recall)",
             radius=0.7, title_color=c_arch, sub_color='#78281F', title_fs=8.5, sub_fs=6.8)

    draw_box(85, 18, 34, 14, '#EBF5FB', c_fisher, "Intra-Archetype Shrunk Fisher LDA (ADR-002)",
             r"Ledoit-Wolf: $\Sigma_{\mathrm{shrunk}}^{(k)} = (1-\lambda)\Sigma_w^{(k)} + \lambda \frac{\mathrm{Tr}(\Sigma_w^{(k)})}{D}I$" + "\n" +
             r"Condition number drops $\infty \to 1428$ ($\lambda=0.60$)" + "\n" +
             r"$P_{\mathrm{vis}}(c \mid x, A_k) \propto \exp\left(-\frac{1}{2}(u - P_c)^\top \Sigma^{-1} (u - P_c)\right)$",
             radius=0.7, title_color=c_fisher, sub_color='#1B4F72', title_fs=8.2, sub_fs=6.7)

    draw_box(85, 5, 34, 11, '#FEF9E7', '#B7950B', "Micro-Symptom Prompt Ensemble (ADR-004)",
             r"BioCLIP Text Prompts: $T_c = \mathrm{norm}\left(\frac{1}{M}\sum g_{\mathrm{text}}(t_{c,m})\right)$" + "\n" +
             r"Convex Fusion: $P_{\mathrm{comb}} = w_{\mathrm{vis}}P_{\mathrm{vis}} + (1-w_{\mathrm{vis}})P_{\mathrm{text}}$",
             radius=0.6, title_color='#7D6608', sub_color='#7D6608', title_fs=8.0, sub_fs=6.7)

    draw_arrow(102, 34, 102, 32, color=c_arch, lw=1.6)
    draw_arrow(102, 16, 102, 18, color='#B7950B', lw=1.6)
    draw_arrow(119, 25, 124, 25, color='#2C3E50', lw=2.0)

    # Stage 5: Bayesian Differential Triage
    draw_group(124, 3, 29, 46, "Stage 5: Differential Triage Engine")
    draw_box(126, 32, 25, 14.5, '#E8F5E9', c_triage, "Cardinality Equalization\n(ADR-003)",
             r"$\mathrm{Score}(c \mid x) = P(A_k \mid x) \cdot [K_{A_k} P_{\mathrm{comb}}]^\alpha$" + "\n" +
             r"Compensates $K_{A_k}$ partition bias" + "\n" +
             r"$\Delta \mathrm{Top\text{-}1}: +3.97\%$, $\Delta \mathrm{Top\text{-}2}: +5.16\%$",
             radius=0.7, title_color=c_triage, sub_color='#145A32', title_fs=8.5, sub_fs=6.8)

    draw_box(126, 14, 25, 16, '#F2F4F4', c_in, "Calibrated Dual Triage\nClinical Diagnosis",
             r"$\mathbf{\hat{c}_1} = \arg\max_c \mathrm{Score}(c \mid x)$" + "\n" +
             r"$\mathbf{\hat{c}_2} = \arg\max_{c \ne \hat{c}_1} \mathrm{Score}(c \mid x)$" + "\n\n" +
             r"$\mathbf{80.95\%}$ Top-2 Field Accuracy" + "\n" +
             r"$\mathbf{-38.0\%}$ Reduction in Sprayed FPR",
             radius=0.7, title_color=c_in, sub_color='#1A5276', title_fs=8.5, sub_fs=7.0)

    draw_arrow(138.5, 32, 138.5, 30, color=c_triage, lw=1.6)

    draw_box(126, 5, 25, 7.0, '#D5F5E3', '#27AE60', "",
             "Real-Time: 18.66 FPS | 53.6 ms CPU\nEdge APK: 22.88 MB | 0 Learned Weights",
             radius=0.5, title_color='#196F3D', sub_color='#145A32', title_fs=7.5, sub_fs=7.2)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.03)
    plt.close()
    print(f"Compact architecture diagram generated at: {output_path}")

if __name__ == '__main__':
    create_architecture_diagram('paper_morphopath/figures/fig_architecture.png')
