from tkinter import *
from PIL import ImageTk,Image
import sqlite3
root = Tk()
root.title("Teza")
root.geometry("400x400")

#Database

#Create a database
conn = sqlite3.connect("Investment.db")
#Create  Cursur
cur = conn.cursor()
# Create Table
cur.execute("""CREATE TABLE IF NOT EXISTS portfolio (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        STOCK STRING NOT NULL,
        PRICE REAL NOT NULL,
        QUANTITY INTEGER NOT NULL,
        INVESTMENT REAL,
        CURRENT_VALUE REAL NOT NULL,
        PROFIT_LOSS REAL
	)""");
# Display Entry Fields
label_stock =Label(root,text="STOCK:").grid(row=0,column=0)
stock = Entry(root,width=30)
stock.grid(row=0,column=1 ,padx=20)

label_price =Label(root,text="BUY PRICE:").grid(row=1,column=0)
price = Entry(root,width=30)
price.grid(row=1,column=1,pady=2)

label_quantity =Label(root,text="QUANTITY:").grid(row=2,column=0)
quantity = Entry(root,width=30)
quantity.grid(row=2,column=1,pady=2)

label_current =Label(root,text="CURRENT PRICE:").grid(row=3,column=0)
current_value = Entry(root,width=30)
current_value.grid(row=3,column=1,pady=2)

#Submit Function : Insert Data into database
def submit():
	price_1 = price.get()
	price_c = float(price_1)

	quantity_1 = quantity.get()
	quantity_c = float(quantity_1)

	current_value_1 = current_value.get()
	current_value_c = float(current_value_1)
	profit_loss = (current_value_c * quantity_c) - ( price_c * quantity_c)
	#Create a database
	conn = sqlite3.connect("Investment.db")
	#Create  Cursur
	cur = conn.cursor()

	#Insert Data
	cur.execute("INSERT INTO portfolio(STOCK,PRICE,QUANTITY,INVESTMENT,CURRENT_VALUE,PROFIT_LOSS) VALUES(:stock,:price,:quantity,:investment,:current_value,:proft_loss)",
		{
			"stock": stock.get(),
			"price": price_c,
			"quantity":quantity.get(),
			"investment":  price_c * quantity_c,
			"current_value":current_value_c,
			"proft_loss": str(round(profit_loss,2))
		})

	#commit Change
	conn.commit()
	#Close Connection
	conn.close()

	#clear the text boxes
	stock.delete(0,END)
	price.delete(0,END)
	quantity.delete(0,END)
	current_value.delete(0,END)
#Query function
def query():
	#New Window
	top = Toplevel()
	top.title("Database")
	top.configure(bg='black')

	conn = sqlite3.connect("Investment.db")
	#Create  Cursur
	cur = conn.cursor()

	
	#Headings
	sl_no= Label(top,text="SL No",bg="black",fg="white")
	sl_no.grid(row=0,column=0)

	Stock=Label(top,text="STOCK",bg="black",fg="white")
	Stock.grid(row=0,column=1)

	price=Label(top,text="BUY PRICE",bg="black",fg="white")
	price.grid(row=0,column=2)

	qty=Label(top,text="QUANTITY",bg="black",fg="white")
	qty.grid(row=0,column=3)

	invest=Label(top,text="INVESTMENT",bg="black",fg="white")
	invest.grid(row=0,column=4)

	current=Label(top,text="CURRENT PRICE",bg="black",fg="white")
	current.grid(row=0,column=5,columnspan=1)

	profit=Label(top,text="PROFIT/LOSS",bg="black",fg="white")
	profit.grid(row=0,column=6)

	cur.execute("SELECT * FROM portfolio")
	records=cur.fetchall()
	print(records)
	i=0
	for record in records:
		for j in range(len(record)):
			e = Entry(top,width=15,fg="black",bg="grey")
			e.grid(row=i+1,column=j)
			e.insert(END, record[j])
		i=i+1
	#commit Change
	conn.commit()
	#Close Connection
	conn.close()
#Create submit button
submit_btn =Button(root, text="Add Record To Database",command=submit)
submit_btn.grid(row=4,column=1)
#Create Query Button
Query_btn = Button(root,text="Show Records",command=query)
Query_btn.grid(row=5,column =1,padx=10,pady=10)


#commit Change
conn.commit()
#Close Connection
conn.close()
root.mainloop()