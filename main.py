import tkinter as tk
import os

class ExpenseTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")

        self.expense_tracker = ExpenseTracker()

        self.label = tk.Label(master, text="Expense Tracker")
        self.label.pack()

        self.add_expense_button = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.view_expenses_button = tk.Button(master, text="View Expenses", command=self.view_expenses)
        self.view_expenses_button.pack()

        self.edit_expense_button = tk.Button(master, text="Edit Expense", command=self.edit_expense)
        self.edit_expense_button.pack()

        self.delete_expense_button = tk.Button(master, text="Delete Expense", command=self.delete_expense)
        self.delete_expense_button.pack()

        self.total_spent_button = tk.Button(master, text="Total Spent", command=self.total_spent)
        self.total_spent_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack()

    def add_expense(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Expense")

        description_label = tk.Label(add_window, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        amount_label = tk.Label(add_window, text="Amount:")
        amount_label.pack()
        amount_entry = tk.Entry(add_window)
        amount_entry.pack()

        def save_expense():
            description = description_entry.get()
            try:
                amount = float(amount_entry.get())
                self.expense_tracker.add_expense(description, amount)
                add_window.destroy()
            except ValueError:
                error_label = tk.Label(add_window, text="Invalid amount. Please enter a number.", fg="red")
                error_label.pack()

        save_button = tk.Button(add_window, text="Save", command=save_expense)
        save_button.pack()

    def view_expenses(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("View Expenses")

        expenses_text = tk.Text(view_window)
        expenses_text.pack()

        expenses = self.expense_tracker.expenses
        if not expenses:
            expenses_text.insert(tk.END, "No expenses yet.")
        else:
            for idx, expense in enumerate(expenses, 1):
                expenses_text.insert(tk.END, f"{idx}. {expense['description']}: {expense['amount']}\n")

    def edit_expense(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Expense")

        index_label = tk.Label(edit_window, text="Index:")
        index_label.pack()
        index_entry = tk.Entry(edit_window)
        index_entry.pack()

        description_label = tk.Label(edit_window, text="New Description:")
        description_label.pack()
        description_entry = tk.Entry(edit_window)
        description_entry.pack()

        amount_label = tk.Label(edit_window, text="New Amount:")
        amount_label.pack()
        amount_entry = tk.Entry(edit_window)
        amount_entry.pack()

        def update_expense():
            try:
                index = int(index_entry.get())
                description = description_entry.get()
                amount = float(amount_entry.get())
                self.expense_tracker.edit_expense(index, description, amount)
                edit_window.destroy()
            except ValueError:
                error_label = tk.Label(edit_window, text="Invalid input. Please enter correct data.", fg="red")
                error_label.pack()
            except IndexError:
                error_label = tk.Label(edit_window, text="Invalid index. Please enter a valid index.", fg="red")
                error_label.pack()

        update_button = tk.Button(edit_window, text="Update", command=update_expense)
        update_button.pack()

    def delete_expense(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Expense")

        index_label = tk.Label(delete_window, text="Index:")
        index_label.pack()
        index_entry = tk.Entry(delete_window)
        index_entry.pack()

        def delete_expense():
            try:
                index = int(index_entry.get())
                self.expense_tracker.delete_expense(index)
                delete_window.destroy()
            except ValueError:
                error_label = tk.Label(delete_window, text="Invalid index. Please enter a number.", fg="red")
                error_label.pack()
            except IndexError:
                error_label = tk.Label(delete_window, text="Invalid index. Please enter a valid index.", fg="red")
                error_label.pack()

        delete_button = tk.Button(delete_window, text="Delete", command=delete_expense)
        delete_button.pack()

    def total_spent(self):
        total = self.expense_tracker.total_spent()
        total_window = tk.Toplevel(self.master)
        total_window.title("Total Spent")

        total_label = tk.Label(total_window, text=f"Total Amount Spent: {total}/-")
        total_label.pack()

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.load_data()

    def load_data(self):
        if os.path.exists("expenses.txt"):
            with open("expenses.txt", "r") as file:
                for line in file:
                    description, amount = line.strip().split(",")
                    self.expenses.append({"description": description, "amount": float(amount)})

    def save_data(self):
        with open("expenses.txt", "w") as file:
            for expense in self.expenses:
                file.write(f"{expense['description']},{expense['amount']}\n")

    def add_expense(self, description, amount):
        self.expenses.append({"description": description, "amount": amount})
        self.save_data()
        print("Expense added successfully!")

    def edit_expense(self, index, description, amount):
        if 0 < index <= len(self.expenses):
            self.expenses[index - 1] = {"description": description, "amount": amount}
            self.save_data()
            print("Expense updated successfully.")
        else:
            print("Invalid expense index.")

    def delete_expense(self, index):
        if 0 < index <= len(self.expenses):
            del self.expenses[index - 1]
            self.save_data()
            print("Expense deleted successfully.")
        else:
            print("Invalid expense index.")

    def total_spent(self):
        return sum(expense['amount'] for expense in self.expenses)

def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
