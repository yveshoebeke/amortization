#!/usr/bin/env python3

# TODO: bind 'Return' to input to evoke calculation and numeric check

import tkinter as tk
from tkinter import messagebox
from app.data import Process

class MyGUI:
    version: str = "0.0.2 beta"
    calc_type: int
    result_prompts = ["Amortization Amount:","Principle Amount:", "Interest Rate:","Hold Time:"]
    intro_msg = "Welcome!\n\nPlease select the desired calculation from the 'Action' menu option."
    # check_float_only = lambda e,v: MyGUI.float_only(e,v)

    def __init__(self):
        self.p = Process()
        self.root = tk.Tk()
        self.root.title("Amortization")
        self.root.iconbitmap("./amortization.png")
        self.root.geometry("500x200")
        self.root.option_add('*tearOff', False)

        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        print(w,h,ws,hs)
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('+%d+%d' % (x, y)) ## this part allows you to only change the location

        # Menu
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="New", command=self.clear)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)
        self.menubar.add_cascade(menu=self.filemenu, label="File")

        # Action menu
        self.actionmenu = tk.Menu(self.menubar)
        self.actionmenu.add_command(label="Amortization", command=self.compose_amortization_form)
        self.actionmenu.add_command(label="Principle", command=self.compose_principle_form)
        self.actionmenu.add_command(label="Interest", command=self.compose_interest_form)
        self.actionmenu.add_command(label="Holding Period", command=self.compose_holdtime_form)
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

        # Help menu
        self.helpmenu = tk.Menu(self.menubar)
        self.helpmenu.add_command(label ='General', command = self.give_help)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label ='Amortization', command = self.give_help)
        self.helpmenu.add_command(label ='Principle', command = self.give_help)
        self.helpmenu.add_command(label ='Interest Rate', command = self.give_help)
        self.helpmenu.add_command(label ='Hold Time', command = self.give_help)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label ='About', command = self.give_info)
        self.menubar.add_cascade(menu=self.helpmenu, label="Help")

        self.root.config(menu=self.menubar)

        # One time intro message
        self.dataentry = tk.Label(self.root, text=self.intro_msg, font=('Arial', 14))
        self.dataentry.pack(padx=20,pady=50)

        # Window close behavior -> close it all
        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.root.mainloop()


    # Close request from app menu -> make sure user wants to
    def on_closing(self):
        if messagebox.askyesno(parent=self.root, title="Quit?", message="Are you sure?"):
            self.root.destroy()

    # Clear (destroy) data entry frame
    def clear(self):
        try:
            self.dataentry.destroy()
        except:
            pass

    # Submit for calc and display result
    def set_result(self):
        try:
            self.p.roiAmnt = float(self.amortizationvalue.get()) 
        except:
            self.p.roiAmnt = 0

        try:
            self.p.principle = float(self.principlevalue.get())
        except:
            self.p.principle = 0

        try:
            self.p.interestRate = float(self.interestvalue.get())
        except:
            self.p.interestRate = 0

        try:
            self.p.investmentTime = float(self.holdtimevalue.get())
        except:
            self.p.investmentTime = 0

        # Apply requested formula
        self.p.calculators[self.calc_type - 1]()

        # Deposit result
        if self.calc_type == 4:
            self.resultvalue.config(text = "{:,.0f} years ".format(self.p.duration["years"]) + "{:,.0f} months".format(self.p.duration["months"]))
        else:
            self.resultvalue.config(text = "{:,.2f}".format(self.p.result))
    
    # About menu
    def give_info(self):
        info_text = "Version " + self.version +"\n\n(c) 2024 Bytesupply LLC\nAll rights Reserved\n\nAuthor: Yves Hoebeke\nyves.hoebeke@bytesupply.com"
        messagebox.showinfo("About Info:",info_text)

    # Help menu
    def give_help(self):
        info_text = "Select desired Action from menu.\nEnter action-appropriate values.\nPress Calculate button."
        messagebox.showinfo("General Help", info_text)

    # Prompt labels Value entries definition segment
    def set_amortization_entry(self, rowpos, focus):
        self.amortizationprompt = tk.Label(self.dataentry, text="Amortization Amount:", font=('Ariel', 16), anchor=tk.E)
        self.amortizationprompt.grid(row=rowpos, column=0, sticky=tk.W+tk.E)
        self.amortizationvalue = tk.Entry(self.dataentry, font=('Ariel', 16))
        # self.amortizationvalue.bind("<KeyRelease>", lambda event: self.float_only(event, "amortizationvalue", self.amortizationvalue))
        self.amortizationvalue.grid(row=rowpos, column=1, sticky=tk.W+tk.E)
        if focus:
            self.amortizationvalue.focus_set()

    def set_principle_entry(self, rowpos, focus):
        self.principleprompt = tk.Label(self.dataentry, text="Principle Amount:", font=('Ariel', 16), anchor=tk.E)
        self.principleprompt.grid(row=rowpos, column=0, sticky=tk.W+tk.E)
        self.principlevalue = tk.Entry(self.dataentry, font=('Ariel', 16))
        # self.principlevalue.bind("<KeyRelease>", lambda event: self.float_only(event, "principlevalue", self.principlevalue))
        self.principlevalue.grid(row=rowpos, column=1, sticky=tk.W+tk.E)
        if focus:
            self.principlevalue.focus_set()

    def set_interestrate_entry(self, rowpos, focus):
        self.interestprompt = tk.Label(self.dataentry, text="Interest Rate (%):", font=('Ariel', 16), anchor=tk.E)
        self.interestprompt.grid(row=rowpos, column=0, sticky=tk.W+tk.E)
        self.interestvalue = tk.Entry(self.dataentry, font=('Ariel', 16))
        # self.interestvalue.bind("<KeyRelease>", lambda event: self.float_only(event, "interestvalue", self.interestvalue))
        self.interestvalue.grid(row=rowpos, column=1, sticky=tk.W+tk.E)
        if focus:
            self.interestvalue.focus_set()
    
    def set_holdtime_entry(self, rowpos, focus):
        self.holdtimeprompt = tk.Label(self.dataentry, text="Hold Time (years):", font=('Ariel', 16), anchor=tk.E)
        self.holdtimeprompt.grid(row=rowpos, column=0, sticky=tk.W+tk.E)
        self.holdtimevalue = tk.Entry(self.dataentry, font=('Ariel', 16))
        # self.holdtimevalue.bind("<KeyRelease>", lambda event: self.float_only(event, "holdtimevalue", self.holdtimevalue))
        self.holdtimevalue.grid(row=rowpos, column=1, sticky=tk.W+tk.E)
        if focus:
            self.holdtimevalue.focus_set()

    def set_result_output(self, prompt):
        self.resultlabel = tk.Label(self.dataentry, text=prompt, font=('Ariel', 16), anchor=tk.E)
        self.resultlabel.grid(row=4, column=0, sticky=tk.W+tk.E)
        self.resultvalue = tk.Label(self.dataentry, text="", font=('Ariel', 16), anchor=tk.E)
        self.resultvalue.grid(row=4, column=1, sticky=tk.W+tk.E)

    def set_calculate_btn(self):
        self.submitbtn = tk.Button(self.dataentry, text="Calculate", font=('Ariel', 16), command=self.set_result)
        self.submitbtn.grid(row=3, column=1, sticky=tk.W+tk.E)
        # self.submitbtn.config(state="disabled") 

    # Start a new data entry frame
    def start_frame(self):
        self.clear()
        self.dataentry = tk.Frame(self.root)
        self.dataentry.columnconfigure(0, weight=1)
        self.dataentry.columnconfigure(2, weight=1)

    # Compose the data entry elements according to request
    def compose_amortization_form(self):
        self.calc_type = 1
        self.start_frame()

        self.set_principle_entry(0, True)
        self.set_interestrate_entry(1, False)
        self.set_holdtime_entry(2, False)
        self.amortizationvalue = tk.Entry(self.dataentry, text="0")
        self.set_calculate_btn()
        self.set_result_output(self.result_prompts[self.calc_type - 1])
        self.dataentry.pack(fill='x', padx=20, pady=20)

    def compose_principle_form(self):
        self.calc_type = 2
        self.start_frame()

        self.set_amortization_entry(0, True)
        self.set_interestrate_entry(1, False)
        self.set_holdtime_entry(2, False)

        self.set_calculate_btn()
        self.set_result_output(self.result_prompts[self.calc_type - 1])
        self.dataentry.pack(fill='x', padx=20, pady=20)
        
    def compose_interest_form(self):
        self.calc_type = 3
        self.start_frame()

        self.set_principle_entry(0, True)
        self.set_amortization_entry(1, False)
        self.set_holdtime_entry(2, False)

        self.set_calculate_btn()
        self.set_result_output(self.result_prompts[self.calc_type - 1])
        self.dataentry.pack(fill='x', padx=20, pady=20)
 
    def compose_holdtime_form(self):
        self.calc_type = 4
        self.start_frame()

        self.set_principle_entry(0, True)
        self.set_amortization_entry(1, False)
        self.set_interestrate_entry(2, False)

        self.set_calculate_btn()
        self.set_result_output(self.result_prompts[self.calc_type - 1])
        self.dataentry.pack(fill='x', padx=20, pady=20)

MyGUI()
