import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch
from datetime import date, timedelta
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; RED="#c92a2a"; LBLUE="#dbe7fd"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/dtt_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def mdy(d): return f"{d.month}.{d.day:02d}{d.year}"
def daynum(d):            # LBL J formula, as programmed
    m,y=d.month,d.year
    I,P=(m+1,y) if m>2 else (m+13,y-1)
    return int(P*365.25)+int(I*30.6001)+d.day+1720982
def true_jdn(d): return d.toordinal()+1721425

# 1 Day numbers
rows=[(date(1900,3,1),"First date in range"),(date(1969,7,20),"Apollo 11"),(date(2000,1,1),"Start of 2000"),(date(2024,1,1),"Example 6.1 start"),(date(2024,7,4),"Example 6.1 end"),(date(2100,2,28),"Last date in range")]
fig,ax=plt.subplots(figsize=(9.5,5)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(-1.6,6.9)
ax.text(0,6.65,"Every Date Is One Integer: the Day Number",fontsize=13,fontweight="bold",va="center")
ax.text(.2,6.05,"Date (M.DDYYYY)",fontsize=10,color=GREY); ax.text(4.3,6.05,"LBL J",fontsize=10,color=GREY,ha="center"); ax.text(5.6,6.05,"Day number",fontsize=10,color=GREY)
for i,(d,lab) in enumerate(rows):
    y=5.3-i*.9; c=BLUE if lab.startswith("Example") else (GREEN if "range" in lab else INK)
    ax.text(.2,y,mdy(d),fontsize=13,family="DejaVu Sans Mono",fontweight="bold",color=c,va="center")
    ax.annotate("",xy=(5.3,y),xytext=(3.3,y),arrowprops=dict(arrowstyle="-|>",color=GREY,lw=1.3))
    ax.text(5.6,y,f"{daynum(d):,}",fontsize=13,family="DejaVu Sans Mono",fontweight="bold",color=c,va="center")
    ax.text(7.75,y,lab,fontsize=9.5,color=GREY,va="center")
ax.plot([.2,9.8],[-.15,-.15],color=GRID,lw=1)
ax.text(.2,-.75,f"XEQ N:   {daynum(date(2024,7,4)):,} − {daynum(date(2024,1,1)):,} = 185 days",fontsize=12,family="DejaVu Sans Mono",color=BLUE,va="center",fontweight="bold")
ax.text(.2,-1.4,"Inside its range the day number equals the astronomical Julian Day Number.",fontsize=9.5,color=GREY,va="center")
save(fig,"day_numbers")

# 2 Computational year
months=["Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb"]; idx=[4,5,6,7,8,9,10,11,12,13,14,15]
lens=[31,30,31,30,31,31,30,31,30,31,31,28]
fig,ax=plt.subplots(figsize=(10,3.9)); ax.grid(axis="x",visible=False)
ax.bar(range(12),lens,color=[BLUE]*10+[ORANGE,ORANGE],alpha=.85,width=.75)
ax.bar(11,1,bottom=28,color=RED,alpha=.85,width=.75,hatch="///",edgecolor="white")
for i,(n,l) in enumerate(zip(idx,lens)):
    ax.text(i,l/2,str(l),ha="center",va="center",color="white",fontweight="bold",fontsize=11)
    ax.text(i,-3.2,str(n),ha="center",va="center",fontsize=10,color=ORANGE if n>13 else INK,fontweight="bold" if n>13 else "normal")
ax.text(11,31.2,"leap day\n(29th)",ha="center",fontsize=9,color=RED)
ax.text(-.95,-3.2,"I",ha="center",va="center",fontsize=10,style="italic",color=GREY)
ax.set_xticks(range(12)); ax.set_xticklabels(months); ax.set_ylim(-5,42); ax.set_yticks([0,10,20,28,31]); ax.set_ylabel("Days")
ax.text(-.4,38.5,"LBL J sets I = month + 1, or month + 13 with the year reduced by 1, so the leap day falls last",ha="left",fontsize=9.5,color=ORANGE)
ax.set_title("The Computational Year Starts on March 1",loc="left"); save(fig,"computational_year")

# 3 Valid range
ys=np.arange(1600,2401); err=[]
for y in ys:
    d=date(int(y),6,1); err.append(daynum(d)-true_jdn(d))
fig,ax=plt.subplots(figsize=(9.5,4))
ax.axvspan(1900.17,2100.16,color=GREEN,alpha=.12,lw=0)
ax.step(ys,err,where="post",color=BLUE,lw=2.2)
ax.axhline(0,color=INK,lw=.8)
ax.text(2000,1.55,"Exact:\n3.011900 to 2.282100",ha="center",fontsize=10.5,color=GREEN,fontweight="bold")
for y,t in [(1700,"1700"),(1800,"1800"),(1900,"1900"),(2100,"2100"),(2200,"2200"),(2300,"2300")]:
    pass
ax.set_xlim(1600,2400); ax.set_ylim(-4.5,4.5); ax.set_yticks(range(-4,5))
ax.set_xlabel("Year"); ax.set_ylabel("Day-number error (days)")
ax.text(1610,-3.9,"Each century year not divisible by 400 shifts the result by one day,\nbecause 365.25 assumes every fourth year is a leap year.",fontsize=9.5,color=GREY)
ax.set_title("Valid Date Range of the Day-Number Formula",loc="left"); save(fig,"valid_range")

# 4 Day-of-week wheel
fig,ax=plt.subplots(figsize=(6.2,6.2)); ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.55,1.5)
days=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
for i,dn in enumerate(days):
    a0=90-i*360/7; c=ORANGE if dn=="Fri" else LBLUE
    ax.add_patch(Wedge((0,0),1.15,a0-360/7,a0,width=.5,fc=c,ec="white",lw=3))
    am=np.radians(a0-180/7); ax.text(.9*np.cos(am),.9*np.sin(am),f"{i}",ha="center",va="center",fontsize=16,fontweight="bold",color="white" if dn=="Fri" else BLUE)
    ax.text(1.32*np.cos(am),1.32*np.sin(am),dn,ha="center",va="center",fontsize=11.5)
