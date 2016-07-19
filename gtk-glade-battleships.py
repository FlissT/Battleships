#using a 9-button grid and glade
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

from random import randint

class Game(object):
    def __init__(self):
        self.ships = []

        for x in range(3):
            battleship = randint (1, 9)
            if battleship not in self.ships:
                self.ships.append(battleship)
    

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.builder = Gtk.Builder()
        self.builder.add_from_file("battleships-gui.glade")
        box2 = self.builder.get_object("box2")
        self.add(box2)

        self.button1 = self.builder.get_object("button1")
        self.button2 = self.builder.get_object("button2")
        self.button3 = self.builder.get_object("button3")
        self.button4 = self.builder.get_object("button4")
        self.button5 = self.builder.get_object("button5")
        self.button6 = self.builder.get_object("button6")
        self.button7 = self.builder.get_object("button7")
        self.button8 = self.builder.get_object("button8")
        self.button9 = self.builder.get_object("button9")

        game_label = self.builder.get_object("label3") 

        self.game = Game()
        self.guesses = []    
        self.hits = 0
        self.won = False
        self.max_turns = 4
        self.turn = 0

        self.button1_connection = 0
        self.button2_connection = 0
        self.button3_connection = 0
        self.button4_connection = 0
        self.button5_connection = 0
        self.button6_connection = 0
        self.button7_connection = 0
        self.button8_connection = 0
        self.button9_connection = 0
        
        self.set_title("Battleships!")
        self.msg_label = self.builder.get_object("label2")

        self.lets_play()

        self.pause_loop = GLib.MainLoop()

        self.show_all()
        self.connect("delete-event", self.on_quit)

    def on_quit(self, widget, event):
        Gtk.main_quit()
        self.pause_loop.quit()

    def lets_play(self):
        print ("play")
        self.disconnect_buttons()

        def on_click(button):
            self.disconnect_buttons()
            self.run_game()

        self.set_button_labels(None, None, None, None, "Start", None, None, None, None)
        self.button5_connection = self.button5.connect("clicked", on_click)

    def run_game(self):
        while self.turn < self.max_turns:
            self.msg_label.set_text("Take a guess: ")
            self.set_button_labels(" ", " ", " ", " ", " ", " ", " ", " ", " ")
            clicked_button = self.wait_for_click2()
            if clicked_button == self.button1:
                guess_ship = 1
            if clicked_button == self.button2:
                guess_ship = 2
            if clicked_button == self.button3:
                guess_ship = 3
            if clicked_button == self.button4:
                guess_ship = 4
            if clicked_button == self.button5:
                guess_ship = 5
            if clicked_button == self.button6:
                guess_ship = 6
            if clicked_button == self.button7:
                guess_ship = 7
            if clicked_button == self.button8:
                guess_ship = 8
            if clicked_button == self.button9:
                guess_ship = 9                

            if guess_ship in self.guesses:
                self.msg_label.set_text("You've already guessed that one!")
                self.set_button_labels(None, None, None, None, "Ok", None, None, None, None)
                clicked_button = self.wait_for_click2()
                continue

            if guess_ship in self.game.ships:
                self.msg_label.set_text("You sunk my battleship!" + " " + u'\U0001F4A3')   
                if clicked_button == self.button1:
                    self.button1.set_label(u'\U0001F6A2')
                    clicked_button = self.wait_for_click2()  
                    
                if clicked_button == self.button2:
                    self.set_button_labels(None, u'\U0001F6A2', None, None, None, None, None, None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button3:
                    self.set_button_labels(None, None, u'\U0001F6A2', None, None, None, None, None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button4:
                    self.set_button_labels(None, None, None, u'\U0001F6A2', None, None, None, None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button5:
                    self.set_button_labels(None, None, None, None, u'\U0001F6A2', None, None, None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button6:
                    self.set_button_labels(None, None, None, None, None,  u'\U0001F6A2', None, None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button7:
                    self.set_button_labels(None, None, None, None, None, None, u'\U0001F6A2', None, None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button8:
                    self.set_button_labels(None, None, None, None, None, None, None, u'\U0001F6A2', None)
                    clicked_button = self.wait_for_click2()
                    
                if clicked_button == self.button9:
                    self.set_button_labels(None, None, None, None, None, None, None, None, u'\U0001F6A2')
                    clicked_button = self.wait_for_click2()
                    
                self.set_button_labels(None, None, None, None, "Ok", None, None, None, None)
                clicked_button = self.wait_for_click2()
                self.hits +=1
                
            else:
                self.msg_label.set_text("You missed my battleship!" + " " + u'\U0001F61E')
                self.set_button_labels(None, None, None, None, "Ok", None, None, None, None)
                clicked_button = self.wait_for_click2()
                
            self.guesses.append(guess_ship)  
            
            if self.hits == 3:
                self.won = True
                break

            self.turn += 1

        if self.won:
            self.msg_label.set_text("Yay! You win!")
            self.set_button_labels(None, None, None, None, "Play again", None, None, None, None)
            clicked_button = self.wait_for_click2()
            if clicked_button == self.button5:
                self.run_game()
                self.rand_num()
                    
                
        else:
            self.msg_label.set_text("You lose")
            self.set_button_labels(None, None, None, None, "Play again", None, None, None, None)
            clicked_button = self.wait_for_click2()
            if clicked_button == self.button5:
                self.run_game()
                self.rand_num()

    def disconnect_buttons(self):
        if self.button1_connection > 0:
            self.button1.disconnect(self.button1_connection)
            self.button1_connection = 0
        if self.button2_connection > 0:
            self.button2.disconnect(self.button2_connection)
            self.button2_connection = 0
        if self.button3_connection > 0:
            self.button3.disconnect(self.button3_connection)
            self.button3_connection = 0
        if self.button4_connection > 0:
            self.button4.disconnect(self.button4_connection)
            self.button4_connection = 0
        if self.button5_connection > 0:
            self.button5.disconnect(self.button5_connection)
            self.button5_connection = 0
        if self.button6_connection > 0:
            self.button6.disconnect(self.button6_connection)
            self.button6_connection = 0
        if self.button7_connection > 0:
            self.button7.disconnect(self.button7_connection)
            self.button7_connection = 0
        if self.button8_connection > 0:
            self.button8.disconnect(self.button8_connection)
            self.button8_connection = 0
        if self.button9_connection > 0:
            self.button9.disconnect(self.button9_connection)
            self.button9_connection = 0

    def set_button_labels(self, label1, label2, label3, label4, label5, label6, label7, label8, label9):
        if label1:
            self.button1.set_sensitive(True)
            self.button1.set_label(label1)
        else:
            self.button1.set_sensitive(False)
            self.button1.set_label("")
            
        if label2:
            self.button2.set_sensitive(True)
            self.button2.set_label(label2)
        else:
            self.button2.set_sensitive(False)
            self.button2.set_label("")
        
        if label3:
            self.button3.set_sensitive(True)
            self.button3.set_label(label3)
        else:
            self.button3.set_sensitive(False)
            self.button3.set_label("")
            
        if label4:
            self.button4.set_sensitive(True)
            self.button4.set_label(label4)
        else:
            self.button4.set_sensitive(False)
            self.button4.set_label("")
            
        if label5:
            self.button5.set_sensitive(True)
            self.button5.set_label(label5)
        else:
            self.button5.set_sensitive(False)
            self.button5.set_label("")

        if label6:
            self.button6.set_sensitive(True)
            self.button6.set_label(label6)
        else:
            self.button6.set_sensitive(False)
            self.button6.set_label("")

        if label7:
            self.button7.set_sensitive(True)
            self.button7.set_label(label7)
        else:
            self.button7.set_sensitive(False)
            self.button7.set_label("")

        if label8:
            self.button8.set_sensitive(True)
            self.button8.set_label(label8)
        else:
            self.button8.set_sensitive(False)
            self.button8.set_label("")

        if label9:
            self.button9.set_sensitive(True)
            self.button9.set_label(label9)
        else:
            self.button9.set_sensitive(False)
            self.button9.set_label("")
            

    def connect_buttons(self, label1, func1, label2, func2, label3, func3, label4, func4, label5, func5, label6, func6, label7, func7, label8, func8, label9, func9):
        self.disconnect_buttons()
        if label1:
            self.button1.set_sensitive(True)
            self.button1.set_label(label1)
        else:
            self.button1.set_sensitive(False)
            self.button1.set_label("")
            
        if func1:
            self.button1_connection = self.button1.connect(("clicked"), func1)
            
        if label2:
            self.button2.set_sensitive(True)
            self.button2.set_label(label2)
        else:
            self.button2.set_sensitive(False)
            self.button2.set_label("")
            
        if func2:
            self.button2_connection = self.button2.connect(("clicked"), func2)
        
        if label3:
            self.button3.set_sensitive(True)
            self.button3.set_label(label3)
        else:
            self.button3.set_sensitive(False)
            self.button3.set_label("")
            
        if func3:
            self.button3_connection = self.button3.connect(("clicked"), func3)

        if label4:
            self.button4.set_sensitive(True)
            self.button4.set_label(label4)
        else:
            self.button4.set_sensitive(False)
            self.button4.set_label("")
            
        if func4:
            self.button4_connection = self.button4.connect(("clicked"), func4)

        if label5:
            self.button5.set_sensitive(True)
            self.button5.set_label(label5)
        else:
            self.button5.set_sensitive(False)
            self.button5.set_label("")
            
        if func5:
            selfbutton5_connection = self.button5.connect(("clicked"), func5)

        if label6:
            self.button6.set_sensitive(True)
            self.button6.set_label(label6)
        else:
            self.button6.set_sensitive(False)
            self.button6.set_label("")
            
        if func6:
            self.button6_connection = self.button6.connect(("clicked"), func6)

        if label7:
            self.button7.set_sensitive(True)
            self.button7.set_label(label7)
        else:
            self.button7.set_sensitive(False)
            self.button7.set_label("")
            
        if func7:
            self.button7_connection = self.button7.connect(("clicked"), func7)

        if label8:
            self.button8.set_sensitive(True)
            self.button8.set_label(label8)
        else:
            self.button8.set_sensitive(False)
            self.button8.set_label("")
            
        if func8:
            self.button8_connection = self.button8.connect(("clicked"), func8)

        if label9:
            self.button9.set_sensitive(True)
            self.button9.set_label(label9)
        else:
            self.button9.set_sensitive(False)
            self.button9.set_label("")
            
        if func9:
            self.button9_connection = self.button9.connect(("clicked"), func9)


    def wait_for_click2(self):
        self.clicked_button = None
        def on_click(button):
            self.disconnect_buttons()
            self.pause_loop.quit()
            self.clicked_button = button
        self.disconnect_buttons()
        self.button1_connection = self.button1.connect("clicked", on_click)
        self.button2_connection = self.button2.connect("clicked", on_click)
        self.button3_connection = self.button3.connect("clicked", on_click)
        self.button4_connection = self.button4.connect("clicked", on_click)
        self.button5_connection = self.button5.connect("clicked", on_click)
        self.button6_connection = self.button6.connect("clicked", on_click)
        self.button7_connection = self.button7.connect("clicked", on_click)
        self.button8_connection = self.button8.connect("clicked", on_click)
        self.button9_connection = self.button9.connect("clicked", on_click)
        self.pause_loop.run()
        return self.clicked_button
                
    def wait_for_click(self, okay_function):
        def on_okay(button):
            self.disconnect_buttons()
            okay_function()            
        self.connect_buttons((""), None, (""), None, (""), None, (""), None, (""), None, (""), None, (""), None, (""), None, ("Okay"), on_okay)
        
window = MyWindow()

Gtk.main()   


    
