# Civic-Tech Corpus

Snapshots of open-source civic-technology repositories, crawled with
[civic-tech-crawler](https://github.com/Japskua/civic-tech-git-crawler). Each
snapshot folder is self-contained: aggregate CSVs, `full_results.json`, one
folder per repository, statistical / weekly-activity / AI-usage analyses,
figures, and a written analysis.

The tool lives in its own repository; this repository holds data only.

## Snapshots

| Snapshot | Crawled | n | Crawler | Archived copy | Used in |
|---|---|---|---|---|---|
| [`2026_06/`](2026_06/) | 2026-06-03 – 06-04 | 55 | [1.2](https://github.com/Japskua/civic-tech-git-crawler/tree/1.2) | Zenodo v1.0, [10.5281/zenodo.20497015](https://doi.org/10.5281/zenodo.20497015) (git tag `2026_06-v1.0`) | Olshanskaia et al., GoodIT '26 ([10.1145/3794786.3830780](https://doi.org/10.1145/3794786.3830780)) |
| [`2026_05/`](2026_05/) | 2026-05-21 – 05-24 | 55 | [1.0](https://github.com/Japskua/civic-tech-git-crawler/tree/1.0); filtered to n=55 in [1.2](https://github.com/Japskua/civic-tech-git-crawler/tree/1.2) | Not on Zenodo (record 10.5281/zenodo.20493288 was removed) | — |

Concept DOI for all Zenodo versions (always resolves to the latest):
[10.5281/zenodo.20493287](https://doi.org/10.5281/zenodo.20493287).

## Freezing policy

- **Published snapshots are immutable.** A git tag `<snapshot>-v<version>`
  marks exactly the content archived on Zenodo under that version DOI. The
  `2026_06-v1.0` tag is byte-identical to the Zenodo v1.0 archive.
- **Corrections** are made as normal commits and released as a new Zenodo
  version. Every change is listed in the changelog below, so nothing is edited
  silently.
- **New crawls** go in a new `YYYY_MM/` folder.
- **Packaged zips are not committed**; they are uploaded to Zenodo only.

## Changelog

### Unreleased (candidate for 2026_06 v1.1)

Corrections to the written analyses and one provenance file; no data files
changed.

- `2026_06/crawl_2026_06.log` added: the full log of the 2026-06 crawl. It
  records, among other things, which repositories needed the commit-history
  fallback because GitHub's `/stats/commit_activity` returned nothing (50 of
  55). It contains no tokens or e-mail addresses.
- `2026_06/analysis_n55.md`: the dataset totals still described the earlier
  n=56 corpus. Corrected to 23 organisations (was 24), 90,468 commits
  (90,669), 660 contributors with 606 human (661 / 607), and 16 primary
  languages (17). The team-size vs. concentration correlation is ρ = −0.75
  (was −0.76).
- `2026_05/analysis_n55.md`: 23 organisations (was 24) and four continents
  (was five). The bus factor vs. HHI correlation has p = 2.3 × 10⁻¹¹ (was
  1.5 × 10⁻¹¹). Burstiness is available for all 55 repositories; the n = 34
  limit applies only to the burstiness vs. stale-issue test.

### 2026_06-v1.0 — 2026-06-01

Initial Zenodo release of the 2026-06 snapshot,
[10.5281/zenodo.20497015](https://doi.org/10.5281/zenodo.20497015).
The 2026-05 snapshot is included as it stood at civic-tech-crawler tag 1.2.

## Citing

Please cite both the dataset and the tool that produced it:

- Parkkila, J., Tran, D. T., Olshanskaia, V., Knutas, A. (2026).
  *Civic-Tech Corpus 06/2026* (v1.0). Zenodo.
  <https://doi.org/10.5281/zenodo.20497015>
- *civic-tech-crawler*: <https://github.com/Japskua/civic-tech-git-crawler>
  (see that repository's `CITATION.cff`).

## License

MIT, matching the Zenodo record. See [`LICENSE`](LICENSE).
