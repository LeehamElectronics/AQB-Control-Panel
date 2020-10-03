########################################################################################################################
#                                           All Code written By Liam Price                                             #
#                                        Automated-IoT-Quad-Bike main_window.py                                        #
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

# Libraries Here #
from tkinter import *
import paho.mqtt.client as mqtt
import time, logging
import multiprocessing

#########################################################################
#                                                                       #
#                        Main Window Functions                          #
#                                                                       #
#########################################################################

def log_out():
    print("Logging out...")
    my_window.destroy()
    # importjj login_window


def power_val_update(*args):
    global power_sel
    val_temp = power_val.get()
    print("power val update sequence")
    if val_temp == "HIGH":
        power_sel.config(bg="RED")
    if val_temp == "MED":
        power_sel.config(bg="ORANGE")
    if val_temp == "LOW":
        power_sel.config(bg="GREEN")


def ctrl_mode_val_update(*args):
    print("Updating Controller Mode")
    if ctrl_mode_val.get() == "Sticky":
        print("Sticky Control Enabled")
    elif ctrl_mode_val.get() == "Momentary":
        print("Momentary Control Enabled")
    elif ctrl_mode_val.get() == "Steering Wheel":
        print("Steering Wheel OptionMenu")
        custom_controller_func()


#########################################################################
#                                                                       #
#                         MQTT Setup Code                               #
#                                                                       #
#########################################################################
online_mode = False
mqtt_ip = ""
mqtt_port = 0
cred_user = ""
cred_pass = ""


def connect_mqtt():
    print("Connecting to mqtt")
    client.username_pw_set(cred_user, cred_pass)
    client.connect(mqtt_ip, mqtt_port)  # establish connection
    time.sleep(1)
    client.loop_start()
    client.subscribe("/AQB/out")  # subscribe to mqtt topic
    print("Connect success!")
    main_window_setup()


def on_subscribe(client, userdata, mid, granted_qos):
    # print("subscribed with qos",granted_qos, "\n")
    time.sleep(1)
    logging.info("sub acknowledge message id=" + str(mid))


def on_disconnect(client, userdata, rc=0):
    logging.info("DisConnected result code " + str(rc))


def on_connect(client, userdata, flags, rc):
    logging.info("Connected flags" + str(flags) + "result code " + str(rc))


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message received  " + msg)
    if msg == "test1":
        print("test1 received from mqtt")
    if msg == "test2":
        print("test2 received from mqtt")


def on_publish(client, userdata, mid):
    logging.info("message published " + str(mid))


