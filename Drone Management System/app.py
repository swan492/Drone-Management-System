
import mysql.connector
import tkinter as tk
import tkinter.ttk

from drones import Drone, DroneStore
from operators import Operator, OperatorStore


class Application(object):
    """ Main application view - displays the menu. """

    def __init__(self, conn):
        # Initialise the stores
        self.drones = DroneStore(conn)
        self.operators = OperatorStore(conn)

        # Initialise the GUI window
        self.root = tk.Tk()
        self.root.title('Drone Allocation and Localisation')
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Add in the buttons
        drone_button = tk.Button(
            frame, text="View Drones", command=self.view_drones, width=40, padx=5, pady=5)
        drone_button.pack(side=tk.TOP)
        operator_button = tk.Button(
            frame, text="View Operators", command=self.view_operators, width=40, padx=5, pady=5)
        operator_button.pack(side=tk.TOP)
        exit_button = tk.Button(frame, text="Exit System",
                                command=quit, width=40, padx=5, pady=5)
        exit_button.pack(side=tk.TOP)

    def main_loop(self):
        """ Main execution loop - start Tkinter. """
        self.root.mainloop()

    def view_operators(self):
        """ Display the operators. """
        # Instantiate the operators window
        # Display the window and wait
        print('FINISH operators')
        wnd = OperatorListWindow(self)
        self.root.wait_window(wnd.root)

    def view_drones(self):
        """ Display the drones. """
        wnd = DroneListWindow(self)
        self.root.wait_window(wnd.root)


class ListWindow(object):
    """ Base list window. """

    def __init__(self, parent, title):
        # Add a variable to hold the stores
        self.drones = parent.drones
        self.operators = parent.operators

        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

    def add_list(self, columns, edit_action):
        # Add the list
        self.tree = tkinter.ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.title())
        ysb = tkinter.ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                            command=self.tree.yview)
        xsb = tkinter.ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL,
                            command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        self.tree.bind("<Double-1>", edit_action)

        # Add tree and scrollbars to frame
        self.tree.grid(in_=self.frame, row=0, column=0, sticky=tk.NSEW)
        ysb.grid(in_=self.frame, row=0, column=1, sticky=tk.NS)
        xsb.grid(in_=self.frame, row=1, column=0, sticky=tk.EW)

        # Set frame resize priorities
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def close(self):
        """ Closes the list window. """
        self.root.destroy()


class DroneListWindow(ListWindow):
    """ Window to display a list of drones. """

    def __init__(self, parent):
        super(DroneListWindow, self).__init__(parent, 'Drones')
        
        # Add the list and fill it with data
        columns = ('id', 'name', 'class', 'rescue', 'operator')
        self.add_list(columns, self.edit_drone)
        self.populate_data()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Add Drone",
                               command=self.add_drone, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=2, column=0, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

    def populate_data(self):
        """ Populates the data in the view. """
        print('FINISH: Load drone data')
        self.tree.delete(*self.tree.get_children())
        for drone in self.drones.list():
            values = (drone.id, drone.name, drone.class_type, drone.rescue, drone.operator)
            self.tree.insert('', 'end', values=values)

    def add_drone(self):
        """ Starts a new drone and displays it in the list. """
        # Start a new drone instance
        print('FINISH: Start a new drone')
        drone = Drone("")

        # Display the drone
        self.view_drone(drone, self._save_new_drone)

    def _save_new_drone(self, drone):
        """ Saves the drone in the store and updates the list. """
        self.drones.add(drone)
        self.populate_data()

    def edit_drone(self, event):
        """ Retrieves the drone and shows it in the editor. """
        # Retrieve the identifer of the drone
        item = self.tree.item(self.tree.focus())
        item_id = item['values'][0]

        # Load the drone from the store
        print('FINISH: Load drone with ID {:04}'.format(item_id))
        drone = self.drones.get(item_id)

        # Display the drone
        self.view_drone(drone, self._update_drone)

    def _update_drone(self, drone):
        """ Saves the new details of the drone. """
        self.drones.save(drone)
        self.populate_data()

    def view_drone(self, drone, save_action):
        """ Displays the drone editor. """
        wnd = DroneEditorWindow(self, drone, save_action)
        self.root.wait_window(wnd.root)
    
    
    
