import tkinter as tk
import tkinter.messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time
#导入FontProperties
from matplotlib.font_manager import FontProperties 
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def toolbox():
    #定义一个Tkinter模块
    tool = tk.Tk()
    #定义窗口名称
    tool.title('密度函数和分布函数工具') 
    #定义窗口的大小
    tool.geometry('1000x550') 
    #ss为字符型变量
    ss = tk.StringVar()
    #ss1为字符型变量
    ss1 = tk.StringVar()
    #显示所选概率分布的名称
    l = tk.Label(tool, bg='white', width=20, text='') 
    #定义标签放置的位置
    l.place(x=400, y=10) 
    def selection():
        global s1,s2_1,s2_2,s3,s4,s5_1,s5_2,s6_1,s6_2
        global LL2_2,LL5_2,LL6_2
        #如果ss输入为泊松分布的分布律
        if ss.get()=='Poisson' and ss1.get()=='PDF': 
            #整型变量
            k1 = tk.IntVar()
            l.config(text=ss.get())
            #标签上显示的文字为“λ”
            LL1=tk.Label(tool, text='λ',width=5) 
            LL1.place(x=270, y=70)
            #泊松分布的分布律
            def poisson(k1):  
                rate = int(k1)
                #参数λ的值
                m = np.arange(0, 41) 
                plt.cla()
                #泊松分布的分布律的计算
                y = stats.poisson.pmf(m, rate) 
                plt.plot(m, y)
                #设置字体
                font = FontProperties(fname="song.ttf", size=14)  
                plt.title('泊松分布: λ=%i' % (rate), fontsize=15)
                plt.xlabel('事件发生的次数', fontsize=15)
                plt.ylabel('分布律的值', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            #制作可以拖动的挂件
            s1 = tk.Scale(tool,
                          from_=0,  
                          to=40,  
                          orient=tk.HORIZONTAL,  
                          length=400,  
                          #是否直接显示值
                          showvalue=1,  
                          #设置变量
                          variable=k1,  
                          #标签的单位长度
                          tickinterval=5,  
                          #保留精度
                          resolution=1, 
                          command=poisson) 
            s1.place(x=320, y=50)
            #设置text属性为“x的取值”
            L1=tk.Label(tool, text='x的取值',width=5) 
            L1.place(x=300, y=200)
            #显示成明文形式
            K1 = tk.Entry(tool, show=None)  
            K1.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t1.delete('1.0', 'end')
                try:
                    var = stats.poisson.pmf(int(K1.get()), k1.get())
                except ValueError:
                    tk.messagebox.showerror("Warning","请输入正确的数字！")
                    t1.insert('insert', "")
                else:
                    t1.insert('insert', format(var, '0.2f'))
            b1 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b1.place(x=300, y=240)
            t1 = tk.Text(tool, width=10, height=2)
            t1.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为泊松分布的分布函数
        elif ss.get()=='Poisson' and ss1.get()=='CDF':
            k1 = tk.IntVar()
            l.config(text=ss.get())
            LL1 = tk.Label(tool, text='λ',width=5)
            LL1.place(x=270, y=70)
            #泊松分布的分布函数
            def poisson(k1):  
                rate = int(k1)
                m = np.arange(0, 41)
                plt.cla()
                y = stats.poisson.cdf(m, rate)
                plt.plot(m, y)
                plt.title('泊松分布 $\lambda$ =%i' % (rate), fontsize=15)
                plt.xlabel('事件发生的次数',fontsize=15)
                plt.ylabel('分布函数值', fontsize=15)
                
                plt.draw()
                time.sleep(0.1)
            s1 = tk.Scale(tool,
                          from_=0,  
                          to=40, 
                          orient=tk.HORIZONTAL, 
                          length=400,  
                          showvalue=1, 
                          variable=k1, 
                          tickinterval=5,  
                          resolution=1,  
                          command=poisson)
            s1.place(x=320, y=50)
            L1 = tk.Label(tool, text='x的取值',width=5)
            L1.place(x=300, y=200)
            #显示成明文形式
            K1 = tk.Entry(tool, show=None)  
            K1.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t1.delete('1.0', 'end')
                try:
                    var = stats.poisson.cdf(int(K1.get()), k1.get())
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t1.insert('insert', "")
                else:
                    t1.insert('insert', format(var, '0.2f'))

            b1 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b1.place(x=300, y=240)
            t1 = tk.Text(tool, width=10, height=2)
            t1.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为二项分布的分布律
        elif ss.get() == 'binomial' and ss1.get()=='PDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL2_1=tk.Label(tool, text='n',width=8)
            LL2_1.place(x=270, y=70)
            LL2_2=tk.Label(tool, text='p',width=8)
            LL2_2.place(x=270, y=150)
            #二项分布的分布律
            def binomial(k1):
                n = int(k1)
                p = s2_2.get()
                k = np.arange(0, 41)
                #清除当前图形
                plt.cla()  
                binomial = stats.binom.pmf(k, n, p)  
                plt.plot(k, binomial) 
                #设置每张图片的标题
                plt.title('二项分布的参数为:n=%i,p=%.2f' % (n, p), fontsize=15)
                #设置x轴名称
                plt.xlabel('成功的次数', fontsize=15) 
                #设置y轴名称
                plt.ylabel('分布律的值', fontsize=15)
                #设置网格线
                plt.grid(True)  
                plt.draw()
                time.sleep(0.1)
            s2_1 = tk.Scale(tool,
                         from_=0, 
                         to=40,  
                         orient=tk.HORIZONTAL,  
                         length=400,  
                         showvalue=1, 
                         variable=k1, 
                         tickinterval=5,  
                         resolution=1, 
                         command=binomial)
            s2_1.place(x=320, y=50)
            def binomial(k2):
                n = s2_1.get()
                p = float(k2)
                k = np.arange(0, 41)
                plt.cla()  
                binomial = stats.binom.pmf(k, n, p)  
                plt.plot(k, binomial) 
                plt.title('二项分布的参数:n=%i,p=%.2f' % (n, p), fontsize=15) 
                plt.xlabel('成功的次数', fontsize=15)  
                plt.ylabel('分布律值', fontsize=15)  
                #设置网格线
                plt.grid(True)  
                plt.draw()
                time.sleep(0.1)
            s2_2 = tk.Scale(tool,
                         from_=0,  
                         to=1,  
                         orient=tk.HORIZONTAL,  
                         length=400,  
                         showvalue=1, 
                         variable=k2, 
                         tickinterval=0.1, 
                         resolution=0.01, 
                         command=binomial)
            s2_2.place(x=320, y=130)
            L2 = tk.Label(tool, text='x的取值',width=5)
            L2.place(x=300, y=200)
            #显示成明文形式
            E2 = tk.Entry(tool, show=None)  
            E2.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t2.delete('1.0', 'end')
                try:
                    var = stats.binom.pmf(int(E4.get()), s2_1.get(),s2_2.get())
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t2.insert('insert', "")
                    pass
                else:
                    t2.insert('insert', format(var, '0.2f'))
            b2 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b2.place(x=300, y=240)
            t2 = tk.Text(tool, width=10, height=2)
            t2.place(x=420, y=250)
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为二项分布的分布函数
        elif ss.get() == 'binomial' and ss1.get()=='CDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL4_1=tk.Label(tool, text='n',width=8)
            LL4_1.place(x=270, y=70)
            LL4_2=tk.Label(tool, text='p',width=8)
            LL4_2.place(x=270, y=150)
            #二项分布的分布函数
            def binomial(k1):
                n = int(k1)
                p = s2_2.get()
                k = np.arange(0, 41)
                plt.cla()  
                binomial = stats.binom.cdf(k, n, p) 
                plt.plot(k, binomial)  
                plt.title('二项分布的参数为n=%i,p=%.2f' % (n, p), fontsize=15)  
                plt.xlabel('成功的次数', fontsize=15)  
                plt.ylabel('分布函数值', fontsize=15)  
                plt.grid(True)  
                plt.draw()
                time.sleep(0.1)
            s2_1 = tk.Scale(tool,
                         from_=0,  
                         to=40,  
                         orient=tk.HORIZONTAL,  
                         length=400,  
                         showvalue=1, 
                         variable=k1,  
                         tickinterval=5, 
                         resolution=1,  
                         command=binomial)
            s2_1.place(x=320, y=50)
            def binomial(k2):
                n = s2_1.get()
                p = float(k2)
                k = np.arange(0, 41)
                plt.cla()  
                binomial = stats.binom.cdf(k, n, p)  
                plt.plot(k, binomial)  
                plt.title('二项分布的参数:n=%i,p=%.2f' % (n, p), fontsize=15)  
                plt.xlabel('成功的次数')  
                plt.ylabel('概率', fontsize=15)  
                plt.grid(True)  
                plt.draw()
                time.sleep(0.1)
            s2_2 = tk.Scale(tool,
                         from_=0, 
                         to=1,  
                         orient=tk.HORIZONTAL,  
                         length=400, 
                         showvalue=1, 
                         variable=k2,  
                         tickinterval=0.1,  
                         resolution=0.01,  
                         command=binomial)
            s2_2.place(x=320, y=130)
            L2 = tk.Label(tool, text='x的取值',width=5)
            L2.place(x=300, y=200)
            E2 = tk.Entry(tool, show=None)  
            E2.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():
                t2.delete('1.0', 'end')
                try:
                    var = stats.binom.cdf(int(E2.get()), s2_1.get(),s2_2.get())
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t2.insert('insert', "")
                    pass
                else:
                    t2.insert('insert', format(var, '0.2f'))
            b2 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b2.place(x=300, y=240)
            t2 = tk.Text(tool, width=10, height=2)
            t2.place(x=420, y=250)
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为几何分布的分布律
        elif ss.get()=='Geometry' and ss1.get()=='PDF':
            k1 = tk.IntVar()
            l.config(text=ss.get())
            LL3 = tk.Label(tool, text='p',width=8)
            LL3.place(x=270, y=70)
            #几何分布的分布律
            def geom(k1):  
                p = float(k1)  #(0-1)
                n = np.arange(0, 40)
                y = stats.geom.pmf(n, p)
                plt.plot(n, y)
                plt.title('几何分布的参数为 p=%.2f' % (p), fontsize=15)
                plt.xlabel('总的实验次数', fontsize=15)
                plt.ylabel('分布律值', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s3 = tk.Scale(tool,
                          from_=0,  
                          to=1, 
                          orient=tk.HORIZONTAL,  
                          length=400, 
                          showvalue=1,  
                          variable=k1, 
                          tickinterval=0.1,  
                          resolution=0.1,  
                          command=geom)
            s3.place(x=320, y=50)
            L3=tk.Label(tool, text='x的取值',width=5)
            L3.place(x=300, y=200)
            E3 = tk.Entry(tool, show=None)  
            E3.place(x=350, y=200)
            def value():
                t3.delete('1.0', 'end')
                try:
                    var = stats.geom.pmf(int(E3.get()), float(s3.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t3.insert('insert', "")
                    pass
                else:
                    t3.insert('insert', format(var, '0.3f'))
            b3 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b3.place(x=300, y=240)
            t3 = tk.Text(tool, width=10, height=2)
            t3.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为几何分布的分布函数
        elif ss.get()=='Geometry' and ss1.get()=='CDF':
            k1 = tk.IntVar()
            l.config(text=ss.get())
            LL3 = tk.Label(tool, text='p',width=8)
            LL3.place(x=270, y=70)
            #几何分布的分布函数
            def geom(k1):  
                p = float(k1)  #(0-1)
                n = np.arange(0, 40)
                y = stats.geom.cdf(n, p)
                plt.plot(n, y)
                plt.title('几何分布的参数p=%.2f' % (p), fontsize=15)
                plt.xlabel('总的实验次数', fontsize=15)
                plt.ylabel('分布律值', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s3 = tk.Scale(tool,
                          from_=0,  
                          to=1,  
                          orient=tk.HORIZONTAL,  
                          length=400,  
                          showvalue=1,  
                          variable=k1,  
                          tickinterval=0.1, 
                          resolution=0.1, 
                          command=geom)
            s3.place(x=320, y=50)
            L3=tk.Label(tool, text='x的取值',width=5)
            L3.place(x=300, y=200)
            E3 = tk.Entry(tool, show=None)  
            E3.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t3.delete('1.0', 'end')
                try:
                    var = stats.geom.cdf(int(E3.get()), float(s3.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t3.insert('insert', "")
                    pass
                else:
                    t3.insert('insert', format(var, '0.3f'))
            b3 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b3.place(x=300, y=240)
            t3 = tk.Text(tool, width=10, height=2)
            t3.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为指数分布的密度函数
        elif ss.get()=='Exponential' and ss1.get()=='PDF':
            k1 = tk.IntVar()
            l.config(text=ss.get())
            LL4 = tk.Label(tool, text='λ',width=8)
            LL4.place(x=270, y=70)
            #指数分布的分布律
            def exp(k1):  
                lambd = int(k1)
                plt.cla()
                x = np.arange(0, 10 / lambd, 0.05)
                y = stats.expon.pdf(x,scale=1/lambd)
                plt.plot(x, y)
                plt.title('指数分布,参数为: λ=%.2f' % (lambd))
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s4 = tk.Scale(tool,
                          from_=0.001,  
                          to=40, 
                          orient=tk.HORIZONTAL, 
                          length=400,  
                          showvalue=1, 
                          variable=k1, 
                          tickinterval=5, 
                          resolution=1,  
                          command=exp)
            s4.place(x=320, y=50)
            L4=tk.Label(tool, text='x的取值',width=5)
            L4.place(x=300, y=200)
            K2 = tk.Entry(tool, show=None)  
            K2.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t2.delete('1.0', 'end')
                try:
                    var = stats.expon.pdf(K2.get(),scale=1/s4.get())
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t4.insert('insert', "")
                    pass
                else:
                    t4.insert('insert', format(var, '0.2f'))
            b4 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b4.place(x=300, y=240)
            t4 = tk.Text(tool, width=10, height=2)
            t4.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为指数分布的分布函数
        elif ss.get()=='Exponential' and ss1.get()=='CDF':
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL4 = tk.Label(tool, text='λ',width=8)
            LL4.place(x=270, y=70)
            #指数分布的分布函数
            def exp(k2):  
                lambd = int(k2)
                plt.cla()
                x = np.arange(0, 10 / lambd, 0.05)
                y = stats.expon.cdf(x,scale=1/lambd)
                plt.plot(x, y)
                plt.title('指数分布,参数为: λ=%.2f' % (lambd))
                plt.xlabel('x', fontsize=15)
                plt.ylabel('分布函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s4 = tk.Scale(tool,
                          from_=0.0001,  
                          to=40,   
                          orient=tk.HORIZONTAL,  
                          length=400,   
                          showvalue=1,   
                          variable=k2,   
                          tickinterval=5,   
                          resolution=1,   
                          command=exp)
            s4.place(x=320, y=50)
            L4=tk.Label(tool, text='x的取值',width=5)
            L4.place(x=300, y=200)
            K2 = tk.Entry(tool, show=None)   
            K2.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():
                t4.delete('1.0', 'end')
                try:
                    var = stats.expon.cdf(K2.get(),scale=1/s4.get())
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t4.insert('insert', "")
                    pass
                else:
                    t4.insert('insert', format(var, '0.2f'))
            b4 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b4.place(x=300, y=240)
            t4 = tk.Text(tool, width=10, height=2)
            t4.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
       #如果ss输入为正态分布的密度函数
        elif ss.get() == 'Normal' and ss1.get()=='PDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            #设置y轴名称
            LL5_1 = tk.Label(tool, text='μ' ,width=8) 
            LL5_1.place(x=270, y=70)
            LL5_2 = tk.Label(tool, text='σ',width=8)
            LL5_2.place(x=270, y=150)
            #正态分布的密度函数
            def norm(k1):  
                mu = float(k1)
                #第二参数
                sigma = s5_2.get()  
                plt.cla()
                #x = np.arange(-4 * mu, 4 * mu, 0.1)
                x = np.arange(-4, 4, 0.1)
                y = stats.norm.pdf(x, mu, sigma)
                plt.plot(x, y)
                plt.title('正态分布的参数: μ=%.1f, σ=%.1f' % (mu, sigma))
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s5_1 = tk.Scale(tool,
                         from_=-10,  
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400,  
                         showvalue=1, 
                         variable=k1,  
                         tickinterval=1,  
                         resolution=1, 
                         command=norm)
            s5_1.place(x=320, y=50)
            def norm(k2):  
                mu = s5_1.get()
                sigma = float(k2)  
                plt.cla()
                #x = np.arange(-4 * mu, 4 * mu, 0.1)
                x = np.arange(-4, 4, 0.1)
                y = stats.norm.pdf(x, mu, sigma)
                plt.plot(x, y)
                plt.title('正态分布的参数: $\mu$ =%.1f,  $\sigma$ =%.1f' % (mu, sigma))
                plt.xlabel('x')
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s5_2 = tk.Scale(tool,
                         from_=1,  
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400,  
                         showvalue=1, 
                         variable=k2,  
                         tickinterval=1,  
                         resolution=1,  
                         command=norm)
            s5_2.place(x=320, y=130)
            L5 = tk.Label(tool, text='x的取值',width=5)
            L5.place(x=300, y=200)
            E5 = tk.Entry(tool, show=None)  
            E5.place(x=350, y=200)
#在鼠标焦点处插入输入内容
            def value():  
                t5.delete('1.0', 'end')
                try:
                    var = stats.norm.pdf(float(E5.get()), float(s5_1.get()), float(s5_2.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t5.insert('insert', "")
                    pass
                else:
                    t5.insert('insert', format(var, '0.2f'))
            b5 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b5.place(x=300, y=240)
            t5 = tk.Text(tool, width=10, height=2)
            t5.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为正态分布的分布函数
        elif ss.get() == 'Normal' and ss1.get()=='CDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL5_1 = tk.Label(tool, text='μ',width=8)
            LL5_1.place(x=270, y=70)
            LL5_2 = tk.Label(tool, text='σ',width=8)
            LL5_2.place(x=270, y=150)
            #正态分布的分布函数
            def norm(k1):  
                mu = float(k1)
                sigma = s5_2.get()  
                plt.cla()
                x = np.arange(-4, 4, 0.1)
                y = stats.norm.cdf(x, mu, sigma)
                plt.plot(x, y)
                plt.title('正态分布的参数: μ=%.1f, σ=%.1f' % (mu, sigma))
                plt.xlabel('x', fontsize=15)
                plt.ylabel('分布函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s5_1 = tk.Scale(tool,
                         from_=-3,  
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400,  
                         showvalue=1,  
                         variable=k1,
                         tickinterval=1,  
                         resolution=1, 
                         command=norm)
            s5_1.place(x=320, y=50)
            def norm(k2):  
                mu = s5_1.get()
                sigma = float(k2) 
                plt.cla()
                x = np.arange(-4, 4, 0.1)
                y = stats.norm.cdf(x, mu, sigma)
                plt.plot(x, y)
                plt.title('正态分布的参数: μ=%.1f, σ=%.1f' % (mu, sigma))
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s5_2 = tk.Scale(tool,
                         from_=1, 
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400,  
                         showvalue=1,  
                         variable=k2, 
                         tickinterval=1,  
                         resolution=1, 
                         command=norm)
            s5_2.place(x=320, y=130)
            L5 = tk.Label(tool, text='x的取值',width=5)
            L5.place(x=300, y=200)
            E5 = tk.Entry(tool, show=None)  
            E5.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t5.delete('1.0', 'end')
                try:
                    var = stats.norm.cdf(float(E5.get()), float(s5_1.get()), float(s5_2.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t5.insert('insert', "")
                    pass
                else:
                    t5.insert('insert', format(var, '0.2f'))
            b5 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b5.place(x=300, y=240)
            t5 = tk.Text(tool, width=10, height=2)
            t5.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s6_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL6_2.destroy()
            except NameError:
                pass
        #如果ss输入为均匀分布的密度函数
        elif ss.get() == 'Uniform' and ss1.get()=='PDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL6_1 = tk.Label(tool, text='a',width=8)
            LL6_1.place(x=270, y=70)
            LL6_2 = tk.Label(tool, text='b',width=8)
            LL6_2.place(x=270, y=150)
             #均匀分布的密度函数
            def uniform(k1): 
                #两个参数
                a = float(k1)
                b = s6_1.get()  
                n = np.arange(a, b)
                y = stats.uniform.pdf(n, a, b)
                plt.plot(n, y)
                plt.title('均匀分布的参数: a=%.1f, b=%.1f' % (a, b), fontsize=15)
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s6_1 = tk.Scale(tool,
                         from_=1, 
                         to=10,  
                         orient=tk.HORIZONTAL,  
                         length=400,  
                         showvalue=1,  
                         variable=k1,  
                         tickinterval=1,  
                         resolution=1,  
                         command=uniform)
            s6_1.place(x=320, y=50)
            def uniform(k2):  
                a = s6_1.get()
                b = float(k2)  
                n = np.arange(a, b)
                y = stats.uniform.pdf(n, a, b)
                plt.plot(n, y)
                plt.title('均匀分布的参数: a=%.1f, b=%.1f' % (a, b), fontsize=15)
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s6_2 = tk.Scale(tool,
                         from_=1,  
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400, 
                         showvalue=1,  
                         variable=k2, 
                         tickinterval=1,  
                         resolution=1, 
                         command=uniform)
            s6_2.place(x=320, y=130)
            L6 = tk.Label(tool, text='x的取值',width=5)
            L6.place(x=300, y=200)
            E6 = tk.Entry(tool, show=None) 
            E6.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():  
                t6.delete('1.0', 'end')
                try:
                    var = stats.uniform.pdf(float(E6.get()), float(s6_1.get()), float(s6_2.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t6.insert('insert', "")
                    pass
                else:
                    t6.insert('insert', format(var, '0.2f'))
            b6 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b6.place(x=300, y=240)
            t6 = tk.Text(tool, width=10, height=2)
            t6.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
        #如果ss输入为均匀分布的分布函数
        elif ss.get() == 'Uniform' and ss1.get()=='CDF':
            k1 = tk.IntVar()
            k2 = tk.IntVar()
            l.config(text=ss.get())
            LL6_1 = tk.Label(tool, text='a',width=8)
            LL6_1.place(x=270, y=70)
            LL6_2 = tk.Label(tool, text='b',width=8)
            LL6_2.place(x=270, y=150)
            #均匀分布的分布函数
            def uniform(k1): 
                a = float(k1)
                b = s6_1.get()   
                n = np.arange(a, b)
                y = stats.uniform.cdf(n, a, b)
                plt.plot(n, y)
                plt.title('均匀分布的参数: a=%.1f, b=%.1f' % (a, b), fontsize=15)
                plt.xlabel('x', fontsize=15)
                plt.ylabel('分布函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s6_1 = tk.Scale(tool,
                         from_=1,  
                         to=10,  
                         orient=tk.HORIZONTAL, 
                         length=400, 
                         showvalue=1,  
                         variable=k1, 
                         tickinterval=1,  
                         resolution=1,  
                         command=uniform)
            s6_1.place(x=320, y=50)
            def uniform(k2):  
                a = s6_1.get()
                b = float(k2)  
                n = np.arange(a, b)
                y = stats.uniform.cdf(n, a, b)
                plt.plot(n, y)
                plt.title('均匀分布的参数 a=%.1f, b=%.1f' % (a, b), fontsize=15)
                plt.xlabel('x', fontsize=15)
                plt.ylabel('密度函数', fontsize=15)
                plt.draw()
                time.sleep(0.1)
            s6_2 = tk.Scale(tool,
                         from_=1, 
                         to=10,  
                         orient=tk.HORIZONTAL,  
                         length=400,  
                         showvalue=1,  
                         variable=k2, 
                         tickinterval=1,  
                         resolution=1,  
                         command=uniform)
            s6_2.place(x=320, y=130)
            L6 = tk.Label(tool, text='x的取值',width=5)
            L6.place(x=300, y=200)
            E6 = tk.Entry(tool, show=None)  
            E6.place(x=350, y=200)
            #在鼠标焦点处插入输入内容
            def value():
                t6.delete('1.0', 'end')
                try:
                    var = stats.uniform.cdf(float(E6.get()), float(s6_1.get()), float(s6_2.get()))
                except ValueError:
                    tk.messagebox.showerror("Warning", "请输入正确的数字！")
                    t6.insert('insert', "")
                    pass
                else:
                    t6.insert('insert', format(var, '0.2f'))
            b6 = tk.Button(tool, text='函数值为', width=10,
                           height=2, command=value)
            b6.place(x=300, y=240)
            t6 = tk.Text(tool, width=10, height=2)
            t6.place(x=420, y=250)
            try:
                s2_2.destroy()
            except NameError:
                pass
            try:
                s5_2.destroy()
            except NameError:
                pass
            try:
                LL2_2.destroy()
            except NameError:
                pass
            try:
                LL5_2.destroy()
            except NameError:
                pass
    r1 = tk.Radiobutton(tool, text='泊松分布', variable=ss, value='Poisson', command=selection)
    r1.place(x=50, y=60)
    r2 = tk.Radiobutton(tool, text='二项分布', variable=ss, value='binomial', command=selection)
    r2.place(x=50, y=110)
    r3 = tk.Radiobutton(tool, text='几何分布', variable=ss, value='Geometry', command=selection)
    r3.place(x=50, y=160)
    r4 = tk.Radiobutton(tool, text='指数分布', variable=ss, value= 'Exponential', command=selection)
    r4.place(x=50, y=210)
    r5 = tk.Radiobutton(tool, text='正态分布', variable=ss, value='Normal', command=selection)
    r5.place(x=50, y=260)
    r6 = tk.Radiobutton(tool, text='均匀分布', variable=ss, value='Uniform', command=selection)
    r6.place(x=50, y=310)
    rr1 = tk.Radiobutton(tool, text='分布函数', variable=ss1, value='CDF', command=selection)
    rr1.place(x=50, y=360)
    rr2 = tk.Radiobutton(tool, text='概率密度函数', variable=ss1, value='PDF', command=selection)
    rr2.place(x=50, y=380)
    tool.mainloop()
toolbox()