def start_steering_wheel_ctrl():
    # Some of the Pygame code was taken directly from the Pygame wiki as an example that I built off. Google Pygame for
    # more info on the module
    print("Starting steering_wheel_module")
    # You will need to manually set your MQTT credentials and connection options here, I know it's annoying, but it's
    # difficult for me to parse the variables from the login screen into this function because it's running on another
    # CPU core, if you would like to help, contact me at liamisprice@gmail.com
    public_user = "public_user_example"
    public_pass = "public_pass_example"
    mqtt_ip = "example.com"
    mqtt_port = 1883
    print("Connecting to mqtt with " + str(mqtt_ip) + " and port " + str(mqtt_port))
    logging.basicConfig(level=logging.INFO)  # Error Logging #
    QOS = 0  # QoS Level keep at 0
    CLEAN_SESSION = True
    client = mqtt.Client("AQB-CtrlP-SW", False)  # create client object
    client.on_subscribe = on_subscribe  # assign function to callback
    client.on_disconnect = on_disconnect  # assign function to callback
    client.on_connect = on_connect  # assign function to callback
    client.on_message = on_message  # when a payload is received this function runs
    client.username_pw_set(public_user, public_pass)
    client.connect(mqtt_ip, mqtt_port)  # establish connection
    time.sleep(1)
    client.loop_start()
    print("Connect success!")
    import pygame
    # Define some colors.
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')

    # This is a simple class that will help us print to the screen.
    # It has nothing to do with the joysticks, just outputting the
    # information.
    class TextPrint(object):
        def __init__(self):
            self.reset()
            self.font = pygame.font.Font(None, 20)

        def tprint(self, screen, textString):
            textBitmap = self.font.render(textString, True, BLACK)
            screen.blit(textBitmap, (self.x, self.y))
            self.y += self.line_height

        def reset(self):
            self.x = 10
            self.y = 10
            self.line_height = 15

        def indent(self):
            self.x += 10

        def unindent(self):
            self.x -= 10

    pygame.init()

    # Set the width and height of the screen (width, height).
    screen = pygame.display.set_mode((500, 700))

    pygame.display.set_caption("AQB Steering Wheel GUI")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Get ready to print.
    textPrint = TextPrint()

    button_0_pressed = False
    button_1_pressed = False
    button_2_pressed = False
    button_3_pressed = False
    button_4_pressed = False
    button_5_pressed = False
    button_6_pressed = False
    button_7_pressed = False
    button_8_pressed = False
    button_9_pressed = False
    button_10_pressed = False
    button_11_pressed = False
    button_12_pressed = False

    axis_temp_check = False

    # -------- Main Program Loop -----------
    while not done:
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if joystick.get_button(0) == True:
                    button_0_pressed = True
                    print("button 1 hit")
                    client.publish("/AQB/in/SW_btn_d", "0")
                elif joystick.get_button(1) == True:
                    button_1_pressed = True
                    print("button 1 hit")
                    client.publish("/AQB/in/SW_btn_d", "1")
                elif joystick.get_button(2) == True:
                    button_2_pressed = True
                    print("button 2 hit")
                    client.publish("/AQB/in/SW_btn_d", "2")
                elif joystick.get_button(3) == True:
                    print("button 3 hit")
                    client.publish("/AQB/in/SW_btn_d", "3")
                    button_3_pressed = True
                elif joystick.get_button(4) == True:
                    print("button 4 hit")
                    client.publish("/AQB/in/SW_btn_d", "4")
                    button_4_pressed = True
                elif joystick.get_button(5) == True:
                    print("button 5 hit")
                    client.publish("/AQB/in/SW_btn_d", "5")
                    button_5_pressed = True
                elif joystick.get_button(6) == True:
                    print("button 6 hit")
                    client.publish("/AQB/in/SW_btn_d", "6")
                    button_6_pressed = True
                elif joystick.get_button(7) == True:
                    print("button 7 hit")
                    client.publish("/AQB/in/SW_btn_d", "7")
                    button_7_pressed = True
                elif joystick.get_button(8) == True:
                    print("button 8 hit")
                    client.publish("/AQB/in/SW_btn_d", "8")
                    button_8_pressed = True
                elif joystick.get_button(9) == True:
                    print("button 9 hit")
                    client.publish("/AQB/in/SW_btn_d", "9")
                    button_9_pressed = True
                elif joystick.get_button(10) == True:
                    print("button 10 hit")
                    client.publish("/AQB/in/SW_btn_d", "k")
                    button_10_pressed = True
                elif joystick.get_button(11) == True:
                    print("button 11 hit")
                    client.publish("/AQB/in/SW_btn_d", "s")
                    button_11_pressed = True
                elif joystick.get_button(12) == True:
                    print("button 12 hit")
                    client.publish("/AQB/in/SW_btn_d", "12")
                    button_12_pressed = True
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
                if joystick.get_button(0) == False and button_0_pressed == True:
                    button_1_pressed = False
                    print("button 0 released")
                    client.publish("/AQB/in/SW_btn_u", "0")
                if joystick.get_button(1) == False and button_1_pressed == True:
                    button_1_pressed = False
                    print("button 1 released")
                    client.publish("/AQB/in/SW_btn_u", "1")
                elif joystick.get_button(2) == False and button_2_pressed == True:
                    button_2_pressed = False
                    print("button 2 released")
                    client.publish("/AQB/in/SW_btn_u", "2")
                elif joystick.get_button(3) == False and button_3_pressed == True:
                    button_3_pressed = False
                    print("button 3 released")
                    client.publish("/AQB/in/SW_btn_u", "3")
                elif joystick.get_button(4) == False and button_4_pressed == True:
                    button_4_pressed = False
                    print("button 4 released")
                    client.publish("/AQB/in/SW_btn_u", "4")
                elif joystick.get_button(5) == False and button_5_pressed == True:
                    button_5_pressed = False
                    print("button 5 released")
                    client.publish("/AQB/in/SW_btn_u", "5")
                elif joystick.get_button(6) == False and button_6_pressed == True:
                    button_6_pressed = False
                    print("button 6 released")
                   # client.publish("/AQB/in/SW_btn_u", "6")
                elif joystick.get_button(7) == False and button_7_pressed == True:
                    button_7_pressed = False
                    print("button 7 released")
                    client.publish("/AQB/in/SW_btn_u", "7")
                elif joystick.get_button(8) == False and button_8_pressed == True:
                    button_8_pressed = False
                    print("button 8 released")
                    client.publish("/AQB/in/SW_btn_u", "8")
                elif joystick.get_button(9) == False and button_9_pressed == True:
                    button_9_pressed = False
                    print("button 9 released")
                    client.publish("/AQB/in/SW_btn_u", "9")
                elif joystick.get_button(10) == False and button_10_pressed == True:
                    button_10_pressed = False
                    print("button 10 released")
                   # client.publish("/AQB/in/SW_btn_u", "10")
                elif joystick.get_button(11) == False and button_11_pressed == True:
                    button_11_pressed = False
                    print("button 11 released")
                    client.publish("/AQB/in/SW_btn_u", "s")
                elif joystick.get_button(12) == False and button_12_pressed == True:
                    button_12_pressed = False
                    print("button 12 released")
                    client.publish("/AQB/in/SW_btn_u", "12")
            elif event.type == pygame.JOYAXISMOTION:
                if not axis_temp_check:
                    axis_0_temp = 1.0
                    axis_1_temp = 1.0
                    axis_2_temp = 1.0
                    axis_temp_check = True
                    print("Values set to 1")
                axis_0_current = round(joystick.get_axis(0), 1) * 10
                axis_1_current = round(joystick.get_axis(1), 1) * 10
                axis_2_current = round(joystick.get_axis(2), 1) * 10
                if axis_0_current != axis_0_temp:
                    axis_0_temp = axis_0_current
                    axis_0_temp = str(axis_0_temp)
                    print(axis_0_temp)
                    client.publish("/AQB/in/SW_axs_0", axis_0_temp)
                    axis_0_temp = axis_0_current
                if axis_1_current != axis_1_temp:
                    axis_1_temp = axis_1_current
                    axis_1_temp = str(axis_1_temp)
                    print(axis_1_temp)
                    client.publish("/AQB/in/SW_axs_1", axis_1_temp)
                    axis_1_temp = axis_1_current
                if axis_2_current != axis_2_temp:
                    axis_2_temp = axis_2_current
                    axis_2_temp = str(axis_2_temp)
                    print(axis_2_temp)
                    client.publish("/AQB/in/SW_axs_2", axis_2_temp)
                    axis_2_temp = axis_2_current

        #
        # DRAWING STEP
        #
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
        textPrint.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            textPrint.tprint(screen, "Joystick {}".format(i))
            textPrint.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            textPrint.tprint(screen, "Joystick name: {}".format(name))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.tprint(screen, "Number of axes: {}".format(axes))
            textPrint.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.tprint(screen,
                                 "Button {:>2} value: {}".format(i, button))
            textPrint.unindent()

            hats = joystick.get_numhats()
            textPrint.tprint(screen, "Number of hats: {}".format(hats))
            textPrint.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
            textPrint.unindent()

            textPrint.unindent()

        #
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second.
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


