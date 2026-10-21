# 泊尘畔 · 个人博客

用 [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 搭建，托管在 GitHub Pages。

访问地址：**https://lunaticud.github.io/**

原博客内容来自[博客园 · 泊尘畔](https://www.cnblogs.com/dragonud/)，已整体迁移（11 篇文章 + 47 张配图本地化）。

## 目录结构

```
.
├── content/
│   ├── posts/           # 所有文章（Markdown）
│   ├── about.md         # 关于页
│   ├── archives.md      # 归档页
│   └── search.md        # 搜索页
├── static/
│   ├── images/posts/    # 文章配图（按 slug 分目录）
│   └── favicon.svg      # 站点图标
├── themes/PaperMod/     # 主题
├── hugo.yaml            # 站点配置（标题、菜单、社交链接都在这）
└── .github/workflows/   # 自动部署
```

## 本地预览

需要先装 Hugo（extended 版，0.146 以上）：

- Windows：`scoop install hugo-extended` 或 `winget install Hugo.Hugo.Extended`
- macOS：`brew install hugo`

然后：

```bash
hugo server -D
```

打开 http://localhost:1313 即可实时预览。

## 写一篇新文章

```bash
hugo new posts/my-new-post.md
```

或者直接在 `content/posts/` 下新建 `.md` 文件，头部格式：

```yaml
---
title: "文章标题"
date: 2026-10-21T10:00:00+08:00
draft: false
slug: "my-new-post"          # 决定 URL：/posts/my-new-post/
tags: ["生信", "Python"]
categories: ["生信分析"]
summary: "列表页显示的摘要"
ShowToc: true                 # 是否显示目录
---
```

写完 `git add . && git commit -m "新文章" && git push`，GitHub Actions 会自动构建发布，约 1 分钟上线。

## 配图怎么放

图片放到 `static/images/posts/<slug>/` 目录下，文章里这样引用：

```markdown
![说明文字](/images/posts/my-new-post/01.png)
```

## 部署

推送到 `main` 分支即触发 `.github/workflows/hugo.yaml` 自动构建并部署到 GitHub Pages。

首次部署需要在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。

## 修改站点信息

标题、副标题、菜单、社交链接、首页欢迎语都在 `hugo.yaml` 的 `params` 里改。
