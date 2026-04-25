# Daily Merged Embodied AI Papers

- Generated at (UTC): 2026-04-25 09:40:23
- Window (UTC dates): 2026-04-23 to 2026-04-25
- Sources:
  - [Embodied-AI-Daily README](https://raw.githubusercontent.com/luohongk/Embodied-AI-Daily/main/README.md)
  - [arXiv cs.RO RSS](https://rss.arxiv.org/rss/cs.RO)
  - [awesome-daily-AI-arxiv Embodied_AI.md](https://raw.githubusercontent.com/Tavish9/awesome-daily-AI-arxiv/main/hot_topic/Embodied_AI.md)
- Dedupe key: canonical arXiv id (version suffix stripped)
- Unique papers: 16

## Source Stats

| Source | Raw Entries | After Filter |
| --- | ---: | ---: |
| Embodied-AI-Daily | 1407 | 10 |
| arXiv cs.RO RSS | 0 | 0 |
| awesome-daily-AI-arxiv | 12 | 12 |

## 1. ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures

- arXiv: `2604.21232`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.AI
- Matched Keywords: vision-language-action, vla
- Links: [abs](https://arxiv.org/abs/2604.21232) | [pdf](https://arxiv.org/pdf/2604.21232)
- Summary: Vision-Language-Action systems follow instructions to execute multi-step tasks in multimodal environments. Recent VLA approaches typically rely on post-hoc correction mechanisms or operate under fixed task decompositions and alignment schemes. However, once an intermediate step is mis-specified, local errors propagate through subsequent steps and eventually…

## 2. Long-Horizon Manipulation via Trace-Conditioned VLA Planning

- arXiv: `2604.21924`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.RO
- Matched Keywords: vision-language-action, vla, manipulation
- Links: [abs](https://arxiv.org/abs/2604.21924) | [pdf](https://arxiv.org/pdf/2604.21924)
- Summary: Long-horizon manipulation remains challenging for vision-language-action (VLA) policies: real tasks are multi-step, progress-dependent, and brittle to compounding execution errors. We present LoHo-Manip, a modular framework that scales short-horizon VLA execution to long-horizon instruction following via a dedicated task-management VLM. The manager is decou…
- Notes: Embodied-AI-Daily: Project page: https://www.liuisabella.com/LoHoManip

## 3. JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy

- arXiv: `2604.20100`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.RO
- Matched Keywords: vision-language-action, vla, foundation model, manipulation, robotic autonomy
- Links: [abs](https://arxiv.org/abs/2604.20100) | [pdf](https://arxiv.org/pdf/2604.20100)
- Summary: Robotic autonomy in open-world environments is fundamentally limited by insufficient data diversity and poor cross-embodiment generalization. Existing robotic datasets are often limited in scale and task coverage, while relatively large differences across robot embodiments impede effective behavior knowledge transfer. To address these challenges, we propose…

## 4. How VLAs (Really) Work In Open-World Environments

- arXiv: `2604.21192`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.RO, cs.AI
- Matched Keywords: vision-language-action, manipulation
- Links: [abs](https://arxiv.org/abs/2604.21192) | [pdf](https://arxiv.org/pdf/2604.21192)
- Summary: Vision-language-action models (VLAs) have been extensively used in robotics applications, achieving great success in various manipulation problems. More recently, VLAs have been used in long-horizon tasks and evaluated on benchmarks, such as BEHAVIOR1K (B1K), for solving complex household chores. The common metric for measuring progress in such benchmarks i…
- Notes: Embodied-AI-Daily: 8 pages, 7 figures, 2 tables

## 5. ExpressMM: Expressive Mobile Manipulation Behaviors in Human-Robot Interactions

- arXiv: `2604.05320`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.RO
- Matched Keywords: vision-language-action, mobile manipulation, manipulation
- Links: [abs](https://arxiv.org/abs/2604.05320) | [pdf](https://arxiv.org/pdf/2604.05320)
- Summary: Mobile manipulators are increasingly deployed in human-centered environments to perform tasks. While completing such tasks, they should also be able to communicate their intent to the people around them using expressive robot behaviors. Prior work on expressive robot behaviors has used preprogrammed or learning-from-demonstration-based expressive motions an…

## 6. CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors

- arXiv: `2604.21241`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`, `Embodied-AI-Daily`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`, `Embodied-AI-Daily: Vision Language Action`
- Categories: cs.RO, cs.AI
- Matched Keywords: vla
- Links: [abs](https://arxiv.org/abs/2604.21241) | [pdf](https://arxiv.org/pdf/2604.21241)
- Summary: Vision--Language--Action (VLA) models often use intermediate representations to connect multimodal inputs with continuous control, yet spatial guidance is often injected implicitly through latent features. We propose $CorridorVLA$, which predicts sparse spatial anchors as incremental physical changes (e.g., $Δ$-positions) and uses them to impose an explicit…

## 7. VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models

- arXiv: `2604.03956`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.CV, cs.AI
- Matched Keywords: vision-language-action, vla, foundation model, manipulation
- Links: [abs](https://arxiv.org/abs/2604.03956) | [pdf](https://arxiv.org/pdf/2604.03956)
- Summary: Vision-language-action (VLA) models are emerging as embodied foundation models for robotic manipulation, but their deployment introduces a new unlearning challenge: removing unsafe, spurious, or privacy-sensitive behaviors without degrading perception, language grounding, and action control. In OpenVLA-style policies, behavior is produced through a fused vi…

## 8. Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics

- arXiv: `2604.21017`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.RO, cs.AI
- Matched Keywords: vision-language-action, world model, foundation model, robot learning, manipulation, medical robotics
- Links: [abs](https://arxiv.org/abs/2604.21017) | [pdf](https://arxiv.org/pdf/2604.21017)
- Summary: Autonomous medical robots hold promise to improve patient outcomes, reduce provider workload, democratize access to care, and enable superhuman precision. However, autonomous medical robotics has been limited by a fundamental data problem: existing medical robotic datasets are small, single-embodiment, and rarely shared openly, restricting the development o…

## 9. Navigating the Clutter: Waypoint-Based Bi-Level Planning for Multi-Robot Systems

- arXiv: `2604.21138`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.RO, cs.AI
- Matched Keywords: vla
- Links: [abs](https://arxiv.org/abs/2604.21138) | [pdf](https://arxiv.org/pdf/2604.21138)
- Summary: Multi-robot control in cluttered environments is a challenging problem that involves complex physical constraints, including robot-robot collisions, robot-obstacle collisions, and unreachable motions. Successful planning in such settings requires joint optimization over high-level task planning and low-level motion planning, as violations of physical constr…

## 10. Learning Physics from Pretrained Video Models: A Multimodal Continuous and Sequential World Interaction Models for Robotic Manipulation

- arXiv: `2603.00110`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.RO
- Matched Keywords: foundation model, manipulation
- Links: [abs](https://arxiv.org/abs/2603.00110) | [pdf](https://arxiv.org/pdf/2603.00110)
- Summary: The scarcity of large-scale robotic data has motivated the repurposing of foundation models from other modalities for policy learning. In this work, we introduce PhysGen (Learning Physics from Pretrained Video Generation Models), a scalable continuous and sequential world interaction framework that leverages autoregressive video generation to solve robotic…

## 11. Instance-level Visual Active Tracking with Occlusion-Aware Planning

- arXiv: `2604.21453`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.CV
- Matched Keywords: navigation
- Links: [abs](https://arxiv.org/abs/2604.21453) | [pdf](https://arxiv.org/pdf/2604.21453)
- Summary: Visual Active Tracking (VAT) aims to control cameras to follow a target in 3D space, which is critical for applications like drone navigation and security surveillance. However, it faces two key bottlenecks in real-world deployment: confusion from visually similar distractors caused by insufficient instance-level discrimination and severe failure under occl…

## 12. From Noise to Intent: Anchoring Generative VLA Policies with Residual Bridges

- arXiv: `2604.21391`
- Date: 2026-04-24
- Sources: `awesome-daily-AI-arxiv`
- Source Sections: `awesome-daily-AI-arxiv: Embodied_AI`
- Categories: cs.RO, cs.AI
- Matched Keywords: embodied intelligence, vla
- Links: [abs](https://arxiv.org/abs/2604.21391) | [pdf](https://arxiv.org/pdf/2604.21391)
- Summary: Bridging high-level semantic understanding with low-level physical control remains a persistent challenge in embodied intelligence, stemming from the fundamental spatiotemporal scale mismatch between cognition and action. Existing generative VLA policies typically adopt a "Generation-from-Noise" paradigm, which disregards this disparity, leading to represen…

## 13. WorldMark: A Unified Benchmark Suite for Interactive Video World Models

- arXiv: `2604.21686`
- Date: 2026-04-23
- Sources: `Embodied-AI-Daily`
- Source Sections: `Embodied-AI-Daily: World Model`
- Categories: N/A
- Matched Keywords: world model, world models, mapping
- Links: [abs](https://arxiv.org/abs/2604.21686) | [pdf](https://arxiv.org/pdf/2604.21686)
- Summary: Interactive video generation models such as Genie, YUME, HY-World, and Matrix-Game are advancing rapidly, yet every model is evaluated on its own benchmark with private scenes and trajectories, making fair cross-model comparison impossible. Existing public benchmarks offer useful metrics such as trajectory error, aesthetic scores, and VLM-based judgments, b…

## 14. Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training

- arXiv: `2604.21741`
- Date: 2026-04-23
- Sources: `Embodied-AI-Daily`
- Source Sections: `Embodied-AI-Daily: World Model`
- Categories: N/A
- Matched Keywords: world model, world models, manipulation
- Links: [abs](https://arxiv.org/abs/2604.21741) | [pdf](https://arxiv.org/pdf/2604.21741)
- Summary: Post-training is essential for turning pretrained generalist robot policies into reliable task-specific controllers, but existing human-in-the-loop pipelines remain tied to physical execution: each correction requires robot time, scene setup, resets, and operator supervision in the real world. Meanwhile, action-conditioned world models have been studied mai…
- Notes: Embodied-AI-Daily: Project Page: https://hi-wm.github.io/

## 15. EgoExo++: Integrating On-demand Exocentric Visuals with 2.5D Ground Surface Estimation for Interactive Teleoperation of Underwater ROVs

- arXiv: `2407.00848`
- Date: 2026-04-23
- Sources: `Embodied-AI-Daily`
- Source Sections: `Embodied-AI-Daily: Visual SLAM`
- Categories: N/A
- Matched Keywords: navigation, slam, visual slam, teleoperation
- Links: [abs](https://arxiv.org/abs/2407.00848) | [pdf](https://arxiv.org/pdf/2407.00848)
- Summary: Underwater ROVs (Remotely Operated Vehicles) are indispensable for subsea exploration and task execution, yet typical teleoperation engines based on egocentric (first-person) video feeds restrict human operators' field-of-view and limit precise maneuvering in complex, unstructured underwater environments. To address this, we first propose EgoExo, a geometry…
- Notes: Embodied-AI-Daily: EgoExo++ (Accepted in IJRR), V6/V2, metadata updated, 15 pages

## 16. E3VS-Bench: A Benchmark for Viewpoint-Dependent Active Perception in 3D Gaussian Splatting Scenes

- arXiv: `2604.17969`
- Date: 2026-04-23
- Sources: `Embodied-AI-Daily`
- Source Sections: `Embodied-AI-Daily: 3D Gaussian Splatting`
- Categories: N/A
- Matched Keywords: embodied ai, 3d gaussian splatting, gaussian splatting
- Links: [abs](https://arxiv.org/abs/2604.17969) | [pdf](https://arxiv.org/pdf/2604.17969)
- Summary: Visual search in 3D environments requires embodied agents to actively explore their surroundings and acquire task-relevant evidence. However, existing visual search and embodied AI benchmarks, including EQA, typically rely on static observations or constrained egocentric motion, and thus do not explicitly evaluate fine-grained viewpoint-dependent phenomena…
- Notes: Embodied-AI-Daily: Project page: https://k0uya.github.io/e3vs-proj/
