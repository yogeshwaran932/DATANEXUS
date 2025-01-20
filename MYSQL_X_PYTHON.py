import mysql.connector
from tabulate import tabulate
from mysql.connector import Error
from tkinter import *
from PIL import ImageTk
import mysql.connector as c
from tkinter import messagebox
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, Tk, StringVar
import tkinter as tk
from tkinter import Label
from PIL import ImageTk, Image
from tkinter import *
import random
import os





def akk():

    ##################################################################################################################################################################################################
    ##################################################################################################################################################################################################
    ##################################################################################################################################################################################################
    def ALTER():

        # Function to connect to MySQL database
        def connect_to_db():
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=password,
                    database=database_var1.get() if database_var1.get() else None
                )
                return connection
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}",parent=root)
                return None

        # Function to execute the ALTER TABLE commands
        def alter_table():
            selected_operation = operation_var.get()
            table_name = table_var.get()
            
            if selected_operation == "Add Column":
                column_name = column_name_entry.get()
                column_type = column_type_entry.get()
                query = f"ALTER TABLE {table_name} ADD {column_name} {column_type};"
            
            elif selected_operation == "Modify Column":
                column_name = column_name_entry.get()
                new_column_type = column_type_entry.get()
                query = f"ALTER TABLE {table_name} MODIFY {column_name} {new_column_type};"
            
            elif selected_operation == "Drop Column":
                column_name = column_name_entry.get()
                query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
            
            elif selected_operation == "Rename Column":
                old_column_name = old_column_name_entry.get()
                new_column_name = new_column_name_entry.get()
                query = f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};"
            
            elif selected_operation == "Rename Table":
                new_table_name = new_table_name_entry.get()
                query = f"ALTER TABLE {table_name} RENAME TO {new_table_name};"
            
            elif selected_operation == "Add Primary Key":
                column_name = column_name_entry.get()
                query = f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_name});"
            
            elif selected_operation == "Add Foreign Key":
                column_name = column_name_entry.get()
                referenced_table = ref_table_entry.get()
                referenced_column = ref_column_entry.get()
                query = f"""
                    ALTER TABLE {table_name}
                    ADD CONSTRAINT fk_{column_name}
                    FOREIGN KEY ({column_name})
                    REFERENCES {referenced_table}({referenced_column});
                    """
            else:
                messagebox.showwarning("Invalid Operation", "Please select a valid operation.",parent=root)
                return
            
            # Execute the query
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute(query)
                    connection.commit()
                    messagebox.showinfo("Success", "Table altered successfully!",parent=root)
                except mysql.connector.Error as err:
                    messagebox.showerror("SQL Error", f"Error: {err}",parent=root)
                finally:
                    cursor.close()
                    connection.close()

        # Function to dynamically display input fields based on selected operation
        def display_fields(*args):
            # Hide all fields first
            for widget in dynamic_fields_frame.winfo_children():
                widget.pack_forget()

            selected_operation = operation_var.get()

            # Show relevant fields for each operation
            
            table_name_entry = Label(dynamic_fields_frame, text='SELECT TABLE')
            table_name_entry.pack()
            table_dropdown1.pack()

            if selected_operation == "Add Column" or selected_operation == "Modify Column":
                Label(dynamic_fields_frame, text="Column Name:").pack()
                column_name_entry.pack()
                Label(dynamic_fields_frame, text="Column Type:").pack()
                column_type_entry.pack()
            
            elif selected_operation == "Drop Column":
                Label(dynamic_fields_frame, text="Column Name:").pack()
                column_name_entry.pack()
            
            elif selected_operation == "Rename Column":
                Label(dynamic_fields_frame, text="Old Column Name:").pack()
                old_column_name_entry.pack()
                Label(dynamic_fields_frame, text="New Column Name:").pack()
                new_column_name_entry.pack()
            
            elif selected_operation == "Rename Table":
                Label(dynamic_fields_frame, text="New Table Name:").pack()
                new_table_name_entry.pack()
            
            elif selected_operation == "Add Primary Key":
                Label(dynamic_fields_frame, text="Column Name:").pack()
                column_name_entry.pack()
            
            elif selected_operation == "Add Foreign Key":
                Label(dynamic_fields_frame, text="Column Name:").pack()
                column_name_entry.pack()
                Label(dynamic_fields_frame, text="Referenced Table:").pack()
                ref_table_entry.pack()
                Label(dynamic_fields_frame, text="Referenced Column:").pack()
                ref_column_entry.pack()

        # Function to get databases
        def get_databases1():
            mydb = connect_to_db()
            if mydb is not None:
                cursor = mydb.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                cursor.close()
                mydb.close()
                return databases
            return [] 
        def get_and_populate_tables(database_name):
            mydb = connect_to_db()
            if mydb is not None:
                cursor = mydb.cursor()
                cursor.execute(f"USE {database_name}")
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                cursor.close()
                mydb.close()
                table_dropdown1['values'] = tables
            else:
                messagebox.showerror("Error", "Error connecting to the database.",parent=root)
                return
        def on_database_select(event):
            global selected_database
            selected_database = database_var1.get()
            if selected_database:
                get_and_populate_tables(selected_database)

        # Tkinter GUI Setup
        root = Tk()
        icon_path="speeds.ico"
        root.wm_iconbitmap(icon_path)
        root.title("ALTER YOUR TABLE")
        root.geometry('670x530')
        
        # Dropdown for selecting a database
        Label(root, text="Select Database:").pack()
        database_var1 = StringVar(root)
        database_dropdown = ttk.Combobox(root, textvariable=database_var1)
        database_dropdown["values"] = get_databases1()
        database_dropdown.pack()


        operation_var1 = Label(root,text='SELECT OPERATIONS')
        operation_var1.pack()
        operation_var = StringVar(root)
        operation_menu = ttk.Combobox(root, textvariable=operation_var)
        operation_menu['values'] = ["Add Column", "Modify Column", "Drop Column", "Rename Column", "Rename Table", "Add Primary Key", "Add Foreign Key"]
        operation_menu.pack()

        # Frame for dynamic fields
        dynamic_fields_frame = Frame(root)
        dynamic_fields_frame.pack()

        # Define entries (initially hidden)
        
        table_var = StringVar(dynamic_fields_frame)
        table_dropdown1 = ttk.Combobox(dynamic_fields_frame, textvariable=table_var)
        database_dropdown.bind("<<ComboboxSelected>>", on_database_select)

        column_name_entry = Entry(dynamic_fields_frame)
        column_type_entry = Entry(dynamic_fields_frame)
        old_column_name_entry = Entry(dynamic_fields_frame)
        new_column_name_entry = Entry(dynamic_fields_frame)
        new_table_name_entry = Entry(dynamic_fields_frame)
        ref_table_entry = Entry(dynamic_fields_frame)
        ref_column_entry = Entry(dynamic_fields_frame)

        # Update the fields when a new operation is selected
        operation_var.trace("w", display_fields)

        # Alter Table button
        Button(root, text="Alter Table", command=alter_table).pack()

        root.mainloop()
        




    ##################################################################################################################################################################################################
    ##################################################################################################################################################################################################
    #for creating table....##################################################################################################################################################################################################
    def createable():
        connection = c.connect(host='localhost', user='root', passwd=password)
        cursor = connection.cursor()
        cursor.execute('show databases')
        data=cursor.fetchall()
        databasess = [item[0] for item in data]  # Extract first element from each tuple
        
        databases = databasess
        default_host = "localhost"
        default_username = "root"
      

        #creating tables's query...
        def create_table():

            if host_entry.get() == '' or username_entry.get() == '' or password_entry.get() == '' or table_name_entry.get() == '' or num_columns_entry.get() == '':
                messagebox.showerror('ERROR','ENTRY FIELDS CANNOT BE EMPTY',parent=create_window)
                return
            else:
                host = host_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                table_name = table_name_entry.get()
                num_columns = int(num_columns_entry.get())
                
                try:    
                    sql = f"CREATE TABLE {table_name} ("
                    for i in range(num_columns):
                        data_type = data_type_entries[i].get()
                        column_name = column_name_entries[i].get()
                        sql += f"{column_name} {data_type},"
                    sql = sql[:-1] + ")"  # Remove trailing comma
                except IndexError as err:
                    messagebox.showerror('ERROR',f'{err}',parent=create_window)
                    return


                
                try:
                    connection = mysql.connector.connect(host=host, user=username, password=password, database=selected_database.get())
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    connection.commit()
                    
                    connection.close()
                    messagebox.showinfo('DONE',f"TABLE '{table_name}' CREATED SUCCESSFULLY IN DATABASE '{selected_database.get()}!'",parent=create_window)
                except mysql.connector.Error as err:
                    messagebox.showerror('ERROR',f"ERROR CREATING TABLE : {err}",parent=create_window)
                    return
                
        
        #adding coloumn fields.....
        def add_column_fields():
            if host_entry.get() == '' or username_entry.get() == '' or password_entry.get() == '' or table_name_entry.get() == '' or num_columns_entry.get() == '':
                messagebox.showerror('ERROR','ENTRY FIELDS CANNOT BE EMPTY',parent=create_window)
                return
            else:
                num_columns = int(num_columns_entry.get())

                # Clear existing column entry fields if any
                data_type_entries.clear()
                column_name_entries.clear()
                for widget in inner_frame.winfo_children():
                    widget.destroy()

                # Create frames and pack them horizontally for each column
                for i in range(num_columns):
                    row_frame = tk.Frame(inner_frame)
                    row_frame.pack(fill='x')

                    data_type_label = tk.Label(row_frame, text=f"Data Type (Column {i+1}):")
                    data_type_label.pack(side='left')
                    data_type_entry = tk.Entry(row_frame)
                    data_type_entry.pack(side='left')
                    data_type_entries.append(data_type_entry)

                    column_name_label = tk.Label(row_frame, text=f"Column Name (Column {i+1}):")
                    column_name_label.pack(side='left')
                    column_name_entry = tk.Entry(row_frame)
                    column_name_entry.pack(side='left')
                    column_name_entries.append(column_name_entry)

                # Update the scroll region
                column_frame.update_idletasks()
                column_frame.configure(scrollregion=column_frame.bbox(tk.ALL))

        # Create tk() for table creation
        create_window = tk.Tk()
        icon_path="speeds.ico"
        create_window.wm_iconbitmap(icon_path)
        create_window.title("TABLE CREATOR")
        create_window.geometry('670x530')
        
        
        '''bg_image = Image.open('bg3.jpg')
        bg2image = ImageTk.PhotoImage(bg_image)
        background_label = Label(create_window, image=bg2image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)'''
                                                                    


        # Database selection frame
        database_frame = tk.Frame(create_window)
        database_frame.pack(fill='x')  # Expand horizontally

        database_label = tk.Label(database_frame, text="SELECT DATABASE")
        database_label.pack(side='left')

        selected_database = tk.StringVar(create_window)
        # Set default selection

        database_dropdown = tk.OptionMenu(database_frame, selected_database, *databases)
        database_dropdown.pack(side='left')

        # Host, username, password entry fields
        host_label = tk.Label(create_window, text="DATABASE HOST")
        host_label.pack()
        host_entry = tk.Entry(create_window)
        host_entry.insert(0, default_host)  
        host_entry.pack()

        username_label = tk.Label(create_window, text="USERNAME")
        username_label.pack()
        username_entry = tk.Entry(create_window)
        username_entry.insert(0, default_username)
        username_entry.pack()

        password_label = tk.Label(create_window, text="PASSWORD")
        password_label.pack()
        password_entry = tk.Entry(create_window, show="*") 
        password_entry.pack()

        table_name_label = tk.Label(create_window, text="TABLE NAME")
        table_name_label.pack()
        table_name_entry = tk.Entry(create_window)
        table_name_entry.pack()

        num_columns_label = tk.Label(create_window, text="NUMBER OF COLUMNS")
        num_columns_label.pack()
        num_columns_entry = tk.Entry(create_window,validate='key',validatecommand=(create_window.register(lambda c: c.isdigit()), '%S'))
        num_columns_entry.pack()

        # Scrollable frame for column entries
        column_frame = tk.Canvas(create_window)
        column_frame.pack(fill=tk.BOTH, expand=True)  # Fill available space

        scrollbar = tk.Scrollbar(column_frame, orient='vertical', command=column_frame.yview)
        scrollbar.pack(side='right', fill='y')

        column_frame.configure(yscrollcommand=scrollbar.set)  # Link canvas and scrollbar
        inner_frame = tk.Frame(column_frame)

        column_frame.create_window((0, 0), window=inner_frame, anchor='nw')
        column_frame.configure(scrollregion=column_frame.bbox(tk.ALL))

        # Initialize lists for column entry widgets
        data_type_entries = []
        column_name_entries = []

        add_column_button = tk.Button(create_window, text="ADD COLUMN FIELDS", command=add_column_fields)
        add_column_button.pack()

        

        create_table_button = tk.Button(create_window, text="CREATE TABLE", command=create_table)
        create_table_button.pack()

        create_window.mainloop()



    ##################################################################################################################################################################################################
    ##################################################################################################################################################################################################
    ##################################################################################################################################################################################################
   
   
    #inserting data.......................................................................................................................
    def connect_to_db(database):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database=database

        )

    

    def get_table_columns(database, table_name):
        db = connect_to_db(database)
        cursor = db.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        cursor.close()
        db.close()
        return columns

    def insert_data(database, table_name, rows):
        db = connect_to_db(database)
        cursor = db.cursor()

        for column_values in rows:
            placeholders = ', '.join(['%s'] * len(column_values))
            columns = ', '.join(column_values.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            try:
                cursor.execute(sql, list(column_values.values()))
                db.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("ERROR", f"ERROR: {err}",parent=main_window)
                return
        messagebox.showinfo("SUCCESS", "DATA INSERTED SUCCESSFULLY",parent=main_window)
        try:
            sqp1=f'select *from {table_name}'
            cursor.execute(sqp1)
            myresult = cursor.fetchall()
            # Get column names
            column_names = [item[0] for item in cursor.description]
            ###################
            table_data = tabulate(myresult, headers=column_names, tablefmt="grid")
            db.close()


            # data retived  window #
            Wc = Tk()
            icon_path="speeds.ico"
            Wc.wm_iconbitmap(icon_path)
            nfn= table_var.get()
            Wc.title(nfn)
            
            Wc.resizable(True, True)  # Allow resizing
            Wc.wm_attributes('-topmost', True)

            # Create a text widget with scrollbars
            text_widget = tk.Text(Wc, wrap="none")
            text_widget.pack(fill="both", expand=True)


            # Create scrollbars
            yscrollbar = tk.Scrollbar(Wc, orient="vertical", command=text_widget.yview)
            yscrollbar.pack(side="right", fill="y")
            xscrollbar = tk.Scrollbar(Wc, orient="horizontal", command=text_widget.xview)
            xscrollbar.pack(side="bottom", fill="x")
            

            # Configure text widget to use scrollbars
            text_widget.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

            text_widget.insert("1.0", table_data)

            Wc.mainloop()
        except:
            messagebox.showerror("ERROR",'DATA NOT FOUND',parent=Wc)
            return
        cursor.close()
        db.close()
        


    def create_main_window():

        def connect_to_mysql():
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=password
                )
                return mydb
            except mysql.connector.Error as err:
                messagebox.showerror('ERROR',f"ERROR CONNECTING TO DATABASE:{err}",parent=main_window)
                return

        def get_databases():
            mydb = connect_to_mysql()
            if mydb is not None:
                cursor = mydb.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                cursor.close()
                mydb.close()
                return databases
            return []  # Return empty list if connection fails

        def get_and_populate_tables(database_name):
            mydb = connect_to_mysql()
            if mydb is not None:
                cursor = mydb.cursor()
                cursor.execute(f"USE {database_name}")
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                cursor.close()
                mydb.close()

                # Clear existing items in second dropdown
                table_dropdown.set(' ')  # Clear the selection (works for most Tkinter versions)

                # Populate second dropdown with tables
                table_dropdown['values'] = tables 
                
                 # Use the 'values' property
            else:
                messagebox.showerror('ERROR',"ERROR CONNECTING THE DATABSAE",parent=main_window)
                return
        

        def on_database_select(event):
            selected_database = database_var.get()
            
            if selected_database:
                get_and_populate_tables(selected_database)
                # Enable second dropdown for table selection
                table_dropdown.config(state='normal')

        

        def on():
            try:

                table_name=table_var.get()
                database=database_var.get()
                create_insert_fields(database,table_name)
            except:
                messagebox.showerror('ERROR','PLEASE SELECT BOTH DATABASE AND TABLE',parent=main_window)


                
        def create_insert_fields(database, table_name):
            
            for widget in entry_frame.winfo_children():
                widget.destroy()

            columns = get_table_columns(database, table_name)

            canvas = tk.Canvas(entry_frame)
            scrollbar_y = tk.Scrollbar(entry_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar_x = tk.Scrollbar(entry_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            for idx, column in enumerate(columns):
                col_name, col_type = column[0], column[1]
                tk.Label(scrollable_frame, text=col_name).grid(row=0, column=idx)
                tk.Label(scrollable_frame, text=col_type).grid(row=1, column=idx)

            rows = []
            
            def add_row():
                
                row_idx = len(rows) + 2
                entry_row = {}
            
                for idx, column in enumerate(columns):
                    entry = tk.Entry(scrollable_frame)
                    entry.grid(row=row_idx, column=idx)
                    entry_row[column[0]] = entry
                    
                rows.append(entry_row)
                
            def on_insert():
                all_values = []
                for row in rows:
                    column_values = {}
                    for col, entry in row.items():
                        value = entry.get()
                        if not value:  # Check if the entry is empty
                            messagebox.showerror("INPUT ERROR", "ALL FIELDS SHOULD NOT BE EMPTY",parent=main_window)
                            return
                        column_values[col] = value
                    all_values.append(column_values)
                insert_data(database, table_name, all_values)
                    
                
            add_row_button = tk.Button(scrollable_frame, text="ADD ROW", command=add_row)
            add_row_button.grid(row=2, column=len(columns))

            insert_button = tk.Button(scrollable_frame, text="INSERT DATA", command=on_insert)
            insert_button.grid(row=3, column=len(columns))

            add_row()

        global main_window
        main_window = tk.Tk()
        icon_path="speeds.ico"
        main_window.wm_iconbitmap(icon_path)
        main_window.title("INSERTING FUNCTION")
        main_window.geometry("800x600")

        #for retrival.....................
        databsebutton=Label(main_window,text='SELECT DATABASE')
        databsebutton.pack()

        database_var = StringVar(main_window)
        database_dropdown = ttk.Combobox(main_window, textvariable=database_var)
        database_dropdown["values"] = get_databases()
        database_dropdown.pack()

        tablebutton=Label(main_window,text='SELECT TABLE')
        tablebutton.pack()

        table_var = StringVar(main_window)
        table_dropdown = ttk.Combobox(main_window, textvariable=table_var)
        table_dropdown.pack()
        database_dropdown.bind("<<ComboboxSelected>>", on_database_select)
        
        #end ..............................

        select_button = tk.Button(main_window, text="SELECT TABLE", command=on)
        select_button.pack()

        entry_frame = tk.Frame(main_window)
        entry_frame.pack(fill=tk.BOTH, expand=True)

        main_window.mainloop()

        ##################################################################################################################
        ##################################################################################################################
        ##################################################################################################################
        ##################################################################################################################


    #retriving data....
    def dbentry():
        try:
            mydb = mysql.connector.connect(host="localhost",user="root",password=password)
            mc = mydb.cursor()
        except:
            messagebox.showerror("ERROR","DATABASE CONNECTIVITY ISSUE,PLS TRY AGAIN !!!")
            return
        dbe = database_var.get()
        try:
            mc.execute(f"use {dbe}")
        except Error as e:
            if e.errno == 1049:
                messagebox.showerror("ERROR",'DATABASE NOT FOUND')
                return

        tbe = table_var.get()
        try:
            mc.execute(f"SELECT * FROM {tbe}")
        except Error as e:
            if e.errno == 1146:
                messagebox.showerror("ERROR",f"NO TABLE NAMED '{tbe}'")
                return
        try:
            myresult = mc.fetchall()
            # Get column names
            column_names = [item[0] for item in mc.description]
            ###################
            table_data = tabulate(myresult, headers=column_names, tablefmt="grid")
            mydb.close()


            # data retived  window #
            Wc = Tk()
            icon_path="speeds.ico"
            Wc.wm_iconbitmap(icon_path)
            tnfn= table_var.get()
            Wc.title(tnfn)
            
            Wc.resizable(True, True)  # Allow resizing
            Wc.wm_attributes('-topmost', True)

            # Create a text widget with scrollbars
            text_widget = tk.Text(Wc, wrap="none")
            text_widget.pack(fill="both", expand=True)


            # Create scrollbars
            yscrollbar = tk.Scrollbar(Wc, orient="vertical", command=text_widget.yview)
            yscrollbar.pack(side="right", fill="y")
            xscrollbar = tk.Scrollbar(Wc, orient="horizontal", command=text_widget.xview)
            xscrollbar.pack(side="bottom", fill="x")
            

            # Configure text widget to use scrollbars
            text_widget.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

            text_widget.insert("1.0", table_data)

            Wc.mainloop()
        except:
            messagebox.showerror("ERROR",'DATA NOT FOUND')
            return




    root = Tk()
    root.title("MYSQL X PYTHON")
    icon_path="speeds.ico"
    root.wm_iconbitmap(icon_path)
    
    
    ####################
    #CANVAS'S
    ####################

    color_for_text='magenta'





    canvass = Canvas(root,width=1920,height=1079) 
    background=ImageTk.PhotoImage(file='bg.jpg')
    canvass.create_image(-50, -50, image=background, anchor="nw")
    
    
    #HEADINGS FOR ALL SECTION

    canvass.create_text(230,45,text='  THIS SECTION IS FOR \nRETIRIVING ALL THE DATA \nFROM THE SELECTED TABLE',font=('Courier',16,'bold'),fill=color_for_text)
    canvass.pack()

    canvass.create_text(580,45,text='  THIS SECTION IS FOR \nRETIRIVING ALL THE DATA \nFROM THE SELECTED TABLE',font=('Courier',16,'bold'),fill=color_for_text)
    canvass.pack()

    canvass.create_text(965,45,text='  THIS SECTION IS FOR \nRETIRIVING ALL THE DATA \nFROM THE SELECTED TABLE',font=('Courier',16,'bold'),fill=color_for_text)
    canvass.pack()


    canvass.create_text(1320,45,text='  THIS SECTION IS FOR \nRETIRIVING ALL THE DATA \nFROM THE SELECTED TABLE',font=('Courier',16,'bold'),fill=color_for_text)
    canvass.pack()

    canvass.create_text(225,542,text='THIS SECTION IS FOR \n  CREATING A TABLE, \nCLICK ON CREATE TABLE',font=('Courier',16,'bold'),fill=color_for_text)
    canvass.pack()


    #MAIN WINDOWS'S LABLES

    color_for_text1='yellow'


    canvass.create_text(220,112,text='SELECT DATABASE',font=('times',12,'bold'),fill=color_for_text1)
    canvass.pack()
    canvass.create_text(220,264,text='SELECT TABLE',font=('times',12,'bold'),fill=color_for_text1)
    canvass.pack()

    ######################
    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the root window size based on the screen dimensions
    root.geometry(f"{screen_width}x{screen_height}")

    # Set the frame color
    color = 'yellow'

    # Function to create vertical frames
    def create_vertical_frames(relative_x_positions, width_ratio=0.005, height_ratio=1):
        for x_ratio in relative_x_positions:
            x_position = int(screen_width * x_ratio)
            frame_width = int(screen_width * width_ratio)
            frame_height = int(screen_height * height_ratio)
            Frame(root, width=frame_width, height=frame_height, bg=color).place(x=x_position)

    # Function to create horizontal frames
    def create_horizontal_frames(relative_y_positions, start_x_ratio, width_ratio, height_ratio=0.005):
        for y_ratio in relative_y_positions:
            y_position = int(screen_height * y_ratio)
            x_position = int(screen_width * start_x_ratio)
            frame_width = int(screen_width * width_ratio)
            frame_height = int(screen_height * height_ratio)
            Frame(root, width=frame_width, height=frame_height, bg=color).place(x=x_position, y=y_position)

    # Vertical frames (x positions as a ratio of screen width)
    vertical_positions = [0.03, 0.26, 0.27, 0.49, 0.53, 0.75, 0.76, 0.98]
    create_vertical_frames(vertical_positions)

    # Horizontal frames (y positions as a ratio of screen height)
    horizontal_positions_top = [0.08]  # Single row for the top
    horizontal_positions_bottom = [0.5, 0.58]  # Rows for the bottom
    create_horizontal_frames(horizontal_positions_top, start_x_ratio=0.03, width_ratio=0.23)
    create_horizontal_frames(horizontal_positions_top, start_x_ratio=0.27, width_ratio=0.22)
    create_horizontal_frames(horizontal_positions_top, start_x_ratio=0.53, width_ratio=0.22)
    create_horizontal_frames(horizontal_positions_top, start_x_ratio=0.76, width_ratio=0.22)
    create_horizontal_frames(horizontal_positions_bottom, start_x_ratio=0.03, width_ratio=0.23)
    create_horizontal_frames(horizontal_positions_bottom, start_x_ratio=0.27, width_ratio=0.22)

    # Horizontal frame at the very top
    Frame(root, width=screen_width, height=5, bg=color).place(x=0, y=0)



    #FULLSCREEN FEATURE & EXTING FEATURE############################################

    root.state('zoomed')


    def toggle_fullscreen(event=None):
        state = not root.attributes('-fullscreen')
        root.attributes('-fullscreen', state)

    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)


    # Set the window to open in full-screen mode
    root.attributes('-fullscreen', True)

    # Bind the Escape key to exit full-screen mode
    root.bind('<Escape>', end_fullscreen)

    # Optionally, you can bind F11 to toggle full-screen mode on and off
    root.bind('<F11>', toggle_fullscreen)


    def exit_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        hide_exit_button()

    def show_exit_button(event=None):
        if root.attributes('-fullscreen') and event.y <= 1 and event.y_root <= 5:
            animate_button_show()

    def hide_exit_button(event=None):
        exit_button.place_forget()

    def animate_button_show():
        y_position = -30
        target_y_position = 10
        exit_button.lift()

        def slide_down():
            nonlocal y_position
            if y_position < target_y_position:
                y_position += 2
                exit_button.place(x=(root.winfo_width() - exit_button.winfo_width()) // 2, y=y_position)
                root.after(10, slide_down)
            else:
                root.after(1000, slide_up_button)  # Wait 1 second before starting slide up

        slide_down()

    def slide_up_button():
        y_position = 10
        target_y_position = -30

        def slide_up():
            nonlocal y_position
            if y_position > target_y_position:
                y_position -= 2
                exit_button.place(x=(root.winfo_width() - exit_button.winfo_width()) // 2, y=y_position)
                root.after(10, slide_up)
            else:
                hide_exit_button()

        slide_up()

    # Create an exit button, initially hidden
    exit_button = tk.Button(root, text="X",width=4,command=exit_fullscreen, bg="red", fg="white")
    exit_button.place_forget()

    # Bind the motion event to show the exit button when the mouse is at the top
    root.bind('<Motion>', show_exit_button)

    #FULLSCREEN FEATURES ENDING ##############################################



    def update():
        def start_marquee(direction):
            x, y = canvas.coords(text_id)
            if direction == 'left':
                canvas.move(text_id, -2, 0)
                if x < -canvas.bbox(text_id)[2]:  # If the text is completely off the canvas on the left
                    direction = 'right'
            else:
                canvas.move(text_id, 2, 0)
                if x > canvas.winfo_width():  # If the text is completely off the canvas on the right
                    direction = 'left'
            canvas.after(10, start_marquee, direction)  # Schedule this function to run again after 50ms with the new direction

        #updates...........
        moot = Tk()
        icon_path="speeds.ico"
        moot.wm_iconbitmap(icon_path)
        moot.title("updates comming....")
        moot.resizable(False,False)
        # Create a canvas widget
        canvas = tk.Canvas(moot, width=400, height=50)
        canvas.pack()

        # Add the text to the canvas
        text_id = canvas.create_text(canvas.winfo_width(), 25, text="WILL BE UPDATED SOON...", font=('Helvetica', 20), fill='black')

        # Start the marquee
        start_marquee('left')

        # Run the tkinter event loop
        moot.mainloop()
    
    #######################
    #select * from all
    #######################
    def connect_to_mysql():
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password
            )
            return mydb
        except mysql.connector.Error as err:
            messagebox.showerror('ERROR',f"ERROR CONNECTING TO DATABASE:{err}")
            return
        



    def get_databases():
        mydb = connect_to_mysql()
        if mydb is not None:
            cursor = mydb.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [row[0] for row in cursor.fetchall()]
            cursor.close()
            mydb.close()
            return databases
        return []  # Return empty list if connection fails

    def get_and_populate_tables(database_name):
        mydb = connect_to_mysql()
        if mydb is not None:
            cursor = mydb.cursor()
            cursor.execute(f"USE {database_name}")
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            mydb.close()

            # Clear existing items in second dropdown
            table_dropdown.set(' ')  # Clear the selection (works for most Tkinter versions)

            # Populate second dropdown with tables
            table_dropdown['values'] = tables  # Use the 'values' property
        else:
            messagebox.showerror('ERROR',"ERROR CONNECTING THE DATABSAE")
            return

    def on_database_select(event):
        selected_database = database_var.get()
        
        if selected_database:
            get_and_populate_tables(selected_database)
            # Enable second dropdown for table selection
            table_dropdown.config(state='normal')
   



    #for retrival.....................
    database_var = StringVar(root)
    database_dropdown = ttk.Combobox(root, textvariable=database_var)
    database_dropdown["values"] = get_databases()
    database_dropdown.place(x=130,y=125)


    table_var = StringVar(root)
    table_dropdown = ttk.Combobox(root, textvariable=table_var, state='disabled')
    table_dropdown.place(x=130,y=275)
    database_dropdown.bind("<<ComboboxSelected>>", on_database_select)
    
    #end ..............................



    ###################
    #ENTRIES
    ###################

    #not DESIDED entries...............
    dbn =Entry(root, width=30)
    dbn.place(x=455,y=100)

    tbn=Entry(root,width=30)
    tbn.place(x=455,y=150)

    runtime=Entry(root,width=30)
    runtime.place(x=455,y=200)

    abetry =Entry(root, width=30)
    abetry.place(x=836,y=100)

    vbetry =Entry(root, width=30)
    vbetry.place(x=1192,y=100)
    #end..............................


    #######################
    #BUTTTONS
    #######################

    # retival button...................
    allbutton =Button(root,text='SUBMIT',width=10,font=('Open Sans',19,'bold'),bd=2,bg='red',fg='white',cursor='hand2',activeforeground='purple',activebackground='purple',command=dbentry)
    allbutton.place(x=143,y=350)

    # end..............................


    #creation buttons..................
    creatbutton=Button(root,text='CREATE TABLE',width=15,font=('Open Sans',15,'bold'),bd=2,bg='red',fg='white',cursor='hand2',activeforeground='purple',activebackground='purple',command=createable)
    creatbutton.place(x=130,y=650)

    #end...............................


    #data insertion button.............
    insertbutton=Button(root,text='INSERT DATA',width=15,font=('Open Sans',15,'bold'),bd=2,bg='red',fg='white',cursor='hand2',activeforeground='purple',activebackground='purple',command=create_main_window)
    insertbutton.place(x=130,y=750)

    #end...............................

    
    #data altering button..............
    alterbutton=Button(root,text='ALTER TABLE',width=15,font=('Open Sans',15,'bold'),bd=2,bg='red',fg='white',cursor='hand2',activeforeground='purple',activebackground='purple',command=ALTER)
    alterbutton.place(x=480,y=650)
    #end...............................



    # own query button.................
    ownquery=Button (root,text='WRITE YOUR OWN QUERY',font=('Open Sans',10,'bold'),bd=2,bg='red',fg='white',cursor='hand2',activeforeground='purple',activebackground='purple',command=update)
    ownquery.place(x=120,y=450)
    #end..............................

   


    # Run the main loop
    root.mainloop()




password='yogi the don 1.555'

akk()




'''






def fn():
    host1 = host.get()
    user1 = user.get()
    passwd1 = passwd.get() 
    global password
    password=passwd1
    try:
        con = c.connect(host=host1, user=user1, passwd=passwd1)
        if con.is_connected():
            sk.destroy()
            akk()
        else:
            sk.destroy()
    except Exception as err:
        messagebox.showerror("Error", str(err))
        sk.destroy()


sk = Tk()
icon_path="speeds.ico"
sk.wm_iconbitmap(icon_path)
sk.geometry('+630+410')
sk.resizable(False, False)
sk.lift()

hostlable = Label(sk, text='HOST')
hostlable.pack()
host = Entry(sk, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='violetred1')
host.insert(0,'localhost')  
host.pack()
userlable = Label(sk, text='USER')
userlable.pack()
user = Entry(sk, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='violetred1')
user.insert(0,'root')
user.pack()

passwordlable = Label(sk, text='PASSWORD')
passwordlable.pack()
passwd = Entry(sk, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='violetred1', show='*')
passwd.pack()

butt = Button(sk, text='SUBMIT', width=8, font=('Open Sans', 19, 'bold'), bd=2, bg='purple', cursor='hand2', fg='violetred', activeforeground='purple', activebackground='purple', command=fn)
butt.pack(pady=10)


sk.mainloop()
'''
