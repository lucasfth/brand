"""Build every hbit brand asset into dist/. Run: scripts/build.sh"""
import subprocess, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RSVG=shutil.which("rsvg-convert") or exit("rsvg-convert not found")
OUT=os.path.join(ROOT,"dist"); WARM=["#f3874e","#859867","#5f9f9d"]
CREAM,SLATE,INK,BLACK="#f3ddb3","#2b3946","#050505","#111111"
PAL={ "warm-on-dark": dict(fill=CREAM,beams=WARM,bg=INK,  text=CREAM,sub="#a8a090"),
      "warm-on-light":dict(fill=SLATE,beams=WARM,bg="#fafafa",text=SLATE,sub="#6b7680"),
      "black":        dict(fill=BLACK,beams=[BLACK]*3,bg="#ffffff",text=BLACK,sub=BLACK),
      "white":        dict(fill="#ffffff",beams=["#ffffff"]*3,bg=INK,text="#ffffff",sub="#ffffff")}
def P(*pts): return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)

def pix(p, N):
    """Hand-placed pixel mark for 16/32 px (vector rendering blurs the corners)."""
    if N==16: m,arm,t, tx,tyc,th,tl, bx,bw,bh,bg = 0,4,1, 3,7,4,7, 11,4,1,1
    else:     m,arm,t, tx,tyc,th,tl, bx,bw,bh,bg = 1,8,2, 8,15,8,13, 20,8,2,1
    s=[]; R=lambda x,y,w,h,c: s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
    f=p["fill"]; e=N-m
    for (x,y,dx,dy) in [(m,m,1,1),(e,m,-1,1),(m,e,1,-1),(e,e,-1,-1)]:
        R(x if dx>0 else x-arm, y if dy>0 else y-t, arm, t, f)
        R(x if dx>0 else x-t, y if dy>0 else y-arm, t, arm, f)
    for y in range(tyc-th, tyc+th+1):
        w=round(tl*(1-abs(y-tyc)/(th+0.6)))
        if w>0: R(tx, y, w, 1, f)
    by = 7 if N==16 else tyc+th-3*bh-2*bg+1
    for i in range(3): R(bx, by+i*(bh+bg), bw, bh, p["beams"][i])
    return s

def mark(p, ox=0, oy=0, k=1.0):
    """F2 bold mark in a 512 box"""
    m,L,w=40,84,40; s=[]
    for (x,y,dx,dy) in [(m,m,1,1),(512-m,m,-1,1),(m,512-m,1,-1),(512-m,512-m,-1,-1)]:
        s.append(f'<path d="M {x} {y+dy*L} L {x} {y} L {x+dx*L} {y}" fill="none" stroke="{p["fill"]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<polygon points="{P((150,140),(330,256),(150,372))}" fill="{p["fill"]}" stroke="{p["fill"]}" stroke-width="30" stroke-linejoin="round"/>')
    for i in range(3): s.append(f'<rect x="324" y="{318+i*30}" width="104" height="22" rx="4" fill="{p["beams"][i]}"/>')
    return f'<g transform="translate({ox} {oy}) scale({k})">'+"".join(s)+'</g>'

FONTS={w:TTFont(f"{ROOT}/fonts/SpaceMono-{w}.ttf") for w in ("Regular","Bold")}
def text(t, weight, size, x, y, fill, track=0):
    f=FONTS[weight]; gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f["head"].unitsPerEm; sc=size/upm
    d=[]; cx=0
    for ch in t:
        g=cmap[ord(ch)]; pen=SVGPathPen(gs)
        gs[g].draw(TransformPen(pen,(sc,0,0,-sc,x+cx,y))); d.append(pen.getCommands())
        cx+=gs[g].width*sc+track
    return f'<path d="{" ".join(d)}" fill="{fill}"/>', cx-track
def svg(w,h,body,bg=None):
    b=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{b}{body}</svg>'
def write(path, content, pngs=()):
    path=os.path.join(OUT,path); os.makedirs(os.path.dirname(path),exist_ok=True); open(path,"w").write(content)
    for (w,h,dst) in pngs: os.makedirs(os.path.dirname(os.path.join(OUT,dst)),exist_ok=True); subprocess.run([RSVG,"-w",str(w),"-h",str(h),path,"-o",os.path.join(OUT,dst)],check=True)

