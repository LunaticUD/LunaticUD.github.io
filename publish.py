# -*- coding: utf-8 -*-
"""
无代理发布：通过 GitHub API 提交文件，不依赖 git 协议。
（github.com 的 git 端口被墙时，api.github.com 通常仍可直连）

用法:
    python publish.py "提交说明"
    python publish.py "提交说明" --no-local-commit

Token 读取顺序:
    1. 环境变量 GITHUB_TOKEN
    2. 项目下 .migrate/token.txt（文件里只放 token，一行）

原理:
    git status 拿到改动 -> Git Data API 创建 blob/tree/commit -> 更新 main 分支引用
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

OWNER = 'LunaticUD'
REPO = 'LunaticUD.github.io'
BRANCH = 'main'
API = 'https://api.github.com'
ROOT = os.path.dirname(os.path.abspath(__file__))


def die(msg):
    print('[错误] ' + msg)
    sys.exit(1)


def get_token():
    t = (os.environ.get('GITHUB_TOKEN') or '').strip()
    if t:
        return t
    p = os.path.join(ROOT, '.migrate', 'token.txt')
    if os.path.exists(p):
        t = open(p, encoding='utf-8').read().strip()
        if t:
            return t
    die('未找到 Token。\n'
        '  方法一：设置环境变量 GITHUB_TOKEN\n'
        '  方法二：把 token 写进 .migrate/token.txt（只写一行）')


def api(method, path, token, data=None):
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(API + path, data=body, method=method)
    req.add_header('Authorization', 'Bearer ' + token)
    req.add_header('Accept', 'application/vnd.github+json')
    if body:
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'ignore')[:500]
        die('API %s %s 失败（HTTP %s）\n%s' % (method, path, e.code, detail))
    except Exception as e:
        die('网络请求失败：%s\n（api.github.com 需要能直连，或临时开代理）' % e)


def git(*args):
    r = subprocess.run(['git', '-c', 'core.quotepath=false'] + list(args),
                       cwd=ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.stdout


def parse_status():
    """返回 [(动作, 路径)]，动作是 add 或 del"""
    changes = []
    for line in git('status', '--porcelain', '-uall').splitlines():
        if len(line) < 4:
            continue
        x, y = line[0], line[1]
        path = line[3:].strip()
        if ' -> ' in path:                      # 重命名 = 删除旧 + 新增新
            old, new = path.split(' -> ')
            changes.append(('del', old.strip('"')))
            changes.append(('add', new.strip('"')))
            continue
        if x == 'D' or y == 'D':
            changes.append(('del', path.strip('"')))
        else:
            changes.append(('add', path.strip('"')))
    return changes


def main():
    if len(sys.argv) < 2:
        die('用法：python publish.py "提交说明" [--no-local-commit]')
    message = sys.argv[1]
    local_commit = '--no-local-commit' not in sys.argv

    token = get_token()

    changes = parse_status()
    if not changes:
        print('没有检测到改动，无需发布。')
        return

    print('检测到 %d 处改动：' % len(changes))
    for act, p in changes:
        print('   %s %s' % ('删除' if act == 'del' else '更新', p))

    # 1. 当前分支头
    ref = api('GET', '/repos/%s/%s/git/ref/heads/%s' % (OWNER, REPO, BRANCH), token)
    head_sha = ref['object']['sha']
    head_commit = api('GET', '/repos/%s/%s/git/commits/%s' % (OWNER, REPO, head_sha), token)
    base_tree = head_commit['tree']['sha']
    print('远端当前 commit：%s' % head_sha[:7])

    # 2. 逐文件建 blob
    tree_entries = []
    for act, path in changes:
        full = os.path.join(ROOT, path.replace('/', os.sep))
        if act == 'del' or not os.path.exists(full):
            tree_entries.append({'path': path, 'mode': '100644',
                                 'type': 'blob', 'sha': None})
            continue
        with open(full, 'rb') as f:
            content = base64.b64encode(f.read()).decode('ascii')
        blob = api('POST', '/repos/%s/%s/git/blobs' % (OWNER, REPO), token,
                   {'content': content, 'encoding': 'base64'})
        tree_entries.append({'path': path, 'mode': '100644',
                             'type': 'blob', 'sha': blob['sha']})

    # 3. 新 tree
    tree = api('POST', '/repos/%s/%s/git/trees' % (OWNER, REPO), token,
               {'base_tree': base_tree, 'tree': tree_entries})

    # 4. 新 commit
    commit = api('POST', '/repos/%s/%s/git/commits' % (OWNER, REPO), token,
                 {'message': message, 'tree': tree['sha'], 'parents': [head_sha]})
    new_sha = commit['sha']
    print('已创建 commit：%s' % new_sha[:7])

    # 5. 移动分支
    api('PATCH', '/repos/%s/%s/git/refs/heads/%s' % (OWNER, REPO, BRANCH), token,
        {'sha': new_sha, 'force': False})

    print('\n[OK] 已发布到 https://github.com/%s/%s' % (OWNER, REPO))
    print('     GitHub Actions 会自动构建，约 1 分钟后生效')
    print('     站点：https://lunaticud.github.io/')

    # 6. 本地留档（sha 与远端不同，仅记录用）
    if local_commit:
        git('add', '-A')
        r = subprocess.run(['git', '-c', 'core.quotepath=false', 'commit', '-m', message],
                           cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        if r.returncode == 0:
            print('     本地已留档提交（注意：本地 sha 与远端不同，属正常）')


if __name__ == '__main__':
    main()