def custom_controller_func():
    sw_ctrl.start()


sw_ctrl = multiprocessing.Process(target=start_steering_wheel_ctrl)

logging.basicConfig(level=logging.INFO)  # Error Logging #
QOS = 0  # QoS Level keep at 0
CLEAN_SESSION = True
client = mqtt.Client("AQB-CtrlP", False)  # create client object
client.on_subscribe = on_subscribe  # assign function to callback
client.on_disconnect = on_disconnect  # assign function to callback
client.on_connect = on_connect  # assign function to callback
client.on_message = on_message  # when a payload is received this function runs

#########################################################################
#                                                                       #
#  Below are the functions specific for each event that is called from  #
#   main_window.py such as when you click a button and it sends a time  #
#                       value to the MQTT broker.                       #
#                                                                       #
#########################################################################


def forward():
    print("forward")  # Diagnostic purposes
    client.publish("/AQB/in", "1")


def back():
    print("back")  # Diagnostic purposes
    client.publish("/AQB/in", "2")


def left():
    print("left")  # Diagnostic purposes
    client.publish("/AQB/in", "l")


def right():
    print("right")  # Diagnostic purposes
    client.publish("/AQB/in", "r")


def stop():
    print("stop")  # Diagnostic purposes
    client.publish("/AQB/in", "c")


