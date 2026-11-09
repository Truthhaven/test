import numpy as np, re, sys, vtracer
from PIL import Image, ImageDraw
from scipy import ndimage as nd
S=sys.argv[1]; OUT=sys.argv[2]
rgb=np.array(Image.open(S+'/cut.png'))[:,:,:3]
fg=np.load(S+'/mask.npy')
H,W=fg.shape
def poly(pts):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(pts,fill=1); return np.array(m).astype(bool)
used=np.zeros_like(fg)
parts={}
def take(name,m):
    global used
    m=m&fg&~used; parts[name]=m; used|=m
take('head',poly([(320,0),(770,0),(770,300),(700,292),(650,378),(556,378),(562,284),(558,298),(542,304),(520,304),(500,298),(478,290),(466,284),(470,320),(430,342),(398,342),(330,322)]))
take('arm-left',poly([(140,300),(318,300),(372,372),(392,470),(422,612),(330,640),(140,640)]))
take('arm-right',poly([(950,300),(745,300),(696,378),(660,470),(598,612),(700,640),(950,640)]))
take('shoe-left',poly([(420,1262),(600,1238),(600,1448),(420,1448)]))
take('shoe-right',poly([(640,1300),(860,1268),(860,1448),(640,1448)]))
take('torso',poly([(300,240),(780,240),(780,648),(300,648)]))
mid=[(506,640),(506,790),(545,900),(575,1000),(605,1100),(640,1448)]
take('leg-left',poly([(300,640)]+mid+[(300,1448)]))
take('leg-right',poly([(506,640),(900,640),(900,1448)]+mid[::-1]))
print({k:int(v.sum()) for k,v in parts.items()}, 'left over', int((fg&~used).sum()))
order=['leg-left','leg-right','shoe-left','shoe-right','arm-left','arm-right','torso','head']
pivots={'head':(512,250),'arm-left':(345,330),'arm-right':(725,345),'torso':(510,640),
        'leg-left':(430,660),'leg-right':(580,660),'shoe-left':(500,1430),'shoe-right':(760,1440)}
body=[]
for name in order:
    m=parts[name]
    # grow a little into neighbouring figure pixels so seams stay hidden when parts move
    grow=nd.binary_dilation(m,iterations=5)&fg
    ys,xs=np.where(grow); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    crop=np.dstack([rgb[y0:y1,x0:x1],(grow[y0:y1,x0:x1]*255).astype(np.uint8)])
    Image.fromarray(crop).save(f'{S}/part.png')
    vtracer.convert_image_to_svg_py(f'{S}/part.png',f'{S}/part.svg',colormode='color',hierarchical='stacked',
        mode='spline',filter_speckle=4,color_precision=7,layer_difference=10,corner_threshold=60,
        length_threshold=4.0,splice_threshold=45,path_precision=1)
    svg=open(f'{S}/part.svg').read()
    paths=re.findall(r'<path[^>]*/>',svg)
    px,py=pivots[name]
    body.append(f'  <g id="{name}" style="transform-origin:{px}px {py}px">\n    <g transform="translate({x0} {y0})">\n'+
        '\n'.join('      '+p for p in paths)+'\n    </g>\n  </g>')
    print(name,len(paths))
open(OUT,'w').write(body and '\n'.join(body))