class OperatorListWindow(ListWindow):
    """ Window to display a list of operators. """

    def __init__(self, parent):
        super(OperatorListWindow, self).__init__(parent, 'Operators')
        
        # Add the list and fill it with data
        columns = ('Name', 'Class', 'Rescue', 'Operations', 'Drone')
        self.add_list(columns, self.edit_operator)
        self.populate_data()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Add Operator",
                               command=self.add_operator, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=2, column=0, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

    def populate_data(self):
        """ Populates the data in the view. """
        print('FINISH: Load operator data')
        self.tree.delete(*self.tree.get_children())
        for operator in self.operators.list():
            values = (operator.name, operator.drone_license, operator.rescue_endorsement, operator.operations, operator.drone)
            self.tree.insert('', 'end', values=values)

    def add_operator(self):
        """ Starts a new operator and displays it in the list. """
        # Start a new operator instance
        print('FINISH: Start a new operator')
        operator = Operator()
        operator.first_name = ""
        operator.family_name = ""
        operator.drone_license = 1
        operator.rescue_endorsement = 1
        operator.operations = 0
        # Display the operator
        self.view_operator(operator, self._save_new_operator)

    def _save_new_operator(self, operator):
        """ Saves the operator in the store and updates the list. """
        self.operators.add(operator)
        self.populate_data()

    def edit_operator(self, event):
        """ Retrieves the operator and shows it in the editor. """
        # Retrieve the identifer of the operator
        item = self.tree.item(self.tree.focus())
        item_name = item['values'][0]

        # Load the operator from the store
        print('FINISH: Load operator with name {}'.format(item_name))
        operator = self.operators.get(item_name)

        # Display the operator
        self.view_operator(operator, self._update_operator)

    def _update_operator(self, operator):
        """ Saves the new details of the operator. """
        self.operators.save(operator)
        self.populate_data()

    def view_operator(self, operator, save_action):
        """ Displays the operator editor. """
        wnd = OperatorEditorWindow(self, operator, save_action)
        self.root.wait_window(wnd.root)



class EditorWindow(object):
    """ Base editor window. """

    def __init__(self, parent, title, save_action):
        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

        # Add the editor widgets
        last_row = self.add_editor_widgets()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Save",
                               command=save_action, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=last_row + 1, column=1, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=last_row + 2, column=1, sticky=tk.E)

    def add_editor_widgets(self):
        """ Adds the editor widgets to the frame - this needs to be overriden in inherited classes. 
        This function should return the row number of the last row added - EditorWindow uses this
        to correctly display the buttons. """
        return -1

    def close(self):
        """ Closes the editor window. """
        self.root.destroy()



class DroneEditorWindow(EditorWindow):
    """ Editor window for drones. """

    def __init__(self, parent, drone, save_action):
        # FINISH: Add either the drone name or <new> in the window title, depending on whether this is a new
        # drone or not
        if drone.name == "":
            item = "<new>"
        else:
            item = drone.name
        super(DroneEditorWindow, self).__init__(parent, 'Drone: '+item, self.save_drone)
        self._drone = drone
        self._save_action = save_action

        # FINISH: Load drone details
        self.name_input.insert(tk.INSERT, self._drone.name)
        if self._drone.class_type != 1:
            self.type_box.current(1)
        if self._drone.rescue == 2:
            self.rescue_box.current(1)
        
    def add_editor_widgets(self):
        """ Adds the widgets for editing a drone. """
        print('FINISH: Create widgets and populate them with data')
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_input = tk.Text(self.root, height=1, width=30)
        self.type_label = tk.Label(self.root, text="Drone Class: ")
        self.type_box = tkinter.ttk.Combobox(self.root, values=["One", "Two"])
        self.rescue_label = tk.Label(self.root, text="Rescue Drone: ")
        self.rescue_box = tkinter.ttk.Combobox(self.root, values=["No", "Yes"])
        self.name_label.grid(in_=self.frame, row=0, column=0, sticky=tk.W)
        self.name_input.grid(in_=self.frame, row=0, column=1,sticky=tk.E)
        self.type_label.grid(in_=self.frame, row=1, column=0, sticky=tk.W)
        self.type_box.grid(in_=self.frame, row=1, column=1,sticky=tk.W)
        self.type_box.current(0)
        self.rescue_label.grid(in_=self.frame, row=2, column=0, sticky=tk.W)
        self.rescue_box.grid(in_=self.frame, row=2, column=1,sticky=tk.W)
        self.rescue_box.current(0) 
        return 3

    def save_drone(self):
        """ Updates the drone details and calls the save action. """
        print('FINISH: Update the drone from the widgets')
        name = self.name_input.get("1.0", "end-1c")
        type = 1 if self.type_box.get() == "One" else 2
        rescue = 1 if self.rescue_box.get() == "No" else 2
        self._drone.name = name if name != self._drone.name else self._drone.name
        self._drone.class_type = type if type != self._drone.class_type else self._drone.class_type
        self._drone.rescue = rescue if rescue != self._drone.rescue else self._drone.rescue
        self._save_action(self._drone)



