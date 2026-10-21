---
title: "从零搭建 Hugo + GitHub Pages 博客：完整实操指南"
slug: "hugo-github-pages-tutorial"
date: 2026-10-21T12:00:00+08:00
draft: false
tags: ["Hugo", "GitHub Pages", "博客", "教程", "Sublime Text"]
categories: ["建站"]
summary: "从装 Hugo 到自动部署上线，把一套免费、快速、能长期维护的个人博客搭起来，附一套用 Sublime Text 写作的工作流。"
cover:
  image: "/images/posts/hugo-github-pages-tutorial/cover.jpg"
  alt: "像素风格的创作房间插画"
  relative: false
ShowToc: true
TocOpen: true
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## 0. 这套方案适合谁

一句话：**想要一个自己的地方写字，不想维护服务器，也不想每年交钱。**

搭完之后你会得到：

- 一个 `https://你的用户名.github.io` 的独立域名（免费）
- 打开速度很快的纯静态页面（没有数据库查询，没有后端渲染）
- 写文章 = 新建一个 Markdown 文件 + 推送
- 完全免费，没有广告，没有平台审核，数据在自己手里

代价也说清楚：

- **没有后台管理界面**，写文章靠编辑器和 Git
- **评论要外挂**（giscus、utterances 之类）
- **不能用 PHP/插件**，纯静态
- 想改样式得懂一点 HTML/CSS

如果你只是偶尔发发感想、不想碰命令行，语雀或 Notion 更合适。但如果你写的是技术笔记、希望内容长期可控，这套组合是目前性价比最高的。

---

## 1. 为什么是 Hugo + GitHub Pages

静态博客生成器不少，主流三个：

| | Hugo | Hexo | Astro |
|---|---|---|---|
| 语言 | Go | Node.js | Node.js |
| 构建速度 | 极快（几百页 < 1 秒） | 中等 | 较慢 |
| 依赖 | 单个二进制，无运行时 | 需要 Node 环境 | 需要 Node 环境 |
| 主题生态 | 多，偏技术风 | 最多，国内最活跃 | 新，设计感强 |
| 上手难度 | 低 | 低 | 中 |

Hugo 最打动我的是**没有依赖**。它是一个编译好的 exe，扔到哪都能跑，不用 `npm install` 一堆包，也不用担心 Node 版本升级把项目搞崩。文章多了以后构建速度也不会变成灾难。

GitHub Pages 则是托管方：仓库里的静态文件直接变成网站，免费，自带 HTTPS，支持自定义域名。

两者组合起来，整个链路是：

```
本地写 Markdown  →  Hugo 构建成 HTML  →  推到 GitHub  →  Actions 自动部署  →  网站更新
```

你只需要关心第一步。

---

## 2. 准备环境

### 2.1 Git

```bash
git --version
```

