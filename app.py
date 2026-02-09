from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "shinya-bbs-secret-key"
# データを保存する簡易データベース(本番環境ではSQLiteやPostgreSQLを使用)
boards = {
    'news': 'ニュース速報',
    'chat': '雑談',
    'programming': 'プログラミング',
    'game': 'ゲーム',
    'music': '音楽'
}

threads = {
    'chat': [
        {'id': 1, 'title': '【雑談】サンプル', 'post_count': 2},
        {'id': 2, 'title': '【質問】サンプル', 'post_count': 0},
        {'id': 3, 'title': '【速報】サンプル', 'post_count': 0}
    ]
}

posts = {
    1: [
        {'id': 1, 'name': '名無しさん', 'body': 'サンプル', 'date': '2026/02/09'},
        {'id': 2, 'name': '名無しさん', 'body': 'サンプル', 'date': '2026/02/09'}
    ]
}

# 共通のHTMLヘッダーとフッター
def render_page(content, boards_dict):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>SHINYA BBS</title>
  <style>
    body {{
      font-family: "MS PGothic", "Hiragino Kaku Gothic ProN", sans-serif;
      background: #efefef;
      margin: 0;
    }}
    a {{ color: #0000cc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    header {{
      background: #0055aa;
      color: #fff;
      padding: 8px 16px;
      font-weight: bold;
      font-size: 18px;
    }}

    #layout {{
      max-width: 1100px;
      margin: 0 auto;
      background: #fff;
      display: flex;
    }}

    aside {{
      width: 220px;
      border-right: 1px solid #ccc;
      background: #f7f7f7;
      padding: 8px;
      font-size: 14px;
    }}
    aside h3 {{
      margin: 8px 0 4px;
      font-size: 14px;
      border-bottom: 1px solid #aaa;
    }}
    .board-list div {{
      padding: 2px 0;
    }}

    main {{
      flex: 1;
      padding: 12px;
    }}

    .thread-list {{
      border: 1px solid #ccc;
      margin-bottom: 16px;
    }}
    .thread-list .row {{
      padding: 6px;
      border-bottom: 1px dotted #999;
      font-size: 14px;
    }}
    .thread-list .row:last-child {{ border-bottom: none; }}
    .thread-list .row span {{
      color: #666;
      font-size: 12px;
    }}

    .thread-title {{
      font-size: 18px;
      font-weight: bold;
      border-bottom: 2px solid #ccc;
      margin-bottom: 8px;
    }}

    .post {{
      border-bottom: 1px dotted #999;
      padding: 6px 0;
      font-size: 14px;
    }}
    .post-header {{
      color: #008800;
      font-size: 12px;
    }}
    .post-body {{
      white-space: pre-wrap;
      line-height: 1.5;
    }}

    .post-form {{
      margin-top: 16px;
      border: 1px solid #ccc;
      background: #f9f9f9;
      padding: 8px;
      font-size: 14px;
    }}
    .post-form label {{
      display: block;
      margin-top: 6px;
    }}
    .post-form input,
    .post-form textarea {{
      width: 100%;
      box-sizing: border-box;
      font-family: inherit;
      margin-top: 2px;
    }}

    .new-thread-form {{
      border: 1px solid #ccc;
      background: #f9f9f9;
      padding: 8px;
      font-size: 14px;
      margin-bottom: 16px;
    }}
    .new-thread-form label {{
      display: block;
      margin-top: 6px;
    }}
    .new-thread-form input,
    .new-thread-form textarea {{
      width: 100%;
      box-sizing: border-box;
      font-family: inherit;
      margin-top: 2px;
    }}

    footer {{
      text-align: center;
      font-size: 12px;
      color: #666;
      padding: 8px;
      border-top: 1px solid #ccc;
      background: #fafafa;
    }}

    .notice {{
      background: #ffffe0;
      border: 1px solid #e0e0a0;
      padding: 6px;
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .success {{
      background: #e0ffe0;
      border: 1px solid #a0e0a0;
      padding: 6px;
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .pager {{
      margin-top: 8px;
      font-size: 13px;
    }}
    .pager a {{ margin-right: 4px; }}

  </style>
</head>
<body>

<header>SHINYA BBS</header>

<div id="layout">
  <aside>
    <h3>板一覧</h3>
    <div class="board-list">
      {''.join([f'<div><a href="/board/{board_id}">{board_name}</a></div>' for board_id, board_name in boards_dict.items()])}
    </div>

    <h3>メニュー</h3>
    <div><a href="/">トップ</a></div>
    <div><a href="/entrance">入口へ</a></div>
  </aside>

  <main>
    {content}
  </main>
</div>

<footer>
  SHINYA BBS
</footer>

</body>
</html>'''

@app.route('/')
def index():
    if not session.get('entered'):
        return redirect(url_for('entrance'))
    thread_list_html = ''
    for board_id, board_name in boards.items():
        thread_count = len(threads.get(board_id, []))
        thread_list_html += f'''
        <div class="row">
          <a href="/board/{board_id}">{board_name}</a>
          <span>({thread_count} スレッド)</span>
        </div>
        '''
    
    content = f'''
    <div class="notice">深夜テンションの猫が集まる匿名掲示板です</div>
    <h2>アクセスカウンタ</h2>
    <img src="http://moecounter.atserver186.jp/@:name" alt=":name" />
    <h2>板一覧</h2>
    <div class="thread-list">
      {thread_list_html}
    </div>
    '''
    
    return render_page(content, boards)
@app.route('/entrance', methods=['GET', 'POST'])
def entrance():
    if request.method == 'POST':
        session['entered'] = True
        return redirect(url_for('index'))

    content = '''
    <div class="notice">
      <strong>SHINYA BBSへようこそ</strong><br><br>
      この掲示板は匿名掲示板です。<br>
      誹謗中傷・違法行為は禁止されています。<br>
      書き込み内容は自己責任でお願いします。
    </div>
    <img src="https://keitagames.com/shinya-tension/bbs.png" width="400"/>
    <form method="POST">
      <p style="text-align:center;">
        <button type="submit" style="font-size:16px;padding:8px 24px;">
          同意して入場する
        </button>
      </p>
    </form>
    '''
    return render_page(content, boards)

@app.route('/board/<board_id>')
def board(board_id):
    if board_id not in boards:
        return redirect(url_for('index'))
    
    board_name = boards[board_id]
    board_threads = threads.get(board_id, [])
    message = request.args.get('message')
    
    message_html = f'<div class="success">{message}</div>' if message else ''
    
    thread_list_html = ''
    if board_threads:
        for thread in board_threads:
            thread_list_html += f'''
            <div class="row">
              <a href="/board/{board_id}/thread/{thread['id']}">{thread['title']}</a>
              <span>({thread['post_count']})</span>
            </div>
            '''
    else:
        thread_list_html = '<div class="row">スレッドがありません</div>'
    
    content = f'''
    {message_html}
    
    <h2>{board_name}</h2>
    
    <div class="new-thread-form">
      <strong>新規スレッド作成</strong>
      <form method="POST" action="/board/{board_id}/create_thread">
        <label>スレッドタイトル</label>
        <input type="text" name="title" required />
        <label>名前(省略可)</label>
        <input type="text" name="name" value="名無しさん" />
        <label>本文</label>
        <textarea name="body" rows="4" required></textarea>
        <p><button type="submit">スレッドを立てる</button></p>
      </form>
    </div>
    
    <h3>スレッド一覧</h3>
    <div class="thread-list">
      {thread_list_html}
    </div>
    '''
    
    return render_page(content, boards)

@app.route('/board/<board_id>/thread/<int:thread_id>')
def thread(board_id, thread_id):
    if board_id not in boards:
        return redirect(url_for('index'))
    
    board_name = boards[board_id]
    board_threads = threads.get(board_id, [])
    thread_obj = next((t for t in board_threads if t['id'] == thread_id), None)
    
    if not thread_obj:
        return redirect(url_for('board', board_id=board_id))
    
    thread_posts = posts.get(thread_id, [])
    message = request.args.get('message')
    
    message_html = f'<div class="success">{message}</div>' if message else ''
    
    posts_html = ''
    for post in thread_posts:
        posts_html += f'''
        <div class="post">
          <div class="post-header">{post['id']} :{post['name']}:{post['date']}</div>
          <div class="post-body">{post['body']}</div>
        </div>
        '''
    
    content = f'''
    {message_html}
    
    <p><a href="/board/{board_id}">← {board_name}に戻る</a></p>
    
    <div class="thread-title">{thread_obj['title']}</div>
    
    {posts_html}
    
    <div class="post-form">
      <strong>書き込みフォーム</strong>
      <form method="POST" action="/board/{board_id}/thread/{thread_id}/post">
        <label>名前(省略可)</label>
        <input type="text" name="name" value="名無しさん" />
        <label>本文</label>
        <textarea name="body" rows="4" required></textarea>
        <p><button type="submit">書き込む</button></p>
      </form>
    </div>
    '''
    
    return render_page(content, boards)

@app.route('/board/<board_id>/create_thread', methods=['POST'])
def create_thread(board_id):
    if board_id not in boards:
        return redirect(url_for('index'))
    
    title = request.form.get('title', '').strip()
    name = request.form.get('name', '名無しさん').strip() or '名無しさん'
    body = request.form.get('body', '').strip()
    
    if not title or not body:
        return redirect(url_for('board', board_id=board_id))
    
    # 新しいスレッドIDを生成
    all_thread_ids = []
    for board_thread_list in threads.values():
        all_thread_ids.extend([t['id'] for t in board_thread_list])
    new_thread_id = max(all_thread_ids) + 1 if all_thread_ids else 1
    
    # スレッドを作成
    new_thread = {
        'id': new_thread_id,
        'title': title,
        'post_count': 1
    }
    
    if board_id not in threads:
        threads[board_id] = []
    threads[board_id].insert(0, new_thread)
    
    # 最初の投稿を作成
    posts[new_thread_id] = [{
        'id': 1,
        'name': name,
        'body': body,
        'date': datetime.now().strftime('%Y/%m/%d %H:%M')
    }]
    
    return redirect(url_for('thread', board_id=board_id, thread_id=new_thread_id, message='スレッドを作成しました'))

@app.route('/board/<board_id>/thread/<int:thread_id>/post', methods=['POST'])
def create_post(board_id, thread_id):
    if board_id not in boards:
        return redirect(url_for('index'))
    
    name = request.form.get('name', '名無しさん').strip() or '名無しさん'
    body = request.form.get('body', '').strip()
    
    if not body:
        return redirect(url_for('thread', board_id=board_id, thread_id=thread_id))
    
    # 投稿を追加
    if thread_id not in posts:
        posts[thread_id] = []
    
    new_post_id = len(posts[thread_id]) + 1
    posts[thread_id].append({
        'id': new_post_id,
        'name': name,
        'body': body,
        'date': datetime.now().strftime('%Y/%m/%d %H:%M')
    })
    
    # スレッドの投稿数を更新
    for board_thread_list in threads.values():
        for thread_obj in board_thread_list:
            if thread_obj['id'] == thread_id:
                thread_obj['post_count'] = len(posts[thread_id])
                break
    
    return redirect(url_for('thread', board_id=board_id, thread_id=thread_id, message='書き込みました'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)