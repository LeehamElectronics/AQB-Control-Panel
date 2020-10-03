########################################################################################################################
#                                                  Written By Liam Price                                               #
#       This module runs in order to prompt user with a login screen and an option to use the software offline.        #
#                                              Date Started: 9-07-2020                                                 #
########################################################################################################################

# ██╗░░░░░███████╗███████╗██╗░░██╗░█████╗░███╗░░░███╗██╗░██████╗
# ██║░░░░░██╔════╝██╔════╝██║░░██║██╔══██╗████╗░████║╚█║██╔════╝
# ██║░░░░░█████╗░░█████╗░░███████║███████║██╔████╔██║░╚╝╚█████╗░
# ██║░░░░░██╔══╝░░██╔══╝░░██╔══██║██╔══██║██║╚██╔╝██║░░░░╚═══██╗
# ███████╗███████╗███████╗██║░░██║██║░░██║██║░╚═╝░██║░░░██████╔╝
# ╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░╚═════╝░

# ░██████╗░█████╗░███████╗████████╗░██╗░░░░░░░██╗░█████╗░██████╗░███████╗
# ██╔════╝██╔══██╗██╔════╝╚══██╔══╝░██║░░██╗░░██║██╔══██╗██╔══██╗██╔════╝
# ╚█████╗░██║░░██║█████╗░░░░░██║░░░░╚██╗████╗██╔╝███████║██████╔╝█████╗░░
# ░╚═══██╗██║░░██║██╔══╝░░░░░██║░░░░░████╔═████║░██╔══██║██╔══██╗██╔══╝░░
# ██████╔╝╚█████╔╝██║░░░░░░░░██║░░░░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║███████╗
# ╚═════╝░░╚════╝░╚═╝░░░░░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝

# Import Modules #
from tkinter import *
from tkinter.messagebox import showinfo

############################################
#                                          #
#   Global Variables and data structures   #
#                                          #
############################################
profile = []
pass_attempt = 0
online_mode = False
login_password = "class"  # You can change this!

#########################################################################
#                                                                       #
#                        Main Window Functions                          #
#                                                                       #
#########################################################################


def login():
    global pass_attempt
    print("Attempting Login")  # Diagnostic purposes
    if password_input.get() == login_password:
        print("Password Correct")
        password_feedback.set("  Enter Password  ")
        if online_mode:  # Online Mode #
            # Close login window #
            login_window.destroy()
            initiate_mqtt()
        if not online_mode:  # Offline Mode #
            print("Logging in with offline mode")
            # Close login window #
            login_window.destroy()
            import main_window as main
            main.online_mode = False  # Tell main_window that we are in online mode
            main.main_window_setup()
    else:
        print("Wrong Password")
        password_input.delete(0, "end")
        password_feedback.set("Wrong Password")
        pass_attempt += 1
        if pass_attempt == 5:
            showinfo("Access Denied", "Password entered incorrectly 5 times! Application will now close.")
            login_window.destroy()


def initiate_mqtt():
    print("Initiating MQTT")
    mqtt_ip = str(ip_input_val.get())
    mqtt_port = int(port_input_val.get())
    cred_user = mqtt_user_input_val.get()
    cred_pass = mqtt_pass_input_val.get()
    try:
        import main_window as main
        main.online_mode = True  # Tell main_window that we are in online mode
        main.mqtt_ip = mqtt_ip
        main.mqtt_port = mqtt_port
        main.cred_user = cred_user
        main.cred_pass = cred_pass
        main.connect_mqtt()
    except Exception as reason:
        online_mode_val.set("Connection Failed!")
        print("Connection Failed")
        print(reason)


def on_network_type_change(*args):
    global online_mode
    c_val = str(online_mode_val.get())
    if c_val == "Online Mode":
        online_mode = True
        print("Online Mode Activated")
        replace_custom_widgets()
    elif c_val == "Offline Mode":
        online_mode = False
        print("Offline Mode Activated")
        remove_custom_widgets()


