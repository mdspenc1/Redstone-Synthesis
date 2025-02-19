import customtkinter as ctk
import tkinter as tk
import sys
import os
import inspect

# Forces working directory to be the parent directory to access other packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from World_File_Management.minecraft_path import mc_saves_directory

# Choose design for all windows
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class terminal_window(ctk.CTk):
    def __init__(self):
        """ Initializes terminal window """
        super().__init__()

        # Configure window appearance
        self.title("Redstone Synthesis - Terminal")
        self.geometry("1250x700")
        self.resizable(True, True)

        # Choose window icon
        self.iconbitmap("Resources/redstone_dust_icon.ico")

        # Choose terminal font
        terminal_font = ctk.CTkFont(family="Courier", size=12)

        # Create menu bar for terminal
        menu_bar = tk.Menu(self)

        # Create drop down menu for file
        file = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file)
        file.add_command(label="Open Minecraft World", command=None)
        file.add_command(label="Set Y-Level", command=None)
        file.add_command(label="Set Minecraft Directory", command=lambda: self.entry_popup(self.cmd_set_minecraft_directory))
        
        # Create drop down menu for algebraic synthesis
        algebraic_synthesis = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Algebraic Synthesis", menu=algebraic_synthesis)
        algebraic_synthesis.add_command(label="New Algebraic Synthesis", command=None)
        algebraic_synthesis.add_command(label="Cancel Algebraic Synthesis", command=None)
        algebraic_synthesis.add_command(label="Create Custom Algebraic Function", command=None)
        algebraic_synthesis.add_command(label="Add Circuit to Algebraic Function", command=None)

        # Create drop down menu for logic synthesis
        logic_synthesis = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Logic Synthesis", menu=logic_synthesis)
        logic_synthesis.add_command(label="New Logic Synthesis", command=None)
        logic_synthesis.add_command(label="Cancel Logic Synthesis", command=None)
        logic_synthesis.add_command(label="Add Circuit to Logic Function", command=None)

        # Create drop down menu for help
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Minecraft World Help", command=None)
        help_menu.add_command(label="Algebraic Synthesis Help", command=None)
        help_menu.add_command(label="Logic Synthesis Help", command=None)
        help_menu.add_command(label="Terminal Command Help", command=None)

        # Explicitly link menu bar to terminal window
        self.config(menu=menu_bar)

        # Terminal output box
        self.output_box = ctk.CTkTextbox(self, wrap="word", state="disabled", font=terminal_font)
        self.output_box.pack(fill="both", expand=True)

        # Terminal input bar
        self.input_bar = ctk.CTkEntry(self, font=terminal_font)
        self.input_bar.pack(fill="x")
        self.input_bar.bind("<Return>", self.process_command)

        # Commands
        self.commands = {
            "minecraft_world_help": self.cmd_minecraft_world_help,
            "terminal_commands_help": self.cmd_terminal_commands_help,
            "clear": self.cmd_clear,
            "set_minecraft_directory": self.cmd_set_minecraft_directory
        }

    def get_num_parameters(self, command):
        """ Takes command string and returns the number of arguments its corresponding function takes excluding self """
        return len(inspect.signature(self.commands[command].__func__).parameters) - 1

    def process_command(self, event):
        """ Processes commands typed into terminal input bar """
        entry = self.input_bar.get().split('~')
        command = entry[0]
        arguments = entry[1:]
        self.input_bar.delete(0, "end")
        self.display_message(f"> {command}\n")
        if command in self.commands and not arguments:
            self.commands[command]()
        elif command in self.commands and len(arguments) == self.get_num_parameters(command):
            self.commands[command](*arguments)
        else:
            self.display_message("ERROR: Unknown command!\n")
            self.display_message("Type \"terminal_commands_help\" for a list of commands and assistance.\n")

    def display_message(self, message):
        """ Displays messages to terminal output box """
        self.output_box.configure(state="normal")
        self.output_box.insert("end", message + "\n")
        self.output_box.configure(state="disabled")
        self.output_box.see("end")

    def cmd_clear(self):
        """ Clears text from terminal output box """
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def cmd_minecraft_world_help(self):
        """ Displays message to help users enter their minecraft saves folder directory and world file """
        with open("Resources/minecraft world help.txt", "r") as file:
            content = file.read()
        self.display_message(content)

    def cmd_terminal_commands_help(self):
        """ Displays a list of all the terminal commands and a short description for each of them """
        self.display_message("List of all terminal commands:\n")
        for command in self.commands:
            self.display_message(command + "\n")

    def entry_popup(self, cmd_function):
        """ General use popup entry box for the drop down menu bar """
        entry_popup = tk.Entry(self)
        entry_popup.place(x=self.winfo_pointerx() - self.winfo_rootx(), y=self.winfo_pointery() - self.winfo_rooty(), width=100, height=20)
        entry_popup.focus_set()
        entry_popup.bind("<Return>", lambda event: self.pass_entry_popup(entry_popup, cmd_function))
        entry_popup.bind("<Escape>", lambda event: entry_popup.destroy())

    def pass_entry_popup(self, tk_entry_widget, cmd_function):
        """ Passes entry from entry popup function to existing cmd functions """
        entry = tk_entry_widget.get()
        cmd_function(entry)
        tk_entry_widget.destroy()
    
    def cmd_set_minecraft_directory(self, entry):
        """ Assigns the minecraft saves folder directory to a global variable """
        mc_saves_directory = entry
        self.display_message(f'Minecraft save directory has been set to: {mc_saves_directory}\n')

if __name__=="__main__":
    terminalWindow = terminal_window()
    terminalWindow.mainloop()