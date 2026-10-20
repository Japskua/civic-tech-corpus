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

Cite the version DOI shown for each snapshot. Do not use Zenodo concept DOI
10.5281/zenodo.20493287 for the dataset: the civic-tech-crawler software
releases are filed under the same concept, so it resolves to the latest
software release.

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

No changes to the 2026_06 data files.

- Pointers to the archived version used in GoodIT '26. `2026_06/README.md`
  (Versioning, How to cite) and `2026_06/CITATION.cff` now name Zenodo version
  1.0 (10.5281/zenodo.20497015), git tag `2026_06-v1.0`, crawler release 1.2, and
  the GoodIT '26 paper that used it. Before, the README said the snapshot was
  still to be deposited under the concept DOI, and `CITATION.cff` had a DOI
  placeholder and a URL to the dataset's old location in the tool repository.
  The `CITATION.cff` abstract's organisation count is corrected from 24 to 23.
  The root `CITATION.cff` names all four crawler authors and release 1.2.
- `2026_06/README.md`: new data-quality caveat. `codeforjapan/BirdXplorer` has no
  CHAOSS, core-periphery, or issue data, because the full crawl reused a cached
  result from a test run that skipped those collectors. The four affected tables
  are named; everything else for the repository is complete. The crawler bug
  behind it is fixed in civic-tech-crawler 1.3.1.
- `2026_06/README.md`: the reproduction steps still used the layout from before
  the data left the tool repository (an unpublished `config.yaml` and a
  `datasets/2026_06` folder). They now check out civic-tech-crawler tag 1.2
  and run its `config.example.yaml`, which lists exactly the 55 repositories.
  The organisation count is corrected from 24 to 23 in both tables, matching
  `analysis_n55.md`.
- Licence metadata corrected to **MIT**, the licence on the Zenodo record.
  `2026_06/CITATION.cff`, `2026_06/.zenodo.json`, and `2026_06/README.md`
  had stated CC-BY-4.0 in error. A root `LICENSE` file is added.
- `2026_05/` removed. It was an earlier internal crawl that will not be
  published; it remains in this repository's history and in
  civic-tech-git-crawler up to tag 1.2. Links to it from `2026_06/` were
  replaced with plain text (they were already dead inside the Zenodo archive).
- `2026_06/ai_signals_audit.csv` and `ai_signals_audit.py` added: every one of
  the 94 rows in `ai_signals.csv` checked against the repositories as they stood
  at crawl time. 91 are true positives and 1 is a false positive: a PR body
  generated with Claude Code that mentions a database "cursor" was also credited
  to the Cursor editor. 2 cannot be checked because their repository has since
  been removed. Precision is therefore 98.9 % (91 of 92). Recall is not measured.
  Each row records the verdict, how it was checked, and an evidence excerpt.
- `2026_06/crawl_2026_06.log` added: the full log of the 2026-06 crawl. It
  records, among other things, which repositories needed the commit-history
  fallback because GitHub's `/stats/commit_activity` returned nothing (50 of
  55). It contains no tokens or e-mail addresses.
- `2026_06/analysis_n55.md`: the dataset totals still described the earlier
  n=56 corpus. Corrected to 23 organisations (was 24), 90,468 commits
  (90,669), 660 contributors with 606 human (661 / 607), and 16 primary
  languages (17). The team-size vs. concentration correlation is ρ = −0.75
  (was −0.76).

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
