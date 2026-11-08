from PIL import Image
import numpy as np, sys
from scipy import ndimage as nd
S=sys.argv[2]
a=np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int)
neutral=(a.max(2)-a.min(2)<=10)&(a.min(2)>=205)
lab,n=nd.label(neutral)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
sz=nd.sum(neutral,lab,range(1,n+1)); g=a.min(2)
dark=nd.sum(neutral&(g>=212)&(g<=228),lab,range(1,n+1)); light=nd.sum(neutral&(g>=246),lab,range(1,n+1))
big={i+1 for i,v in enumerate(sz) if v>1500 or (dark[i]>=6 and light[i]>=6)}
bg=np.isin(lab,list(border|big))
fg=nd.binary_opening(~bg,iterations=2)
lab2,n2=nd.label(fg); sizes=nd.sum(fg,lab2,range(1,n2+1)); fg=lab2==(np.argmax(sizes)+1)
h=nd.binary_fill_holes(fg)&~fg; hl,hn=nd.label(h); hs=nd.sum(h,hl,range(1,hn+1)); fg=fg|np.isin(hl,[i+1 for i,v in enumerate(hs) if v<40])
np.save(S+'/mask.npy',fg)
rgba=np.dstack([a.astype(np.uint8),(fg*255).astype(np.uint8)])
Image.fromarray(rgba).save(S+'/cut.png')
v=Image.new('RGBA',(1086,1448),(40,120,60,255)); v.alpha_composite(Image.fromarray(rgba)); v.resize((543,724)).save(S+'/cutview.png')
print(fg.mean())
