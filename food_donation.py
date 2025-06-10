import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class FoodApp:
    def __init__(self, master):
        self.master = master
        master.title("Food Management System")
        master.geometry("900x600")

        # Database connection (update credentials)
        try:
            self.conn = mysql.connector.connect(
                host='Neha',
                user='nehaaaa',
                password='Neha@123',
                database='food'
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Cannot connect to database:\n{err}")
            master.destroy()
            return

        # Sidebar
        sidebar = tk.Frame(master, width=200, bg='lightgray')
        sidebar.pack(side='left', fill='y')
        self.content = tk.Frame(master)
        self.content.pack(side='right', fill='both', expand=True)

        # Sidebar buttons
        tk.Button(sidebar, text="Donors", width=20, command=self.show_donors).pack(pady=5)
        tk.Button(sidebar, text="Receivers", width=20, command=self.show_receivers).pack(pady=5)
        tk.Button(sidebar, text="Food Items", width=20, command=self.show_food_items).pack(pady=5)
        tk.Button(sidebar, text="Pickup Requests", width=20, command=self.show_pickups).pack(pady=5)
        tk.Button(sidebar, text="Feedback", width=20, command=self.show_feedback).pack(pady=5)
        tk.Button(sidebar, text="Delivery Staff", width=20, command=self.show_staff).pack(pady=5)
        tk.Label(sidebar, text="Views", bg='lightgray').pack(pady=(20,0))
        tk.Button(sidebar, text="Available Food", width=20, command=self.show_available_food).pack(pady=5)
        tk.Button(sidebar, text="Pending Pickups", width=20, command=self.show_pending_pickups).pack(pady=5)
        tk.Button(sidebar, text="Feedback Summary", width=20, command=self.show_feedback_summary).pack(pady=5)
        tk.Label(sidebar, text="Actions", bg='lightgray').pack(pady=(20,0))
        tk.Button(sidebar, text="Mark Donated", width=20, command=self.mark_donated).pack(pady=5)
        tk.Button(sidebar, text="Assign Staff", width=20, command=self.assign_staff).pack(pady=5)
        tk.Button(sidebar, text="Mark Delivered", width=20, command=self.mark_delivered).pack(pady=5)

        self.clear_content()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def create_table(self, columns, headings, title=None):
        self.clear_content()
        if title:
            tk.Label(self.content, text=title, font=('Arial',14)).pack(pady=10)
        tree = ttk.Treeview(self.content, columns=columns, show='headings')
        for c,h in zip(columns, headings):
            tree.heading(c, text=h)
            tree.column(c, width=100)
        tree.pack(fill='both', expand=True)
        return tree

    def fetch_and_populate(self, tree, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)
            return
        for r in rows:
            tree.insert('', 'end', values=r)

    # --- Donors ---
    def show_donors(self):
        cols = ("donor_id","name","contact_info","donor_type")
        tree = self.create_table(cols, ["ID","Name","Contact","Type"], "Donors")
        self.fetch_and_populate(tree, "SELECT donor_id,name,contact_info,donor_type FROM donor")
        tk.Button(self.content, text="Add Donor", command=self.add_donor).pack(pady=5)

    def add_donor(self):
        win = tk.Toplevel(self.master); win.title("Add Donor")
        labels = ["Donor ID","Name","Contact Info","Donor Type"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                did = int(entries[0].get())
                name = entries[1].get().strip()
                contact = entries[2].get().strip()
                dtype = entries[3].get().strip()
                if not name or not contact or not dtype:
                    raise ValueError("All fields required")
                self.cursor.execute(
                    "INSERT INTO donor(donor_id,name,contact_info,donor_type) VALUES(%s,%s,%s,%s)",
                    (did,name,contact,dtype))
                self.conn.commit()
                win.destroy(); self.show_donors()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Receivers ---
    def show_receivers(self):
        cols = ("receiver_id","name","contact_info","location")
        tree = self.create_table(cols, ["ID","Name","Contact","Location"], "Receivers")
        self.fetch_and_populate(tree, "SELECT receiver_id,name,contact_info,location FROM receiver")
        tk.Button(self.content, text="Add Receiver", command=self.add_receiver).pack(pady=5)

    def add_receiver(self):
        win = tk.Toplevel(self.master); win.title("Add Receiver")
        labels = ["Receiver ID","Name","Contact Info","Location"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                rid = int(entries[0].get())
                name = entries[1].get().strip()
                contact = entries[2].get().strip()
                loc = entries[3].get().strip()
                if not name or not contact or not loc:
                    raise ValueError("All fields required")
                self.cursor.execute(
                    "INSERT INTO receiver(receiver_id,name,contact_info,location) VALUES(%s,%s,%s,%s)",
                    (rid,name,contact,loc))
                self.conn.commit()
                win.destroy(); self.show_receivers()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Food Items ---
    def show_food_items(self):
        cols = ("food_id","donor_id","item_name","quantity","expiry_time","status")
        tree = self.create_table(cols, ["ID","Donor","Item","Qty","Expiry","Status"], "Food Items")
        self.fetch_and_populate(tree,
            "SELECT food_id,donor_id,item_name,quantity,expiry_time,status FROM food_item")
        tk.Button(self.content, text="Add Food Item", command=self.add_food_item).pack(pady=5)

    def add_food_item(self):
        win = tk.Toplevel(self.master); win.title("Add Food Item")
        labels = ["Food ID","Donor ID","Item Name","Quantity","Expiry (YYYY-MM-DD HH:MM:SS)","Status"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                fid = int(entries[0].get())
                did = int(entries[1].get())
                item = entries[2].get().strip()
                qty = int(entries[3].get())
                exp = entries[4].get().strip()
                stat = entries[5].get().strip()
                if not item or not exp or not stat:
                    raise ValueError("All fields required")
                self.cursor.execute(
                    "INSERT INTO food_item(food_id,donor_id,item_name,quantity,expiry_time,status) "
                    "VALUES(%s,%s,%s,%s,%s,%s)",
                    (fid,did,item,qty,exp,stat))
                self.conn.commit()
                win.destroy(); self.show_food_items()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Pickup Requests ---
    def show_pickups(self):
        cols = ("pickup_id","food_id","receiver_id","pickup_time","delivery_time","status","delivery_staff_id")
        tree = self.create_table(cols,
            ["ID","Food","Receiver","Picked At","Delivered At","Status","Staff ID"],
            "Pickup Requests")
        self.fetch_and_populate(tree,
            "SELECT pickup_id,food_id,receiver_id,pickup_time,delivery_time,status,delivery_staff_id FROM pickup_request")
        tk.Button(self.content, text="Add Pickup Request", command=self.add_pickup).pack(pady=5)

    def add_pickup(self):
        win = tk.Toplevel(self.master); win.title("Add Pickup Request")
        labels = ["Pickup ID","Food ID","Receiver ID","Status","Delivery Staff ID (opt)"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                pid = int(entries[0].get())
                fid = int(entries[1].get())
                rid = int(entries[2].get())
                stat = entries[3].get().strip() or "Pending"
                staff = entries[4].get().strip()
                staff_id = int(staff) if staff else None
                self.cursor.execute(
                    "INSERT INTO pickup_request(pickup_id,food_id,receiver_id,status,delivery_staff_id) "
                    "VALUES(%s,%s,%s,%s,%s)",
                    (pid,fid,rid,stat,staff_id))
                self.conn.commit()
                # assigned_deliveries increments via trigger or manual procedure as per your schema
                win.destroy(); self.show_pickups()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Feedback ---
    def show_feedback(self):
        cols = ("feedback_id","food_id","receiver_id","rating","comments")
        tree = self.create_table(cols, ["ID","Food","Receiver","Rating","Comments"], "Feedback")
        self.fetch_and_populate(tree,
            "SELECT feedback_id,food_id,receiver_id,rating,comments FROM feedback")
        tk.Button(self.content, text="Add Feedback", command=self.add_feedback).pack(pady=5)

    def add_feedback(self):
        win = tk.Toplevel(self.master); win.title("Add Feedback")
        labels = ["Feedback ID","Food ID","Receiver ID","Rating (1-5)","Comments"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                fid = int(entries[0].get())
                food = int(entries[1].get())
                recv = int(entries[2].get())
                rating = int(entries[3].get())
                com = entries[4].get().strip()
                if rating<1 or rating>5:
                    raise ValueError("Rating 1-5")
                self.cursor.execute(
                    "INSERT INTO feedback(feedback_id,food_id,receiver_id,rating,comments) "
                    "VALUES(%s,%s,%s,%s,%s)",
                    (fid,food,recv,rating,com))
                self.conn.commit()
                win.destroy(); self.show_feedback()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Delivery Staff ---
    def show_staff(self):
        cols = ("staff_id","name","contact_info","assigned_deliveries")
        tree = self.create_table(cols, ["ID","Name","Contact","Assigned"], "Delivery Staff")
        self.fetch_and_populate(tree,
            "SELECT staff_id,name,contact_info,assigned_deliveries FROM delivery_staff")
        tk.Button(self.content, text="Add Staff", command=self.add_staff).pack(pady=5)

    def add_staff(self):
        win = tk.Toplevel(self.master); win.title("Add Delivery Staff")
        labels = ["Staff ID","Name","Contact Info"]
        entries = []
        for i,lab in enumerate(labels):
            tk.Label(win, text=lab).grid(row=i,column=0,padx=10,pady=5)
            e = tk.Entry(win); e.grid(row=i,column=1,padx=10,pady=5)
            entries.append(e)
        def save():
            try:
                sid = int(entries[0].get())
                name = entries[1].get().strip()
                contact = entries[2].get().strip()
                if not name or not contact:
                    raise ValueError("All fields required")
                self.cursor.execute(
                    "INSERT INTO delivery_staff(staff_id,name,contact_info) VALUES(%s,%s,%s)",
                    (sid,name,contact))
                self.conn.commit()
                win.destroy(); self.show_staff()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(win, text="Save", command=save).grid(row=len(labels),column=0,columnspan=2,pady=10)

    # --- Views ---
    def show_available_food(self):
        cols = ("food_id","item_name","quantity","expiry_time","donor_name")
        tree = self.create_table(cols, ["ID","Item","Qty","Expiry","Donor"], "Available Food")
        self.fetch_and_populate(tree, "SELECT * FROM available_food")

    def show_pending_pickups(self):
        cols = ("pickup_id","item_name","receiver_name","pickup_time","status")
        tree = self.create_table(cols, ["ID","Item","Receiver","Picked At","Status"], "Pending Pickups")
        self.fetch_and_populate(tree, "SELECT * FROM pending_pickups")

    def show_feedback_summary(self):
        cols = ("feedback_id","item_name","receiver_name","rating","comments")
        tree = self.create_table(cols, ["ID","Item","Receiver","Rating","Comments"], "Feedback Summary")
        self.fetch_and_populate(tree, "SELECT * FROM feedback_summary")

    # --- Actions ---
    def mark_donated(self):
        self.clear_content()
        tk.Label(self.content, text="Mark Food Donated", font=('Arial',14)).pack(pady=10)
        tk.Label(self.content, text="Food ID:").pack()
        eid = tk.Entry(self.content); eid.pack(pady=5)
        def go():
            try:
                fid = int(eid.get())
                self.cursor.execute("UPDATE food_item SET status='donated' WHERE food_id=%s", (fid,))
                self.conn.commit()
                messagebox.showinfo("Done", "Food marked donated")
                self.show_food_items()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(self.content, text="Mark", command=go).pack(pady=10)

    def assign_staff(self):
        self.clear_content()
        tk.Label(self.content, text="Assign Delivery Staff", font=('Arial',14)).pack(pady=10)
        tk.Label(self.content, text="Pickup ID:").pack()
        pid = tk.Entry(self.content); pid.pack(pady=5)
        tk.Label(self.content, text="Staff ID:").pack()
        sid = tk.Entry(self.content); sid.pack(pady=5)
        def go():
            try:
                p = int(pid.get()); s = int(sid.get())
                self.cursor.execute("UPDATE pickup_request SET delivery_staff_id=%s WHERE pickup_id=%s", (s,p))
                self.cursor.execute("UPDATE delivery_staff SET assigned_deliveries=assigned_deliveries+1 WHERE staff_id=%s", (s,))
                self.conn.commit()
                messagebox.showinfo("Done", "Staff assigned")
                self.show_pickups()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(self.content, text="Assign", command=go).pack(pady=10)

    def mark_delivered(self):
        self.clear_content()
        tk.Label(self.content, text="Mark Delivered", font=('Arial',14)).pack(pady=10)
        tk.Label(self.content, text="Pickup ID:").pack()
        pid = tk.Entry(self.content); pid.pack(pady=5)
        def go():
            try:
                p = int(pid.get())
                self.cursor.execute("UPDATE pickup_request SET delivery_time=CURRENT_TIMESTAMP, status='Delivered' WHERE pickup_id=%s", (p,))
                self.conn.commit()
                messagebox.showinfo("Done", "Marked Delivered")
                self.show_pickups()
            except Exception as e:
                messagebox.showerror("Error", e)
        tk.Button(self.content, text="Mark Delivered", command=go).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()
