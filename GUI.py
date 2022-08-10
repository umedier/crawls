import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.main import parse_url


root = ttk.Window(
    title="Dr Crawls",
    minsize=(800, 200)
)
app = ttk.Frame(root, padding=15)
app.pack(fill=BOTH, expand=YES)

bar = ttk.Frame(app)
bar.pack(fill=X, pady=1, side=TOP)

text = ttk.Text(bar)
text.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5), pady=10)

btn = ttk.Button(bar, text="Dowmload", command=lambda: parse_url(text.get('0.0', 'end')))
btn.pack(side=LEFT, fill=X, padx=(5, 0), pady=10)



screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
dialog_width = 800
dialog_height = 200
root.resizable(False,False)
root.geometry("%dx%d+%d+%d" % (dialog_width, dialog_height,
              (screenwidth-dialog_width)/2, (screenheight-dialog_height)/2))
root.mainloop()


# https://www.douyin.com/user/MS4wLjABAAAAgY0pHqb3lG95_yoh_Y3vJs4zVinNyXG-V5s9sMiMevA