没有的话去 [git-scm.com](https://git-scm.com/) 装，一路默认即可。

装完配一下身份，否则提交记录里没有作者：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

邮箱建议用 GitHub 账号绑定的那个，提交才会算到你名下。

### 2.2 Hugo

**必须装 extended 版本**，标准版不支持 SCSS/SASS 编译，很多主题（包括 PaperMod 的部分功能）会构建失败。

Windows：

```bash
winget install Hugo.Hugo.Extended
# 或者 scoop install hugo-extended
```

macOS：

```bash
brew install hugo
```

Linux（Debian/Ubuntu）直接下 deb 包最省事：

```bash
wget https://github.com/gohugoio/hugo/releases/download/v0.168.0/hugo_extended_0.168.0_linux-amd64.deb
sudo dpkg -i hugo_extended_0.168.0_linux-amd64.deb
```

验证：

```bash
hugo version
```

输出里必须带 `extended` 字样：

```
hugo v0.168.0+extended windows/amd64 BuildDate=...
```

> **版本要记住。** 后面配 GitHub Actions 时，线上用的 Hugo 版本必须和本地一致，否则会出现"本地能构建、线上报错"的情况。Hugo 从 0.146 之后改了不少配置项，跨版本踩坑很常见。

### 2.3 GitHub 账号

没有就注册一个。用户名会直接变成你的域名，比如用户名 `zhangsan`，博客地址就是 `zhangsan.github.io`。

---

## 3. 创建站点骨架

```bash
hugo new site myblog
cd myblog
```

生成的结构：

```
myblog/
├── archetypes/     # 新建文章的模板
├── assets/         # 需要 Hugo 处理的资源（SCSS 等）
├── content/        # 所有文章，你 99% 的时间在这里
├── data/           # 结构化数据（可选）
├── layouts/        # 自定义模板，覆盖主题用
├── static/         # 原样拷贝到网站根目录的文件（图片、favicon）
├── themes/         # 主题
└── hugo.yaml       # 站点配置
```

现在还没有配置文件和主题，直接 `hugo server` 会报错，继续往下走。

顺手初始化 Git：

```bash
git init -b main
```

`-b main` 指定主分支叫 `main`，和 GitHub 默认一致，省得后面改名。

---

## 4. 安装主题 PaperMod

PaperMod 是 Hugo 社区最流行的主题之一：极简、自带深色模式、全文搜索、代码高亮、目录、归档，该有的都有，不该有的不塞。

```bash
git clone --depth 1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**关键一步，必须做：**

```bash
rm -rf themes/PaperMod/.git
```

不删的话，Git 会把这个目录识别成**嵌套仓库（submodule）**，你 `git add` 的时候它只记录一个空引用，推到 GitHub 上主题文件全丢，构建直接失败。这个坑非常隐蔽，报错信息也看不出原因。

删掉 `.git` 之后，主题就变成普通文件夹，跟着你的仓库一起走。

> 另一种做法是用 git submodule 管理主题，更新方便，但 clone 时容易漏掉 `--recursive`，新手更容易踩坑。直接删 `.git` 最稳。

---

## 5. 写配置文件

在项目根目录新建 `hugo.yaml`。这是一份可以直接用的完整配置：

```yaml
baseURL: "https://你的用户名.github.io/"
title: 我的博客
theme: PaperMod
locale: zh-CN
defaultContentLanguage: zh
hasCJKLanguage: true
enableRobotsTXT: true
enableEmoji: true

pagination:
  pagerSize: 10

permalinks:
  posts: /posts/:slug/

outputs:
  home:
    - HTML
    - RSS
    - JSON          # 搜索功能需要

params:
  env: production
  description: "我的个人笔记"
  author: 你的名字
  DateFormat: "2006-01-02"
  defaultTheme: auto      # 跟随系统深/浅色

  ShowReadingTime: true
  ShowShareButtons: true
  ShowPostNavLinks: true
  ShowBreadCrumbs: true
  ShowCodeCopyButtons: true
  ShowToc: true
  TocOpen: false

  homeInfoParams:
    Title: "你好 👋"
    Content: "这里是我的笔记。"

  socialIcons:
    - name: github
      url: "https://github.com/你的用户名"
    - name: rss
      url: "/index.xml"

menu:
  main:
    - name: 文章
      url: /posts/
      weight: 10
    - name: 归档
      url: /archives/
      weight: 20
    - name: 标签
      url: /tags/
      weight: 30
    - name: 搜索
      url: /search/
      weight: 40

markup:
  goldmark:
    renderer:
      unsafe: true      # 允许 Markdown 里写原始 HTML
  highlight:
    noClasses: false
    guessSyntax: true
    lineNos: false
```

几个容易搞错的地方：

**`locale` 不是 `languageCode`。** 老教程里都是 `languageCode: zh-cn`，Hugo 0.158 之后改名为 `locale`，用旧字段会报弃用警告。

**`pagerSize` 不是 `paginate`。** 分页配置从顶层 `paginate: 10` 变成了 `pagination.pagerSize`。

**`permalinks` 里的 `:slug`** 指的是文章 front matter 里的 `slug` 字段。不填的话 Hugo 会用标题生成 URL，中文标题会变成一长串中文路径（能访问，但分享出去很丑，也不利于别人引用）。

---

## 6. 写第一篇文章

```bash
hugo new posts/hello-world.md
```

Hugo 会按 `archetypes/default.md` 生成一个带日期的空文件。直接改成这样：

```markdown
---
title: "第一篇"
slug: "hello-world"
date: 2026-10-21T12:00:00+08:00
draft: false
tags: ["随笔"]
categories: ["记录"]
summary: "列表页显示的一句话摘要"
ShowToc: true
---

正文从这里开始。
```

front matter 逐项说明：

| 字段 | 作用 | 注意 |
|---|---|---|
| `title` | 文章标题 | 会显示在页面和列表 |
| `slug` | URL 片段 | **必须填英文**，决定 `/posts/hello-world/` |
| `date` | 发布时间 | 必须是 `YYYY-MM-DDTHH:MM:SS+08:00` 格式 |
| `draft` | 草稿标记 | `true` 时本地预览可见，构建时跳过 |
| `tags` / `categories` | 标签 / 分类 | 会自动生成聚合页 |
| `summary` | 列表页摘要 | 不填则截取正文前 70 字 |
| `ShowToc` | 是否显示目录 | 长文建议开 |
| `cover` | 封面图 | 见下方 |

### 图片怎么放

图片统一放 `static/` 下，按文章分目录：

```
static/
└── images/
    └── posts/
        └── hello-world/
            ├── 01.png
            └── 02.png
```

文章里用**绝对路径**引用：

```markdown
![](/images/posts/hello-world/01.png)
```

`static/` 里的东西会被原样拷贝到网站根目录，所以 `/images/...` 就是最终 URL。

> 别用相对路径 `./01.png`，Hugo 的路径解析规则和普通 Markdown 编辑器不一样，很容易图裂。

### 加封面

```yaml
cover:
  image: "/images/posts/hello-world/cover.png"
  alt: "封面说明"
  relative: false
```

`relative: false` 表示用站点根路径，和上面图片引用规则一致。

---

## 7. 本地预览

```bash
hugo server -D
```

打开 http://localhost:1313

`-D` 是 `--buildDrafts`，把草稿也渲染出来。**不写这个参数，`draft: true` 的文章看不到。**

改文件保存后浏览器会自动刷新（热重载），不用重启服务。

两个常用参数：

```bash
hugo server -D --navigateToChanged   # 保存后自动跳到当前编辑的页面
hugo server -D --disableFastRender   # 改配置/模板后行为更准确
```

`--disableFastRender` 在改 `hugo.yaml` 或主题模板时建议加上，否则有时改动不生效。

停止服务：`Ctrl + C`。

---

## 8. 用 Sublime Text 写博客

命令行 `hugo new` 只是创建文件，真正写字还是在编辑器里。Sublime Text 是我用得最顺的一个：启动快、不占内存、Markdown 支持够用、跨平台。

这一节把 Sublime 配成一个"博客写作台"。

### 8.1 把项目文件夹打开

`Project → Add Folder to Project`，选中博客根目录。

然后 `Project → Save Project As`，存成 `myblog.sublime-project`。

以后从 `Project → Open Recent` 直接打开，侧边栏会保留整个目录树，`Ctrl + P` 可以按文件名模糊搜索 —— 文章多了以后这个功能救命。

> 项目文件里可以写排除规则，把 `public/`、`resources/` 这些构建产物隐藏掉，侧边栏会干净很多：

```json
{
  "folders": [
    {
      "path": ".",
      "folder_exclude_patterns": ["public", "resources", ".git", ".migrate"]
    }
  ]
}
```

### 8.2 装 Package Control 和插件

如果没装过 Package Control：`Ctrl + Shift + P` → 输入 `Install Package Control` → 回车。

然后 `Ctrl + Shift + P` → `Package Control: Install Package`，装这几个：

| 插件 | 作用 | 必要性 |
|---|---|---|
| **MarkdownEditing** | Markdown 语法高亮、快捷键、列表自动续行 | 推荐 |
| **Terminal** | 在 Sublime 里直接开终端，跑 hugo server | 强烈推荐 |
| MarkdownPreview | 在浏览器预览 Markdown | 可选 |
| SublimeLinter | 语法检查 | 可选 |

**MarkdownPreview 其实可以跳过** —— Hugo 的 `hugo server` 本身就是最好的预览，还能看到主题的真实效果。MarkdownPreview 渲染出来的是纯 Markdown 样式，和最终页面差别很大，反而容易误判。

### 8.3 配置一个 Build System 跑 hugo server

`Tools → Build System → New Build System`，粘贴：

```json
{
    "shell_cmd": "hugo server -D --navigateToChanged --disableFastRender",
    "working_dir": "${project_path:${folder}}",
    "selector": "text.html.markdown",
    "quiet": true,
    "encoding": "utf-8"
}
```

保存为 `Hugo Server.sublime-build`（默认会存到 `Packages/User/`）。

之后 `Ctrl + B` 就直接启动本地服务，底部面板显示构建日志，`Ctrl + Break` 停止。

`working_dir` 那行很关键 —— 它让命令在项目根目录执行，否则 Hugo 找不到 `hugo.yaml`。

> **便携版注意**：如果你用的是便携版 Sublime（`Data` 目录在安装目录里，不在 `AppData`），配置都保存在 `安装目录\Data\Packages\User\` 下。比如装在 `E:\Sublime`，那就是 `E:\Sublime\Data\Packages\User\`。换电脑时整个文件夹拷走，配置和插件全跟着走。

### 8.4 做一个 front matter 模板

每篇文章的头部字段都一样，手打太累。用 Snippet 解决。

`Tools → Developer → New Snippet`，替换成：

```xml
<snippet>
    <content><![CDATA[
---
title: "${1:文章标题}"
slug: "${2:my-post}"
date: ${3:2026-01-01T10:00:00+08:00}
draft: false
tags: ["${4:标签}"]
categories: ["${5:分类}"]
summary: "${6:一句话摘要}"
ShowToc: true
TocOpen: false
cover:
  image: ""
  alt: ""
---

${0}
]]></content>
    <tabTrigger>hugo</tabTrigger>
    <scope>text.html.markdown</scope>
    <description>Hugo front matter 模板</description>
</snippet>
```

保存到 `Packages/User/hugo-frontmatter.sublime-snippet`。

以后新建 `.md` 文件，输入 `hugo` 按 `Tab`，模板直接展开，光标停在标题位置，按 `Tab` 依次跳到下一个字段。

### 8.5 改几个关键设置

`Preferences → Settings`，在右侧用户设置里加：

```json
{
    "translate_tabs_to_spaces": true,
    "tab_size": 2,
    "word_wrap": "auto",
    "default_line_ending": "unix",
    "ensure_newline_at_eof_on_save": true,
    "trim_trailing_white_space_on_save": "all"
}
```

**`default_line_ending: unix` 这条别漏。** Windows 默认用 CRLF 换行，推到 GitHub 后 Git 会不停地警告 `LF will be replaced by CRLF`，虽然不影响构建，但看着烦，而且和 Linux 上的协作者混用时会出问题。统一成 LF 最省事。

`word_wrap: auto` 让长段落自动折行，写长文时不用横向滚动。

### 8.6 配两个快捷键

`Preferences → Key Bindings`，在右侧用户键位里加：

```json
[
    {
        "keys": ["ctrl+alt+n"],
        "command": "new_file"
    },
    {
        "keys": ["ctrl+alt+b"],
        "command": "build",
        "args": { "build_system": "Hugo Server.sublime-build" }
    }
]
```

`Ctrl + Alt + N` 新建文件，`Ctrl + Alt + B` 启动本地预览。

### 8.7 完整的写作流程

配好之后，写一篇文章是这样的：

1. `Ctrl + Alt + N` 新建文件
2. 输入 `hugo` + `Tab`，front matter 自动填好
3. 存到 `content/posts/我的文章.md`
4. 图片丢进 `static/images/posts/我的文章/`，正文里写 `![](/images/posts/我的文章/01.png)`
5. `Ctrl + Alt + B` 起本地服务，浏览器看效果
6. 满意了，终端里提交推送

全程不用离开编辑器。

---

## 9. 推到 GitHub

### 9.1 建仓库

仓库名有硬性规则：**必须是 `你的用户名.github.io`**。

这是 GitHub Pages 的个人主页站点规则 —— 只有这个名字的仓库，才会被映射到 `https://你的用户名.github.io/` 这个根域名。叫 `blog` 或 `my-site` 的话，地址会变成 `https://你的用户名.github.io/blog/`，多一层路径。

创建时**不要**勾选 "Add a README file"，否则会和本地仓库冲突。

### 9.2 关联并推送

```bash
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git add .
git commit -m "初始化博客"
git push -u origin main
```

### 9.3 加一个 .gitignore

构建产物不该进仓库：

```gitignore
# Hugo 构建产物
public/
resources/_gen/
.hugo_build.lock

# 系统文件
.DS_Store
Thumbs.db
```

`public/` 是 Hugo 生成的最终 HTML，GitHub Actions 会自己构建，不需要提交。提交了反而会让仓库体积暴涨，还可能和线上构建结果打架。

---

## 10. 配置自动部署

在项目里新建 `.github/workflows/hugo.yaml`：

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

defaults:
  run:
    shell: bash

env:
  HUGO_VERSION: 0.168.0

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Install Hugo CLI
        run: |
          wget -q -O ${{ runner.temp }}/hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i ${{ runner.temp }}/hugo.deb
          hugo version

      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          TZ: Asia/Shanghai
        run: |
          hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

几个必须理解的点：

**`permissions` 三行不能少。** `pages: write` 给部署权限，`id-token: write` 是 OIDC 认证用的，缺了会在 deploy 阶段报权限错误。

**`HUGO_VERSION` 要和本地一致。** 这里装的是 extended 版，和本地版本对上，避免配置语法差异。

**`concurrency`** 防止连续两次推送时两个构建同时跑、互相覆盖。`cancel-in-progress: false` 表示不取消正在跑的任务，避免部署到一半被打断。

**`HUGO_CACHEDIR` 为什么写在 step 里而不是 job 里** —— 这是最容易踩的坑。`${{ runner.temp }}` 属于 runner 上下文，在 job 级 `env` 里不可用，会直接报错：

```
Unrecognized named-value: 'runner'
```

而且这个错误发生在 workflow 解析阶段，**不会产生任何 job 日志**，你在 Actions 页面只能看到一个红色的 failure，点进去什么都没有。排查时非常误导人。

---

## 11. 开启 GitHub Pages

推到 GitHub 之后，去仓库：

`Settings → Pages → Build and deployment → Source`

选 **GitHub Actions**（不要选 "Deploy from a branch"，那是给纯静态上传用的，和我们的 workflow 冲突）。

选完之后，每次推送 `main` 分支，Actions 会自动构建部署，大约 1 分钟。

在仓库的 **Actions** 标签页可以看到运行状态，**Pages** 设置页会显示访问地址。

---

## 12. 五个常见的坑

### 坑一：主题目录变成 submodule，线上构建失败

**现象**：本地一切正常，推送后 Actions 报 `theme "PaperMod" not found`。

**原因**：`git clone` 下来的主题带 `.git`，Git 把它当嵌套仓库，只提交了一个空引用。

**解决**：`rm -rf themes/PaperMod/.git` 后重新 `git add`。如果已经提交过，需要先 `git rm --cached themes/PaperMod` 再重新加。

### 坑二：文章 URL 变成一长串中文

**现象**：`/posts/从零搭建博客完整指南/`，分享出去很别扭。

**原因**：front matter 没写 `slug`，Hugo 用标题生成路径。

**解决**：每篇文章都加 `slug: "english-slug"`。已经发出去的文章想改 URL，记得在旧地址留一个 `aliases` 做跳转：

```yaml
aliases:
  - /posts/旧地址/
```

### 坑三：本地能构建，线上报错

**现象**：本地 `hugo server` 正常，Actions 里报配置项未知或模板错误。

**原因**：两边 Hugo 版本不一致。GitHub Actions 默认装最新版，本地可能是旧版（或反过来）。

**解决**：把 workflow 里的 `HUGO_VERSION` 固定成和本地 `hugo version` 完全一致的版本号。别用 `latest`。

### 坑四：图片全裂

**现象**：本地预览正常，线上图片 404。

**原因**：路径写法不对。常见三种错法：

- 用了相对路径 `./01.png`
- 图片放在 `content/` 里而不是 `static/`
- 大小写不一致（Linux 服务器区分大小写，Windows 不区分）

**解决**：图片统一放 `static/images/posts/<slug>/`，正文统一用 `/images/posts/<slug>/xx.png` 这种以 `/` 开头的绝对路径。

### 坑五：日期格式写错，文章不显示

**现象**：文章写了但首页看不到。

**原因**：`date` 格式不合法，Hugo 解析失败后当作零值处理，排序时被扔到最后；或者 `draft: true` 忘了改。

**解决**：统一用 `2026-10-21T12:00:00+08:00` 这种带时区的 ISO 8601 格式。时区别漏，否则可能因为时差被判定为未来时间而不显示。

---

## 13. 日常写作流程

配好之后，你每天只需要做三件事：

```bash
# 1. 写
# 在 Sublime 里新建 content/posts/xxx.md

# 2. 看
hugo server -D

# 3. 发
git add .
git commit -m "新文章：xxx"
git push
```

推送后 1 分钟自动上线。

如果想写草稿但先不发，把 `draft: true` 留着，`git push` 也不会出现在线上（构建时跳过），等写完了改成 `false` 再推。

---

## 14. 还能加什么

**评论系统**：giscus 是基于 GitHub Discussions 的，免费、无广告、不需要单独注册账号。在 [giscus.app](https://giscus.app/) 填仓库信息，拿到一段 script，塞进 `layouts/partials/comments.html` 即可。

**自定义域名**：买个域名，在仓库 `Settings → Pages → Custom domain` 填上，然后去域名商加一条 CNAME 记录指向 `你的用户名.github.io`。GitHub 会自动签 HTTPS 证书。

**SEO**：PaperMod 自带 `og:` 标签和 sitemap。再补一个 `robots.txt` 和 Google Search Console / Bing 站长验证，收录会快一些。

**统计分析**：不想用 Google Analytics 的话，可以用 Umami 或 Plausible 自建，或者直接看 GitHub 仓库的 Traffic 数据（虽然只有 14 天）。

**备份**：文章都在 Git 里，本身就是备份。想更保险可以定期 `git clone` 一份到别的盘，或者加一个 Gitee 镜像。

---

## 最后

这套东西搭一次，能用很多年。之后所有精力都在"写"上面，而不是"维护"上面 —— 这大概是我最看重的一点。

如果这篇文章帮你省下了几个小时，那就够了。有问题欢迎在下面留言。