def on_custom_connection_change(*args):
    connection_id = str(connection_type_sel_val.get())
    if connection_id == "Public":
        print("Displaying Public Creds")
        ip_input_val.set(public_IP)
        port_input_val.set(public_port)
        mqtt_user_input_val.set(public_user)
        mqtt_pass_input_val.set(public_pass)
        set_entry_read_only()
        save_butt.grid_remove()  # Remove save button if it is there because we don't want to modify this data
    if connection_id == "Internal":
        print("Displaying Internal Creds")
        ip_input_val.set(internal_IP)
        port_input_val.set(internal_port)
        mqtt_user_input_val.set(internal_user)
        mqtt_pass_input_val.set(internal_pass)
        set_entry_read_only()
        save_butt.grid_remove()  # Remove save button if it is there because we don't want to modify this data
    if connection_id == "Custom":
        print("Loading Custom Profile")
        read_custom_connection()
        set_entry_normal()
        save_butt.grid(row=7, column=0)


def set_entry_read_only():
    ip_input.config(state='readonly')
    port_input.config(state='readonly')
    user_input.config(state='readonly')
    pass_input.config(state='readonly')


def set_entry_normal():
    ip_input.config(state='normal')
    port_input.config(state='normal')
    user_input.config(state='normal')
    pass_input.config(state='normal')


def remove_custom_widgets():  # Call this function when offline mode enabled so as to not confuse user #
    save_butt.grid_remove()  # Remove save button
    customization_lab.grid_remove()
    connect_type_sel.grid_remove()
    ip_input.grid_remove()
    port_input.grid_remove()
    user_input.grid_remove()
    pass_input.grid_remove()
    bottom_frame.grid_remove()


def replace_custom_widgets():  # Inverse of remove_custom_widgets #
    print("Replacing custom widgets")
    bottom_frame.grid()
    customization_lab.grid(row=0, column=0)
    connect_type_sel.grid(row=2, column=0)
    ip_input.grid(row=3, column=0)
    port_input.grid(row=4, column=0)
    user_input.grid(row=5, column=0)
    pass_input.grid(row=6, column=0)
    connection_type_sel_val.set("Public")  # Return to default values #


def read_custom_connection(*args):
    print("Reading connection profile")
    connection_list = []
    custom_profiles = 'MQTT_profiles.txt'
    f = open(custom_profiles, "r")  # open this file
    field = 0
    for line in f.readlines():   # read lines
        line = line.rstrip('\n') # remove the carriage return /n at the end of each line
        if field == 0:
            connection_list.append(line)
            field += 1
        elif field == 1:
            connection_list.append(line)
            field += 1
        elif field == 2:
            connection_list.append(line)
            field += 1
        elif field == 3:
            connection_list.append(line)
            field = 0
    print(connection_list)
    ip_input_val.set(connection_list[0])
    port_input_val.set(connection_list[1])
    mqtt_user_input_val.set(connection_list[2])
    mqtt_pass_input_val.set(connection_list[3])
    f.close()


def save_custom_connection(*args):
    print("Saving connection vars to txt file")
    connection_list = [ip_input_val.get(), port_input_val.get(), mqtt_user_input_val.get(), mqtt_pass_input_val.get()]
    print(connection_list)
    custom_profiles = 'MQTT_profiles.txt'
    f = open(custom_profiles, "w")  # open this file
    f.write('%s\n' % connection_list[0])
    f.write('%s\n' % connection_list[1])
    f.write('%s\n' % connection_list[2])
    f.write('%s\n' % connection_list[3])
    f.close()


# Function that runs when the "enter" key is hit #
def key_pressed(event):
    if event.keysym == "Return":
        print("return hit")
        login()


#########################################################################
#                                                                       #
#                         MQTT Setup Code                               #
#                                                                       #
#########################################################################

# Password Variables, these a predefined so you can easily select them #
# I added options for both internal and external, meaning inside of    #
# private network or outside for those running their MQTT servers in   #
# their own homes.                                                     #
public_user = "public_user_example"
public_pass = "public_pass_example"
internal_user = "internal_user_example"
internal_pass = "internal_pass_example"

# MQTT Server Variables #
public_IP = "public_ip_example"  # MQTT Broker public IPv4 / DNS address #
internal_IP = "internal_ip_example"  # MQTT Broker public IPv4 / DNS address #
public_port = 1883  # External MQTT Broker port number #
internal_port = 1883  # Internal MQTT Broker port number #

#########################################################################
#                                                                       #
#                         Tkinter Setup Code                            #
#                                                                       #
#########################################################################

