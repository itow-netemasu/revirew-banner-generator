#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64, os

def b64img(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

D = '/Users/tanoshikacreative/Downloads'
I = D + '/アイコン'

img_data = {}
img_data['ichigo_top'] = b64img(D + '/いちご装飾.png')
img_data['ichigo_br']  = b64img(D + '/いちご装飾右下用.png')
for n in range(1, 9):
    img_data['f' + str(n)] = b64img(I + '/女性' + str(n) + '.png')
    img_data['m' + str(n)] = b64img(I + '/男性' + str(n) + '.png')

parts = ['const IMG_SRC = {']
for k, v in img_data.items():
    parts.append('  ' + k + ': "data:image/png;base64,' + v + '",')
parts.append('};')
imgs_js = '\n'.join(parts)

css = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #efefef; font-family: 'Hiragino Sans', 'Yu Gothic UI', Meiryo, sans-serif; }
h1 { font-size: 16px; color: #b00019; padding: 14px 20px; border-bottom: 2px solid #b00019; }
#app { display: flex; gap: 24px; padding: 20px; max-width: 1500px; margin: 0 auto; }
#controls { width: 380px; flex-shrink: 0; display: flex; flex-direction: column; gap: 14px; }
.panel { background: #fff; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.panel-title { font-size: 13px; font-weight: bold; color: #555; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 12px; }
.name-row { display: flex; align-items: center; gap: 6px; }
.name-row input { flex: 1; border: 1px solid #ccc; border-radius: 6px; padding: 8px 10px; font-size: 15px; font-family: inherit; }
.name-row input:focus { outline: none; border-color: #b00019; }
.suffix { font-size: 15px; white-space: nowrap; color: #333; }
.tabs { display: flex; gap: 4px; margin-bottom: 10px; }
.tab-btn { padding: 5px 18px; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; background: #f5f5f5; font-size: 13px; font-family: inherit; }
.tab-btn.active { background: #b00019; color: #fff; border-color: #b00019; }
.avatar-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; }
.avatar-item { border-radius: 50%; overflow: hidden; cursor: pointer; border: 2px solid transparent; transition: border-color .15s; aspect-ratio: 1; }
.avatar-item:hover { border-color: #ffaaaa; }
.avatar-item.selected { border-color: #b00019; box-shadow: 0 0 0 2px #b00019; }
.avatar-item img { width: 100%; height: 100%; object-fit: cover; display: block; }
.color-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 6px; }
.color-swatch { border-radius: 50%; cursor: pointer; border: 3px solid transparent; aspect-ratio: 1; transition: border-color .15s, box-shadow .15s; }
.color-swatch:hover { box-shadow: 0 0 0 2px rgba(0,0,0,0.25); }
.color-swatch.selected { border-color: #fff; box-shadow: 0 0 0 3px #333; }
.setting-row { display: flex; align-items: center; gap: 8px; }
.setting-row + .setting-row { margin-top: 8px; }
.setting-label { font-size: 12px; color: #666; width: 52px; flex-shrink: 0; }
.toggle-group { display: flex; gap: 4px; flex: 1; }
.toggle-btn { flex: 1; padding: 6px 4px; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; background: #f5f5f5; font-size: 13px; font-family: inherit; transition: all .15s; }
.toggle-btn.active { background: #b00019; color: #fff; border-color: #b00019; }
.block-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px; }
.block { border: 1px solid #e5e5e5; border-radius: 8px; padding: 10px; background: #fafafa; }
.block-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.block-style { font-size: 12px; padding: 4px 8px; border-radius: 4px; border: 1px solid #ccc; font-family: inherit; cursor: pointer; }
.block-del { background: none; border: none; color: #bbb; cursor: pointer; font-size: 20px; line-height: 1; padding: 0 2px; }
.block-del:hover { color: #b00019; }
.block-text { width: 100%; border: 1px solid #ddd; border-radius: 4px; padding: 6px 8px; font-size: 14px; resize: vertical; font-family: inherit; min-height: 64px; }
.block-text:focus { outline: none; border-color: #b00019; }
.add-btn { width: 100%; padding: 8px; border: 2px dashed #ccc; border-radius: 8px; background: none; cursor: pointer; color: #888; font-size: 13px; font-family: inherit; transition: all .15s; }
.add-btn:hover { border-color: #b00019; color: #b00019; }
.dl-btn { width: 100%; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: bold; font-family: inherit; transition: opacity .15s; background: #b00019; color: #fff; }
.dl-btn:hover { opacity: .82; }
#preview { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 10px; }
.preview-label { font-size: 12px; color: #888; }
canvas { box-shadow: 0 4px 20px rgba(0,0,0,.18); width: 520px; max-width: 100%; display: block; }
"""

body = """
<h1>ONE GO レビューバナージェネレーター</h1>
<div id="app">
  <div id="controls">
    <div class="panel">
      <div class="panel-title">投稿者名</div>
      <div class="name-row">
        <input type="text" id="poster-name" placeholder="例：田中">
        <span class="suffix">様</span>
      </div>
    </div>
    <div class="panel">
      <div class="panel-title">アバター選択</div>
      <div class="tabs">
        <button class="tab-btn active" data-gender="f">女性</button>
        <button class="tab-btn" data-gender="m">男性</button>
      </div>
      <div class="avatar-grid" id="avatar-grid"></div>
    </div>
    <div class="panel">
      <div class="panel-title">背景カラー</div>
      <div class="color-grid" id="color-grid"></div>
    </div>
    <div class="panel">
      <div class="panel-title">テキスト設定</div>
      <div class="setting-row">
        <span class="setting-label">揃え</span>
        <div class="toggle-group">
          <button class="toggle-btn active" data-align="left">左揃え</button>
          <button class="toggle-btn" data-align="center">中央揃え</button>
        </div>
      </div>
      <div class="setting-row">
        <span class="setting-label">サイズ</span>
        <div class="toggle-group">
          <button class="toggle-btn active" data-size="medium">中</button>
          <button class="toggle-btn" data-size="large">大</button>
        </div>
      </div>
      <div class="setting-row">
        <span class="setting-label">太さ</span>
        <div class="toggle-group">
          <button class="toggle-btn" data-weight="normal">標準</button>
          <button class="toggle-btn active" data-weight="bold">太字</button>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-title">テキストブロック</div>
      <div class="block-list" id="block-list"></div>
      <button class="add-btn" id="add-block">＋ ブロックを追加</button>
    </div>
    <div class="panel">
      <button class="dl-btn" id="dl-png">PNG 保存</button>
    </div>
  </div>
  <div id="preview">
    <div class="preview-label">プレビュー（50%表示 ／ 出力 W=1040px）</div>
    <canvas id="canvas" width="1040"></canvas>
  </div>
</div>
"""

# NOTE: This JS block is intentionally NOT an f-string to preserve ${} template literals.
# The __IMGS_JS__ token is replaced after generation.
js = r"""
// ─── Constants ───────────────────────────────────────────────
const W = 1040;
const BG_COLORS = ['#c4001e','#1256a0','#1a7a3c','#7b1fa2','#e65100','#00695c','#4e342e','#1a237e'];
const C_WHITE = '#ffffff';
const C_BODY  = '#222222';
const ICHIGO_TOP_H = 220;
const CARD_MX = 72;
const CARD_X  = CARD_MX;
const CARD_W  = W - CARD_MX * 2;    // 896
const CARD_R  = 38;
const AVATAR_R = 110;
const TEXT_L  = CARD_X + 71;        // 143
const TEXT_W  = CARD_W - 142;       // 754
const BODY_SZ = 32;
const BODY_LH = 60;
const BODY_SIZES = {
  large:  { sz: 40, lh: 74 },
  medium: { sz: 32, lh: 60 },
  small:  { sz: 24, lh: 46 }
};
const HEAD_SZ = 76;
const HEAD_LH = 104;
const ICHIGO_BR_W = 140;
const ICHIGO_BR_H = Math.round(140 * 139 / 127);
const FONT_JP = '"Hiragino Sans","Yu Gothic UI","Meiryo",sans-serif';

// ─── State ───────────────────────────────────────────────────
const state = {
  name:    '',
  avatar:  'f1',
  gender:  'f',
  bgColor: '#c4001e',
  align:   'left',
  weight:   'bold',
  bodySize: 'medium',
  blocks: [{ id: 1, style: 'normal', text: '' }],
  nextId: 2
};

// ─── Image cache ─────────────────────────────────────────────
const imgs = {};

async function loadImages() {
  const tasks = Object.entries(IMG_SRC).map(([k, url]) =>
    new Promise(resolve => {
      const img = new Image();
      img.onload = () => {
        imgs[k] = (k.startsWith('f') || k.startsWith('m'))
          ? processAvatar(img) : img;
        resolve();
      };
      img.onerror = resolve;
      img.src = url;
    })
  );
  await Promise.all(tasks);
}

// ─── Avatar background removal ───────────────────────────────
function processAvatar(img) {
  const oc = document.createElement('canvas');
  oc.width  = img.naturalWidth;
  oc.height = img.naturalHeight;
  const octx = oc.getContext('2d');
  octx.drawImage(img, 0, 0);

  const id = octx.getImageData(0, 0, oc.width, oc.height);
  const d  = id.data;
  const w  = oc.width, h = oc.height;

  // If corners are already transparent, background removal is not needed
  const corners = [0, (w-1), w*(h-1), w*(h-1)+(w-1)];
  const isAlreadyTransparent = corners.every(px => d[px*4+3] < 128);
  if (isAlreadyTransparent) return oc;

  // Opaque background: flood-fill from edges to find background region
  const visited = new Uint8Array(w * h);
  const queue   = [];
  let head = 0;

  // Sample background color from top-left corner
  const bgR = d[0], bgG = d[1], bgB = d[2];
  const isBg = px => {
    const i = px * 4;
    return d[i+3] > 128 &&
           Math.abs(d[i]   - bgR) < 30 &&
           Math.abs(d[i+1] - bgG) < 30 &&
           Math.abs(d[i+2] - bgB) < 30;
  };

  for (let x = 0; x < w; x++) {
    for (const px of [x, w*(h-1)+x]) {
      if (!visited[px] && isBg(px)) { visited[px] = 1; queue.push(px); }
    }
  }
  for (let y = 1; y < h-1; y++) {
    for (const px of [y*w, y*w+w-1]) {
      if (!visited[px] && isBg(px)) { visited[px] = 1; queue.push(px); }
    }
  }

  while (head < queue.length) {
    const px = queue[head++];
    d[px*4+3] = 0;
    const x = px % w, y = (px / w) | 0;
    const ns = [];
    if (x > 0)   ns.push(px - 1);
    if (x < w-1) ns.push(px + 1);
    if (y > 0)   ns.push(px - w);
    if (y < h-1) ns.push(px + w);
    for (const n of ns) {
      if (!visited[n] && isBg(n)) { visited[n] = 1; queue.push(n); }
    }
  }

  octx.putImageData(id, 0, 0);
  return oc;
}

// ─── Inline text layout ──────────────────────────────────────
function layoutInline(ctx, blocks, x0, maxW, align, bodySz, bodyLh) {
  ctx.font = state.weight + ' ' + bodySz + 'px ' + FONT_JP;
  let x = x0, y = 0;
  const chars = [];
  const BAND_GAP = 14;
  let prevStyle = null;
  for (let bi = 0; bi < blocks.length; bi++) {
    const b = blocks[bi];
    if (!b.text) continue;
    for (const ch of b.text) {
      if (ch === '\n') {
        chars.push({ ch: '\n', style: b.style, x, y, w: 0 });
        x = x0; y += bodyLh; prevStyle = null; continue;
      }
      const cw = ctx.measureText(ch).width;
      if (prevStyle !== null && prevStyle !== b.style &&
          (b.style === 'band' || prevStyle === 'band')) {
        x += BAND_GAP;
      }
      if (x + cw > x0 + maxW + 0.5) { x = x0; y += bodyLh; prevStyle = null; }
      chars.push({ ch, style: b.style, x, y, w: cw });
      x += cw;
      prevStyle = b.style;
    }
  }

  if (align === 'center') {
    const byLine = {};
    for (const c of chars) {
      if (c.ch === '\n') continue;
      (byLine[c.y] = byLine[c.y] || []).push(c);
    }
    for (const line of Object.values(byLine)) {
      const last = line[line.length - 1];
      const lineW = last.x + last.w - x0;
      const offset = (maxW - lineW) / 2;
      for (const c of line) c.x += offset;
    }
  }

  return { chars, totalH: y + bodyLh };
}

// Render pre-laid-out chars. Band rects drawn first, then all text on top.
function renderChars(ctx, chars, offsetY, bodySz, bodyLh) {
  ctx.font = state.weight + ' ' + bodySz + 'px ' + FONT_JP;
  ctx.textBaseline = 'top';
  ctx.textAlign = 'left';

  // Pass 1: band backgrounds
  let i = 0;
  while (i < chars.length) {
    const c = chars[i];
    if (c.style === 'band' && c.ch !== '\n') {
      const lineY = c.y;
      const sx = c.x;
      let j = i;
      while (j < chars.length && chars[j].style === 'band' && chars[j].y === lineY && chars[j].ch !== '\n') j++;
      const ex = chars[j-1].x + chars[j-1].w;
      ctx.fillStyle = state.bgColor;
      ctx.fillRect(sx - 8, offsetY + lineY - 4, ex - sx + 16, bodySz + 12);
      i = j;
    } else { i++; }
  }

  // Pass 2: all text
  for (const c of chars) {
    if (c.ch === '\n') continue;
    if (c.style === 'band') {
      ctx.fillStyle = C_WHITE;
      ctx.fillText(c.ch, c.x, offsetY + c.y);
    } else {
      ctx.fillStyle = c.style === 'red' ? state.bgColor : C_BODY;
      ctx.fillText(c.ch, c.x, offsetY + c.y);
    }
  }
}

// ─── Rounded rect path ───────────────────────────────────────
function roundedRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.arcTo(x+w, y,   x+w, y+r,   r);
  ctx.lineTo(x+w, y+h-r);
  ctx.arcTo(x+w, y+h, x+w-r, y+h, r);
  ctx.lineTo(x+r, y+h);
  ctx.arcTo(x,   y+h, x,   y+h-r, r);
  ctx.lineTo(x, y+r);
  ctx.arcTo(x,   y,   x+r, y,     r);
  ctx.closePath();
}

// ─── Main render ─────────────────────────────────────────────
function render() {
  const canvas = document.getElementById('canvas');
  const ctx    = canvas.getContext('2d');

  // Layout positions
  const headY       = ICHIGO_TOP_H + 27;
  const dividerY    = headY + HEAD_SZ + HEAD_LH + 35;
  const cardTopY    = dividerY + 328;
  const avatarCY    = cardTopY;
  const nameY       = avatarCY + AVATAR_R + 30;
  const textStartY  = nameY + BODY_SZ + 38;

  // Inline layout for all text blocks
  const { sz: bodySz, lh: bodyLh } = BODY_SIZES[state.bodySize];
  const activeBlocks = state.blocks.filter(b => b.text.trim());
  const { chars, totalH: textH } = layoutInline(ctx, activeBlocks, TEXT_L, TEXT_W, state.align, bodySz, bodyLh);

  const contentEndY  = textStartY + textH + 38;
  const cardBottomY  = Math.max(contentEndY, cardTopY + 480) + 20;
  const footerTextY  = cardBottomY + 58;
  const footerCircY  = footerTextY + 70;
  const totalH       = footerCircY + 126;

  canvas.height = totalH;

  // 1. Red background
  ctx.fillStyle = state.bgColor;
  ctx.fillRect(0, 0, W, totalH);

  // 2. Heading
  ctx.fillStyle    = C_WHITE;
  ctx.textBaseline = 'top';
  ctx.textAlign    = 'center';
  ctx.font = 'bold ' + HEAD_SZ + 'px ' + FONT_JP;
  ctx.fillText('レビューを頂いたので', W/2, headY);
  ctx.fillText('紹介します', W/2, headY + HEAD_LH);

  // 3. Divider
  ctx.strokeStyle = 'rgba(255,255,255,0.8)';
  ctx.lineWidth   = 4;
  ctx.beginPath();
  ctx.moveTo(270, dividerY);
  ctx.lineTo(W - 270, dividerY);
  ctx.stroke();

  // 3.5 Subheading below divider
  ctx.fillStyle    = C_WHITE;
  ctx.font         = BODY_SZ + 'px ' + FONT_JP;
  ctx.textAlign    = 'center';
  ctx.textBaseline = 'top';
  const subY = dividerY + 28;
  ctx.fillText('実際にご注文いただいたお客様から', W/2, subY);
  ctx.fillText('嬉しいお声が届きました。', W/2, subY + BODY_LH);
  ctx.fillText('一部を紹介します。', W/2, subY + BODY_LH * 2);

  // 4. Card (white rounded rect with soft shadow)
  ctx.shadowColor   = 'rgba(0,0,0,0.14)';
  ctx.shadowBlur    = 20;
  ctx.shadowOffsetY = 8;
  ctx.fillStyle = C_WHITE;
  roundedRect(ctx, CARD_X, cardTopY, CARD_W, cardBottomY - cardTopY, CARD_R);
  ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.shadowBlur  = 0;
  ctx.shadowOffsetY = 0;

  // 5. Ichigo top (drawn on top of everything in the heading area)
  if (imgs.ichigo_top) {
    const iW = Math.round(W * 0.68);
    const iH = Math.round(102 * iW / 682);
    ctx.drawImage(imgs.ichigo_top, (W - iW) / 2, 72, iW, iH);
  }

  // 6. Avatar
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(W/2, avatarCY, AVATAR_R, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.beginPath();
  ctx.arc(W/2, avatarCY, AVATAR_R, 0, Math.PI * 2);
  ctx.clip();
  if (imgs[state.avatar]) {
    ctx.drawImage(imgs[state.avatar], W/2 - AVATAR_R, avatarCY - AVATAR_R, AVATAR_R*2, AVATAR_R*2);
  }
  ctx.restore();

  ctx.strokeStyle = C_WHITE;
  ctx.lineWidth   = 6;
  ctx.beginPath();
  ctx.arc(W/2, avatarCY, AVATAR_R + 2, 0, Math.PI * 2);
  ctx.stroke();

  // 7. Name
  ctx.font         = state.weight + ' ' + BODY_SZ + 'px ' + FONT_JP;
  ctx.fillStyle    = C_BODY;
  ctx.textAlign    = 'center';
  ctx.textBaseline = 'top';
  ctx.fillText((state.name || '？') + '様', W/2, nameY);

  // 8. Text blocks (inline continuous flow)
  renderChars(ctx, chars, textStartY, bodySz, bodyLh);

  // 9. Ichigo BR (bottom-right corner of card)
  if (imgs.ichigo_br) {
    ctx.drawImage(imgs.ichigo_br,
      CARD_X + CARD_W - ICHIGO_BR_W - 12,
      cardBottomY - ICHIGO_BR_H - 12,
      ICHIGO_BR_W, ICHIGO_BR_H);
  }

  // 10. Footer text — scale font so text width matches card width
  const footerStr = 'ONE GOについてご質問やご相談などはこちらから';
  ctx.font = 'bold 33px ' + FONT_JP;
  const footerFontSz = (33 * CARD_W / ctx.measureText(footerStr).width).toFixed(1);
  ctx.font         = 'bold ' + footerFontSz + 'px ' + FONT_JP;
  ctx.fillStyle    = C_WHITE;
  ctx.textAlign    = 'left';
  ctx.textBaseline = 'top';
  ctx.fillText(footerStr, CARD_X, footerTextY);

  // 11. Footer circle with solid triangle arrow
  const cx = W/2, cy = footerCircY + 46, cr = 46;
  ctx.fillStyle = C_WHITE;
  ctx.beginPath();
  ctx.arc(cx, cy, cr, 0, Math.PI * 2);
  ctx.fill();
  // Solid downward triangle
  ctx.beginPath();
  ctx.moveTo(cx - 21, cy - 10);
  ctx.lineTo(cx + 21, cy - 10);
  ctx.lineTo(cx,      cy + 17);
  ctx.closePath();
  ctx.fillStyle = state.bgColor;
  ctx.fill();
}

// ─── UI: Color grid ──────────────────────────────────────────
function renderColorGrid() {
  const grid = document.getElementById('color-grid');
  grid.innerHTML = '';
  for (const color of BG_COLORS) {
    const div = document.createElement('div');
    div.className = 'color-swatch' + (state.bgColor === color ? ' selected' : '');
    div.style.background = color;
    div.dataset.color = color;
    div.addEventListener('click', () => {
      state.bgColor = color;
      document.querySelectorAll('.color-swatch').forEach(el => {
        el.classList.toggle('selected', el.dataset.color === color);
      });
      render();
    });
    grid.appendChild(div);
  }
}

// ─── UI: Avatar grid ─────────────────────────────────────────
function renderAvatarGrid() {
  const grid = document.getElementById('avatar-grid');
  grid.innerHTML = '';
  for (let n = 1; n <= 8; n++) {
    const key = state.gender + n;
    const div = document.createElement('div');
    div.className = 'avatar-item' + (state.avatar === key ? ' selected' : '');
    div.dataset.key = key;
    const img = document.createElement('img');
    img.src = IMG_SRC[key];
    img.alt = key;
    div.appendChild(img);
    div.addEventListener('click', () => {
      state.avatar = key;
      document.querySelectorAll('.avatar-item').forEach(el => {
        el.classList.toggle('selected', el.dataset.key === key);
      });
      render();
    });
    grid.appendChild(div);
  }
}

// ─── UI: Block list ──────────────────────────────────────────
function renderBlocks() {
  const list = document.getElementById('block-list');
  list.innerHTML = '';
  for (const b of state.blocks) {
    const div = document.createElement('div');
    div.className = 'block';

    const header = document.createElement('div');
    header.className = 'block-header';

    const sel = document.createElement('select');
    sel.className = 'block-style';
    [['normal','通常（黒文字）'],['red','赤字'],['band','赤帯白文字']].forEach(([v, t]) => {
      const opt = document.createElement('option');
      opt.value = v; opt.textContent = t;
      if (b.style === v) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener('change', () => {
      b.style = sel.value;
      render();
    });

    const del = document.createElement('button');
    del.className = 'block-del';
    del.textContent = '×';
    del.title = '削除';
    del.addEventListener('click', () => {
      state.blocks = state.blocks.filter(x => x.id !== b.id);
      renderBlocks();
      render();
    });

    header.append(sel, del);

    const ta = document.createElement('textarea');
    ta.className = 'block-text';
    ta.rows = 3;
    ta.value = b.text;
    ta.addEventListener('input', () => {
      b.text = ta.value;
      render();
    });

    div.append(header, ta);
    list.appendChild(div);
  }
}

// ─── Downloads ───────────────────────────────────────────────
function downloadPNG() {
  const canvas = document.getElementById('canvas');
  const a = document.createElement('a');
  a.download = 'review_banner.png';
  a.href = canvas.toDataURL('image/png');
  a.click();
}

// ─── Init ────────────────────────────────────────────────────
async function init() {
  await loadImages();

  document.getElementById('poster-name').addEventListener('input', e => {
    state.name = e.target.value;
    render();
  });

  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      state.gender = btn.dataset.gender;
      state.avatar = state.gender + '1';
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderAvatarGrid();
      render();
    });
  });

  document.querySelectorAll('[data-align]').forEach(btn => {
    btn.addEventListener('click', () => {
      state.align = btn.dataset.align;
      document.querySelectorAll('[data-align]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });
  });

  document.querySelectorAll('[data-size]').forEach(btn => {
    btn.addEventListener('click', () => {
      state.bodySize = btn.dataset.size;
      document.querySelectorAll('[data-size]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });
  });

  document.querySelectorAll('[data-weight]').forEach(btn => {
    btn.addEventListener('click', () => {
      state.weight = btn.dataset.weight;
      document.querySelectorAll('[data-weight]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });
  });

  document.getElementById('add-block').addEventListener('click', () => {
    state.blocks.push({ id: state.nextId++, style: 'normal', text: '' });
    renderBlocks();
  });

  document.getElementById('dl-png').addEventListener('click', downloadPNG);

  renderColorGrid();
  renderAvatarGrid();
  renderBlocks();
  render();
}

init().catch(console.error);
"""

# Compose final HTML
html = (
    '<!DOCTYPE html>\n'
    '<html lang="ja">\n'
    '<head>\n'
    '  <meta charset="UTF-8">\n'
    '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '  <title>レビューバナージェネレーター | ONE GO</title>\n'
    '  <style>\n' + css + '\n  </style>\n'
    '</head>\n'
    '<body>\n' + body +
    '<script>\n' + imgs_js + '\n' + js + '\n</script>\n'
    '</body>\n'
    '</html>\n'
)

out = D + '/index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(out) / 1024
print('Generated: ' + out)
print('Size: {:.1f} KB'.format(size_kb))
