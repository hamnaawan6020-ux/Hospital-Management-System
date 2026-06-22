import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image, ImageTk

# ================== THEME & DATABASE ==================
THEME = {
    "primary_brown": "#4E342E",
    "sidebar_beige": "#D7CCC8",
    "bg_cream": "#EFEBE9",
    "header_accent": "#795548",
    "zebra_even": "#D7CCC8",
    "zebra_odd": "#FFFFFF",
    "font_main": ("Segoe UI", 10)
}

def init_db():
    conn = sqlite3.connect("hospital_pro.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age TEXT, disease TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS doctors(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, spec TEXT, fee INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY AUTOINCREMENT, p_name TEXT, d_name TEXT, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS billing(id INTEGER PRIMARY KEY AUTOINCREMENT, p_name TEXT, amount TEXT, status TEXT)")
    
    try:
        c.execute("SELECT fee FROM doctors LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE doctors ADD COLUMN fee INTEGER DEFAULT 0")
        
    conn.commit()
    return conn

db_conn = init_db()

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CarePoint Pro | Healthcare Management")
        self.root.state('zoomed') 
        self.show_login()

    def show_login(self):
        for w in self.root.winfo_children(): w.destroy()
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        try:
            self.root.update()
            img = Image.open("hospital_bg.jpg").resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except:
            self.canvas.configure(bg=THEME["primary_brown"])

        card = tk.Frame(self.canvas, bg="white", padx=45, pady=45)
        self.canvas.create_window(self.root.winfo_width()//2, self.root.winfo_height()//2, window=card)
        
        tk.Label(card, text="CAREPOINT 🏥", font=("Segoe UI", 26, "bold"), bg="white", fg=THEME["primary_brown"]).pack()
        self.u = tk.Entry(card, font=THEME["font_main"], width=30, bg="#F5F5F5", relief="flat")
        self.u.pack(pady=10, ipady=8); self.u.insert(0, "DSA_PROJECT")
        self.p = tk.Entry(card, show="*", font=THEME["font_main"], width=30, bg="#F5F5F5", relief="flat")
        self.p.pack(pady=10, ipady=8); self.p.insert(0, "09871234")
        tk.Button(card, text="SIGN IN", bg=THEME["primary_brown"], fg="white", font=("Segoe UI", 10, "bold"), width=25, command=self.dashboard).pack(pady=20, ipady=5)

    def dashboard(self):
        for w in self.root.winfo_children(): w.destroy()
        side = tk.Frame(self.root, bg=THEME["sidebar_beige"], width=220)
        side.pack(side="left", fill="y")
        tk.Label(side, text="CP HEALTH", font=("Impact", 22), bg=THEME["sidebar_beige"], fg=THEME["primary_brown"]).pack(pady=40)
        
        menu = [("Patients", self.view_patients), ("Doctors", self.view_doctors), 
                ("Schedules", self.view_appointments), ("Billing", self.view_billing), ("Logout", self.show_login)]
        
        for t, c in menu:
            tk.Button(side, text=f"  {t.upper()}", font=("Segoe UI", 9, "bold"), bg=THEME["sidebar_beige"], 
                      fg=THEME["primary_brown"], relief="flat", pady=15, anchor="w", command=c).pack(fill="x")

        self.main = tk.Frame(self.root, bg=THEME["bg_cream"], padx=25, pady=25)
        self.main.pack(side="right", expand=True, fill="both")
        self.view_patients()

    def get_list(self, table):
        cursor = db_conn.execute(f"SELECT name FROM {table}")
        return [row[0] for row in cursor.fetchall()]

    def create_table(self, title, cols, query, table_name):
        for w in self.main.winfo_children(): w.destroy()
        tk.Label(self.main, text=title, font=("Segoe UI Semibold", 18), bg=THEME["bg_cream"], fg=THEME["primary_brown"]).pack(anchor="w", pady=(0, 15))

        entry_bar = tk.LabelFrame(self.main, text="New Entry", bg="white", font=("Segoe UI", 9, "bold"), padx=15, pady=15)
        entry_bar.pack(fill="x", pady=(0, 20))

        self.inputs = {}
        input_cols = cols[1:] 
        
        for c in input_cols:
            f = tk.Frame(entry_bar, bg="white")
            f.pack(side="left", padx=10)
            tk.Label(f, text=c.upper(), font=("Segoe UI", 7, "bold"), bg="white", fg="#8D6E63").pack(anchor="w")
            
            if (table_name in ["billing", "appointments"] and c in ["Patient", "Doctor"]):
                dropdown_vals = self.get_list("patients") if c == "Patient" else self.get_list("doctors")
                e = ttk.Combobox(f, values=dropdown_vals, font=THEME["font_main"], width=20, state="readonly")
            elif c == "Status":
                e = ttk.Combobox(f, values=["Paid", "Pending", "Cancelled"], font=THEME["font_main"], width=20, state="readonly")
            elif c == "Date":
                e = DateEntry(f, width=19, background=THEME["primary_brown"], foreground='white', borderwidth=2)
            else:
                e = tk.Entry(f, bg="#F5F5F5", relief="flat", font=THEME["font_main"], width=22)
            
            e.pack(ipady=3 if isinstance(e, tk.Entry) else 0, pady=2)
            self.inputs[c] = e

        def save_entry():
            vals = [self.inputs[c].get() for c in input_cols]
            if not all(vals):
                messagebox.showwarning("Incomplete", "Required fields missing.")
                return
            
            col_map = {
                "patients": "name, age, disease", "doctors": "name, spec, fee",
                "appointments": "p_name, d_name, date", "billing": "p_name, amount, status"
            }
            try:
                db_conn.execute(f"INSERT INTO {table_name} ({col_map[table_name]}) VALUES (?, ?, ?)", vals)
                db_conn.commit()
                getattr(self, f"view_{table_name}")() 
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {e}")

        tk.Button(entry_bar, text="SAVE", bg=THEME["header_accent"], fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=30, command=save_entry).pack(side="right", padx=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=THEME["font_main"])
        style.configure("Treeview.Heading", background=THEME["sidebar_beige"], font=("Segoe UI", 9, "bold"))
        
        tree = ttk.Treeview(self.main, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.upper()); tree.column(c, anchor="center")
        
        tree.tag_configure('even', background=THEME["zebra_even"])
        tree.tag_configure('odd', background=THEME["zebra_odd"])
        tree.pack(fill="both", expand=True)

        rows = db_conn.execute(query).fetchall()
        for i, row in enumerate(rows):
            tree.insert("", "end", values=row, tags=('even' if i % 2 == 0 else 'odd'))
        return tree

    def view_patients(self):
        tree = self.create_table("PATIENTS", ("ID", "Name", "Age", "Diagnosis"), "SELECT * FROM patients", "patients")
        self.add_action_btns(tree, "patients", self.view_patients)
        # Add the 'Export All' button specifically for patients
        self.add_export_all_btn()

    def view_doctors(self):
        tree = self.create_table("DOCTORS", ("ID", "Name", "Spec", "Fee"), "SELECT * FROM doctors", "doctors")
        self.add_action_btns(tree, "doctors", self.view_doctors)

    def view_appointments(self):
        tree = self.create_table("SCHEDULES", ("ID", "Patient", "Doctor", "Date"), "SELECT * FROM appointments", "appointments")
        self.add_action_btns(tree, "appointments", self.view_appointments)

    def view_billing(self):
        tree = self.create_table("BILLING", ("ID", "Patient", "Amount", "Status"), "SELECT * FROM billing", "billing")
        self.add_action_btns(tree, "billing", self.view_billing)

    def add_action_btns(self, tree, table, refresh):
        self.btn_frame = tk.Frame(self.main, bg=THEME["bg_cream"])
        self.btn_frame.pack(fill="x", pady=15)
        
        tk.Button(self.btn_frame, text="🗑 DELETE", bg="#A1887F", fg="white", relief="flat", 
                  command=lambda: self.delete_record(tree, table, refresh), padx=20).pack(side="left")
        
        tk.Button(self.btn_frame, text="📄 SINGLE PDF", bg=THEME["primary_brown"], fg="white", relief="flat", 
                  command=lambda: self.gen_pdf_logic(tree), padx=20).pack(side="left", padx=10)

    def add_export_all_btn(self):
        """Adds a button to export all patient records to PDF."""
        tk.Button(self.btn_frame, text="📂 EXPORT ALL PATIENTS", bg=THEME["header_accent"], fg="white", relief="flat", 
                  command=self.export_all_patients_pdf, padx=20).pack(side="right")

    def delete_record(self, tree, table, refresh):
        sel = tree.focus()
        if sel:
            item_id = tree.item(sel, 'values')[0]
            db_conn.execute(f"DELETE FROM {table} WHERE id=?", (item_id,))
            db_conn.commit()
            refresh()

    def export_all_patients_pdf(self):
        """Fetches all patient data and generates a professional registry PDF."""
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="All_Patients_Registry.pdf")
        if not save_path: return

        try:
            cursor = db_conn.execute("SELECT * FROM patients")
            all_patients = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        doc = SimpleDocTemplate(save_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Styles
        title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=20, textColor=colors.HexColor(THEME["primary_brown"]), spaceAfter=12)
        sub_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=1)

        # Content
        elements.append(Paragraph("CAREPOINT HEALTHCARE", title_style))
        elements.append(Paragraph("Full Patient Registry Report", sub_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Table Data
        data = [["ID", "NAME", "AGE", "DIAGNOSIS"]]
        for p in all_patients:
            data.append([str(p[0]), str(p[1]), str(p[2]), str(p[3])])

        table = Table(data, colWidths=[40, 140, 60, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(THEME["primary_brown"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor(THEME["zebra_even"]), colors.white]),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8)
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("__________________________", styles['Normal']))
        elements.append(Paragraph("Authorized Administrator Signature", styles['Normal']))

        try:
            doc.build(elements)
            messagebox.showinfo("Success", "Full Patient Registry PDF Saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not create PDF: {e}")

    def gen_pdf_logic(self, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selection", "Please select a record first.")
            return
            
        record_values = tree.item(sel, 'values')
        column_names = tree.cget('columns')
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"Report_{record_values[1]}.pdf")
        
        if save_path:
            doc = SimpleDocTemplate(save_path, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=22, textColor=colors.HexColor(THEME["primary_brown"]), spaceAfter=10)
            sub_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=1)

            elements.append(Paragraph("CAREPOINT HEALTHCARE", title_style))
            elements.append(Paragraph("Official Electronic Medical Record", sub_style))
            elements.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 20))

            data = [["FIELD NAME", "RECORD DETAILS"]]
            for i in range(len(column_names)):
                data.append([column_names[i].upper(), str(record_values[i])])

            table = Table(data, colWidths=[160, 280])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(THEME["primary_brown"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor(THEME["zebra_even"]), colors.white]),
                ('PADDING', (0, 0), (-1, -1), 10)
            ]))
            elements.append(table)

            elements.append(Spacer(1, 40))
            elements.append(Paragraph("__________________________", styles['Normal']))
            elements.append(Paragraph("Authorized Medical Registrar Signature", styles['Normal']))
            
            try:
                doc.build(elements)
                messagebox.showinfo("Success", "Professional PDF has been saved.")
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to save PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
#pip install tkcalendar
#pip install reportlab
#pip install pillow
#python -m pip install tkcalendar reportlab pillow
#py -m pip install tkcalendar reportlab pillow

