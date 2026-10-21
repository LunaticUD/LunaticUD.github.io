---
title: "基础设置——快捷键与界面设置（二）"
slug: "nvim-basic-settings-2"
date: 2022-04-21T15:49:00+08:00
draft: false
tags: ["Neovim", "Vim"]
categories: ["Neovim 配置"]
summary: "基础设置——快捷键与界面设置（二）"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## nvim的配置文件init.vim

```powershell
"default{{
lua require('plugins')
source D:/Dragon/nvim/default.vim
"}}
```

## nvim的默认配置

```powershell
" Editor UI {{{
"字体
set guifont=mononoki\ NF\ Font:h6
"高亮一行
set cursorline
set laststatus=0
"禁止警告
let g:VM_show_warnings = 0
"解释器路径
let g:python3_host_prog = 'e:\Python399\python.exe'
"保存所有
let g:auto_save = 1
let g:auto_save_silent = 1
"显示修改的行数"
set report=0
"是否报错响铃及行为"
set errorbells
set visualbell
"允许在未保存的情况下切换缓存区"
set hidden
"自动切换工作目录"
set autochdir
set magic
"不知道
set path+=**
"文件和路径名可用的字符
"文本格式化方式
set formatoptions+=1
set formatoptions-=t
set formatoptions-=o
"关闭兼容模式
set nocompatible
"检测到的文件类型
filetype plugin on
"开启语法高亮显示
set syntax=on
" Mouse
set mouse=nv
:inoremap ( ()<ESC>i
:inoremap ) <c-r>=ClosePair(')')<CR>
:inoremap { {<CR>}<ESC>O
:inoremap } <c-r>=ClosePair('}')<CR>
:inoremap [ []<ESC>i
:inoremap ] <c-r>=ClosePair(']')<CR>
:inoremap " ""<ESC>i
:inoremap ' ''<ESC>i
function! ClosePair(char)
    if getline('.')[col('.') - 1] == a:char
        return "\<Right>"
    else
        return a:char
    endif
endfunction
filetype plugin indent on 
"不保存缓存文件
set nobackup
set nowritebackup
set noundofile 
set noswapfile
" History saving
" 历史记录
set history=2000
augroup user_persistent_undo
	autocmd!
	au BufWritePre /tmp/*          setlocal noundofile
	au BufWritePre COMMIT_EDITMSG  setlocal noundofile
	au BufWritePre MERGE_MSG       setlocal noundofile
	au BufWritePre *.tmp           setlocal noundofile
	au BufWritePre *.bak           setlocal noundofile
augroup END
"UI
set termguicolors       " Enable true color
set number              " Show number
set relativenumber      " Show relative number
set noshowmode          " Don't show mode on bottom
set noruler             " Disable default status ruler
set shortmess=aFc
set scrolloff=2         " Keep at least 2 lines above/below
set fillchars+=vert:\|  " add a bar for vertical splits
set fcs=eob:\           " hide ~ tila
set title
" }}}
```

## nvim的快捷键配置

```powershell
"键盘快捷键{{{
"mapleader键为空格
let mapleader=" "
"移动一个单位
noremap w k
noremap s j
noremap a h
noremap d l
"移动五个单位
noremap W 5k
noremap S 5j
noremap A 5h
noremap D 5l
"进入编辑模式
"在前
noremap e i
"在后
noremap r a
"在首
noremap E I
"在尾
noremap R A
"前进
noremap h w
"删除这一行
noremap c d
"剪切
noremap j c
"替换
noremap m r
"进入命令行
noremap ; :
"退出编辑模式
inoremap jj <esc>

"保存
map <C-s> :w<CR>
"退出
map <C-q> :q<CR>
"写入退出
map Q :wq<CR>
"退出全部
map <A-q> :qa<CR>
"垂直分屏
map <LEADER>+ :vsplit<CR>
"水平分屏
map <LEADER>- :split<CR>
"光标在右边
map <A-d> <C-w>l
"光标在上边
map <A-w> <C-w>k
"光标在在左边
map <A-a> <C-w>h
"光标在下边
map <A-s> <C-w>j
"窗口创建
noremap tn :tabe<CR>
"窗口切换
nmap <leader>1 :bn<CR>
nmap <leader>2 :bp<CR>
"插件安装
nmap <F2> :PackerSync<CR>
"vim内置检察器
map <LEADER>sc :set spell!<CR>
"可视模式下的复制 
vnoremap <C-c> "+y
vnoremap <C-v> "+p
"}}}
```
