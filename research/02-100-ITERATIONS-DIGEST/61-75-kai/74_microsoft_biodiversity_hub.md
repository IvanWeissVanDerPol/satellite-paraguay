[Skip to content](https://github.com/microsoft/Biodiversity#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/microsoft/Biodiversity) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/microsoft/Biodiversity) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/microsoft/Biodiversity) to refresh your session.Dismiss alert

{{ message }}

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/microsoft/Biodiversity).

[microsoft](https://github.com/microsoft)/ **[Biodiversity](https://github.com/microsoft/Biodiversity)** Public

- [Notifications](https://github.com/login?return_to=%2Fmicrosoft%2FBiodiversity) You must be signed in to change notification settings
- [Fork\\
298](https://github.com/login?return_to=%2Fmicrosoft%2FBiodiversity)
- [Star\\
1.1k](https://github.com/login?return_to=%2Fmicrosoft%2FBiodiversity)


main

[**40** Branches](https://github.com/microsoft/Biodiversity/branches) [**11** Tags](https://github.com/microsoft/Biodiversity/tags)

[Go to Branches page](https://github.com/microsoft/Biodiversity/branches)[Go to Tags page](https://github.com/microsoft/Biodiversity/tags)

Go to file

Code

Open more actions menu

## Latest commit

[![zhmiao](https://avatars.githubusercontent.com/u/7812475?v=4&size=40)](https://github.com/zhmiao)[Zhongqi Miao (zhmiao)](https://github.com/microsoft/Biodiversity/commits?author=zhmiao)

[Merge pull request](https://github.com/microsoft/Biodiversity/commit/d3e0a0697167bb859a6f1c97b2e81344ff86c28a) [#661](https://github.com/microsoft/Biodiversity/pull/661) [from microsoft/fix/dependabot-alerts-20260812](https://github.com/microsoft/Biodiversity/commit/d3e0a0697167bb859a6f1c97b2e81344ff86c28a)

Open commit detailssuccess

2 weeks agoAug 19, 2026

[d3e0a06](https://github.com/microsoft/Biodiversity/commit/d3e0a0697167bb859a6f1c97b2e81344ff86c28a) · 2 weeks agoAug 19, 2026

## History

[3,921 Commits](https://github.com/microsoft/Biodiversity/commits/main/)

Open commit details

[View commit history for this file.](https://github.com/microsoft/Biodiversity/commits/main/) 3,921 Commits

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| [.github](https://github.com/microsoft/Biodiversity/tree/main/.github ".github") | [.github](https://github.com/microsoft/Biodiversity/tree/main/.github ".github") | [Pin GitHub Actions to full-length commit SHAs](https://github.com/microsoft/Biodiversity/commit/072f1c1972bc1d5321db3fe60625af6d0f8b4359 "Pin GitHub Actions to full-length commit SHAs") | 2 weeks agoAug 19, 2026 |
| [PW\_Bioacoustics](https://github.com/microsoft/Biodiversity/tree/main/PW_Bioacoustics "PW_Bioacoustics") | [PW\_Bioacoustics](https://github.com/microsoft/Biodiversity/tree/main/PW_Bioacoustics "PW_Bioacoustics") | [Update outdated CameraTraps references to Biodiversity](https://github.com/microsoft/Biodiversity/commit/39d9f07e713d3f83e0773069d01485e528c4e486 "Update outdated CameraTraps references to Biodiversity  Replace old microsoft/CameraTraps repository references with current microsoft/Biodiversity in: - mkdocs.yml repo_url and repo_name - PW_Bioacoustics README installation instructions  Aligns documentation with repository rename.  Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>") | 4 months agoMay 13, 2026 |
| [PW\_FT\_classification](https://github.com/microsoft/Biodiversity/tree/main/PW_FT_classification "PW_FT_classification") | [PW\_FT\_classification](https://github.com/microsoft/Biodiversity/tree/main/PW_FT_classification "PW_FT_classification") | [Merge pull request](https://github.com/microsoft/Biodiversity/commit/8abbad3afe15ac0dfbe446971fffd86b8eef8723 "Merge pull request #628 from bachdev/contribai/fix/security/insecure-yaml-deserialization-via-yaml-f  Security: Insecure YAML Deserialization via `yaml.FullLoader`") [#628](https://github.com/microsoft/Biodiversity/pull/628) [from bachdev/contribai/fix/security/insecure-…](https://github.com/microsoft/Biodiversity/commit/8abbad3afe15ac0dfbe446971fffd86b8eef8723 "Merge pull request #628 from bachdev/contribai/fix/security/insecure-yaml-deserialization-via-yaml-f  Security: Insecure YAML Deserialization via `yaml.FullLoader`") | 4 months agoMay 24, 2026 |
| [PW\_FT\_detection](https://github.com/microsoft/Biodiversity/tree/main/PW_FT_detection "PW_FT_detection") | [PW\_FT\_detection](https://github.com/microsoft/Biodiversity/tree/main/PW_FT_detection "PW_FT_detection") | [fix(security): insecure yaml deserialization via `yaml.fullloader`](https://github.com/microsoft/Biodiversity/commit/e2550a02ba3723060e8bac7514cbc464f99e95f8 "fix(security): insecure yaml deserialization via `yaml.fullloader`  The application uses `yaml.load(f, Loader=yaml.FullLoader)` to parse a configuration file (`config`) whose path can be controlled by a command-line argument. While `FullLoader` is safer than the default `yaml.load` without a specified loader, it still allows the construction of arbitrary Python objects. If an attacker can provide a specially crafted malicious YAML file, this can lead to arbitrary code execution on the system where the application is run. This is a severe vulnerability as it allows an attacker to execute arbitrary code with the privileges of the running application.   Affected files: main.py, main.py  Signed-off-by: BachDEV <1437214+bachdev@users.noreply.github.com>") | 6 months agoMar 31, 2026 |
| [PytorchWildlife](https://github.com/microsoft/Biodiversity/tree/main/PytorchWildlife "PytorchWildlife") | [PytorchWildlife](https://github.com/microsoft/Biodiversity/tree/main/PytorchWildlife "PytorchWildlife") | [Merge pull request](https://github.com/microsoft/Biodiversity/commit/1cd46cffcd94c12c1da3b6b7cf908b69f11b18ce "Merge pull request #616 from jQuinRivero/fix/batch-classification-imagefolder-error  Fix batch classification TypeError when using data_path (#611)") [#616](https://github.com/microsoft/Biodiversity/pull/616) [from jQuinRivero/fix/batch-classification-ima…](https://github.com/microsoft/Biodiversity/commit/1cd46cffcd94c12c1da3b6b7cf908b69f11b18ce "Merge pull request #616 from jQuinRivero/fix/batch-classification-imagefolder-error  Fix batch classification TypeError when using data_path (#611)") | 4 months agoMay 24, 2026 |
| [demo](https://github.com/microsoft/Biodiversity/tree/main/demo "demo") | [demo](https://github.com/microsoft/Biodiversity/tree/main/demo "demo") | [fix: resolve Dependabot dependency alerts](https://github.com/microsoft/Biodiversity/commit/49f4e0a6ae82433594de17f8b08fa125a7332a2c "fix: resolve Dependabot dependency alerts  Raise Gradio and setuptools to patched release lines, remove the duplicate setuptools pin, and correct the invalid MegaDetector v6 dropdown default found while validating the Gradio 6 migration.  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com> Copilot-Session: 36ec7e53-a85b-4661-bc84-964b6efe7d86") | 3 weeks agoAug 12, 2026 |
| [docs](https://github.com/microsoft/Biodiversity/tree/main/docs "docs") | [docs](https://github.com/microsoft/Biodiversity/tree/main/docs "docs") | [Update collaborators list with jocotoco](https://github.com/microsoft/Biodiversity/commit/20f3a92e1ebc4415c7d5a29a497a0e6f1847ecd4 "Update collaborators list with jocotoco  Added jocotoco organization to the collaborators section.") | last monthAug 3, 2026 |
| [overrides](https://github.com/microsoft/Biodiversity/tree/main/overrides "overrides") | [overrides](https://github.com/microsoft/Biodiversity/tree/main/overrides "overrides") | [docs(seo): shared Lab Organization](https://github.com/microsoft/Biodiversity/commit/8010142c2d7087b5ae0fd9ddb86c72b1a2609198 "docs(seo): shared Lab Organization @id, inLanguage, twitter:image:alt; omit private Acoustic from ItemList") [@id](https://github.com/id) [, inLanguage, twitter:image:alt…](https://github.com/microsoft/Biodiversity/commit/8010142c2d7087b5ae0fd9ddb86c72b1a2609198 "docs(seo): shared Lab Organization @id, inLanguage, twitter:image:alt; omit private Acoustic from ItemList") | 3 months agoJun 3, 2026 |
| [.gitignore](https://github.com/microsoft/Biodiversity/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/microsoft/Biodiversity/blob/main/.gitignore ".gitignore") | [chore: add .DS\_Store and \*.code-workspace to .gitignore](https://github.com/microsoft/Biodiversity/commit/39e707b8626a320f03113e2e44ac0a350c1076ad "chore: add .DS_Store and *.code-workspace to .gitignore") | 4 months agoMay 14, 2026 |
| [Dockerfile](https://github.com/microsoft/Biodiversity/blob/main/Dockerfile "Dockerfile") | [Dockerfile](https://github.com/microsoft/Biodiversity/blob/main/Dockerfile "Dockerfile") | [harden grado serve and bump up python floor](https://github.com/microsoft/Biodiversity/commit/d7d03bd1ec74d37502f5bb3c1af6534a5ceac6a7 "harden grado serve and bump up python floor") | 2 months agoJul 10, 2026 |
| [LICENSE](https://github.com/microsoft/Biodiversity/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/microsoft/Biodiversity/blob/main/LICENSE "LICENSE") | [Update LICENSE to Microsoft public repo standards](https://github.com/microsoft/Biodiversity/commit/f900649887c9ceb0e149698ce5da306cdaa94b1a "Update LICENSE to Microsoft public repo standards  - Rename LICENSE.md to plain LICENSE file for GitHub recognition - Update copyright line from placeholder [2023] [Microsoft] to   standard Microsoft Corporation format - Aligns with current Microsoft public repository conventions - SECURITY.md already compliant with v0.0.9 standard  Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>") | 4 months agoMay 12, 2026 |
| [MANIFEST.in](https://github.com/microsoft/Biodiversity/blob/main/MANIFEST.in "MANIFEST.in") | [MANIFEST.in](https://github.com/microsoft/Biodiversity/blob/main/MANIFEST.in "MANIFEST.in") | [chore: fix mkdocstrings refs after localization/ reorg; include versi…](https://github.com/microsoft/Biodiversity/commit/50b4ff9db0217a25c0f13d4b201c7e044389bbf2 "chore: fix mkdocstrings refs after localization/ reorg; include version.txt in sdist  - Update seven mkdocstrings :::::: references in docs/base/models/detection/   herdnet*.md from PytorchWildlife.models.detection.herdnet.* to   PytorchWildlife.models.detection.localization.* to match the actual   module layout after the codebase-reorganization commit (98fda158).   Without this, 'mkdocs build' aborts with BuildError. - MANIFEST.in: include version.txt and README.md so source distributions   have everything setup.py needs (setup.py now reads version from   version.txt, so the sdist was failing to build a wheel without it).  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>") | 5 months agoApr 22, 2026 |
| [README.md](https://github.com/microsoft/Biodiversity/blob/main/README.md "README.md") | [README.md](https://github.com/microsoft/Biodiversity/blob/main/README.md "README.md") | [docs: link MegaDetector documentation site from the repo table](https://github.com/microsoft/Biodiversity/commit/b59f5bd1bde69770fa3f5989721169dafbddf052 "docs: link MegaDetector documentation site from the repo table  Add a link to the MegaDetector docs (https://microsoft.github.io/MegaDetector/) alongside the existing repo link, so readers reach the user guide directly.") | 4 months agoJun 2, 2026 |
| [SECURITY.md](https://github.com/microsoft/Biodiversity/blob/main/SECURITY.md "SECURITY.md") | [SECURITY.md](https://github.com/microsoft/Biodiversity/blob/main/SECURITY.md "SECURITY.md") | [Microsoft mandatory file](https://github.com/microsoft/Biodiversity/commit/0eac86e0103366b188212139978174eed23c8dfd "Microsoft mandatory file") | 3 years agoNov 22, 2023 |
| [citation.cff](https://github.com/microsoft/Biodiversity/blob/main/citation.cff "citation.cff") | [citation.cff](https://github.com/microsoft/Biodiversity/blob/main/citation.cff "citation.cff") | [chore: deploy workflow, citation.cff fix, and nav update](https://github.com/microsoft/Biodiversity/commit/c0d21d02a47470d20ea471d23c0673d29bca442c "chore: deploy workflow, citation.cff fix, and nav update  - Add .github/workflows/deploy-docs.yml for automatic docs deployment on push to main - Add docs-requirements.txt (lightweight MkDocs-only deps for CI) - Fix citation.cff: correct title, repository-code, add version/date-released, fix PyTorch-Wildlife keyword - Add build_mkdocs.md to nav under Contribute > Developer Guide") | 4 months agoMay 14, 2026 |
| [docs-requirements.txt](https://github.com/microsoft/Biodiversity/blob/main/docs-requirements.txt "docs-requirements.txt") | [docs-requirements.txt](https://github.com/microsoft/Biodiversity/blob/main/docs-requirements.txt "docs-requirements.txt") | [docs(seo): hub structured-data + social + self-hosted assets parity](https://github.com/microsoft/Biodiversity/commit/fa2661d33e15882054cd99824daf44b762e2eebb "docs(seo): hub structured-data + social + self-hosted assets parity  Brings the Biodiversity hub to the MegaDetector docs gold standard (infra layer):  - Add overrides/main.html: Organization JSON-LD + an ItemList of the cluster's   four documentation sites (the entity anchor tying the cluster together for   search), BreadcrumbList on interior pages, and a clean homepage <title>. - Add Open Graph + Twitter Card meta with a local share image. - Self-host favicon/logo and the homepage banner in docs/assets/ (drop the   cross-origin Zenodo requests on render-blocking assets). - Fix site_description and the homepage description: they described   PyTorch-Wildlife and carried the deprecated \"SPARROW Studio\" name; they now   describe the hub and target its umbrella keywords. - Add mkdocs-callouts and git-revision-date-localized plugins (+ deps) and set   fetch-depth: 0 in the docs deploy workflow so last-updated dates render.  Part of the cluster SEO-parity work (ADO Epic 506340).") | 3 months agoJun 3, 2026 |
| [megadetector.md](https://github.com/microsoft/Biodiversity/blob/main/megadetector.md "megadetector.md") | [megadetector.md](https://github.com/microsoft/Biodiversity/blob/main/megadetector.md "megadetector.md") | [Fix broken and legacy repo URLs](https://github.com/microsoft/Biodiversity/commit/577c91fe097b54f44262701faa64daa889174454 "Fix broken and legacy repo URLs  - github.com/microsoft/PytorchWildlife → Pytorch-Wildlife (correct dash) - github.com/microsoft/CameraTraps → Biodiversity (repo was renamed) - /content/CameraTraps-main path refs in Colab notebooks → Biodiversity-main") | 4 months agoMay 20, 2026 |
| [mkdocs.yml](https://github.com/microsoft/Biodiversity/blob/main/mkdocs.yml "mkdocs.yml") | [mkdocs.yml](https://github.com/microsoft/Biodiversity/blob/main/mkdocs.yml "mkdocs.yml") | [docs(seo): hub structured-data + social + self-hosted assets parity](https://github.com/microsoft/Biodiversity/commit/fa2661d33e15882054cd99824daf44b762e2eebb "docs(seo): hub structured-data + social + self-hosted assets parity  Brings the Biodiversity hub to the MegaDetector docs gold standard (infra layer):  - Add overrides/main.html: Organization JSON-LD + an ItemList of the cluster's   four documentation sites (the entity anchor tying the cluster together for   search), BreadcrumbList on interior pages, and a clean homepage <title>. - Add Open Graph + Twitter Card meta with a local share image. - Self-host favicon/logo and the homepage banner in docs/assets/ (drop the   cross-origin Zenodo requests on render-blocking assets). - Fix site_description and the homepage description: they described   PyTorch-Wildlife and carried the deprecated \"SPARROW Studio\" name; they now   describe the hub and target its umbrella keywords. - Add mkdocs-callouts and git-revision-date-localized plugins (+ deps) and set   fetch-depth: 0 in the docs deploy workflow so last-updated dates render.  Part of the cluster SEO-parity work (ADO Epic 506340).") | 3 months agoJun 3, 2026 |
| [requirements.txt](https://github.com/microsoft/Biodiversity/blob/main/requirements.txt "requirements.txt") | [requirements.txt](https://github.com/microsoft/Biodiversity/blob/main/requirements.txt "requirements.txt") | [fix: resolve Dependabot dependency alerts](https://github.com/microsoft/Biodiversity/commit/49f4e0a6ae82433594de17f8b08fa125a7332a2c "fix: resolve Dependabot dependency alerts  Raise Gradio and setuptools to patched release lines, remove the duplicate setuptools pin, and correct the invalid MegaDetector v6 dropdown default found while validating the Gradio 6 migration.  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com> Copilot-Session: 36ec7e53-a85b-4661-bc84-964b6efe7d86") | 3 weeks agoAug 12, 2026 |
| [setup.py](https://github.com/microsoft/Biodiversity/blob/main/setup.py "setup.py") | [setup.py](https://github.com/microsoft/Biodiversity/blob/main/setup.py "setup.py") | [fix: resolve Dependabot dependency alerts](https://github.com/microsoft/Biodiversity/commit/49f4e0a6ae82433594de17f8b08fa125a7332a2c "fix: resolve Dependabot dependency alerts  Raise Gradio and setuptools to patched release lines, remove the duplicate setuptools pin, and correct the invalid MegaDetector v6 dropdown default found while validating the Gradio 6 migration.  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com> Copilot-Session: 36ec7e53-a85b-4661-bc84-964b6efe7d86") | 3 weeks agoAug 12, 2026 |
| [version.txt](https://github.com/microsoft/Biodiversity/blob/main/version.txt "version.txt") | [version.txt](https://github.com/microsoft/Biodiversity/blob/main/version.txt "version.txt") | [release: bump to v1.3.0; add bioacoustics + OWL to docs](https://github.com/microsoft/Biodiversity/commit/dc4da1cf20c55b62a3726437921776e0c28d9f77 "release: bump to v1.3.0; add bioacoustics + OWL to docs  Version bump: - setup.py 1.2.4.2 -> 1.3.0 (matches version.txt) - release_notes.md: replace 1.2.4 entry with a 1.3.0 entry covering   Sparrow Studio beta, the bioacoustics module, OWL, and the PW-Engine   preview pointer. - past_releases.md: preserve the 1.2.4 entry at the top.  MkDocs content: - Add docs/bioacoustics.md under the Pytorch Wildlife nav (module   overview: CLI scripts, ResNetClassifier, demo notebook, projects   using it). - Add docs/model_zoo/bioacoustics.md under the Model Zoo nav   (MD_AudioBirds_V1 entry). - Add OWL-T and OWL-C rows to model_zoo/other_detectors.md. - mkdocs.yml nav entries for both new pages.  Note: license for OWL-T/OWL-C is set to MIT matching repo defaults; confirm before merge if that's not correct.  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>") | 5 months agoApr 22, 2026 |
| View all files |

## Repository files navigation

![A colorful banner illustrating various species of animals and plants in a natural environment, symbolizing biodiversity and the use of AI for conservation purposes.](https://camo.githubusercontent.com/83f75e2ecbaf157a47fb8cfbde6e97f7f01d3b6a75aca7ce73d2ef12122bbb45/68747470733a2f2f7a656e6f646f2e6f72672f7265636f7264732f32303034343638302f66696c65732f42696f6469766572736974795f42616e6e65722e706e67)

# Microsoft Biodiversity

[Permalink: Microsoft Biodiversity](https://github.com/microsoft/Biodiversity#microsoft-biodiversity)

**Open-source AI for biodiversity monitoring and conservation.**

Microsoft AI for Good Lab — camera-trap detection, bioacoustic analysis, species classification, field deployment.

Open-source AI for camera traps, bioacoustics, and wildlife monitoring

* * *

[![](https://camo.githubusercontent.com/d6bc2b26794002c24d023acaab01b6dbb953c57ab9cb80ba5b8aa2f2bd5de99a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d626c7565)](https://github.com/microsoft/Biodiversity/blob/main/LICENSE)[![](https://camo.githubusercontent.com/9eceea7844eb05402a9dd91ba0212487bb81d1034b9183c7f3e09b5686c6c777/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446973636f72642d4a6f696e5f75732d3538363546323f6c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.gg/TeEVxzaYtm)[![](https://camo.githubusercontent.com/420b8dc2619e4cd3f2d25295c1d8526a1eb93c7cdd99e3120c3a278e74b00399/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f63732d3532364346453f6c6f676f3d4d6174657269616c466f724d6b446f6373266c6f676f436f6c6f723d7768697465)](https://microsoft.github.io/Biodiversity/)[![](https://camo.githubusercontent.com/26e71264d628a8dd055f260912d95dd0fd06dac3b383df93356ba5c00f337fba/68747470733a2f2f7374617469632e706570792e746563682f62616467652f7079746f72636877696c646c696665)](https://pypi.org/project/PytorchWildlife)[![](https://camo.githubusercontent.com/90791dd325970df153b71dbb65c6f84c148d94d289638cc7a7de16319770ae12/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f25463025394625413425393725323048756767696e67253230466163652d44656d6f2d626c7565)](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife)[![](https://camo.githubusercontent.com/02f43f27385985a87e1b919df78e89b1cb72a3962b80fa10de906145af29e109/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f436f6c61622d44656d6f2d626c75653f6c6f676f3d476f6f676c65436f6c6162)](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing)

## 📣 Announcements

[Permalink: 📣 Announcements](https://github.com/microsoft/Biodiversity#-announcements)

### What we've been up to

[Permalink: What we've been up to](https://github.com/microsoft/Biodiversity#what-weve-been-up-to)

Our journey started with **MegaDetector** — a camera-trap animal detection model that became a widely adopted tool in the conservation community. Building on that foundation, we created **PyTorch-Wildlife** as a unified platform to host all of our AI for biodiversity work, bringing together detection, classification, and eventually much more.

Over time, our scope grew well beyond camera-trap imagery. We now have active work in bioacoustics, overhead animal detection, and edge computing for remote field deployments. As the ecosystem expanded, it became clear that keeping everything inside a single repository was working against us. Code was harder to find, harder to maintain, and harder to extend.

So we made a deliberate decision: break the work into focused, dedicated repositories — one per project — where the code in each repo is concentrated, the ownership is clear, and future contributors know exactly where to go. This repository is the hub that ties them together. PyTorch-Wildlife now lives at [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife), MegaDetector at [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector), and everything else is linked in the table below.

#### Previous versions:

[Permalink: Previous versions:](https://github.com/microsoft/Biodiversity#previous-versions)

- [Release notes](https://microsoft.github.io/Biodiversity/releases/release_notes/)

## Projects

[Permalink: Projects](https://github.com/microsoft/Biodiversity#projects)

| Repo | What it is |
| --- | --- |
| [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) | AI model for detecting animals, people, and vehicles in camera-trap imagery — where it all started ( [documentation](https://microsoft.github.io/MegaDetector/)) |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic AI for biodiversity monitoring — audio classification and species identification from sound |
| [microsoft/MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) | Camera-trap species classification fine-tuning — adapt classifiers to your own datasets and geographic regions |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Overhead imagery detection — point-based wildlife localization from aerial views |
| [microsoft/MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar) | Sonar-based wildlife detection — processing and feature detection in sidescan sonar imagery |
| [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) | The collaborative deep learning framework and model zoo for conservation AI |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch — AI edge device for remote field deployments |

## Cite us

[Permalink: Cite us](https://github.com/microsoft/Biodiversity#cite-us)

When citing work that uses any of the repositories under this umbrella, please cite:

- **Hernandez et al. 2024** — _Pytorch-Wildlife: A Collaborative Deep Learning Framework for Conservation_ — for any use of the PyTorch-Wildlife framework or models accessed through it
- **Beery, Morris, Yang 2019** — _Efficient Pipeline for Camera Trap Image Review_ — for any use of MegaDetector specifically

A `citation.cff` file is included in this repository for automated citation tools.

## Contributing

[Permalink: Contributing](https://github.com/microsoft/Biodiversity#contributing)

We welcome community contributions. See our [Contribution Guidelines](https://microsoft.github.io/Biodiversity/contribute/#how-to-participate) for how to participate.

## Community

[Permalink: Community](https://github.com/microsoft/Biodiversity#community)

Have questions or want to connect with the team? Join us on Discord: [![Discord](https://camo.githubusercontent.com/9eceea7844eb05402a9dd91ba0212487bb81d1034b9183c7f3e09b5686c6c777/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446973636f72642d4a6f696e5f75732d3538363546323f6c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.gg/TeEVxzaYtm)

A list of organizations using MegaDetector across global conservation work — six years of partnerships, from national parks to research universities to NGOs — is maintained on the [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) repository.

Important

If you would like to be added to this list or have any questions regarding MegaDetector and PyTorch-Wildlife, please [email us](https://github.com/microsoft/Biodiversity/blob/main/zhongqimiao@microsoft.com) or join us in our Discord channel: [![](https://camo.githubusercontent.com/7eee9a7daba632e10f28aabee6fe182fa21ecb18c66c5885de962e4a46554f4e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f616e795f746578742d4a6f696e5f7573212d626c75653f6c6f676f3d646973636f7264266c6162656c3d5079746f72636857696c64696665)](https://discord.gg/TeEVxzaYtm)

## About

[Permalink: About](https://github.com/microsoft/Biodiversity#about)

Maintained by [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/research/group/ai-for-good-research-lab/).

## About

Microsoft AI for Good Lab — Biodiversity research hub. Open-source AI models, edge devices, and tools for biodiversity monitoring and conservation. Your source for MegaDetector, SPARROW, PytorchWildlife, Bioacoustics, and more.

[microsoft.github.io/Biodiversity/](https://microsoft.github.io/Biodiversity/)

### Topics

[ai-for-good](https://github.com/topics/ai-for-good) [animal-detection](https://github.com/topics/animal-detection) [bioacoustics](https://github.com/topics/bioacoustics) [biodiversity](https://github.com/topics/biodiversity) [camera-traps](https://github.com/topics/camera-traps) [computer-vision](https://github.com/topics/computer-vision) [conservation](https://github.com/topics/conservation) [conservation-ai](https://github.com/topics/conservation-ai) [deep-learning](https://github.com/topics/deep-learning) [ecology](https://github.com/topics/ecology) [edge-ai](https://github.com/topics/edge-ai) [machine-learning](https://github.com/topics/machine-learning) [megadetector](https://github.com/topics/megadetector) [object-detection](https://github.com/topics/object-detection) [sparrow](https://github.com/topics/sparrow) [wildlife-detection](https://github.com/topics/wildlife-detection) [wildlife-monitoring](https://github.com/topics/wildlife-monitoring)

### Resources

[Readme](https://github.com/microsoft/Biodiversity#readme-ov-file)

[MIT license](https://github.com/microsoft/Biodiversity#MIT-1-ov-file)

### Code of conduct

[Code of conduct](https://github.com/microsoft/Biodiversity#coc-ov-file)

### Security policy

[Security policy](https://github.com/microsoft/Biodiversity#security-ov-file)

Cite this repository

[Activity](https://github.com/microsoft/Biodiversity/activity)

[Custom properties](https://github.com/microsoft/Biodiversity/custom-properties)

### Stars

**1.1k** stars

### Watchers

**51** watching

### Forks

[**298** forks](https://github.com/microsoft/Biodiversity/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fmicrosoft%2FBiodiversity&report=microsoft+%28user%29)

## Releases

## Packages

## Used by

## Contributors

## Languages

You can’t perform that action at this time.