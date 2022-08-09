
from tkinter import ttk,filedialog
from tkinter import *
from matplotlib.ft2font import BOLD
from ttkwidgets.autocomplete import AutocompleteCombobox
import datetime as dt
import csv
from tkcalendar import DateEntry
from fpdf import FPDF
from PIL import Image, ImageTk
import cv2
from tkinter.messagebox import askokcancel, showinfo, WARNING
import os
from PyPDF2 import PdfWriter, PdfReader,PdfFileWriter, PdfFileReader





import sqlite3
dtime = dt.datetime.now()
with sqlite3.connect("database.db") as db:
    cursor=db.cursor() 

cursor.execute("""CREATE TABLE IF NOT EXISTS info(ID INTEGER PRIMARY KEY AUTOINCREMENT,date_time blob,
Vehicle_no BLOB CHECK(Vehicle_no != ''),Transporter_name TEXT CHECK(Transporter_name != ''),Driver_name TEXT CHECK(Driver_name != ''),
Lic_no blob CHECK(Lic_no != ''),Item_name blob CHECK(Item_name != ''),Qty integer CHECK(Qty != ''),
Mobile TEXT CHECK(Mobile GLOB '[1-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),Destination text,party_name text,Address text,Invoice_no blob);  """)


def insert():
    global error
    import datetime as dt
    dateTime1=str(date_time.get_date())+' '+ str(dt.datetime.now().time())
    try:
        cursor.execute("""INSERT INTO info(Vehicle_no,date_time,Item_name,Qty,Destination,party_name,Address,Invoice_no,
        Transporter_name,Driver_name,Lic_no,Mobile) values
        (?,?,?,?,?,?,?,?,?,?,?,?)""",(vechicle_no.get(),dateTime1,Item_name.get(),Qty.get(),
        Destination.get(),party_name.get(),Address.get(),Invoice_no.get(),transporter_name.get(),driver_name.get(),
        lic_no.get(),mobile.get().strip()))
        db.commit()
        
        error["text"] = "Data successfully recorded"
        error.config(bg='lightgreen',padx=0) 
        

        trv.delete(*trv.get_children())

        r_set=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Item_name,
        Qty from info where date_time>=? order by id desc;''',[str(dt.date.today())+" 00:00:00:000000"])


        trv.tag_configure('oddrow',background='white')
        trv.tag_configure('evenrow',background='lightblue')

        count=0 
        for dt in r_set: 
            if count%2==0:
                trv.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]),tags=('evenrow',))
            else:
                trv.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]),tags=('oddrow',))
            count+=1

        
        r=cursor.execute('''SELECT Max(ID) from info;''')
        for d in r:
            pass
        global k
        k=d[0]
        savePDF()

        
    except sqlite3.IntegrityError as e:
        if 'Mobile' in e.args[0]:
            error["text"] = "Error: Enter valid Mobile No."
        else:
            error["text"] = "Error: Enter all compulsory fields" 
        error.config(bg='red',padx=0)      



window = Tk()
window.title('KCC Data Entry')
window.geometry('950x600')


list=["Driver's Name* :","Transporter's Name* :","Vechicle No.* :","Driver's Licence No.* :","Driver's Mobile No.* :","Date :",
"Item Name* :","Qty* :","Destination :","Party Name :","Address :","Invoice No. :"]
list1=["vechicle_no","date_time","transporter_name","driver_name","lic_no","mobile","Item_name",
"Qty","Destination","party_name","Address","Invoice_no","ID"]

x=Label(text =' KCC PVT LTD.')
x.place(x=90,y=30)
x.configure(font=('', 18))

for i in range(len(list)):
    x ='label'+str(i+1)
    x = Label(text = list[i])
    x.place( x = 40 ,y = 35*(i+1)+50 )

listx,lst=[],[]

def check_input(event):
    
    value = event.widget.get()
    if value == '':
        driver_name['values'] = []
    else:
        listx.clear()
        lst.clear()
        data=cursor.execute('''SELECT DISTINCT Driver_name,vehicle_no,Lic_no,Mobile,transporter_name
            from info where Driver_name LIKE ? ;''',[value+'%'])
        
        for i in data:
            listx.append([i[0],i[1],i[2],i[3],i[4]])
            lst.append(i[0])

        driver_name['values'] = lst
        
    
def other_input(event):    

    c=driver_name.current()
    vechicle_no.delete(0,END)
    vechicle_no.insert(0,listx[c][1])
    lic_no.delete(0,END)
    lic_no.insert(0,listx[c][2])
    mobile.delete(0,END)
    mobile.insert(0,listx[c][3])
    transporter_name.delete(0,END)
    transporter_name.insert(0,listx[c][4])

    

driver_name = ttk.Combobox(window)
driver_name['values'] = []
driver_name.place ( x = 170 , y = 85, width = 170 , height = 25 )
driver_name.bind('<KeyRelease>', check_input)
driver_name.bind('<<ComboboxSelected>>', other_input)
d_name=driver_name.get()

transporter_name = Entry ( text = "" )
transporter_name.place ( x = 170 , y = 120, width = 170 , height = 25 )
t_name=transporter_name.get()

vechicle_no = Entry ( text = "" )
vechicle_no.place ( x = 170 , y = 155, width = 170 , height = 25 )
vno=vechicle_no.get()

lic_no = Entry ( text = "" )
lic_no.place ( x = 170 , y = 190, width = 170 , height = 25 )
l_no=lic_no.get()

mobile = Entry ( text = "" )
mobile.place ( x = 170 , y = 225, width = 170 , height = 25 )
m_no=mobile.get()

date_time = DateEntry(window,selectmode='day')
date_time.place ( x = 170 , y =260)
d_t=date_time

values=['HR Coils','CR Coils','GP Coils','PPGI Coils','GA Coils','HR Sheets',' CR Sheets','GP Sheets','PPGI Sheets','GA Sheets']
Item_name =AutocompleteCombobox(window, width=27,completevalues=values)
Item_name.place ( x = 170 , y =295, width = 170 , height = 25 )
Item_name.current()
i_name=Item_name.get()

Qty = Entry ( text = "" )
Qty.place ( x = 170 , y =330, width = 170 , height = 25 )
q=Qty.get()

Destination = Entry ( text = "" )
Destination.place ( x = 170 , y =365, width = 170 , height = 25 )
d=Destination.get()

party_name = Entry ( text = "" )
party_name.place ( x = 170 , y =400, width = 170 , height = 25 )
p_name=party_name.get()

Address = Entry ( text = "" )
Address.place ( x = 170 , y =435, width = 170 , height = 25 )
ad=Address.get()

Invoice_no = Entry ( text = "" )
Invoice_no.place ( x = 170 , y =470, width = 170 , height = 25 )
ino=Invoice_no.get()

mem=Message(text="Complusory ( * )",width=160)
mem.place( x = 30, y = 550 )

image=Message(text="Image Capture *:",width=160)
image.place( x = 30, y = 510 )

mem2=Message(text="Today's Recent Records :",width=1060)
mem2.place( x = 450, y = 40 )
mem2.configure(font=('', 10))



def viewData():
    top = Toplevel(window)
    top.geometry("800x600")
    top.title("KCC View Data") 

    l = Label(top,text = "Search by:")
    l.place( x = 30 ,y = 10)

    l1 = Label(top,text = "Date  from/on :")
    l1.place( x = 30 ,y = 30)

    l2 = Label(top,text = "To :")
    l2.place( x = 415 ,y = 30)

    l4 = Label(top,text = "Transporter's Name :")
    l4.place( x = 30 ,y = 55)

    l5 = Label(top,text = "Drivers's Name :")
    l5.place( x = 300 ,y = 55)

    l6 = Label(top,text = "Vehicle No.:")
    l6.place( x = 580 ,y = 55)
    
    fromDate = DateEntry(top,selectmode='day')
    fromDate.place ( x = 150 , y =30)

    toDate = DateEntry(top,selectmode='day')
    toDate.place ( x = 450 , y =30)

    fromDate.configure(state=DISABLED)
    toDate.configure(state=DISABLED)

    fromDate.configure(validate='none')

    global n
    n=0
    def naccheck():
        global n
        if nac.get() == 0:
            fromDate.configure(state=DISABLED)
            toDate.configure(state=DISABLED)
            ck2.configure(state=DISABLED)
            n=0
            

        else:
            fromDate.configure(state=NORMAL)
            ck2.configure(state=NORMAL)
            
          
            

    nac = IntVar()      
    ck1 = Checkbutton(top, text='use',variable=nac,onvalue = 1, offvalue = 0, command=naccheck)
    ck1.place ( x = 250 , y =30)

    def naccheck1():
        global n
        if nac1.get() == 0:
            toDate.configure(state=DISABLED)
            n=0
        else:
            toDate.configure(state=NORMAL)
            n=1
      

    nac1 = IntVar()      
    ck2 = Checkbutton(top, text='use',variable=nac1,onvalue = 1, offvalue = 0, command=naccheck1)
    ck2.place ( x = 550 , y =30)
    ck2.configure(state=DISABLED)



    tn = Entry ( top,text = "" )
    tn.place ( x = 150 , y =55)

    dn = Entry ( top,text = "" )
    dn.place ( x = 400 , y =55)

    vehn = Entry ( top,text = "" )
    vehn.place ( x = 650 , y =55)
    

    tree_frame= Frame(top)
    tree_frame.pack(pady=100,padx=50)

    tree_scroll=ttk.Scrollbar(tree_frame,orient=HORIZONTAL)
    tree_scroll.pack(side=BOTTOM,fill=X)

    s1=ttk.Style()
    s1.configure('Treeview', rowheight=25)
    trv1 = ttk.Treeview(tree_frame, selectmode ='browse',height=30,xscrollcommand=tree_scroll.set)
    
    trv1.pack()

    tree_scroll.config(command=trv1.xview)
    
    trv1["columns"] = ("1", "2", "3","4","5","6","7", "8", "9","10","11","12","13")
    
    trv1['show'] = 'headings'
    
    trv1.column("1", width = 90, anchor ='c')
    trv1.column("2", width = 120, anchor ='c')
    trv1.column("3", width = 110, anchor ='c')
    trv1.column("4", width = 80, anchor ='c')
    trv1.column("5", width = 80, anchor ='c')
    trv1.column("6", width = 110, anchor ='c')
    trv1.column("7", width = 80, anchor ='c')
    trv1.column("8", width = 80, anchor ='c')
    trv1.column("9", width = 80, anchor ='c')
    trv1.column("10", width = 80, anchor ='c')
    trv1.column("11", width = 100, anchor ='c')
    trv1.column("12", width = 80, anchor ='c')
    trv1.column("13", width = 80, anchor ='c')
    

    trv1.heading("1", text ="Vehicle No.")
    trv1.heading("2", text ="date_time")
    trv1.heading("3", text ="Transporter_Name")
    trv1.heading("4", text ="Driver_name") 
    trv1.heading("5", text ="Licence No.") 
    trv1.heading("6", text ="Driver Mobile No.")  
    trv1.heading("7", text ="Item_name")
    trv1.heading("8", text ="Qty")
    trv1.heading("9", text ="Destination")
    trv1.heading("10", text ="party_name")
    trv1.heading("11", text ="Address")
    trv1.heading("12", text ="Invoice_no")
    trv1.heading("13", text ="ID")


    r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
    Qty,Destination,party_name,Address,Invoice_no,ID from info order by id desc;''')
    
    result=cursor.fetchall()

    r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
    Qty,Destination,party_name,Address,Invoice_no,ID from info order by id desc;''')
    
    trv1.tag_configure('oddrow',background='white')
    trv1.tag_configure('evenrow',background='lightblue')

    count=0 
    for dt in r_set1: 
        if count%2==0:
            trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
            dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('evenrow',))
        else:
            trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
            dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('oddrow',))
        count+=1

    def exportCSV(result):
        with open( 'data.csv' ,'w+',newline='') as f :
            w = csv.writer(f, dialect ='excel')
            w.writerow (list1)
            for record in result :
                w.writerow (record)
        os.startfile('data.csv')
    
    def show():
        trv1.delete(*trv1.get_children())
        fd=str(fromDate.get_date())
        td=str(toDate.get_date())
       
        if nac.get()==0:
            r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
            Qty,Destination,party_name,Address,Invoice_no,ID from info where transporter_name=? or Driver_name=? or vehicle_no=?;''',
            (tn.get(),dn.get(),vehn.get()))
        elif  nac.get()==1 and nac1.get()==0 and n==0 and (tn.get()=='' and dn.get() =='' and vehn.get()=='' ):
            r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
            Qty,Destination,party_name,Address,Invoice_no,ID from info where date_time between ? and ? ;''',
            (fd+" 00:00:00:000000",fd+"23:59:59:000000"))    
        elif  nac.get()==1 and nac1.get()==0 and n==0 and (tn.get()!='' or dn.get() !='' or vehn.get()!='' ):
            r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
            Qty,Destination,party_name,Address,Invoice_no,ID from info where date_time between ? and ? and (transporter_name=? or Driver_name=?  or vehicle_no=?) ;''',
            (fd+" 00:00:00:000000",fd+"23:59:59:000000",tn.get(),dn.get(),vehn.get()))
        elif  nac.get()==1 and nac1.get()==1 and n==1 and (tn.get()=='' and dn.get() =='' and vehn.get()=='' ):
            r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
            Qty,Destination,party_name,Address,Invoice_no,ID from info where date_time between ? and ?;''',
            (fd+" 00:00:00:000000",td+"23:59:59:000000"))
        elif  nac.get()==1 and nac1.get()==1 and n==1 and (tn.get()!='' or dn.get() !='' or vehn.get()!='' ):
            r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
            Qty,Destination,party_name,Address,Invoice_no,ID from info where date_time between ? and ? and (transporter_name=? or Driver_name=?  or vehicle_no=?) ;''',
            (fd+" 00:00:00:000000",td+"23:59:59:000000",tn.get(),dn.get(),vehn.get()))
          
          
        trv1.tag_configure('oddrow',background='white')
        trv1.tag_configure('evenrow',background='lightblue')

        count=0 
        for dt in r_set1: 
            if count%2==0:
                trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('evenrow',))
            else:
                trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('oddrow',))
            count+=1 
        csv_button.destroy()    
            
    def fun1_showPDF():
        global error2
        item = trv1.selection()
        if len(item)==0:
            error2["text"] = "Select an Entry First"
            error2.config(bg='red',padx=0)
        else:  
            error2.destroy()  
            error2=Message(top,text="",width=260)
            error2.place( x = 350, y = 500 )
            for i in item:
                p=trv1.item(i,'values')[12]
            
            os.startfile('pdf_folder\pdf_'+str(p)+'.pdf')

    def fun2_delete():
        global error2
        item = trv1.selection()
        if len(item)==0:
            error2["text"] = "Select an Entry First"
            error2.config(bg='red',padx=0)
        else:    
            answer = askokcancel(
            title='Confirmation',
            message='Deleting will delete the data in database and PDF.',
            icon=WARNING,parent=top)

            if answer:
                showinfo(
                    title='Deletion Status',
                    message='The data is deleted successfully',parent=top)

                for i in item:
                    p=trv1.item(i,'values')[12]
                error2.destroy()
                error2=Message(top,text="",width=260)
                error2.place( x = 350, y = 500 )
                cursor.execute('''DELETE FROM info
                            WHERE ID=?;''',[p])
                        
                trv1.delete(*trv1.get_children())

                r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
                Qty,Destination,party_name,Address,Invoice_no,ID from info order by id desc;''')
                trv1.tag_configure('oddrow',background='white')
                trv1.tag_configure('evenrow',background='lightblue')

                count=0 
                for dt in r_set1: 
                    if count%2==0:
                        trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                        dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('evenrow',))
                    else:
                        trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                        dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('oddrow',))
                    count+=1
                db.commit()    

                if os.path.exists('pdf_folder/pdf_'+str(p)+'.pdf'):
                    os.remove('pdf_folder/pdf_'+str(p)+'.pdf')               

    def fun2_edit():
        global error2
        item = trv1.selection()
        if len(item)==0:
            error2["text"] = "Select an Entry First"
            error2.config(bg='red',padx=0)
        else:    

            for i in item:
                p=trv1.item(i,'values')[12]
             
            v1=trv1.item(i,'values')[0]
            v2=trv1.item(i,'values')[1]
            v3=trv1.item(i,'values')[2]
            v4=trv1.item(i,'values')[3]
            v5=trv1.item(i,'values')[4]
            v6=trv1.item(i,'values')[5]
            v7=trv1.item(i,'values')[6]
            v8=trv1.item(i,'values')[7]
            v9=trv1.item(i,'values')[8]
            v10=trv1.item(i,'values')[9]
            v11=trv1.item(i,'values')[10]
            v12=trv1.item(i,'values')[11]
            error2.destroy()
            error2=Message(top,text="",width=260)
            error2.place( x = 350, y = 500 )
            
            top1 = Toplevel(top)
            top1.geometry("600x600")
            top1.title("KCC Edit Data")

            for i in range(len(list)):
                x ='label'+str(i+1)
                x = Label(top1,text = list[i])
                x.place( x = 40 ,y = 35*(i+1)+50 )

            driver_name = Entry (top1, text = "" )
            driver_name.place ( x = 170 , y = 85, width = 170 , height = 25 )
            driver_name.insert(0,v4)

            transporter_name = Entry (top1, text = "" )
            transporter_name.place ( x = 170 , y = 120, width = 170 , height = 25 )
            transporter_name.insert(0,v3)

            vechicle_no = Entry (top1, text = "" )
            vechicle_no.place ( x = 170 , y = 155, width = 170 , height = 25 )
            vechicle_no.insert(0,v1)

            lic_no = Entry (top1, text = "" )
            lic_no.place ( x = 170 , y = 190, width = 170 , height = 25 )
            lic_no.insert(0,v5)

            mobile = Entry (top1, text = "" )
            mobile.place ( x = 170 , y = 225, width = 170 , height = 25 )
            mobile.insert(0,v6)

            date_time = Entry(top1,text="")
            date_time.place ( x = 170 , y =260,width = 170 , height = 25)
            date_time.insert(0,v2)


            Item_name = Entry (top1, text = "" )
            Item_name.place ( x = 170 , y =295, width = 170 , height = 25 )
            Item_name.insert(0,v7)

            Qty = Entry (top1, text = "" )
            Qty.place ( x = 170 , y =330, width = 170 , height = 25 )
            Qty.insert(0,v8)

            Destination = Entry (top1, text = "" )
            Destination.place ( x = 170 , y =365, width = 170 , height = 25 )
            Destination.insert(0,v9)

            party_name = Entry (top1, text = "" )
            party_name.place ( x = 170 , y =400, width = 170 , height = 25 )
            party_name.insert(0,v10)

            Address = Entry (top1, text = "" )
            Address.place ( x = 170 , y =435, width = 170 , height = 25 )
            Address.insert(0,v11)

            Invoice_no = Entry (top1, text = "" )
            Invoice_no.place ( x = 170 , y =470, width = 170 , height = 25 )
            Invoice_no.insert(0,v12)

            def update():
                cursor.execute('''UPDATE info
                    SET Vehicle_no=?,date_time=?,Item_name=?,Qty=?,Destination=?
                    ,party_name=?,Address=?,Invoice_no=?,Transporter_name=?
                    ,Driver_name=?,Lic_no=?,Mobile=?
                    WHERE ID = ?;''',(vechicle_no.get(),date_time.get(),Item_name.get(),Qty.get(),
                    Destination.get(),party_name.get(),Address.get(),Invoice_no.get(),transporter_name.get(),driver_name.get(),
                    lic_no.get(),mobile.get().strip(),p))
                db.commit()    
                 
                trv1.delete(*trv1.get_children())

                r_set1=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Lic_no,Mobile,Item_name,
                Qty,Destination,party_name,Address,Invoice_no,ID from info order by id desc;''')
                trv1.tag_configure('oddrow',background='white')
                trv1.tag_configure('evenrow',background='lightblue')

                count=0 
                for dt in r_set1: 
                    if count%2==0:
                        trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                        dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('evenrow',))
                    else:
                        trv1.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],
                        dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12]),tags=('oddrow',))
                    count+=1


                pdf = FPDF( 'P' ,'mm' , 'A4' )
                pdf.add_page()
                pdf.set_font ( 'times' ,'BU',16)

                pdf.cell ( 0, 10 , 'KRISHNA SHEET PROCESSORS PVT.LTD', ln=1,align="C")

                pdf.set_font ( 'times' ,'BU',13)
                
                pdf.cell ( 0, 10 , 'Plot No C-26, MIDC Taloja, Dist. Raigad', ln=1,align="C")
                pdf.cell ( 0, 20 , 'VEHICLE DETAILS', ln=1,align="C")

                pdf.set_font ( 'times' ,'',13)
                data=(('Date :  ',date_time.get()[0:10])
                    ,('Vehicle No. :  ',vechicle_no.get()) 
                    ,( 'Name of Transporter :  ',transporter_name.get())
                    ,( 'Name of Driver :   ',driver_name.get())
                    ,( "Driver's Licence No. :  ",lic_no.get() )
                    ,( "Driver's Mobile No.  :  ",mobile.get())
                    ,( 'Loading From : ' ,'TALOJA')
                    ,( 'Destination :  ',Destination.get() )
                    ,( 'Party Name :  ',party_name.get())
                    ,( 'Adddress :  ',Address.get() )
                    ,( 'Invoice No. :  ',Invoice_no.get())
                    ,( 'Item Name :  ',Item_name.get())
                    ,( 'Qty :  ',Qty.get())    )
                

                line_height = pdf.font_size * 1.5
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        if j==0:
                            pdf.multi_cell(pdf.epw /3, line_height, data[i][j], border=1,
                                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
                        else:
                            pdf.multi_cell(2*pdf.epw /3, line_height, data[i][j], border=1,
                                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)           
                    pdf.ln(line_height)

                pdf.cell ( 0, 20 , '                            ',ln=1,align="R")
                pdf.set_font ( 'times' ,'BU',20)
                pdf.cell ( 0, 0 , '                            ',align="R")
                pdf.set_font ( 'times' ,'B',13)
                pdf.cell ( 0, 20 ,"Driver's Signature", ln=1,align="R")

                
                path='pdf_folder/pdf_'+str(p)+'.pdf'

                reader = PdfReader(path) 
                writer = PdfWriter()
                for page in reader.pages:
                    page.cropbox.upper_left = (0,350)
                    
                    writer.add_page(page) 
                
                with open('result.pdf','wb') as fp:
                    writer.write(fp) 

                pdf.output ( 'pdf_folder/pdf_'+str(p)+'.pdf' )
                
                watermark = PdfFileReader('result.pdf')
                watermarkpage = watermark.getPage(0)
                pdf1 = PdfFileReader(path)
                pdfwrite = PdfFileWriter()
                
                pdfpage = pdf1.getPage(0)
                pdfpage.mergePage(watermarkpage)
                pdfwrite.addPage(pdfpage)
                with open(path, 'wb') as fh:
                    pdfwrite.write(fh)
                    


                conf=Message(top1,text="Updated Successfully",width=260)
                conf.place( x = 150, y = 500 )
                conf.config(bg='light green',padx=0) 
            
            update_button = Button(top1,text = "Update", command = update)
            update_button.place(x=150,y=520,width=75,height=25)
        
            top1.mainloop()
                    
    def fun2_addImage():
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        from reportlab.lib.pagesizes import letter,A4

        global error2
        item = trv1.selection()
        if len(item)==0:
            error2["text"] = "Select an Entry First"
            error2.config(bg='red',padx=0)
        else:    
            error2.destroy()
            top3 = Toplevel(top)
            top3.geometry("300x300")
            top3.title("Add Image")

            img_button = Button(top3,text = "Select Image", command = capture )
            img_button.place(x=100,y=100,width=100,height=35)

            def print_pdf():
                for i in item:
                    v1=trv1.item(i,'values')[0]
                    v2=trv1.item(i,'values')[1]
                    v3=trv1.item(i,'values')[2]
                    v4=trv1.item(i,'values')[3]
                    v5=trv1.item(i,'values')[4]
                    v6=trv1.item(i,'values')[5]
                    v7=trv1.item(i,'values')[6]
                    v8=trv1.item(i,'values')[7]
                    v9=trv1.item(i,'values')[8]
                    v10=trv1.item(i,'values')[9]
                    v11=trv1.item(i,'values')[10]
                    v12=trv1.item(i,'values')[11]
                    p=trv1.item(i,'values')[12]
                  


                pdf = FPDF( 'P' ,'mm' , 'A4' )
                pdf.add_page()
                pdf.set_font ( 'times' ,'BU',16)

                pdf.cell ( 0, 10 , 'KRISHNA SHEET PROCESSORS PVT.LTD', ln=1,align="C")

                pdf.set_font ( 'times' ,'BU',13)
                
                pdf.cell ( 0, 10 , 'Plot No C-26, MIDC Taloja, Dist. Raigad', ln=1,align="C")
                pdf.cell ( 0, 20 , 'VEHICLE DETAILS', ln=1,align="C")

                pdf.set_font ( 'times' ,'',13)
                data=(('Date :  ',v1)
                    ,('Vehicle No. :  ',v2) 
                    ,( 'Name of Transporter :  ',v3)
                    ,( 'Name of Driver :   ',v4)
                    ,( "Driver's Licence No. :  ",v5 )
                    ,( "Driver's Mobile No.  :  ",v6)
                    ,( 'Loading From : ' ,'TALOJA')
                    ,( 'Destination :  ',v7 )
                    ,( 'Party Name :  ',v8)
                    ,( 'Adddress :  ',v9 )
                    ,( 'Invoice No. :  ',v10)
                    ,( 'Item Name :  ',v11)
                    ,( 'Qty :  ',v12))
                

                line_height = pdf.font_size * 1.5
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        if j==0:
                            pdf.multi_cell(pdf.epw /3, line_height, data[i][j], border=1,
                                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
                        else:
                            pdf.multi_cell(2*pdf.epw /3, line_height, data[i][j], border=1,
                                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)           
                    pdf.ln(line_height)

                pdf.cell ( 0, 20 , '                            ',ln=1,align="R")
                pdf.set_font ( 'times' ,'BU',20)
                pdf.cell ( 0, 0 , '                            ',align="R")
                pdf.set_font ( 'times' ,'B',13)
                pdf.cell ( 0, 20 ,"Driver's Signature", ln=1,align="R")

                img = Image.open("frame_2.jpg")
                width, height = img.size
                if width/height>1 and 190*(height/width)<115:
                    pdf.image(img,x=10,y=175,h=0,w=190)
                elif width/height>1 and 190*(height/width)>115:
                    pdf.image(img,x=10,y=175,h=115,w=190)
                elif width/height<=1:
                    pdf.image(img,x=10,y=175,h=115,w=120)

                import datetime as dt    

                pdf.cell ( 5, 0 ,"",align="R")
                pdf.set_fill_color(r=255,g=255,b=255)
                pdf.cell ( 42, 5 ,str(dt.datetime.now().replace(microsecond=0)),fill=True)
                pdf.cell ( 42, 5 ,'',)

                pdf.output ( 'pdf_folder/pdf_'+str(p)+'.pdf' )
                os.startfile('pdf_folder\pdf_'+str(p)+'.pdf')


            p_button = Button(top3,text = "Make Pdf & Print", command = print_pdf )
            p_button.place(x=70,y=200,width=175,height=35)

            top3.mainloop()


            
                    


    global error2
    error2=Message(top,text="",width=260)
    error2.place( x = 350, y = 500 )

    select_button = Button(top,text = "Enter", command = show)
    select_button.place(x=650,y=25,width=75,height=25)  

    pdf_button  = Button(top,text = "Show pdf", command = fun1_showPDF)
    pdf_button .place(x=250,y=525,width=75,height=25)

    del_button  = Button(top,text = "Delete Record", command = fun2_delete)
    del_button .place(x=450,y=525,width=100,height=25)

    edit_button  = Button(top,text = "Edit pdf", command = fun2_edit)
    edit_button .place(x=150,y=525,width=75,height=25)

    img_button  = Button(top,text = "Add Image", command = fun2_addImage)
    img_button .place(x=70,y=525,width=75,height=25)
     
    csv_button= Button(top,text = "Export to Excel", command = lambda: exportCSV(result))   
    csv_button.place(x=600,y=525,width=105,height=25)
    
    top.mainloop()



def capture():
    top = Toplevel(window)
    top.geometry("800x600")
    top.title("KCC Capture Image")

    
    label =Label(top)
    label.grid(row=0, column=0)
    
   
    def cam1():
        cam2_button.destroy()
        cap= cv2.VideoCapture('rtsp://admin:cctv@321@192.168.0.164:554/Streaming/Channels/001/?transportmode=unicast')
        
        
        def show_frames():
            global cv2image,cv2image1
            
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            cv2image1 = cv2.resize(cv2image, (2560, 1440))
            cv2image = cv2.resize(cv2image, (760, 440 ))

            img = Image.fromarray(cv2image)
            
            imgtk = ImageTk.PhotoImage(image = img)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            label.after(20, show_frames)
        
        def capt():
            cv2.imwrite("frame_2.jpg",cv2.cvtColor(cv2image1,cv2.COLOR_RGB2BGR))
            message["text"]='Screen captures successfully'
            message.config(bg='lightgreen',padx=0)

            

            s_button = Button(top,text = "Select Area", command = select )
            s_button.place(x=400,y=550,width=120,height=35)

        def select():
            
            im=cv2.imread("frame_2.jpg")
            half = cv2.resize(im, (0, 0), fx = 0.5, fy = 0.5)
            x,y,w,h=cv2.selectROI('select Area',half)
            x,y,w,h=2*x,2*y,2*w,2*h
            cropped_image=im[y:y+h,x:x+w]
            cv2.imwrite("frame_2.jpg",cropped_image)
            cv2.destroyAllWindows()


        cap_button = Button(top,text = "Capture", command = capt )
        cap_button.place(x=400,y=500,width=100,height=35)

        message=Message(top,text="",width=260)
        message.place( x = 400, y = 465 )
        show_frames()
    
   

    def cam2():
        cam1_button.destroy()
        cap= cv2.VideoCapture('rtsp://admin:cctv@321@192.168.0.165:554/Streaming/Channels/001/?transportmode=unicast')
        
        def show_frames():
            global cv2image,cv2image1
            
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            cv2image1 = cv2.resize(cv2image, (2560, 1440))
            cv2image = cv2.resize(cv2image, (760, 440))
            
            img = Image.fromarray(cv2image)
            
            imgtk = ImageTk.PhotoImage(image = img)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            label.after(20, show_frames)
        
        def capt():
            cv2.imwrite("frame_2.jpg",cv2.cvtColor(cv2image1,cv2.COLOR_RGB2BGR))
            message["text"]='Screen captures successfully'
            message.config(bg='lightgreen',padx=0)

            

            s_button = Button(top,text = "Select Area", command = select )
            s_button.place(x=400,y=550,width=120,height=35)

        def select():
            
            im=cv2.imread("frame_2.jpg")
            half = cv2.resize(im, (0, 0), fx = 0.5, fy = 0.5)
            x,y,w,h=cv2.selectROI('select Area',half)
            x,y,w,h=2*x,2*y,2*w,2*h
            cropped_image=im[y:y+h,x:x+w]
            cv2.imwrite("frame_2.jpg",cropped_image)
            cv2.destroyAllWindows()

        cap_button = Button(top,text = "Capture", command = capt )
        cap_button.place(x=400,y=500,width=100,height=35)

        message=Message(top,text="",width=260)
        message.place( x = 400, y = 465 )
        show_frames()


    def upload_file():
        filename = filedialog.askopenfilename ( parent=top,initialdir = " / " , title = " Select A File " , filetype = ( ('Jpg Files', '*.jpg'),('Jpeg Files', '*.jpeg')))

        image = Image.open(filename)
        global resize_image
        resize_image = image.resize((700, 450))
        img = ImageTk.PhotoImage(resize_image)
        label.imgtk = img
        label.configure(image=img)

        def capt():
            global resize_image
            resize_image=resize_image.save("frame-1.jpg")

        cap_button = Button(top,text = "Capture", command = capt )
        cap_button.place(x=400,y=500,width=100,height=35)

     

        message=Message(top,text="",width=260)
        message.place( x = 400, y = 465 )


    browse_button = Button(top, text='Upload File', width=20,command =upload_file)
    browse_button.place(x=100,y=550,width=100,height=35)


    cam1_button = Button(top,text = "Cam1", command = cam1 )
    cam1_button.place(x=100,y=500,width=100,height=35)
    
    cam2_button = Button(top,text = "Cam2", command = cam2 )
    cam2_button.place(x=250,y=500,width=100,height=35)
    
    top.mainloop()

def clear():
    
    vechicle_no.delete(0, END)
    transporter_name.delete(0, END)
    driver_name.delete(0, END)
    lic_no.delete(0, END)
    mobile.delete(0, END)
    Item_name.delete(0, END)
    Qty.delete(0, END)
    Destination.delete(0, END)
    party_name.delete(0, END)
    Address.delete(0, END)
    Invoice_no.delete(0, END)
    error["text"] = ""
    error.config(bg='#f0f0f0',padx=0) 
    
    

def printPDF():
    os.startfile('pdf_folder\pdf_'+str(k)+'.pdf')
    

def savePDF():
    
    pdf = FPDF( 'P' ,'mm' , 'A4' )
    pdf.add_page()
    pdf.set_font ( 'times' ,'BU',16)

    pdf.cell ( 0, 10 , 'KRISHNA SHEET PROCESSORS PVT.LTD', ln=1,align="C")

    pdf.set_font ( 'times' ,'BU',13)
    
    pdf.cell ( 0, 10 , 'Plot No C-26, MIDC Taloja, Dist. Raigad', ln=1,align="C")
    pdf.cell ( 0, 20 , 'VEHICLE DETAILS', ln=1,align="C")

    pdf.set_font ( 'times' ,'',13)
    data=(('Date :  ',str(date_time.get_date()))
        ,('Vehicle No. :  ',vechicle_no.get()) 
        ,( 'Name of Transporter :  ',transporter_name.get())
        ,( 'Name of Driver :   ',driver_name.get())
        ,( "Driver's Licence No. :  ",lic_no.get() )
        ,( "Driver's Mobile No.  :  ",mobile.get())
        ,( 'Loading From : ' ,'TALOJA')
        ,( 'Destination :  ',Destination.get() )
        ,( 'Party Name :  ',party_name.get())
        ,( 'Adddress :  ',Address.get() )
        ,( 'Invoice No. :  ',Invoice_no.get())
        ,( 'Item Name :  ',Item_name.get())
        ,( 'Qty :  ',Qty.get()))
    

    line_height = pdf.font_size * 1.5
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j==0:
                pdf.multi_cell(pdf.epw /3, line_height, data[i][j], border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            else:
                pdf.multi_cell(2*pdf.epw /3, line_height, data[i][j], border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)           
        pdf.ln(line_height)

    pdf.cell ( 0, 20 , '                            ',ln=1,align="R")
    pdf.set_font ( 'times' ,'BU',20)
    pdf.cell ( 0, 0 , '                            ',align="R")
    pdf.set_font ( 'times' ,'B',13)
    pdf.cell ( 0, 20 ,"Driver's Signature", ln=1,align="R")


    img = Image.open("frame_2.jpg")
    width, height = img.size
    if width/height>1 and 190*(height/width)<115:
        pdf.image(img,x=10,y=175,h=0,w=190)
    elif width/height>1 and 190*(height/width)>115:
        pdf.image(img,x=10,y=175,h=115,w=190)
    elif width/height<=1:
        pdf.image(img,x=10,y=175,h=115,w=120)

    import datetime as dt    

    pdf.cell ( 5, 0 ,"",align="R")
    pdf.set_fill_color(r=255,g=255,b=255)
    pdf.cell ( 42, 5 ,str(dt.datetime.now().replace(microsecond=0)),fill=True)
    pdf.cell ( 42, 5 ,'',)

    pdf.output ( 'pdf_folder/pdf_'+str(k)+'.pdf' )


if not os.path.exists('pdf_folder'):
    os.makedirs('pdf_folder')   


clear_button = Button(text = "Clear", command = clear )
clear_button.place(x=210,y=550,width=75,height=35)

view_button = Button(text = "View Data", command = viewData )
view_button.place(x=800,y=500,width=75,height=35)


image_button = Button(text = "Select", command = capture )
image_button.place(x = 170 , y =500,width=170,height=35)


print_button = Button(window,text = "print", command = printPDF )
print_button.place(x=470,y=500,width=75,height=35)


input_button = Button(window,text = "Add", command = insert )
input_button.place(x=370,y=500,width=75,height=35)


error=Message(window,text="",width=260)
error.place( x = 370, y = 475 )


s=ttk.Style()
s.configure('Treeview', rowheight=25)
trv = ttk.Treeview(window, selectmode ='browse',height=15)
  
trv.grid(row=1,column=1,padx=370,pady=70)
trv["columns"] = ("1", "2", "3","4","5","6")
  
trv['show'] = 'headings'
   
trv.column("1", width = 90, anchor ='c')
trv.column("2", width = 120, anchor ='c')
trv.column("3", width = 110, anchor ='c')
trv.column("4", width = 80, anchor ='c')
trv.column("5", width = 80, anchor ='c')
trv.column("6", width = 30, anchor ='c')
  

trv.heading("1", text ="Vehicle No.")
trv.heading("2", text ="date_time")
trv.heading("3", text ="Transporter_Name")
trv.heading("4", text ="Driver_name")  
trv.heading("5", text ="Item_name")
trv.heading("6", text ="Qty")



r_set=cursor.execute('''SELECT vehicle_no,date_time,transporter_name,Driver_name,Item_name,
Qty from info where date_time>=? order by id desc;''',[str(dt.date.today())+" 00:00:00:000000"])

trv.tag_configure('oddrow',background='white')
trv.tag_configure('evenrow',background='lightblue')

count=0 
for dt in r_set: 
    if count%2==0:
        trv.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]),tags=('evenrow',))
    else:
        trv.insert(parent='', index='end', text=dt[0],values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]),tags=('oddrow',))
    count+=1


window.mainloop()