def light_toggle():
    print("Light Toggle")
    client.publish("/AQB/in", "8")


def key_pressed(event):
    global arrow_forward_button
    key = event.keysym
    print("You hit the " + key + " Key")
    if key == "Up":
        forward()
    if key == "Down":
        back()
    if key == "Right":
        right()
    if key == "Left":
        left()
    if key == "space":
        stop()


def upload_steering_align():
    temp_l = steering_align_left_input.get()
    temp_r = steering_align_right_input.get()
    if temp_l != "":
        swa_left = str(float(temp_l))
        print("Uploading Left: " + swa_left)
        client.publish("/AQB/in/swal", swa_left)
    if temp_r != "":
        swa_right = str(float(temp_r))
        print("Uploading Right: " + swa_right)
        client.publish("/AQB/in/swar", swa_right)

    #client.publish("/AQB/in/swar", swa_right)

#########################################################################
#                                                                       #
#                         Tkinter Setup Code                            #
#                                                                       #
#########################################################################
my_window = Tk()
# Key listener setup code #
my_window.bind("<Key>", key_pressed)

#########################################################################
#                                                                       #
#                           String Variables                            #
#                                                                       #
#########################################################################

power_val = StringVar()
power_val.set("HIGH")
power_val.trace('w', power_val_update)

ctrl_mode_val = StringVar()
ctrl_mode_val.set("Sticky")
ctrl_mode_val.trace('w', ctrl_mode_val_update)

steering_align_left_input = StringVar()
steering_align_right_input = StringVar()

#########################################################################
#                                                                       #
#                         Geometry Management                           #
#                                                                       #
#########################################################################