for pn,p in PAL.items():
    # mark, transparent + tile
    write(f"mark/hbit-mark-{pn}.svg", svg(512,512,mark(p)), [(s,s,f"mark/png/hbit-mark-{pn}-{s}.png") for s in (64,128,256,512,1024)])
    write(f"mark/hbit-mark-{pn}-tile.svg", svg(512,512,mark(p),p["bg"]), [(1024,1024,f"mark/png/hbit-mark-{pn}-tile-1024.png")])
    # horizontal lockup: mark | hbit / Hanson BitOptik
    t1,w1=text("hbit","Bold",300,560,250,p["text"],track=-6)
    t2,w2=text("HANSON BITOPTIK","Regular",62,566,380,p["sub"],track=6)
    W=int(560+max(w1,w2)+40)
    write(f"lockup/hbit-horizontal-{pn}.svg", svg(W,512,mark(p)+t1+t2), [(W*2,1024,f"lockup/png/hbit-horizontal-{pn}.png")])
    # stacked
    t1,w1=text("hbit","Bold",260,0,0,p["text"],track=-6); t2,w2=text("HANSON BITOPTIK","Regular",54,0,0,p["sub"],track=5)
    W=int(max(512,w2)+80); mx=(W-512)/2
    t1,_=text("hbit","Bold",260,(W-w1)/2,760,p["text"],track=-6); t2,_=text("HANSON BITOPTIK","Regular",54,(W-w2)/2,860,p["sub"],track=5)
    write(f"lockup/hbit-stacked-{pn}.svg", svg(W,900,mark(p,mx,0)+t1+t2), [(W*2,1800,f"lockup/png/hbit-stacked-{pn}.png")])

# favicon set (hand-pixelled 16/32, vector 48+), on dark tile
fd=dict(bg=INK,fill=CREAM,beams=WARM)
for N in (16,32):
    write(f"favicon/favicon-{N}.svg", '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" shape-rendering="crispEdges"><rect width="%d" height="%d" fill="%s"/>%s</svg>'%(N,N,N,N,N,N,INK,"".join(pix(fd,N))), [(N,N,f"favicon/favicon-{N}x{N}.png")])
write("favicon/icon.svg", svg(512,512,mark(fd),INK), [(48,48,"favicon/favicon-48x48.png"),(180,180,"favicon/apple-touch-icon.png"),(192,192,"favicon/icon-192.png"),(512,512,"favicon/icon-512.png")])
subprocess.run(["magick",f"{OUT}/favicon/favicon-16x16.png",f"{OUT}/favicon/favicon-32x32.png",f"{OUT}/favicon/favicon-48x48.png",f"{OUT}/favicon/favicon.ico"],check=True)

# QR: dark modules on light, F2 frame language, prism in the centre
URL=os.environ.get("QR_URL","HTTPS://HBIT.SH")
qr=subprocess.run(["qrencode","-t","ASCII","-l","H","-m","0",URL],check=True,capture_output=True,text=True).stdout
rows=[l for l in qr.split("\n") if l.strip()]
Q=[[c=="#" for c in r[::2]] for r in rows]; N=len(Q)
def qr_svg(p, size=600):
    q=380; x0=(size-q)/2; m=q/N; s=[]; hole=7; lo=(N-hole)//2; hi=lo+hole
    fin=lambda r,c:(r<7 and c<7) or (r<7 and c>=N-7) or (r>=N-7 and c<7)
    for r in range(N):
        for c in range(N):
            if Q[r][c] and not fin(r,c) and not (lo<=r<hi and lo<=c<hi):
                s.append(f'<rect x="{x0+c*m+m*.07:.2f}" y="{x0+r*m+m*.07:.2f}" width="{m*.86:.2f}" height="{m*.86:.2f}" rx="{m*.25:.2f}" fill="{p["fill"]}"/>')
    for (r,c) in [(0,0),(0,N-7),(N-7,0)]:
        x,y=x0+c*m,x0+r*m
        s.append(f'<rect x="{x+m/2:.2f}" y="{y+m/2:.2f}" width="{6*m:.2f}" height="{6*m:.2f}" rx="{1.4*m:.2f}" fill="none" stroke="{p["fill"]}" stroke-width="{m:.2f}"/><rect x="{x+2*m:.2f}" y="{y+2*m:.2f}" width="{3*m:.2f}" height="{3*m:.2f}" rx="{.7*m:.2f}" fill="{p["fill"]}"/>')
    c=x0+(lo+hole/2)*m; k=hole*m/330
    s.append(f'<g transform="translate({c} {c}) scale({k}) translate(-289 -256)"><polygon points="{P((150,140),(330,256),(150,372))}" fill="{p["fill"]}" stroke="{p["fill"]}" stroke-width="30" stroke-linejoin="round"/>'+"".join(f'<rect x="324" y="{318+i*30}" width="104" height="22" rx="4" fill="{p["beams"][i]}"/>' for i in range(3))+'</g>')
    mm,L,w=34,90,26
    for (x,y,dx,dy) in [(mm,mm,1,1),(size-mm,mm,-1,1),(mm,size-mm,1,-1),(size-mm,size-mm,-1,-1)]:
        s.append(f'<path d="M {x} {y+dy*L} L {x} {y} L {x+dx*L} {y}" fill="none" stroke="{p["fill"]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(size,size,"".join(s),"#ffffff" if p["fill"]==BLACK else "#fafafa")
for pn in ("warm-on-light","black"):
    write(f"qr/hbit-qr-{pn}.svg", qr_svg(PAL[pn]), [(s,s,f"qr/png/hbit-qr-{pn}-{s}.png") for s in (1200,600,300,200,150)])
