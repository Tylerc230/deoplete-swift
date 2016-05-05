# deoplete-swift

Adds auto-completion support for Swift-based Xcode projects in Neovim using Shougo's `deoplete`.

## Installation

Install [`deoplete`](https://github.com/Shougo/deoplete.nvim)

Install [`SourceKittenDaemon`](https://github.com/terhechte/SourceKittenDaemon) (deoplete-swift depends on it for completion)

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

`deoplete-swift` expects `SourceKittenDaemon` to be running on `port 8081`, properly configured for the project you need completions for.

Eventually `deoplete-swift` will auto-run `SourceKittenDaemon` and be more configurable in general.