def main_window_setup():
    global bg_photo  # This stops the garbage collector from deleting the photo #
    global video_frame
    global power_sel
    global lte_1_pic
    global bottom_frame
    global four_g_pic
    global three_g_pic
    global arrow_forward_button
    global steering_align_right_input
    global steering_align_left_input
    my_window.title("AQB Desktop v1.0")
    # screen_width = my_window.winfo_screenwidth()
    # screen_height = my_window.winfo_screenheight()
    width = 1450
    height = 900
    my_window.geometry(f'{width}x{height}')
    my_window.iconbitmap('media/A-IOT-QB-Icon.ico')
    my_window.configure(background='grey')
    my_window.grid_rowconfigure(1, weight=1)
    my_window.grid_columnconfigure(0, weight=1)

    # Background Photo Setup (needs to be done first otherwise it wont be put at the back) #
    bg_photo = PhotoImage(file="media/bg_main_window.png")
    bg_photo_label = Label(my_window, image=bg_photo)
    bg_photo_label.place(x=0, y=0)

    # Organise sections of GUI into frames #
    top_frame = Frame(my_window, bg='gray')
    bottom_frame = Frame(my_window, bg="dim gray")
    video_frame = Frame(my_window, bg="dim gray")
    left_frame = Frame(my_window, bg="dim gray")
    right_frame = Frame(my_window, bg="dim gray")
    video_option_frame = Frame(my_window, bg="dim gray")
    # Grid all the frames in place #
    top_frame.grid(row=0, column=0, columnspan=3, sticky="n")
    video_frame.grid(row=1, column=0, sticky="n")
    video_option_frame.grid(row=2, column=0, sticky="sw")
    left_frame.grid(row=1, column=0, sticky="nw")
    right_frame.grid(row=1, column=0, sticky="ne")
    bottom_frame.grid(row=3, column=0, columnspan=3, sticky="sw")

    # top_frame Widget Creation #

    # top_frame Widget Placement #

    # video_frame Widget Creation #

    # video_frame Widget Placement #

    # left_frame Widget Creation #
    bat_lvl_lab = Message(left_frame, text="Battery Level:", width=110, justify=CENTER, relief=RAISED, bg="Red")
    bat_lvl = Scale(left_frame, from_=100, to=0, orient=VERTICAL, width=30, relief=SUNKEN)
    bat_lvl.config(state='disabled')
    power_usage_lab = Message(left_frame, text="Power Usage:", width=60, justify=CENTER, relief=SUNKEN, bg="Green")
    power_in_lab = Message(left_frame, text="Power Input:", width=60, justify=CENTER, relief=SUNKEN, bg="Green")
    power_usage = Scale(left_frame, from_=100, to=0, orient=VERTICAL, width=15, relief=SUNKEN)
    power_usage.config(state='disabled')
    power_in = Scale(left_frame, from_=100, to=0, orient=VERTICAL, width=15, relief=SUNKEN)
    power_in.config(state='disabled')
    power_eta_lab = Message(left_frame, text="ETA Battery: 2 Hours", width=90, justify=CENTER, relief=RAISED)
    petrol_lab = Message(left_frame, text="Petrol Fuel Level:", width=90, justify=CENTER, relief=RAISED, bg="Red")
    fuel_lvl = Scale(left_frame, from_=100, to=0, orient=VERTICAL, width=30, relief=SUNKEN)
    fuel_lvl.config(state='disabled')
    fuel_eta_lab = Message(left_frame, text="ETA Petrol: 1 Hour", width=90, justify=CENTER, relief=RAISED)
    # left_frame Widget Placement #
    bat_lvl_lab.grid(row=0, column=0, columnspan=2, pady=(0, 5))
    bat_lvl.grid(row=1, column=0, sticky='news', columnspan=2)
    power_usage_lab.grid(row=3, column=0, pady=(20, 5))
    power_usage.grid(row=4, column=0)
    power_in_lab.grid(row=3, column=1, pady=(20, 5))
    power_in.grid(row=4, column=1)
    power_eta_lab.grid(row=5, column=0, columnspan=2, pady=(5, 0))
    petrol_lab.grid(row=6, column=0, columnspan=2, pady=(20, 5))
    fuel_lvl.grid(row=7, column=0, sticky='news', columnspan=2)
    fuel_eta_lab.grid(row=8, column=0, sticky='news', columnspan=2, pady=(5, 0))

    # right_frame Widget Creation #
    power_sel_label = Label(right_frame, text="Performance:", justify=CENTER, relief=RAISED, font="bold")
    power_sel = OptionMenu(right_frame, power_val, "HIGH", "MED", "LOW")
    power_sel.config(bg="RED")
    ctrl_mode_sel_label = Label(right_frame, text="Controller Mode:", justify=CENTER, relief=RAISED, font="bold")
    ctrl_mode_sel = OptionMenu(right_frame, ctrl_mode_val, "Sticky", "Momentary", "Steering Wheel")
    ctrl_mode_sel.config(bg="GRAY")
    steering_align_label = Label(right_frame, text="Steering Alignment:", justify=CENTER, relief=RAISED, font="bold")
    steering_align_left_input = Entry(right_frame, text="Rotation Map Left:", justify=CENTER, relief=RAISED, font="bold")
    steering_align_right_input = Entry(right_frame, text="Rotation Map Right:", justify=CENTER, relief=RAISED, font="bold")
    steering_align_left_lab = Label(right_frame, text="Left:", justify=CENTER, relief=RAISED, font="bold")
    steering_align_right_lab = Label(right_frame, text="Right:", justify=CENTER, relief=RAISED, font="bold")
    steering_align_right_send = Button(right_frame, text='Upload', bg="dim gray", command=upload_steering_align)
    arrow_forward_pic = PhotoImage(file="media/arrow_forward.png")
    arrow_back_pic = PhotoImage(file="media/arrow_down.png")
    arrow_left_pic = PhotoImage(file="media/arrow_left.png")
    arrow_right_pic = PhotoImage(file="media/arrow_right.png")
    stop_sign_pic = PhotoImage(file="media/stop_sign.png")
    arrow_forward_button = Button(right_frame, image=arrow_forward_pic, bg="dim gray", command=forward)
    arrow_back_button = Button(right_frame, image=arrow_back_pic, bg="dim gray", command=back)
    arrow_left_button = Button(right_frame, image=arrow_left_pic, bg="dim gray", command=left)
    arrow_right_button = Button(right_frame, image=arrow_right_pic, bg="dim gray", command=right)
    stop_button = Button(right_frame, image=stop_sign_pic, bg="dim gray", command=stop)

    # right_frame Widget Placement #
    power_sel_label.grid(row=0, column=3)
    power_sel.grid(row=0, column=4)
    ctrl_mode_sel_label.grid(row=1, column=3)
    ctrl_mode_sel.grid(row=1, column=4)
    steering_align_label.grid(row=2, column=4, sticky='s')
    steering_align_left_input.grid(row=3, column=4, sticky='w')
    steering_align_right_input.grid(row=4, column=4, sticky='w')
    steering_align_left_lab.grid(row=3, column=3, sticky='e')
    steering_align_right_lab.grid(row=4, column=3, sticky='e')
    steering_align_right_send.grid(row=4, column=3, sticky='n')
    arrow_forward_button.grid(row=1, column=1)
    arrow_back_button.grid(row=3, column=1)
    arrow_left_button.grid(row=2, column=0)
    arrow_right_button.grid(row=2, column=2)
    stop_button.grid(row=2, column=1)

    # video_frame_options Widget Creation #
    light_toggle_button = Button(video_option_frame, text="Toggle Lights", bg="dim gray", command=light_toggle)
    start_video_but = Button(video_option_frame, text="Start Video")
    # video_frame_options Widget Placement #
    light_toggle_button.grid(row=0, column=0, pady=(0, 40))
    start_video_but.grid(row=0, column=1, pady=(0, 40))

    # bottom_frame Widget Creation #
    net_stat_label = Label(bottom_frame, text="Network Status:", justify=CENTER, relief=RAISED, font="bold")
    ping_server_label = Message(bottom_frame, text=" Ping To Server: 500ms ", justify=CENTER, relief=RAISED, bg="black",
                                fg="white", width=190)
    ping_traverse_label = Message(bottom_frame, text=" Ping To AQB: 800ms   ", justify=CENTER, relief=RAISED,
                                  bg="black", fg="white", width=190)
    bandwidth_stat_label = Label(bottom_frame, text="  Network Bandwidth:  ", justify=CENTER, relief=RAISED, font="bold")
    bandwidth_out_label = Message(bottom_frame, text=" Out: 30 bps     ", justify=CENTER, relief=RAISED, bg="black",
                                  fg="white", width=190)
    bandwidth_in_label = Message(bottom_frame, text=" In: 50 bps      ", justify=CENTER, relief=RAISED, bg="black",
                                 fg="white", width=190)
    signal_strength_label = Message(bottom_frame, text="Signal Strength:", justify=CENTER, relief=RAISED, bg="white",
                                 fg="black", width=190)
    lte_0_pic = PhotoImage(file="media/lte-0.png")
    lte_1_pic = PhotoImage(file="media/lte-1.png")
    lte_2_pic = PhotoImage(file="media/lte-2.png")
    lte_3_pic = PhotoImage(file="media/lte-3.png")
    lte_4_pic = PhotoImage(file="media/lte-4.png")
    signal_strength = Label(bottom_frame, image=lte_0_pic)
    signal_type_label = Message(bottom_frame, text="Connection Via:", justify=CENTER, relief=RAISED, bg="white",
                                 fg="black", width=190)
    wifi_pic = PhotoImage(file="media/wifi_symbol.png")
    three_g_pic = PhotoImage(file="media/3g_symbol.png")
    four_g_pic = PhotoImage(file="media/4g_symbol.png")
    signal_type = Label(bottom_frame, image=wifi_pic)

    # bottom_frame Widget Placement #
    net_stat_label.grid(row=0, column=0, pady=(0, 0), padx=(0, 20), sticky='n')
    ping_server_label.grid(row=1, column=0, sticky='nw')
    ping_traverse_label.grid(row=2, column=0, sticky='nw', pady=(0, 40))
    bandwidth_stat_label.grid(row=0, column=1, pady=(0, 0), padx=(0, 0), sticky='n')
    bandwidth_out_label.grid(row=1, column=1, sticky='nw')
    bandwidth_in_label.grid(row=2, column=1, sticky='nw', pady=(0, 40))
    signal_strength_label.grid(row=0, column=2, sticky='nw', rowspan=2)
    signal_strength.grid(row=1, column=2, sticky='nw', rowspan=2)
    signal_type_label.grid(row=0, column=3, sticky='nw', rowspan=2)
    signal_type.grid(row=1, column=3, sticky='nw', rowspan=2)
    # Runs the main loop that updates the GUI #
    loop_main_window()


# Runs the main loop that updates the GUI #
def loop_main_window():
    if online_mode:
        print("Starting in Online Mode")
    else:
        print("Starting in Offline Mode")
    my_window.mainloop()