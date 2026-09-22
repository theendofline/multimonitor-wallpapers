## [0.2.2](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.2.1...v0.2.2) (2026-09-22)
### Bug Fixes

* **release:** include every commit type in changelog notes ([bfb767b](https://github.com/theendofline/multimonitor-wallpapers/commit/bfb767bdce25b1768eb94331b3e34d0ced2d0a1d))

## [0.2.1](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.2.0...v0.2.1) (2026-09-22)

### Bug Fixes

* **ci:** lock workflow installs against supply-chain findings ([34e196f](https://github.com/theendofline/multimonitor-wallpapers/commit/34e196f6672adfa0f29ab7da23a460d536677c6c))

### Code Refactoring

* extract geometry parser helper and cache dark mode state to improve readability and avoid repeated system checks ([c2c7db7](https://github.com/theendofline/multimonitor-wallpapers/commit/c2c7db756baed55de5262d1474156d62923f282a))

### Documentation

* **copilot:** add repo-tailored Copilot code-review instructions ([5ebbc69](https://github.com/theendofline/multimonitor-wallpapers/commit/5ebbc6951cb56385056b5625f3a1f8c2f73565a1))

### Build System

* **deps:** bump actions/checkout from 6.0.2 to 7.0.0 ([a8b4d37](https://github.com/theendofline/multimonitor-wallpapers/commit/a8b4d378e481c9104ccc33aec9ddce9a446f9870))
* **deps:** bump actions/checkout from 7.0.0 to 7.0.1 ([34865b4](https://github.com/theendofline/multimonitor-wallpapers/commit/34865b4976c5d355d56ccd5df0dc3a9f06f77f87))
* **deps:** bump actions/setup-node from 6.4.0 to 7.0.0 ([4cf34c9](https://github.com/theendofline/multimonitor-wallpapers/commit/4cf34c99f55c899b525ec311d2a3760a2579d22b))
* **deps:** bump actions/setup-python from 6.2.0 to 6.3.0 ([31cc381](https://github.com/theendofline/multimonitor-wallpapers/commit/31cc381f48d2af5e115065064ae3576e59117936))
* **deps:** bump actions/setup-python from 6.3.0 to 7.0.0 ([8fd27ac](https://github.com/theendofline/multimonitor-wallpapers/commit/8fd27acf8650c2f8c8f32e5b5a1c403e71480d26))
* **deps:** bump astral-sh/setup-uv from 8.1.0 to 8.2.0 ([0fa5a4d](https://github.com/theendofline/multimonitor-wallpapers/commit/0fa5a4d0a026e842425882eea2f05e68f0e528dc))
* **deps:** bump astral-sh/setup-uv from 8.2.0 to 10.1.0 ([c8905ef](https://github.com/theendofline/multimonitor-wallpapers/commit/c8905efbec1e366d9248eb7c8f4aa14bc259814d))
* **deps:** bump black from 26.3.1 to 26.5.1 ([b8e93f5](https://github.com/theendofline/multimonitor-wallpapers/commit/b8e93f56f585499d47a967c28d839b0c78d886f4))
* **deps:** bump github/codeql-action from 4 to 4.37.4 ([31a2603](https://github.com/theendofline/multimonitor-wallpapers/commit/31a26031709a1bb68277cb1a80497c5c30f3aba9))
* **deps:** bump mypy from 2.0.0 to 2.1.0 ([757d883](https://github.com/theendofline/multimonitor-wallpapers/commit/757d8839ea6c89262147d44d71ec6b929ddb4598))
* **deps:** bump pytest from 9.0.3 to 9.1.1 ([d5adb4a](https://github.com/theendofline/multimonitor-wallpapers/commit/d5adb4abd35b799f0ced5d45f46b207fbbd90ef4))
* **deps:** bump ruff from 0.15.12 to 0.15.13 ([9b180ec](https://github.com/theendofline/multimonitor-wallpapers/commit/9b180ec68c010dbacc0edab99ba5daf44a5b1a84))
* **deps:** bump ruff from 0.15.13 to 0.15.20 ([9e8af6a](https://github.com/theendofline/multimonitor-wallpapers/commit/9e8af6af9cd3fbb381218cde27e33b5f1c6467a8))
* **deps:** bump the production-dependencies-minor group across 1 directory with 3 updates ([a233820](https://github.com/theendofline/multimonitor-wallpapers/commit/a2338203eeea7c0b45a0fcf99a0e75bcb7145440))
* **deps:** bump the uv group across 1 directory with 2 updates ([0e32074](https://github.com/theendofline/multimonitor-wallpapers/commit/0e32074b4f6854b0705cc4e38eb3bbff6b940a12))

### Continuous Integration

* enforce conventional commits and group Dependabot updates ([d451f1d](https://github.com/theendofline/multimonitor-wallpapers/commit/d451f1d99fd46ff0ef71564fe6a576c314ef8ddb))

### Other Changes

* note that semantic-release publishes from main ([e597b59](https://github.com/theendofline/multimonitor-wallpapers/commit/e597b59a40b481f2a31bc2a5bd5bc746ea5e32df))

## [0.2.0](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.1.3...v0.2.0) (2026-05-10)

### Features

* **assets:** replace procedural placeholder with a designed app icon ([12602fe](https://github.com/theendofline/multimonitor-wallpapers/commit/12602fe335a98740c62488667bd8bcd6c10b3f36))
* **ui:** show per-monitor thumbnail of the chosen image ([4f1f942](https://github.com/theendofline/multimonitor-wallpapers/commit/4f1f942c2a2a9b3717fbc4434838062a594581d5))

### Tests

* **ui:** cover the four thumbnail update states ([554c701](https://github.com/theendofline/multimonitor-wallpapers/commit/554c7019a34f7a55320af73d6d302df59b3a8504))

### Miscellaneous Chores

* **justfile:** close numbering gap left by removing the icon recipe ([bf61938](https://github.com/theendofline/multimonitor-wallpapers/commit/bf6193891c2e08338cf6214eba4bc1b9992ccd56))

## [0.1.3](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.1.2...v0.1.3) (2026-05-10)

### Bug Fixes

* **build:** drop unused ImageMagick convert from AppImage payload ([5517bc5](https://github.com/theendofline/multimonitor-wallpapers/commit/5517bc5b93254d7e5ecd3bafc62562f7bd78c5f7))
* **build:** stop bundling pip/setuptools/pkg_resources/_distutils_hack ([c9fe595](https://github.com/theendofline/multimonitor-wallpapers/commit/c9fe595806f4975352fe6a3473648a383a19c0cf))
* **build:** trim unused PySide6/Qt6 modules from AppImage payload ([0165160](https://github.com/theendofline/multimonitor-wallpapers/commit/01651600e00abe5856f3b990f53877be52589406))

## [0.1.2](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.1.1...v0.1.2) (2026-05-10)

### Bug Fixes

* **build:** fetch appimagetool from the supported AppImage/appimagetool repo ([ed300c8](https://github.com/theendofline/multimonitor-wallpapers/commit/ed300c83a18a29cc99c66ba5672eaf4e4808aa39))

## [0.1.1](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.1.0...v0.1.1) (2026-05-10)

### Bug Fixes

* **compositor:** raise clear error on empty monitor list ([f216b18](https://github.com/theendofline/multimonitor-wallpapers/commit/f216b18bd5152461d25ff0e8528ec0deb309fb77))
* **desktop:** return False when all GNOME picture-options fail ([fb0666f](https://github.com/theendofline/multimonitor-wallpapers/commit/fb0666f2bc0f254dbd72be701b1d6b1a976557c9))
* drop unused ImageMagick convert dependency ([5797c4f](https://github.com/theendofline/multimonitor-wallpapers/commit/5797c4f242f8204bc91a03a9a61e950b63df0e26))
* **monitors:** degrade gracefully when xrandr is unavailable ([3f809ae](https://github.com/theendofline/multimonitor-wallpapers/commit/3f809aef87b8aa9198249e60f482b1ae94bf3861))
* **release:** build artifacts inside semantic-release as the only version source ([f97ba15](https://github.com/theendofline/multimonitor-wallpapers/commit/f97ba1596e5f2cb7c5a5ed8868de66615f359727))
* **release:** include version in AppImage filename, derive from pyproject ([e20b63f](https://github.com/theendofline/multimonitor-wallpapers/commit/e20b63f1e7e26da129cab1e26da67807f6e867cf))
* **ui:** reuse detected monitors when applying the wallpaper ([3e54699](https://github.com/theendofline/multimonitor-wallpapers/commit/3e546991e9b66004e331f9ea7e5d1ff1d7276c22))

### Code Refactoring

* **packaging:** make src-layout console entry the single source of truth ([aac733e](https://github.com/theendofline/multimonitor-wallpapers/commit/aac733e1c0c00c48f43199003d7863e0ca3164e6))
* split widget.py into focused modules (monitors/compositor/desktop/ui) ([2c29ce0](https://github.com/theendofline/multimonitor-wallpapers/commit/2c29ce008f6fd8c1df67d3e2759023b3bd5b5eb2))
* **widget:** add type hints and modernize Qt/PIL enum usage ([7d81a7b](https://github.com/theendofline/multimonitor-wallpapers/commit/7d81a7b5cd3febf5b45aabf744e1cceab7e11c60))
* **widget:** replace ad-hoc prints with stdlib logging ([60d2600](https://github.com/theendofline/multimonitor-wallpapers/commit/60d260037f3fde3502349f34cb35cf741a8327cf))

### Documentation

* list build_release_artifacts.sh in README scripts table ([ba0588f](https://github.com/theendofline/multimonitor-wallpapers/commit/ba0588fa63bfa483d275cab3dab00e6b442505b8))
* update README layout and dev.py mypy target after the module split ([6ba553d](https://github.com/theendofline/multimonitor-wallpapers/commit/6ba553deb5bf399f2b51f9954a72560133b035e2))

### Tests

* add unit tests for monitor parsing and compositor canvas math ([9364951](https://github.com/theendofline/multimonitor-wallpapers/commit/9364951e82d342d58091a5399c9951b80f8fbd1c))
* **monitors:** rename DUAL_MONITOR_XRANDR fixture to TRIPLE_MONITOR_XRANDR ([29b10b7](https://github.com/theendofline/multimonitor-wallpapers/commit/29b10b7b1e39e34602608557c299c430902d229a))

### Styles

* **widget:** drop redundant comments, keep intent-only ones ([08ba530](https://github.com/theendofline/multimonitor-wallpapers/commit/08ba5307b6fe8bdc5b8b7bbbca3ae2b274160b18))

### Miscellaneous Chores

* add LICENSE (GPLv3) and .editorconfig ([ec15c99](https://github.com/theendofline/multimonitor-wallpapers/commit/ec15c993795d2eca8aad325e65d0a3ca77958d4a))
* **build:** drop unreachable Pillow ImportError fallback ([273af62](https://github.com/theendofline/multimonitor-wallpapers/commit/273af62e9bd1387d0bee78dfeb25b4d5bbdf2f39))
* **build:** remove dead libQt5 fallback in build_appimage.py ([ad9c15a](https://github.com/theendofline/multimonitor-wallpapers/commit/ad9c15ac739cb39ba1d94f2657198f19d5065bbe))
* consolidate mypy config to pyproject.toml ([6e38072](https://github.com/theendofline/multimonitor-wallpapers/commit/6e380728d2b5e4b94c82527bce26d128c6d72cbb))
* delete .uv/settings.toml (uv never reads it) ([1949319](https://github.com/theendofline/multimonitor-wallpapers/commit/1949319479364191415cac6654bacb28fd68f657))
* group GITHUB_OUTPUT writes in release workflow and add actionlint  pre-commit hook to enforce GitHub Actions validation ([15a2e05](https://github.com/theendofline/multimonitor-wallpapers/commit/15a2e05b15032e6be9ba819b72451b89ad1db2ee))
* prune stale .gitignore entries ([7eb3a88](https://github.com/theendofline/multimonitor-wallpapers/commit/7eb3a8844b7ed33c79530e6d3225f37d8fbfb858))
* remove dev.py (redundant with justfile) ([02fe5ca](https://github.com/theendofline/multimonitor-wallpapers/commit/02fe5ca7519d902746f3d262884ee96bc4e985f9))
* remove stale/dead ruff configuration ([c0db8db](https://github.com/theendofline/multimonitor-wallpapers/commit/c0db8db77f5f37e7fc2559d1dbacc29b3f9d117d))

## [0.1.0](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.0.3...v0.1.0) (2026-05-10)

### Features

* **packaging:** add DEB package build from AppImage ([ee74fe5](https://github.com/theendofline/multimonitor-wallpapers/commit/ee74fe57a65e878aa7a4530be6f028e61e8c5ca5))

### Documentation

* document uv workflows, releases, and local development ([9699185](https://github.com/theendofline/multimonitor-wallpapers/commit/9699185eb00e0c91c8686f4973c4eb5df1a6dbae))

### Build System

* **deps:** add PEP 621 metadata, extras, and uv.lock ([13dc585](https://github.com/theendofline/multimonitor-wallpapers/commit/13dc585d5b695433bd3c33b4c18eb0d402ef90d1))
* **deps:** bump actions/upload-artifact from 5 to 6 ([a7f24bf](https://github.com/theendofline/multimonitor-wallpapers/commit/a7f24bfac158966e06dab094436b957ff28fdc32))
* **deps:** bump astral-sh/setup-uv from 6 to 7 ([911a091](https://github.com/theendofline/multimonitor-wallpapers/commit/911a091c97c42da539534e3fe15a59d5123f22c1))
* **deps:** bump black from 25.12.0 to 26.1.0 ([3553dd4](https://github.com/theendofline/multimonitor-wallpapers/commit/3553dd4abcc2c91c5d0bb5761df6fa4785d65737))
* **deps:** bump keninkujovic/gitlab-sync from 2.1.0 to 2.1.3 ([463cca2](https://github.com/theendofline/multimonitor-wallpapers/commit/463cca2f2a2308ed898394386004c6ea4c4e6ee8))
* **deps:** bump keninkujovic/gitlab-sync from 2.1.3 to 2.2.1 ([3d063ce](https://github.com/theendofline/multimonitor-wallpapers/commit/3d063ce8c2fa9197435cfe9e6ede65d736848924))
* **deps:** bump mypy from 1.19.0 to 1.19.1 ([04c9f21](https://github.com/theendofline/multimonitor-wallpapers/commit/04c9f21d73ec7e94f5f687e16fef4e046be05a3b))
* **deps:** bump softprops/action-gh-release from 2 to 3 ([ed17464](https://github.com/theendofline/multimonitor-wallpapers/commit/ed174647c11faa523e0539433692b0a32357d9bd))

### Continuous Integration

* add GitHub Actions workflow to sync repository to GitLab on dev branch pushes ([c6bbfaa](https://github.com/theendofline/multimonitor-wallpapers/commit/c6bbfaab505b5e43fef62676e00e3192d84b2296))
* add main-branch release workflow with AppImage, DEB, and semantic-release ([35347a5](https://github.com/theendofline/multimonitor-wallpapers/commit/35347a59fb6a9ef840328991172083eb6555f94a))
* align workflows to use actions/setup-python@v6.2.0 for Python 3.12 ([b6580c2](https://github.com/theendofline/multimonitor-wallpapers/commit/b6580c24c0b4dcbad59c53b3d56c56794725475d))
* **dependabot:** use uv ecosystem for dependency updates ([fd81c83](https://github.com/theendofline/multimonitor-wallpapers/commit/fd81c837b609568f389ecda2a11acaf29d60afff))
* run tests with uv sync --frozen and uv run ([a591390](https://github.com/theendofline/multimonitor-wallpapers/commit/a59139061f155ee72f1b1e8aaa618fc67913be44))

### Miscellaneous Chores

* add CODEOWNERS and increase Dependabot PR limit to 20 ([1a32bdf](https://github.com/theendofline/multimonitor-wallpapers/commit/1a32bdffc1b77dd0138382553d08147cf7fd50d3))
* add pre-commit config and apply formatting tweaks for consistency ([c00648a](https://github.com/theendofline/multimonitor-wallpapers/commit/c00648ae0f443fa3a570ae093273a2eaa45a2a16))
* drop requirements.txt; use pyproject.toml and uv.lock ([97e40e5](https://github.com/theendofline/multimonitor-wallpapers/commit/97e40e5c42e0ba689460d757aaca603cbc2ee8a9))
* **just:** use uv sync and lock for dev and build recipes ([40ff38f](https://github.com/theendofline/multimonitor-wallpapers/commit/40ff38fc6b242e7c4b78b024549817e31b045102))
* update GitHub Actions, tooling, and Python deps to newer versions ([5c68b9f](https://github.com/theendofline/multimonitor-wallpapers/commit/5c68b9fe35cf24224ccd4e981492b5c23cace2e5))

### Dependency Updates

* Bump pytest from 9.0.1 to 9.0.2 ([d6d07cc](https://github.com/theendofline/multimonitor-wallpapers/commit/d6d07cca31d359657f9e9d5ef289494c6bf72c7d))
* Bump black from 25.11.0 to 25.12.0 ([f18ba11](https://github.com/theendofline/multimonitor-wallpapers/commit/f18ba11a096ac3f08a453acbab6a457f98c811e6))
* Bump ruff from 0.14.6 to 0.14.8 ([33e5528](https://github.com/theendofline/multimonitor-wallpapers/commit/33e552889db8fe04e2d8c632ffc31a8c1a4ecf6b))
* Bump mypy from 1.18.2 to 1.19.0 ([4c13f37](https://github.com/theendofline/multimonitor-wallpapers/commit/4c13f3720c44a920444438c103cedc4120b797f6))
* Bump ruff from 0.14.4 to 0.14.6 ([3c29aa9](https://github.com/theendofline/multimonitor-wallpapers/commit/3c29aa98e1d966282d60d8e78dae6f651bb06739))
* Bump actions/checkout from 5 to 6 ([e5fcd7a](https://github.com/theendofline/multimonitor-wallpapers/commit/e5fcd7a4c11cb49b8c239d3821b2055dab520bd5))
* Bump pyside6 from 6.10.0 to 6.10.1 ([7469f4f](https://github.com/theendofline/multimonitor-wallpapers/commit/7469f4ff65d2c6cc7e0785f23bec0e0e05095f69))
* Bump pytest from 8.4.2 to 9.0.0 ([3c220e8](https://github.com/theendofline/multimonitor-wallpapers/commit/3c220e8d1fd7f6ccc89e97934345f012d368dd97))
* Bump black from 25.9.0 to 25.11.0 ([00972fe](https://github.com/theendofline/multimonitor-wallpapers/commit/00972fee19339c6dda226b4e45e39443b4495924))
* Bump ruff from 0.14.2 to 0.14.4 ([91a578c](https://github.com/theendofline/multimonitor-wallpapers/commit/91a578cd576d0cf4d94252841f243c296837e39b))
* Bump actions/upload-artifact from 4 to 5 ([1da3a1c](https://github.com/theendofline/multimonitor-wallpapers/commit/1da3a1c6af8a8b148c68a3c8d0cb38191a4c67bd))
* Bump ruff from 0.14.1 to 0.14.2 ([c6b1dc5](https://github.com/theendofline/multimonitor-wallpapers/commit/c6b1dc50723f929c320e9f2faa5ff806922f09f1))
* Bump ruff from 0.14.0 to 0.14.1 ([a7b9374](https://github.com/theendofline/multimonitor-wallpapers/commit/a7b9374247c56a70d15a416586dc756463c874f4))
* Bump pillow from 11.3.0 to 12.0.0 ([2b7393f](https://github.com/theendofline/multimonitor-wallpapers/commit/2b7393f949d05b6e1c0c9948c7b52307f755379a))
* Bump pyside6 from 6.9.3 to 6.10.0 ([9fbd650](https://github.com/theendofline/multimonitor-wallpapers/commit/9fbd6507064fd042cfba3935981dc337b4d06d8b))
* Bump ruff from 0.13.2 to 0.14.0 ([515832a](https://github.com/theendofline/multimonitor-wallpapers/commit/515832ae19e31daf4fa91ba1975879055b9b52cf))
* Bump github/codeql-action from 3 to 4 ([a067deb](https://github.com/theendofline/multimonitor-wallpapers/commit/a067deb0b7a16e1aab347144c6454a1185ae0909))
* Bump pyside6 from 6.9.2 to 6.9.3 ([c7fb021](https://github.com/theendofline/multimonitor-wallpapers/commit/c7fb02138c86079770a32c6ca7d66cdde7266284))
* Bump mypy from 1.18.1 to 1.18.2 ([e986d4f](https://github.com/theendofline/multimonitor-wallpapers/commit/e986d4f2cf6d07f6ad6182ad08cf7022347c0f0b))
* Bump ruff from 0.13.1 to 0.13.2 ([7b99ef4](https://github.com/theendofline/multimonitor-wallpapers/commit/7b99ef4fef2f954f4d9de9c73b608e66bb1d0de9))
* Bump ruff from 0.13.0 to 0.13.1 ([bd9e59a](https://github.com/theendofline/multimonitor-wallpapers/commit/bd9e59a7e8a6bcab43d4d77d9bc0124709da1b13))
* Bump black from 25.1.0 to 25.9.0 ([b6ceb77](https://github.com/theendofline/multimonitor-wallpapers/commit/b6ceb77a3ad8820e429a3e0012bc0443f6e58614))
* Bump mypy from 1.17.1 to 1.18.1 ([e8a1255](https://github.com/theendofline/multimonitor-wallpapers/commit/e8a1255a482280f749f0d56c1da8135a70893a55))
* Bump ruff from 0.12.12 to 0.13.0 ([182e718](https://github.com/theendofline/multimonitor-wallpapers/commit/182e718d8961beb5f6fa68e3fdcdbaac0772e6c3))
* Bump pytest from 8.4.1 to 8.4.2 ([d8b7413](https://github.com/theendofline/multimonitor-wallpapers/commit/d8b74138ce700211776e4d1f0256cf0ae88745cc))
* Bump ruff from 0.12.11 to 0.12.12 ([2e1428c](https://github.com/theendofline/multimonitor-wallpapers/commit/2e1428cf4d35fb703ef886995c0bcb0acaa54d86))
* Bump actions/setup-python from 5 to 6 ([29fcf0d](https://github.com/theendofline/multimonitor-wallpapers/commit/29fcf0d6ead8277fbb77a9a99b93a9d02f17da18))
* Bump ruff from 0.12.10 to 0.12.11 ([3047706](https://github.com/theendofline/multimonitor-wallpapers/commit/304770623a259cc71b1fa32672d6d30fd0aa0b7f))
* Bump pyside6 from 6.9.1 to 6.9.2 ([4c07b8a](https://github.com/theendofline/multimonitor-wallpapers/commit/4c07b8aa11b79efa267ea7f314421c44186f855f))
* Bump ruff from 0.12.9 to 0.12.10 ([d6848ab](https://github.com/theendofline/multimonitor-wallpapers/commit/d6848ab9e18ed5d70e63278bc9ba38e22ef2cd8f))
* Bump ruff from 0.12.8 to 0.12.9 ([bead1eb](https://github.com/theendofline/multimonitor-wallpapers/commit/bead1ebc5687e50b79cad859b1304aa311320d3a))
* Bump actions/checkout from 4 to 5 ([d6f8fae](https://github.com/theendofline/multimonitor-wallpapers/commit/d6f8fae44ba05dc6659909da4305582b7c813a58))
* Bump ruff from 0.12.7 to 0.12.8 ([a2e593b](https://github.com/theendofline/multimonitor-wallpapers/commit/a2e593b61b695f7fb36ab78b7784727369fcbba2))
* Bump mypy from 1.17.0 to 1.17.1 ([0551df1](https://github.com/theendofline/multimonitor-wallpapers/commit/0551df18b804117ec7c357b52f27fc9538cddc1b))
* Bump ruff from 0.12.5 to 0.12.7 ([53f0afa](https://github.com/theendofline/multimonitor-wallpapers/commit/53f0afa19df778a0ca1a96e2a174f19b6aa29f2f))
* Bump ruff from 0.12.2 to 0.12.5 ([5e3679e](https://github.com/theendofline/multimonitor-wallpapers/commit/5e3679e375a70303525c95907fd8d28491907300))
* Bump mypy from 1.16.1 to 1.17.0 ([413ed71](https://github.com/theendofline/multimonitor-wallpapers/commit/413ed71879dcb9f1d56e0de43075a31b05f798e7))
* Bump ruff from 0.12.1 to 0.12.2 ([d29beb5](https://github.com/theendofline/multimonitor-wallpapers/commit/d29beb5e0a25f901ad6ef0f1656619b07c0f55a5))
* Bump pillow from 11.2.1 to 11.3.0 in the pip group ([2fb7c80](https://github.com/theendofline/multimonitor-wallpapers/commit/2fb7c80577182cbc8db622c7a950f72386f97fcb))
* Bump ruff from 0.12.0 to 0.12.1 ([6a5f9ab](https://github.com/theendofline/multimonitor-wallpapers/commit/6a5f9abc7eade367e36b11fa6ffb474dacfc9a0b))
* Bump ruff from 0.11.13 to 0.12.0 ([5340a8e](https://github.com/theendofline/multimonitor-wallpapers/commit/5340a8efe7e056e5e3cbc046825a1867b90d67ed))
* Bump pytest from 8.4.0 to 8.4.1 ([4769dba](https://github.com/theendofline/multimonitor-wallpapers/commit/4769dba1d261d4ff9a293c12f562e62b6bcc49c2))
* Bump mypy from 1.16.0 to 1.16.1 ([c8186cf](https://github.com/theendofline/multimonitor-wallpapers/commit/c8186cf9f0d2c6d67c532b0e0ff2d0020d47a439))
* Bump ruff from 0.11.12 to 0.11.13 ([ef70b04](https://github.com/theendofline/multimonitor-wallpapers/commit/ef70b0499c59fad2b376e9596e974e020e1b18a4))
* Bump pyside6 from 6.9.0 to 6.9.1 ([4a97237](https://github.com/theendofline/multimonitor-wallpapers/commit/4a972376e732632945d10ffea5b6a2fe6f77e744))
* Bump pytest from 8.3.5 to 8.4.0 ([9fbe235](https://github.com/theendofline/multimonitor-wallpapers/commit/9fbe23578f75bb50685fc213b1ffd65f6f6d01c8))
* Bump mypy from 1.15.0 to 1.16.0 ([00688b1](https://github.com/theendofline/multimonitor-wallpapers/commit/00688b18525f3b4be2baf9b08adcd794f3adfa2a))
* Bump ruff from 0.11.11 to 0.11.12 ([db223b7](https://github.com/theendofline/multimonitor-wallpapers/commit/db223b7a0facb00f93396910ee9ccf1326523289))
* Bump ruff from 0.11.10 to 0.11.11 ([c1d184b](https://github.com/theendofline/multimonitor-wallpapers/commit/c1d184bb25cccf4a367389806b995b00d0266c45))
* Bump ruff from 0.11.9 to 0.11.10 ([6561a62](https://github.com/theendofline/multimonitor-wallpapers/commit/6561a6221e2d009d86d8c0d3605633699a24d13d))

### Other Changes

* Add assignees to Dependabot configuration ([205a198](https://github.com/theendofline/multimonitor-wallpapers/commit/205a1989ea62d9b3d203edefef02dea8f93aa9f7))

## [0.0.3](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.0.2...v0.0.3) (2025-05-13)

### Other Changes

* Improve justfile and build script ([726cca7](https://github.com/theendofline/multimonitor-wallpapers/commit/726cca79ab1a905d6cd70884fd47fdce823eddfd))
* Fix linting error: replace bare except with except Exception ([49698e8](https://github.com/theendofline/multimonitor-wallpapers/commit/49698e8db99e4c5dd778591e1fa2a926766c1633))
* Add Ubuntu GNOME support ([1d00efa](https://github.com/theendofline/multimonitor-wallpapers/commit/1d00efacb1cc7830fdc3d55db38a1f7bc8bafa98))
* Update .github/workflows/release.yml ([8da9b01](https://github.com/theendofline/multimonitor-wallpapers/commit/8da9b01182b450e136ab0cacfde425a6eb73d683))
* drop the trailing newline in requirements.txt ([776cf0c](https://github.com/theendofline/multimonitor-wallpapers/commit/776cf0c8a4952c930ef58b52225605f8d61ee2c8))
* add pytest, black, flake8, and mypy to requirements.txt ([fda1fc1](https://github.com/theendofline/multimonitor-wallpapers/commit/fda1fc1dff2ee91330383ac2e01dd59dce097411))
* Fix depentabot jobs ([cba73c2](https://github.com/theendofline/multimonitor-wallpapers/commit/cba73c2dd0cdf3d7f635a792ec739311ff5102b6))

## [0.0.2](https://github.com/theendofline/multimonitor-wallpapers/compare/v0.0.1...v0.0.2) (2025-05-12)

### Dependency Updates

* Bump ruff from 0.11.8 to 0.11.9 ([d749497](https://github.com/theendofline/multimonitor-wallpapers/commit/d749497ab1991f0ef6bc84fa7de716f19a20b8de))
* Bump pillow from 11.0.0 to 11.2.1 ([14d15e2](https://github.com/theendofline/multimonitor-wallpapers/commit/14d15e218455b0765e4908dd703b7541c49a5571))
* Bump pyside6 from 6.8.0.1 to 6.9.0 ([06dba03](https://github.com/theendofline/multimonitor-wallpapers/commit/06dba031f35c05c33e646f2f8b92ff1a76d052ff))

### Other Changes

* Fix no background after set pic ([794090e](https://github.com/theendofline/multimonitor-wallpapers/commit/794090ee152bcc9a9fff65b1bb69eedadce06681))
* Fix no background after set pic ([389a519](https://github.com/theendofline/multimonitor-wallpapers/commit/389a5195104728cbb334b97f18a23716cf8a514d))
* Fix No module named 'PIL' ([c6999b6](https://github.com/theendofline/multimonitor-wallpapers/commit/c6999b6e3a760cb75d159a62d0160c07ac05754b))
* Fix No module named 'encodings'-added lint fix ([f0d0c53](https://github.com/theendofline/multimonitor-wallpapers/commit/f0d0c53f9e9cea6f82feb3d769bf25188a4092be))
* Fix No module named 'encodings' ([97d0529](https://github.com/theendofline/multimonitor-wallpapers/commit/97d0529581d4d1e38856117cfefc00b71a78ce97))
* Fix lint ([fee0cdc](https://github.com/theendofline/multimonitor-wallpapers/commit/fee0cdc6e094659e11158b70dfff72a06464c79e))
* Fix AppImage build: specify architecture explicitly ([7b27c4c](https://github.com/theendofline/multimonitor-wallpapers/commit/7b27c4cc138853d5ba17e0c80a35a81ac71dfe66))
* Fix lint ([5a4fa99](https://github.com/theendofline/multimonitor-wallpapers/commit/5a4fa99085dbbab7b14a854ed7bf0d9e5adce872))
* Completely overhaul AppImage Python bundling to fix encodings module error ([4c8ee6a](https://github.com/theendofline/multimonitor-wallpapers/commit/4c8ee6a0d48d8696b44f2667d928e5924554177a))
* Fix AppImage Python bundling to include standard library ([3f9c29c](https://github.com/theendofline/multimonitor-wallpapers/commit/3f9c29c3ae6a404a3f7289ef111d94d356300a7c))
* Fix AppImage Python bundling to include standard library ([caf2315](https://github.com/theendofline/multimonitor-wallpapers/commit/caf2315c5f2b13b0fa3d54ef587cca51d962a90b))
* Fix release workflow: remove ldd installation ([9f99316](https://github.com/theendofline/multimonitor-wallpapers/commit/9f993167706d5f111b91edde7efad303b7bd4531))
* Added release deletion ([1fd0687](https://github.com/theendofline/multimonitor-wallpapers/commit/1fd06879799f8074f914bbf84aaee8a6b5cec412))
* Fixed build ([27af406](https://github.com/theendofline/multimonitor-wallpapers/commit/27af40632774028f58aa755a454aa85ba3b66958))
* Enhance AppImage build process for better dependency handling ([b814073](https://github.com/theendofline/multimonitor-wallpapers/commit/b81407383d773ba7e1d1975952da8050d71b9c72))
* Fixed lint errors ([322ae66](https://github.com/theendofline/multimonitor-wallpapers/commit/322ae6633635a5f29601d03dfdefe51b306baea9))
* Fix CI: update dependency packages and avoid loading GUI in CI tests ([e1aec2d](https://github.com/theendofline/multimonitor-wallpapers/commit/e1aec2d061ac0aebdeda24616601c5832c089ecc))
* Fixed lint errors ([001b76b](https://github.com/theendofline/multimonitor-wallpapers/commit/001b76bec19a496003d368a7044e54600a6c4742))
* Fix CI tests: add Qt dependencies and make tests robust against missing GUI libraries ([2b44c67](https://github.com/theendofline/multimonitor-wallpapers/commit/2b44c676cdf01418e4bf9d2bf826e37a63ec5a2e))
* Skip mypy check in CI due to package name issues ([d7bec8b](https://github.com/theendofline/multimonitor-wallpapers/commit/d7bec8ba323af3c047d9ab69c7bf71ff42436a37))
* Fix E501 linting errors in CI by ignoring line length checks ([ad4c91a](https://github.com/theendofline/multimonitor-wallpapers/commit/ad4c91a131cd7049ffb2e82bf79e47d469397626))
* Fixed lint errors ([ba9fc8d](https://github.com/theendofline/multimonitor-wallpapers/commit/ba9fc8d622f23dbb53a6ffe140ba492139366c67))
* Update README.md ([dbb6ee6](https://github.com/theendofline/multimonitor-wallpapers/commit/dbb6ee689829aae8a099d1b55fc7d923c6271480))
* Update dependabot.yml ([e20fec2](https://github.com/theendofline/multimonitor-wallpapers/commit/e20fec20ee82a0a40f0bfde91a89c3808574bc69))
* Fix AppImage build: bundle all code, fix line endings, update release workflow ([2bfc0bc](https://github.com/theendofline/multimonitor-wallpapers/commit/2bfc0bc2b4864d198bf0f23c992dd76ef6b39f2f))
* Test release ([0f6949d](https://github.com/theendofline/multimonitor-wallpapers/commit/0f6949d8927ddf8ccde51c77b129877321e49d8d))
* Fix tests-1 ([914c24a](https://github.com/theendofline/multimonitor-wallpapers/commit/914c24ab45446b7258f91661241eb486aa39fb16))
* Fix tests-1 ([602eea7](https://github.com/theendofline/multimonitor-wallpapers/commit/602eea77c64a8f2add0c6bc4e85dcbb055895fb1))
* Fix tests ([723c23f](https://github.com/theendofline/multimonitor-wallpapers/commit/723c23f3eb190c637d1acf81ade0be580fad6021))
* Fix tests ([19b3c1a](https://github.com/theendofline/multimonitor-wallpapers/commit/19b3c1ac430d2325272159009614f049dc43a1bf))
* Update python-tests.yml ([d49ef98](https://github.com/theendofline/multimonitor-wallpapers/commit/d49ef98c1a5e9a1ef61ffe3885472519e99814a2))
* Project improvements ([30a7250](https://github.com/theendofline/multimonitor-wallpapers/commit/30a7250fb40db7c3491fb5d12dcebaff88d86564))
* Create codeql.yml ([a709409](https://github.com/theendofline/multimonitor-wallpapers/commit/a7094097d0bbd366d0e0b5940d7908eae1596d3c))
* Create dependabot.yml ([ef6d11a](https://github.com/theendofline/multimonitor-wallpapers/commit/ef6d11a8b5cc664610c20867185dac34de7ddc59))
* Updated ([b45821f](https://github.com/theendofline/multimonitor-wallpapers/commit/b45821f004efd3f680e4b344af97a9fd91284145))
* Updated ([621068d](https://github.com/theendofline/multimonitor-wallpapers/commit/621068d5bed0e01ce260e0c1e678c7b3fdbae5d8))
* Delete .qtcreator/Python_3_10_12venv directory ([7486ac3](https://github.com/theendofline/multimonitor-wallpapers/commit/7486ac3d1b5341b621b076798771d33f33fc3a10))
* Delete .qtcreator/Python_3_10_12venv directory ([4f64e28](https://github.com/theendofline/multimonitor-wallpapers/commit/4f64e2825ac49b47b9bcd2c445c2b0a11f9ec022))

## 0.0.1 (2024-10-18)

### Other Changes

* Update project files ([7710e59](https://github.com/theendofline/multimonitor-wallpapers/commit/7710e59994fc68de97b002d084772e2e26f73b47))
* Initial commit ([af9e096](https://github.com/theendofline/multimonitor-wallpapers/commit/af9e096b449e526539f6b96d67c5bea1bf436292))
