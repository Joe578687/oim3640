import io,base64,matplotlib.pyplot as plt
def _to64():
    b=io.BytesIO(); plt.savefig(b,format="png",bbox_inches="tight"); b.seek(0)
    s=base64.b64encode(b.getvalue()).decode(); plt.close(); return s
def make_win_rate_chart(w,l):
    plt.figure(); plt.bar(["Wins","Losses"],[w,l]); plt.title("Win/Loss")
    return _to64()
def make_opponent_chart(opp):
    items=sorted(opp.items(),key=lambda x:x[1],reverse=True)[:5]
    if not items: return None
    n=[i[0] for i in items]; c=[i[1] for i in items]
    plt.figure(); plt.bar(n,c); plt.xticks(rotation=30,ha="right"); plt.title("Top Opponents")
    return _to64()
