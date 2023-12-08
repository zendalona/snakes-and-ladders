###########################################################################
#   SALG - SNAKE AND LADDER GAME 
#
#    Copyright (C) 2022-2023 ARCHANA.V S <archanavs1211@gmail.com>
#    
#    FILL-VTB-INFO 
#    Supervised by Zendalona(2022-2023)
#
#    Project home page : www.zendalona.com/SNAKE AND LADDER GAME
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################


import cairo ,speechd ,math,time,threading
import gi
import random
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import re
import os
from gi.repository import Gtk,Gdk,GLib
from gi.repository import Atk
import pygame

Gst.init(None)

class Player:
    def __init__(self, name, position,color,chance):
        self.name = name
        self.position = position
        self.color=color
        self.chance=chance
        
class Board:
    def __init__(self, board_num,diff):
        self.board_num = board_num
        if board_num ==1:
           
            self.ladder_coordinates = [ [ (6,25)] ,[(13,65)] , [(21,59)] ,  [(50,70)] , [(64,96)] , [(68,86)] , [(80,98)]]
            self.board_color=[[(1,1,1),(0,0,1)]]
            self.snake_heads = [ [(23 , 5 ),(1,0,0)], [(35 , 7),(0,1,1)] , [(49 , 12 ),(1,1,0)], [(56 , 24 ),(0,0.5,1)],
								[(79 , 60 ),(0,1,0.5)], [(89 , 55 ),(0.9,0.5,0.5)], [(94 , 52),(1,0,0)] , [(99 , 37),(1,0.5,0)]]
             
            
        if board_num==2:
            
            self.ladder_coordinates = [ [(8,28)] , [(17,57)] , [(22,59)] ,  [(50,70)] , [(65,96)] , [(53,88)] , [(78,98)]]
            self.board_color=[[(1,1,1),(0.3,0.5,0)]]
            self.snake_heads = [ [(38 , 4 ),(1,1,0.3)], [(34, 5),(1,0.5,0.6)] , [(48 , 12 ),(1,1,0)], [(56 , 24 ),(0,1,1)], 
								[(79 , 60 ),(0,0.5,1)], [(87 , 55 ),(1,0,0)], [(94 , 52),(0.9,0.5,0.5)] , [(97 , 37),(0,1,0.6)]]
           
        if board_num==3:
             self.ladder_coordinates = [ [(19,37)] , [(11,47)] , [(43,75)] ,  [(52,74)] , [(71,93)] , [(80,99)] , [(32,70)]]
             self.board_color=[[(1,1,1),(1,0,1)]]
             self.snake_heads=[ [(13,5),(1,0.5,0.6)],[(25,7),(0,1,0.3)],[(57,2),(0,1,1)],[(54,36),(0.4,0.8,0.3)],[(78,40),(0.6,0,0.6)],
								[(84,55),(0.7,0,0.3)],[(96,73),(0.4,0.8,0.6)],[(90,48),(0.4,0.8,0)]]
             
        if board_num==4:
             self.ladder_coordinates = [ [(4,24)] , [(10,50)] , [(52,92)] ,  [(38,63)] , [(47,87)] , [(55,95)] , [(59,99)]]
             self.board_color=[[(1,1,1),(0.5,0.5,0.4)]]
             self.snake_heads=[ [(26,5),(1,0.5,0.6)],[(30,7),(0,1,0.3)],[(42,18),(0.5,1,0.3)],[(54,35),(0,1,1)],[(49,28),(0.4,0.8,0.3)],
								[(81,62),(0.6,0,0.6)],[(86,73),(0.7,0,0.3)],[(85,64),(0.4,0.8,0.6)]]
            
