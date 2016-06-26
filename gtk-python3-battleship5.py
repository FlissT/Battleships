import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

from random import randint

class Game(object):
    def __init__(self):
        self.board = []
        for x in range(4):  
            self.board.append(["."] *4)
            
        self.ships = []
        
        for x in range(3):
            row = randint (0, len(self.board)-1)
            col = randint (0, len(self.board)-1)
            self.ships.append((row, col))

    def print_board(self):
        for row in self.board:
            print (" ".join(row))

    def fire(self, row, col):
        if (row, col) in self.ships:
            self.board[row][col] = "X"
            return True
        else:
            self.board[row][col] = "O"
            return False

        
#name = str(input("What is your name?" " "))      
#print ("Hello" " " + name + "!" + " " "Let's play Battleships!")


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

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

        self.set_title("Battleships")
        self.msg_label = Gtk.Label()
        self.board_label = Gtk.Label("Let's play battleships!")
        
        self.button1 = Gtk.Button()
        self.button2 = Gtk.Button()
        self.button3 = Gtk.Button()
        self.button4 = Gtk.Button()

        vbox = Gtk.VBox()
        bbox = Gtk.HButtonBox()
        bbox.add(self.button1)
        bbox.add(self.button2)
        bbox.add(self.button3)
        bbox.add(self.button4)
        vbox.add(self.board_label)
        vbox.add(self.msg_label)
        vbox.add(bbox)
        self.add(vbox)

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

        self.set_button_labels(None, None, None, "Start game")
        self.button4_connection = self.button4.connect("clicked", on_click)

    def run_game(self):
        self.update_board_label()
        print (self.game.ships) #just for testing
        while self.turn < self.max_turns:
            self.msg_label.set_text("Guess the column: ")
            self.set_button_labels("A", "B", "C", "D")
            clicked_button = self.wait_for_click2()
            if clicked_button == self.button1:
                guess_col = 0
            if clicked_button == self.button2:
                guess_col = 1
            if clicked_button == self.button3:
                guess_col = 2
            if clicked_button == self.button4:
                guess_col = 3  
            #print(clicked_button.get_label())
            
            self.msg_label.set_text("Guess the row: ")
            self.set_button_labels("1", "2", "3", "4")
            clicked_button = self.wait_for_click2()
            if clicked_button == self.button1:
                guess_row = 0
            if clicked_button == self.button2:
                guess_row = 1
            if clicked_button == self.button3:
                guess_row = 2
            if clicked_button == self.button4:
                guess_row = 3
            #print(clicked_button.get_label())

            if([guess_col, guess_row]) in self.guesses:
                self.msg_label.set_text("You've already guessed that one!")
                self.set_button_labels(None, None, None, "Ok")
                clicked_button = self.wait_for_click2()
                continue

            if (guess_col, guess_row) in self.game.ships:
                self.game.board[guess_col][guess_row] = "X"
                self.update_board_label()
                self.msg_label.set_text("You sunk my battleship!")
                self.set_button_labels(None, None, None, "Ok")
                clicked_button = self.wait_for_click2()
                self.hits +=1
                
            else:
                self.game.board[guess_col][guess_row] = "O"
                self.update_board_label()
                self.msg_label.set_text("You missed my battleship!")
                self.set_button_labels(None, None, None, "Ok")
                clicked_button = self.wait_for_click2()
                
            self.guesses.append([guess_col, guess_row])  
            
            if self.hits == 3:
                self.won = True
                break

            self.turn += 1

        if self.won:
            self.msg_label.set_text("Yay! You win!")
        else:
            self.msg_label.set_text("You lose")
        
    def update_board_label(self):
        text = ""
        text += "   A B C D"
        text += "\n"
        i = 1
        for row in self.game.board:
            text += str(i) + "  " + "  ".join(row) + "\n"
            i += 1
        self.board_label.set_text(text)
        

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

    def set_button_labels(self, label1, label2, label3, label4):
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

    def connect_buttons(self, label1, func1, label2, func2, label3, func3, label4, func4):
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
        self.pause_loop.run()
        return self.clicked_button
                
    def wait_for_click(self, okay_function):
        def on_okay(button):
            self.disconnect_buttons()
            okay_function()            
        self.connect_buttons((""), None, (""), None, (""), None, ("Okay"), on_okay)
        
window = MyWindow()

Gtk.main()   


    
