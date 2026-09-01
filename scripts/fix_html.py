#!/usr/bin/env python3
"""Post-process generated HTML: readable tables, visible links and a wider page.
Usage: python3 fix_html.py [path/to/report.html]
"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'report_zh.html'
raw = open(path, encoding='utf-8').read()

css = '''
<style id="dsh-table-fix">
.dsh-table-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1.2em 0;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.06);}
.dsh-table-scroll table{width:100%;border-collapse:collapse;font-size:13px;line-height:1.55;table-layout:auto;}
.dsh-table-scroll th,.dsh-table-scroll td{padding:8px 10px;border:1px solid #e7e0da;vertical-align:top;word-break:break-word;text-align:left;}
.dsh-table-scroll th{background:#f7efe9;color:#4a2f23;white-space:nowrap;font-weight:700;}
.dsh-table-scroll tr:nth-child(even) td{background:#fcf9f7;}
.dsh-table-scroll tr:hover td{background:#fdf1e8;}
.dsh-table-scroll a{color:#c2410c;text-decoration:underline;font-weight:600;word-break:break-all;}
.dsh-table-scroll td:first-child{white-space:nowrap;text-align:center;}
.dsh-copy-btn{display:inline-flex;align-items:center;gap:4px;background:#f3f4f6;border:1px solid #d1d5db;border-radius:4px;padding:2px 8px;font-size:12px;cursor:pointer;color:#374151;margin-left:6px;transition:all 0.15s;}
.dsh-copy-btn:hover{background:#e5e7eb;color:#111827;}
@media (max-width:600px){.dsh-table-scroll table{font-size:12px;}.dsh-table-scroll th,.dsh-table-scroll td{padding:6px 7px;}}
</style>
<script>
function dshCopy(text, btn) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      const orig = btn.innerText;
      btn.innerText = '✓ 已复制';
      setTimeout(() => { btn.innerText = orig; }, 2000);
    });
  }
}
</script>
'''
if '</head>' in raw:
    raw = raw.replace('</head>', css + '</head>', 1)
else:
    raw = raw.replace('</body>', css + '</body>', 1)

raw = re.sub(r'(<table[^>]*>.*?</table>)',
             lambda m: '<div class="dsh-table-scroll">' + m.group(1) + '</div>',
             raw, flags=re.S)

hint = '<div style="background:#fdf3ec;border:1px solid #f0c8a8;border-left:4px solid #c2410c;border-radius:8px;padding:10px 14px;margin:14px 0;font-size:14px;color:#5b3a26;">🔗 表格中的「链接」列均可直接点击，打开官方岗位页面；宽表格可左右滑动查看。</div>'
m = re.search(r'<body[^>]*>', raw)
if m:
    raw = raw[:m.end()] + hint + raw[m.end():]

raw = raw.replace('max-width: 860px', 'max-width: min(1500px, 96vw)')
raw = raw.replace('padding: 24px', 'padding: 36px 40px')

open(path, 'w', encoding='utf-8').write(raw)
print('tables wrapped:', len(re.findall(r'<div class="dsh-table-scroll">', raw)))
print('links:', len(re.findall(r'<a ', raw)))
print('done:', path)
