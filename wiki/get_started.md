# Data911 - Monorepo

## IDE configuration

It is highly recommended to be working with VSCode, an IDE that does not need to be presented. Internally, we use a set of code extensions enabling a minimum of code standardization, making the life of many developers more enjoyable. Those extensions are given in `vscode.extensions`, and can be downloaded directly via the VSCode extension store.

- [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur) - Prettier for Vue templates
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) - Python path resolver
- [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments) - Comments highlighter
- [Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) - Guided docstring generation
- [SonarLint](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode) - Code best practices highlighter
- [Code Metrics](https://marketplace.visualstudio.com/items?itemName=kisstkondoros.vscode-codemetrics) - Complexity monitoring
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) - Code formatter

This goes hand and hand with properly configured VSCode workspace settings. Here is an example:

```json
{
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.languageServer": "Pylance",
  "python.analysis.extraPaths": [
    "{path/to/monorepo}/dispox/server",
    "{path/to/monorepo}/dispox/bastion",
    "{path/to/monorepo}/dispox/industry",
    "{path/to/monorepo}/dispox/worker"
  ],
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Python helpers

We use two very popular (and opinionated) helpers for any Python-related development. Those two are [black](https://pypi.org/project/black/) and [isort](https://pypi.org/project/isort/). Based on the configuration provided above, they should be triggered on each file save, and help you figure out whether your code is properly written or not.

Those requirements, as well as all the packages needed across applications, can be easily set up via:

```bash
pip install -r requirements.dev
```

## Github

### Branches:

We have a simple convention for branch naming: `{initials}/{descriptive-kebab-case}`. Keep them all lowercase.

### Commits:

We have a simple convention for commits writing, enabling a quick look at `git logs` and a great way to avoid absurd changelogs. This rely on the Angular convention (thus Google), with the exception of the `improvement` tag which is a well accepted add to the family of prefixes. Keep them all lowercase.

- **build**: changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- **ci**: changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- **docs**: documentation only changes
- **feat**: new feature
- **fix**: bug fix
- **perf**: code change that improves performance
- **refactor**: code change that neither fixes a bug nor adds a feature
- **style**: changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **test**: adding missing tests or correcting existing tests
- **improv**: improve a current implementation without adding a new feature or fixing a bug

### Pull requests:

As we are currently in a sprint to get a product to the market, our main objective is to get PRs merged as fast as possible, because other team members will most likely depend on the code changes you are making. However, there is one rule to ensure we do not lose information in such a rush: a PR can only be merged if **all** comments are resolved! There are multiple ways of closing a PR:

- if the comment is about a punctual element of the code (e.g. typo), it needs to be resolved with a fresh commit **before** resolving the conversation
- if the comment is about a change to be spread (e.g. naming convention), then a ticket needs to be opened with the given change to be resolved in **another** PR **before** resolving the conversation
- if the comment opens up a complex conversation that is not solved within 3-4 messages, then a **Github issue** is opened and referred to in the conversation. The PR conversation will be resolved **once** the Github issue is resolved

## Naming conventions

"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

That is exactly why it is important everyone follow guidelines regarding naming conventions, especially when moving quickly as a team. Here are a set of rules that will most likely guide you through any problem you would face:

**DO NOT USE ABBREVIATIONS, with the only exception of `ref` for Vue.js!**

_Python_

1. Use `snake_case` for folder names, function names
2. Use `PascalCase` for class names
3. Use `SCREAMING_SNAKE_CASE` for constants

_Java/Type-script_

1. Use `PascalCase` for component registration (e.g. `import Component from './Component/main.vue'`)
2. Use `kebab-case` for global component registration (e.g. `Vue.component('component-name', { })`)
3. Use `PascalCase` for component folders
4. Use `camelCase` for JS/TS files, Vue templates and functions
5. Try to limit the amount of words in shared folders
6. Use `SCREAMING_SNAKE_CASE` for constants defined by hand
7. Use `camelCase` for constants computed once

## Port mapping

- **8080** - _client_
- **8000** - _server_