class OperatorEditorWindow(EditorWindow):
    """ Editor window for operators. """

    def __init__(self, parent, operator, save_action):
        # FINISH: Add either the operator name or <new> in the window title, depending on whether this is a new
        # operator or not
        if operator.first_name == "" and operator.family_name == "":
            item = "<new>"
        else:
            item = operator.first_name + " " + operator.family_name
        super(OperatorEditorWindow, self).__init__(parent, 'Operator: '+item, self.save_operator)
        self._operator = operator
        self._save_action = save_action

        # FINISH: Load operator details
        self.rescue_field.configure(state="normal")
        self._operator.operations = 0 if self._operator.operations == None else self._operator.operations
        self.first_input.insert(tk.INSERT, self._operator.first_name)
        self.family_input.insert(tk.INSERT, self._operator.family_name)
        if self._operator.drone_license == 2:
            self.type_box.current(1)
        elif self._operator.drone_license == None:
            self.type_box.current(2)
        if self._operator.operations >= 5:
            self.rescue_field.delete("1.0", tk.END)
            self.rescue_field.insert("1.0", "Yes")
        if self._operator.operations > 0:
            self.operation_box.delete(0, "end")
            self.operation_box.insert(0,self._operator.operations)
        self.rescue_field.configure(state="disabled")
        
    def add_editor_widgets(self):
        """ Adds the widgets for editing an operator. """
        print('FINISH: Create widgets and populate them with data')
        self.first_label = tk.Label(self.root, text="First Name:")
        self.first_input = tk.Text(self.root, height=1, width=30)
        self.family_label = tk.Label(self.root, text="Family Name:")
        self.family_input = tk.Text(self.root, height=1, width=30)
        self.type_label = tk.Label(self.root, text="Drone License: ")
        self.type_box = tkinter.ttk.Combobox(self.root, values=["One", "Two", ""])
        self.rescue_label = tk.Label(self.root, text="Rescue Endorsement: ")
        self.rescue_field = tk.Text(self.root, height=1, width=10)
        self.operation_label = tk.Label(self.root, text="Number of Operation: ")
        self.var = tk.DoubleVar(value=0)
        self.operation_box = tk.Spinbox(self.root, from_=0, to=10000, textvariable=self.var)
        self.first_label.grid(in_=self.frame, row=0, column=0, sticky=tk.W)
        self.first_input.grid(in_=self.frame, row=0, column=1,sticky=tk.E)
        self.family_label.grid(in_=self.frame, row=1, column=0, sticky=tk.W)
        self.family_input.grid(in_=self.frame, row=1, column=1,sticky=tk.E)
        self.type_label.grid(in_=self.frame, row=2, column=0, sticky=tk.W)
        self.type_box.grid(in_=self.frame, row=2, column=1,sticky=tk.W)
        self.type_box.current(0)
        self.rescue_label.grid(in_=self.frame, row=3, column=0, sticky=tk.W)
        self.rescue_field.grid(in_=self.frame, row=3, column=1,sticky=tk.W)
        self.rescue_field.insert("end", "No")
        self.rescue_field.configure(state="disabled")
        self.operation_label.grid(in_=self.frame, row=4, column=0, sticky=tk.W)
        self.operation_box.grid(in_=self.frame, row=4, column=1,sticky=tk.W)
        return 5

    def save_operator(self):
        """ Updates the operator details and calls the save action. """
        print('FINISH: Update the operator from the widgets')
        first = self.first_input.get("1.0", "end-1c")
        family = self.family_input.get("1.0", "end-1c")
        type = 1 if self.type_box.get() == "One" else 2
        self._operator.first_name = first if first != self._operator.first_name else self._operator.first_name
        self._operator.family_name = family if family != self._operator.family_name else self._operator.family_name
        self._operator.drone_license = type if type != self._operator.drone_license else self._operator.drone_license
        self._operator.rescue_endorsement = 1 if int(self.operation_box.get()) <= 5 else 2
        self._operator.operations = self.operation_box.get()
        self._save_action(self._operator)


if __name__ == '__main__':
    conn = mysql.connector.connect(user='root',
                                   password='<your password>',
                                   host='127.0.0.1',
                                   database='DroneManagement',
                                   charset='utf8')
    print('... connected, starting application')
    app = Application(conn)
    app.main_loop()
    conn.close()
