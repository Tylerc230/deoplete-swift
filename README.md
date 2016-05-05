# deoplete-swift

Adds auto-complete support for Swift-based Xcode projects to Vim.

## Installation

Install SourceKittenDaemon (deoplete-swift depends on it for completion)

Using your favorite vim package manager:

```
" dein
dein#add('smallfx/deoplete-swift')

" or neobundle
NeoBundle 'smallfx/deoplete-swift'

" et cetera
```

## Configuration

Configuration is currently limited.

deoplete-swift expects SourceKittenDaemon to be running on port 8081, properly configured for the project you need completions for.

Eventually deoplete-swift will auto-run SourceKittenDaemon and be more configurable in general.