class GameBoard(Gtk.Window):
    def __init__(self,board_num,num_players,players_names,mode):
        Gtk.Window.__init__(self, title="Game Board")

        pygame.mixer.init()

        if mode ==0:
            self.add_mode=False
        else:
            self.add_mode=True  
       
        self.count = num_players
        self.i=2
        color_rgb = Gdk.RGBA(1, 1, 1, 1)
        
        self.speech = speechd.SSIPClient('game_board')  
        self.dice_number=1
        self.typed_value =0
        self.correct_answer=0
       
        self.board_num = board_num
        self.connect("destroy", self.cleanup)
        
        vbox = Gtk.VBox()
        self.add(vbox)
        screen = Gdk.Screen.get_default()
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request((self.width*80)/100,(self.height*80)/100)
        drawing_area.connect("draw", self.draw_board)
        drawing_area.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)  
        
        
        self.current_cell= [9, 0]
       
        vbox.pack_start(drawing_area, False, True, 0)

        self.status_bar = AccessibleStatusbar()
        
        vbox.pack_start(self.status_bar, False, True, 0)

        vbox.show_all()
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.players = [] 
        self.num_players = num_players
        self.players_names=players_names
       
        self.create_players()
        self.cwd = os.getcwd()
        self.data_directory = "/usr/share/SnakesAndLadders"

        # Load and play the background music
        pygame.mixer.music.load(self.data_directory+'/sounds/bgmusic.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.player1 = Gst.ElementFactory.make('playbin', 'player1')
        # Playing starting sound
        self.play_file("start")
        time.sleep(1)
        self.notify(self.players_names[0]+" can roll dice by pressing the space bar")

        Gtk.main()
   
    def create_players(self):
        colors = [(0.5, 0.3, 0), (0, 0.7, 0.4), (0.2, 0, 0.5), (0.6, 0.7, 0),(0.0,0.9,0.2)] 
        
        for i in range(self.num_players):
            player_name = self.players_names[i]
            player_color = colors[i % len(colors)] 
            player = Player(player_name, [9, -1],player_color,1)  
            self.players.append(player)
        
        if self.num_players == 1:
            player = Player("Machine", [9, -1], colors[1 % len(colors)],1)  
            self.players.append(player)
            self.num_players=2
            self.count =2
    
    def draw_board(self, widget, cr):
        self.window_width = widget.get_allocated_width() - 300
        self.window_height = widget.get_allocated_height()
      
        # Calculate the size of each square based on the window dimensions
        self.square_size = min(self.window_width // 10, self.window_height  // 10)
        self.diff = self.square_size - 50
        board_size = self.square_size * 10
        self.Board = Board(self.board_num,self.diff)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
    
        cr.set_source_rgb(0, 0, 0)
        for i in range(10):
            for j in range(10):
                cr.rectangle(i * self.square_size, j * self.square_size, self.square_size, self.square_size)
                for k in self.Board.board_color:
                    c1,c2,c3=k[0]
                    c4,c5,c6=k[1]
                
                if (i+j) % 2 == 0:
                    cr.set_source_rgb(c1,c2,c3)
                else:
                    cr.set_source_rgb(c4,c5,c6)
                cr.fill_preserve()
                cr.stroke()
    
        num = 100
        for i in range(10):
            if i % 2 == 0:
                for j in range(10):
                    x = j * self.square_size
                    y = i * self.square_size
                    cr.set_source_rgb(0, 0, 0)
                    cr.rectangle(x, y, self.square_size, self.square_size)
                    cr.stroke()
                    cr.set_source_rgb(0, 0, 0)
                    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    cr.set_font_size(20 +self.diff // 3)
                    cr.move_to(x + self.square_size/2 -6, y + self.square_size/2)
                    cr.show_text(str(num))
                    num -= 1
            else:
                for j in range(10):
                    x = (9 - j) * self.square_size
                    y = i * self.square_size
                    cr.set_source_rgb(0, 0, 0)
                    cr.rectangle(x, y, self.square_size, self.square_size)
                    cr.stroke()
                    cr.set_source_rgb(0, 0, 0)
    
                    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    cr.set_font_size(20+ self.diff // 3)
                    cr.move_to(x + self.square_size/2 - 6, y + self.square_size/2)
                    cr.show_text(str(num))
                    num -= 1
    
       
    

        cr.set_source_rgb(0.6, 0.7, 0.2)
        cr.set_line_width(5+self.diff // 4)
        
        for ladders in self.Board.ladder_coordinates :
            x,y=ladders[0]
            x1,y1=self.cell_values(x)
            x2,y2=self.cell_values(y)
            newx,newy=self.get_cell_coordinates(x1,y1)
            endx,endy=self.get_cell_coordinates(x2,y2)
            
            line1_start_x, line1_start_y = endx+(self.square_size// 3) ,endy+(self.square_size// 3)
            line1_end_x, line1_end_y =newx+(self.square_size// 3),newy+(self.square_size// 3)
    
            line2_start_x, line2_start_y = line1_start_x + (self.square_size// 2), line1_start_y 
            line2_end_x, line2_end_y = line1_end_x + (self.square_size// 2), line1_end_y
            cr.move_to(line1_start_x, line1_start_y)
            cr.line_to(line1_end_x, line1_end_y)
            cr.stroke()
    
            cr.move_to(line2_start_x, line2_start_y)
            cr.line_to(line2_end_x, line2_end_y)
            cr.stroke()
    
            
            rung_count = 10
            rung_height = (line2_end_y - line1_start_y) / (rung_count + 1)
    
            
            
            for j in range(1, rung_count + 1):
                rung_y = line1_start_y + (rung_height * j)
                         
                rung_start_x = line1_start_x + ((line1_end_x - line1_start_x) * (rung_y - line1_start_y) // (line1_end_y - line1_start_y))
                rung_end_x = line2_start_x + ((line2_end_x - line2_start_x) * (rung_y - line2_start_y) // (line2_end_y - line2_start_y))

                cr.move_to(rung_start_x, rung_y)
                cr.line_to(rung_end_x, rung_y)
                cr.stroke()

       
 
        radius = self.square_size// 3
        rad_eye = self.square_size// 15 
        body_width =self.square_size //5 
       
        for snakes in self.Board.snake_heads:
            c1,c2,c3=snakes[1]
           
            cr.set_source_rgb(c1,c2,c3)
            
            s,e=snakes[0]
            x,y=self.cell_values(s)
            
            x,y=self.get_cell_coordinates(x,y)
            center_x=x+(self.square_size// 2)
            center_y=y+(self.square_size// 2)
            cr.arc(center_x, center_y, radius, 0, 2 * 3.14)
            cr.fill()
            x1,y1=self.cell_values(e)
            x1,y1=self.get_cell_coordinates(x1,y1)
            cr.set_line_width(body_width)
            cr.move_to(center_x , center_y)
            
           
            
            cr.curve_to(center_x,center_y,center_x+2*self.square_size,center_y+1.5*self.square_size,x1+20,y1+20)
            cr.stroke()
            cr.set_source_rgb(0.0, 0.0, 0.0)
            cr.arc(center_x, center_y, rad_eye, 0, 2 * 3.14)
            cr.fill()
            cr.arc(center_x-5, center_y-5, rad_eye, 0, 2 * 3.14)
            cr.fill()
            
       
        
        dice_size = self.square_size
        dice_x = board_size + 150
        dice_y = board_size - dice_size
            
       
        cr.set_line_width(2)
        cr.set_source_rgb(0, 0, 1)
        cr.rectangle(dice_x, dice_y, dice_size, dice_size)
        cr.stroke()
        dot_radius = 4
        dot_margin = 10
    
        dot_positions = [
        [],  # No dots for 0
        [(dice_x + dice_size / 2, dice_y + dice_size / 2)], 
        [(dice_x + dice_size / 4, dice_y + dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + 3 * dice_size / 4)],  
        [(dice_x + dice_size / 4, dice_y + dice_size / 4),
         (dice_x + dice_size / 2, dice_y + dice_size / 2),
         (dice_x + 3 * dice_size / 4, dice_y + 3 * dice_size / 4)], 
        [(dice_x + dice_size / 4, dice_y + dice_size / 4),
         (dice_x + dice_size / 4, dice_y + 3 * dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + 3 * dice_size / 4)], 
        [(dice_x + dice_size / 4, dice_y + dice_size / 4),
         (dice_x + dice_size / 4, dice_y + 3 * dice_size / 4),
         (dice_x + dice_size / 2, dice_y + dice_size / 2),
         (dice_x + 3 * dice_size / 4, dice_y + dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + 3 * dice_size / 4)],  
        [(dice_x + dice_size / 4, dice_y + dice_size / 4),
         (dice_x + dice_size / 4, dice_y + dice_size / 2),
         (dice_x + dice_size / 4, dice_y + 3 * dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + dice_size / 4),
         (dice_x + 3 * dice_size / 4, dice_y + dice_size / 2),
         (dice_x + 3 * dice_size / 4, dice_y + 3 * dice_size / 4)] 
    ]
        for dot_x, dot_y in dot_positions[self.dice_number]:
            dot_radius = 4
            cr.arc(dot_x, dot_y, dot_radius, 0, 2 * math.pi)
            cr.fill()
            
        cr.set_source_rgb(1, 0, 0)
        cr.move_to(board_size+board_size // 10,2 * self.square_size)
        cr.set_font_size(self.square_size // 3)
        cr.show_text("Player Name") 
        cr.move_to(board_size+(board_size //10  * 4),2 * self.square_size)
        cr.show_text("Position")      
        i=1
        for player in self.players:
            x, y = self.get_cell_coordinates(player.position[0], player.position[1])
            cr.set_source_rgb(*player.color)
            cr.arc(x + self.square_size/2, y +self.square_size/2, self.square_size // 4, 0, 2 * math.pi)  
            cr.fill()
            
            cr.arc( board_size+board_size // 10 -20,(2 + i) * self.square_size-10 , 10, 0, 2 * math.pi)
            cr.fill()  
            cr.select_font_face("Arial", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(self.square_size // 3)
            cr.move_to(board_size+board_size // 10,(2+ i) * self.square_size )
            cr.show_text(player.name)
            
            row=player.position[0]
            col=player.position[1]
            if(row % 2 != 0) :
                num = (9 - row) * 10 + col + 1
            else:
               num = (9 - row) * 10 +(9 - col) + 1 
            cr.move_to(board_size+(board_size //10  * 4) + 30,(2+i) * self.square_size)
            cr.show_text(str(num))
            i+=1
            
         
	       
            cr.set_source_rgba(1, 0, 0.5, 1)
            x = player.position[1] * self.square_size
            y = player.position[0] * self.square_size
            cr.rectangle(x, y, self.square_size, self.square_size)
            
            
            cr.set_source_rgba(1, 1, 0, 0.3)
            cr.fill()
            
        #to mark the current position in gameboard
        x = self.current_cell[1] * self.square_size
        y = self.current_cell[0] * self.square_size
        cr.rectangle(x+5, y+5, self.square_size -10, self.square_size -10)
        cr.set_source_rgba(1, 0.2,0.4, 0.6)
        cr.fill()
        widget.queue_draw()
       
    def get_cell_coordinates(self, row, column):
       
        x = column *self.square_size
        y = row * self.square_size
        return x, y
        
    #method to get the value of x and y coordinate of a cell   
    def cell_values(self,x):
       
        row=9-(x//10)
        if(x%10 == 0):
            row=9-(x//10 -1)
            if row%2 ==0:
                col=0
            else:
                col=9
        elif row%2==0:
            col=10-(x% 10)
        else:
            
            col=( x%10)-1
       
        return row,col

    def roll_dice(self):
        self.typed_value = 0
        self.correct_answer=0
        self.wrong_count = 1
        if self.check_game_over():
            return
        self.play_file('dice_sound')
        self.dice_number = random.randint(1, 6)
        self.i=1
        self.notify("you got a "+str(self.dice_number)+" on the dice")
        player = self.players[self.count % len(self.players)] 
        if player.chance == 1 :
            if self.dice_number != 1 and self.dice_number != 6 :
                self.notify(str(player.name)+" , you need a one or six , to get start ")
                self.count += 1
                player = self.players[self.count % len(self.players)]
                
                if player.name == "Machine":
                    GLib.timeout_add(6000, self.roll_dice)
                else:
                    self.notify(player.name+" can roll dice by pressing space bar")
            
            else:
                player.chance += 1
                self.current_row, self.current_col = player.position[0], player.position[1]
                if player.name == "Machine" :
                    self.move_pos(self.dice_number)
        
                else:
                    if self.add_mode == True:
                        self.calc_position(self.dice_number,player.position[0], player.position[1])
                        
                    else:
                        self.move_pos(self.dice_number)
                    
        else:
            
            player.chance += 1
            self.current_row, self.current_col = player.position[0], player.position[1]
            self.name=player.name
            if player.name == "Machine" :
                self.move_pos(self.dice_number)
        
            else:
                if self.add_mode == True:
                    self.calc_position(self.dice_number,player.position[0], player.position[1])
                else:
                    self.move_pos(self.dice_number)
                    
    
    def move_pos(self,dice_number) :  
        player = self.players[self.count % len(self.players)]
        current_row, current_col = player.position[0], player.position[1]  
        if current_row % 2 != 0:
            new_col = current_col + self.dice_number
            if new_col >= 10:
                new_col = 9
                count= self.dice_number- (10 - current_col)
                current_row -= 1
                new_col = new_col - count
                
        elif current_row % 2 == 0:
            new_col = current_col - self.dice_number
            if new_col < 0:
                count = new_col  
                new_col = 0
                current_row -= 1
                new_col -= count + 1
                
        if current_row < 0 :
            current_row =0
            new_col=current_col
            self.notify_cancel()
            self.notify("the number is larger than the number you were hoping to win")
            
        player.position = [current_row, new_col]
        
        self.queue_draw() 
        time.sleep(1)
        self.speak_number(current_row, new_col,player) 
                

        
    def calc_position(self,dice_num,row,col):
        
        self.current_pos=self.calculate_cell(row,col)
        self.correct_answer=str(self.correct_answer)+str( self.current_pos+dice_num)
        self.notify(str(self.current_pos)+" plus "+str(dice_num)+" equals to ")     
        
            
        
    def speak_number(self, row, col,player):
         
        
         
        if(row % 2 != 0) :
            number = (9 - row) * 10 + col + 1
            
            self.notify(player.name+" in position "+str(number))
        else :
            number = (9 - row) * 10 +(9 - col) + 1
            
            self.notify(player.name+" in position "+str(number))
        
       
        n1=-1
        n2=-1
        for ladder in self.Board.ladder_coordinates:
            ladders=ladder[0]
            l=ladders[0]
            end=ladders[1]
            if number == l:
                n1=l
                self.notify("great !! You have found a ladder!")
           
                self.move_player(player,number,end) 
    
        for snake in self.Board.snake_heads:
            snakes=snake[0]
            s=snakes[0]
            end=snakes[1]
            if number == s:
                n2=s
                self.notify("oops !! you are on a snake ")
                self.move_player(player,number,end)
        if(number !=n1 and number !=n2):
            
            for snake in self.Board.snake_heads:
                snakes=snake[0]
                s=snakes[0]
                if ( s - number) <=6 and (s -number) > 0 :
                    pos = s-number
                    self.notify("watch out !there is a snake at " + str(s) +" and it is " +str(pos)+" position away from you")
            for ladder in self.Board.ladder_coordinates :
                ladders=ladder[0]
                l=ladders[0]
                if (l - number) <= 6 and (l - number) > 0:
                    pos = l - number
                    self.notify(" there is a ladder at " + str(l) +" it is " +str(pos)+" position away from you")
            
         
                
            if self.check_game_over():
                winner = self.get_winner()
                

            # Randomly select a file name
                
                self.play_file("win")
                self.notify("Congratulations, " + winner.name + " has won the game!")
                
            elif self.dice_number == 6:
                if player.name == "Machine":
                    self.notify(str(player.name)+" got another chance to roll dice") 
                    GLib.timeout_add(9000, self.roll_dice)
                else:
                    self.notify(player.name+" got another chance to roll dice")
                    self.notify("roll dice by pressing space bar")
                
                
            else:
                self.count += 1
                player = self.players[self.count % len(self.players)] 
                if player.name == "Machine":
                    GLib.timeout_add(10000, self.roll_dice)
                else: 
                  
                    self.notify(player.name+" can roll dice by pressing spacebar")
                        
    def calculate_cell(self,row,col):
        if(row % 2 != 0) :
            cell_val = (9 - row) * 10 + col + 1
            return cell_val
        else :
            cell_val = (9 - row) * 10 +(9 - col) + 1
         
            return cell_val 
            
    def move_player(self, player, number,end):
        
        end_pos = self.cell_values(end)
        if end_pos[0] < player.position[0]:
            thread = threading.Thread(target=self.climb_up, args=(player, end_pos))
        else:
            thread = threading.Thread(target=self.descend, args=(player, end_pos))

        thread.start()
        
    
    
    def climb_up(self, player, end_pos):
        start_pos = player.position
        time.sleep(3)
        self.play_file("climb",3)
        col = player.position[1]
        for row in range(start_pos[0], end_pos[0], -1):
            if col < end_pos[1] :
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                col=col+1
            elif col > end_pos[1] :
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                col=col-1
            else:
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                
                
            # Delay between each step
            time.sleep(0.2)
    
            
        
        player.position = end_pos
        self.speak_number(player.position[0], player.position[1], player)
        self.queue_draw()
    
        
        
    def descend(self, player, end_pos):
        start_pos = player.position
        time.sleep(3)
        col=start_pos[1]
        for row in range(start_pos[0], end_pos[0]):
            if col<end_pos[1]:
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                col = col+1
            elif col > end_pos[1]:
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                col = col-1
            else:
                player.position = [row, col]
                Gdk.threads_enter()
                self.queue_draw()
                Gdk.threads_leave()
                
                
            self.play_file("fall",3)
            # Delay between each step
            time.sleep(0.2)
    
           
        player.position = end_pos
        self.speak_number(player.position[0], player.position[1], player)
        self.queue_draw()
        
    
   

    def cleanup(self, widget):
        self.speech.close() 
    
    
    def check_game_over(self):
        for player in self.players:
            if player.position[0] ==  0 and player.position[1] == 0:
                return True
        return False

    def get_winner(self):
        for player in self.players:
            if player.position[0] == 0 and player.position[1] == 0:
                return player
        return None
               
    def on_key_press(self, widget, event):
        self.i=1
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        keyval = event.keyval
        if keyval == Gdk.KEY_Left:
            self.move_current_cell(-1, 0)
        elif keyval == Gdk.KEY_Right:
            self.move_current_cell(1, 0)
        elif keyval == Gdk.KEY_Up:
            self.move_current_cell(0, -1)
        elif keyval == Gdk.KEY_Down:
            self.move_current_cell(0, 1)
        #check whether player pressed spacebar ,and execute roll_dice method
        elif keyval == Gdk.KEY_space:
            self.roll_dice()
        elif  keyval == Gdk.KEY_p :
            self.speak_player_position()
        elif   keyval == Gdk.KEY_a :
            self.speak_board()
        
        elif Gdk.keyval_name(keyval).isdigit():
            self.typed_value =str(self.typed_value)+ Gdk.keyval_name(keyval)
            print("ans"+str(self.typed_value) ) 
            
        elif keyval == Gdk.KEY_BackSpace:
            key_value_str = str(self.typed_value)
            if len(key_value_str) > 1:
                self.typed_value = (key_value_str[:-1])
            
        elif keyval == Gdk.KEY_Return:
            self.check_ans()
        self.queue_draw()
    
    def check_ans(self):
        
        print("Correct answer:", self.correct_answer)
    
        if (self.typed_value) == str(self.correct_answer):
            self.play_file("correct",2)
            self.notify("You are correct!")
            
            self.move_pos(self.dice_number)
        else:
            if self.wrong_count == 3:
                self.notify("you are wrong")
                self.play_file("wrong-anwser",3)
                self.notify("the correct position is "+str(int(self.correct_answer)));
                self.move_pos(self.dice_number)
            else:
                self.notify("your answer "+str(int(self.typed_value)))
                self.notify("You are wrong.")
                self.play_file("wrong-anwser",3)
                self.notify(str(self.current_pos)+" plus "+str(self.dice_number)+" equals to ")
                self.wrong_count+=1
                self.typed_value=0
    def move_current_cell(self, dx, dy):
        new_row = self.current_cell[0] + dy
        new_col = self.current_cell[1] + dx
        if 0 <= new_row < 10 and 0 <= new_col < 10:
            self.current_cell = [new_row, new_col]    
            self.speak(new_row,new_col)
            
    # method to speak number and player position by pressing arrow keys        
    def speak(self,row,col):
        if(row % 2 != 0) :
            num = (9 - row) * 10 + col + 1
            self.notify_cancel()
            self.notify(str(num))
        else :
            num = (9 - row) * 10 +(9 - col) + 1
            self.notify_cancel()
            self.notify(str(num))
       
        for ladder in self.Board.ladder_coordinates:
            ladders=ladder[0]
            l=ladders[0]
            if num == l:
                self.notify("its a Ladder")
        for snake in self.Board.snake_heads:
            snakes=snake[0]
            s=snakes[0]
            if num == s:
                self.notify("its a Snake")
        for i in range(self.num_players):
            player = self.players[i] 
            if player.position == [row ,col]:
                self.notify(player.name +" in  position "+str(num))
                
    #to speak the current positions of players by pressing shortcut key            
    def speak_player_position(self):
        for j in range(self.num_players):
            player = self.players[j]
            pos=self.calculate_cell(player.position[0],player.position[1])
            self.notify(player.name+" in position "+str(pos))
    
    #method to speak the position of snake and ladders on pressing ctrl+s            
    def speak_board(self):
        for i in range(100):
            position_text = ""
            for snake in self.Board.snake_heads:
                start,end=snake[0]
                if start == i:
                    position_text += f" Snake at position  {start} takes you to position {end}. "
            for ladder in self.Board.ladder_coordinates:
                start,end=ladder[0]
                if start == i:
                    position_text += f" Ladder at position  {start} takes you to position {end}. "
            if position_text:
                self.notify(position_text)
                        

    def notify(self, text):
	   
	    thread2 = threading.Thread(target=self.status_bar.set_text, args=(text, self.i))
	    thread2.start()
	    self.i=self.i+1
	   

    def notify_cancel(self):
	    self.speech.cancel()
	   

                
    #method to play music            
    def play_file(self, name, rand_range=1):
       
        if(rand_range == 1):
            file_path_and_name = 'file:///'+self.data_directory+'/sounds/'+name+".ogg";
        else:
            value = str(random.randint(1, rand_range))
           
            file_path_and_name = 'file:///'+self.data_directory+'/sounds/'+name+"-"+value+".ogg";
            print( file_path_and_name);
        self.player1.set_state(Gst.State.READY)
        self.player1.set_property('uri',file_path_and_name)
        self.player1.set_state(Gst.State.PLAYING)
          

class AccessibleStatusbar(Gtk.Frame):
	def __init__(self):
		super(AccessibleStatusbar,self).__init__()
		
		self.label = Gtk.Label()
		frame_inner = Gtk.Frame()
		frame_inner.add(self.label)
		atk_ob1 = frame_inner.get_accessible()
		atk_ob1.set_role(Atk.Role.NOTIFICATION)

		self.add(frame_inner)
		atk_ob = self.get_accessible()
		atk_ob.set_role(Atk.Role.STATUSBAR)
		

	def set_text(self,text,delay):
		
		time.sleep(delay)
		self.label.set_text(text)
		child = self.get_children()[0]
		atk_ob = child.get_accessible()
		atk_ob.notify_state_change(Atk.StateType.SHOWING,True)
		
	


	def set_line_wrap(self,val):
		self.label.set_line_wrap(val)

if __name__ == "__main__":
	
	game_board = GameBoard(1,2,["Kevin","Lenin" ],0)
	game_board.connect("destroy", Gtk.main_quit)
	Gtk.main()