login_window = Tk()
login_window.title("Automated-IoT-Quad-Bike Login")
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
width = 800
height = 600
login_window.geometry(f'{width}x{height}')
login_window.iconbitmap('media/A-IOT-QB-Icon.ico')
login_window.configure(background='grey')
# Background Photo Setup (needs to be done first otherwise it wont be put at the back) #
bg_photo = PhotoImage(file="media/bg_login_pic.PNG")
bg_photo_label = Label(login_window, image=bg_photo)
bg_photo_label.place(x=-32, y=-20)

#########################################################################
#                                                                       #
#                           String Variables                            #
#                                                                       #
#########################################################################

online_mode_val = StringVar()
online_mode_val.set("Offline Mode")
online_mode_val.trace('w', on_network_type_change)
connection_type_sel_val = StringVar()
connection_type_sel_val.set("Public")
connection_type_sel_val.trace('w', on_custom_connection_change)
ip_input_val = StringVar()
port_input_val = StringVar()
mqtt_user_input_val = StringVar()
mqtt_pass_input_val = StringVar()
password_feedback = StringVar()


#########################################################################
#                                                                       #
#                         Geometry Management                           #
#                                                                       #
#########################################################################

# Organise sections of GUI into frames #
top_frame = Frame(login_window)
bottom_frame = Frame(login_window, bg='gray')
# Grid all the frames in place #
top_frame.grid(row=0, sticky="n")
bottom_frame.grid(row=3, sticky="s")

# Main Frame Widget Creation #
enter_pass_lab = Label(login_window, textvariable=password_feedback, justify=LEFT, bg="Red", fg="White", relief=RAISED)
password_input = Entry(login_window, width=20, justify='center', show="*")
login_butt = Button(login_window, text="Login", bg="white", fg="black", height=2, width=15, command=login)
connection_sel = OptionMenu(login_window, online_mode_val, "Online Mode", "Offline Mode")
connection_sel.config(bg="white")
customization_lab = Label(bottom_frame, justify='center', text="Customize Connection")
connect_type_sel = OptionMenu(bottom_frame, connection_type_sel_val, "Public", "Internal", "Custom")
connect_type_sel.config(bg="white")
ip_input = Entry(bottom_frame, width=20, justify='center', textvariable=ip_input_val)
port_input = Entry(bottom_frame, width=20, justify='center', textvariable=port_input_val)
user_input = Entry(bottom_frame, width=20, justify='center', textvariable=mqtt_user_input_val)
pass_input = Entry(bottom_frame, width=20, justify='center', textvariable=mqtt_pass_input_val)
save_butt = Button(login_window, text="Save", bg="white", fg="black", height=2, width=15, command=save_custom_connection)

# Main Frame Widget Placement #
enter_pass_lab.place(relx=0.43, rely=0.45, anchor=CENTER)
password_input.place(relx=0.57, rely=0.45, anchor=CENTER)
login_butt.place(relx=0.5, rely=0.5, anchor=CENTER)
connection_sel.place(relx=0.5, rely=.3, anchor=CENTER)
customization_lab.grid(row=0, column=0)
connect_type_sel.grid(row=2, column=0)
ip_input.grid(row=3, column=0)
port_input.grid(row=4, column=0)
user_input.grid(row=5, column=0)
pass_input.grid(row=6, column=0)

# Side Panel Frame Widget Creation #


# Side Panel Frame Widget Placement #

# Set any Entry Variables Here #
print("Displaying Public Creds")
ip_input_val.set(public_IP)
port_input_val.set(public_port)
mqtt_user_input_val.set(public_user)
mqtt_pass_input_val.set(public_pass)
password_feedback.set("  Enter Password  ")

# Set entry's to read only mode #
set_entry_read_only()

# Default to offline mode #
remove_custom_widgets()

# Assign key-bind to login window #
login_window.bind("<Key>", key_pressed)

# Runs the main loop that updates the GUI #
login_window.mainloop()

#########################################################################
#                                                                       #
#                             Acknowledgments                           #
#                                                                       #
#########################################################################
#                                                                       #
# I decided to format my Tkinter widgets in the way I have because of   #
# what read in the following StackOverflow post...                      #
# https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using #
#       -frames-and-grid                                                #
# I figured I needed some way or organising my Tkinter widgets because  #
# there is A LOT of widgets in my design.                               #
#########################################################################
