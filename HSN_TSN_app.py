import tkinter as tk
from tkinter import messagebox
import sys
from crawler1bynetwork import download_csv
sys.path = ['C:/Users/joe881003/Desktop/HSN TSN'] + sys.path

window = tk.Tk()#建立一個空視窗
window.title('HSN TSN')#標題
window.geometry('380x400')#視窗大小
window.resizable(False, False)

def bt_download():
    if chks.get() == True:
        download_csv(begin_date = date_text.get(), end_date = end_date_text.get(), ALL = True)
        messagebox.showinfo("訊息", "下載成功")
    elif chks.get() == False:
        download_csv(begin_date = date_text.get(), end_date = end_date_text.get(), ALL = False)
        messagebox.showinfo("訊息", "下載成功")
    else:
        messagebox.showinfo("訊息", "下載失敗")

date_label = tk.Label(window, text = '起始日期:', height=4)#起始日期label及位置
date_label.place(x = 0, y = 83)

ex_label_1 = tk.Label(window, text = '(ex:2023-01-01)', height = 4)#起始日期輸入框中的範例
ex_label_1.place(x = 58, y = 109)

date_text = tk.Entry(window, width=40)#起始日期的輸入框
date_text.place(x = 58, y = 108)


end_date_label = tk.Label(window, text = '結束日期:', height=4)#結束日期label及位置
end_date_label.place(x = 0, y = 163)

ex_label_2 = tk.Label(window, text = '(ex:2023-01-31)', height = 4)#結束日期輸入框中的範例
ex_label_2.place(x = 58, y = 189)

end_date_text = tk.Entry(window, width=40)#結束日期輸入框
end_date_text.place(x = 58, y = 188)



dct = '下載所有資料(confirm包含0, 1)'#建立checkbox顯示的文字
chks = tk.BooleanVar()#建立checkbox的變數

Cb = tk.Checkbutton(window, text=dct, variable=chks)#第一個checkbox設定
Cb.place(x = 100, y = 40)




bt_plt = tk.Button(window, text = '下載', command = bt_download, height=6, width = 30, background='#f90')#下載按鈕的設定      
bt_plt.place(x = 80, y = 250)     

window.mainloop()