ax.text(0,.05,"W = (day number + 1)\nmod 7",ha="center",va="center",fontsize=11.5,fontweight="bold")
ax.text(0,-1.45,f"5.242024: day number {daynum(date(2024,5,24)):,} → 5 (Friday)",ha="center",fontsize=10.5,color=ORANGE,fontweight="bold")
ax.text(-1.5,1.45,"Day of Week with LBL W",fontsize=13,fontweight="bold",va="center")
save(fig,"day_of_week")

# 5 Date arithmetic on 2024
fig,ax=plt.subplots(figsize=(10,3.6)); ax.axis("off"); ax.set_xlim(-12,380); ax.set_ylim(-2.2,3.2)
y0=date(2024,1,1)
def dx(d): return (d-y0).days
ax.plot([0,366],[0,0],color=INK,lw=2)
for m in range(1,13):
    x=dx(date(2024,m,1)); ax.plot([x,x],[-.1,.1],color=INK,lw=1); ax.text(x+15,-.28,date(2024,m,1).strftime("%b"),ha="center",va="top",fontsize=9,color=GREY)
ops=[(date(2024,1,1),date(2024,7,4),"XEQ N: 185 days",BLUE),(date(2024,3,15),date(2024,6,13),"XEQ D: + 90 days",GREEN),(date(2024,12,25),date(2024,11,10),"XEQ D: − 45 days",ORANGE)]
for a,b,lab,c in ops:
    xa,xb=dx(a),dx(b)
    ax.add_patch(FancyArrowPatch((xa,.15),(xb,.15),connectionstyle=f"arc3,rad={-0.32 if xb>xa else 0.32}",arrowstyle="-|>",mutation_scale=16,color=c,lw=2))
    ax.plot([xa,xb],[0,0],"o",color=c,ms=7,zorder=5)
    lx,ly={"XEQ N: 185 days":(92,2.3),"XEQ D: + 90 days":(120,1.35),"XEQ D: − 45 days":(342,1.05)}[lab]
    ax.text(lx,ly,lab,ha="center",fontsize=10,color=c,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1))
for d,c,dy in [(date(2024,1,1),BLUE,-.75),(date(2024,7,4),BLUE,-.75),(date(2024,3,15),GREEN,-1.3),(date(2024,6,13),GREEN,-1.3),(date(2024,12,25),ORANGE,-.75),(date(2024,11,10),ORANGE,-1.3)]:
    ax.text(dx(d),dy,mdy(d),ha="center",fontsize=9.5,color=c,family="DejaVu Sans Mono",fontweight="bold")
ax.text(-12,3.05,"Examples 6.1 to 6.3 on the 2024 Calendar",fontsize=13,fontweight="bold",va="center")
save(fig,"date_arithmetic")

# 6 Time difference
fig,ax=plt.subplots(figsize=(10,3.9)); ax.set_xlim(0,31); ax.set_ylim(-.6,3.4); ax.grid(axis="y",visible=False)
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.axvspan(24,31,color=GREY,alpha=.08,lw=0); ax.text(27.5,3.15,"next day\n(+24)",ha="center",fontsize=9,color=GREY,va="top")
bars=[(2.3,8.5,17.25,"8.30 → 17.15","8.4500  (8 h 45 min)",BLUE),(1.3,9+15/60+30/3600,14+5/60+45/3600,"9.1530 → 14.0545","4.5015  (4 h 50 min 15 s)",GREEN),(.3,22,30.5,"22.00 → 30.30","8.3000  (overnight)",ORANGE)]
for y,a,b,lab,res,c in bars:
    ax.barh(y,b-a,left=a,height=.5,color=c,alpha=.85)
    ax.text(a-.3,y,lab,ha="right",va="center",fontsize=10,family="DejaVu Sans Mono")
    ax.text(b+.3 if b<29 else a+(b-a)/2,y,res,ha="left" if b<29 else "center",va="center",fontsize=10,fontweight="bold",color=c if b<29 else "white")
ax.set_xticks(range(0,31,3)); ax.set_xticklabels([f"{h%24:02d}:00" for h in range(0,31,3)],fontsize=9)
ax.set_xlabel("Time of day")
ax.set_title("Time Differences with LBL T (H.MMSS in, H.MMSS out)",loc="left"); save(fig,"time_difference")
