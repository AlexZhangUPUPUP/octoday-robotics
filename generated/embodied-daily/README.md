# Generated Daily Embodied Paper Merge

This directory stores the daily merged embodied-AI paper feed built from three public sources.

Sources:
- [Embodied-AI-Daily README](https://raw.githubusercontent.com/luohongk/Embodied-AI-Daily/main/README.md)
- [arXiv cs.RO RSS](https://rss.arxiv.org/rss/cs.RO)
- [awesome-daily-AI-arxiv Embodied_AI.md](https://raw.githubusercontent.com/Tavish9/awesome-daily-AI-arxiv/main/hot_topic/Embodied_AI.md)

Outputs:
- `daily/latest.md`: merged markdown snapshot
- `daily/latest.json`: merged JSON snapshot
- `daily/candidates-for-03-papers.md`: candidate list for `03-papers.md`

Deduplication rule:
- Papers are deduped by canonical arXiv id with the version suffix removed.

Generation script:
- `scripts/update_embodied_daily_sources.py`
