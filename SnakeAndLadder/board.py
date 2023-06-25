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

Gst.init(None)

class Player:
    def __init__(self, name, position,color,chance):
        self.name = name
        self.position = position
        self.color=color
        self.chance=chance
class GameBoard(Gtk.Window):
    def __init__(self,board_num,num_players,players_names,mode):
        Gtk.Window.__init__(self, title="Game Board")
        if mode ==0:
            self.add_mode=False
        else:
            self.add_mode=True  
        
        self.count = num_players
        self.i=2
        color_rgb = Gdk.RGBA(1, 1, 1, 1)
        #self.override_background_color(Gtk.StateFlags.NORMAL,color_rgb)
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
        #print("Monitor resolution:", width, "x", height)
       
        #self.set_default_size(width,700)
        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request(800,self.height - 115)
        drawing_area.connect("draw", self.draw_board)
        drawing_area.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)  
        self.snakes = [ (23 , 5 ), (35 , 7) , (49 , 12 ), (56 , 24 ), (79 , 60 ), (89 , 55 ), (94 , 52) , (99 , 37)]
        self.ladders = [ (6,25) , (13,65) , (21,59) ,  (50,70) , (64,96) , (68,86) , (80,98)]
        
        
        
       
        '''scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_size_request(600,600)
        scrolled_window.add(drawing_area)'''
        self.current_cell= [9, 0]
       
       

        vbox.pack_start(drawing_area, False, True, 0)

        self.status_bar = AccessibleStatusbar()
        #self.status_bar.set_text("HELLO",2 )
        vbox.pack_start(self.status_bar, False, True, 0)

        
       
        

        '''button = Gtk.Button(label="Roll dice")
        button.connect("clicked", self.roll_dice)'''        
      
        vbox.show_all()
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.players = [] 
        self.num_players = num_players
        self.players_names=players_names
       
        self.create_players()
        self.cwd = os.getcwd()
        self.player1 = Gst.ElementFactory.make('playbin', 'player1')
        # Playing starting sound
        play_thread = threading.Thread(target=self.play_file, args=('start.wav',))
        play_thread.start()

        time.sleep(1)
        
        self.notify(self.players_names[0]+" can roll dice by pressing the space bar")
   
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
        #print("width="+str(self.window_width))
        #print("height="+str(self.window_height))
       
        
        # Calculate the size of each square based on the window dimensions
        self.square_size = min(self.window_width // 10, self.window_height  // 10)
        self.diff = self.square_size - 50
        board_size = self.square_size * 10
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
    
        cr.set_source_rgb(0, 0, 0)
    
        for i in range(10):
            for j in range(10):
                cr.rectangle(i * self.square_size, j * self.square_size, self.square_size, self.square_size)
    
                if self.board_num == 1:
                    if (i+j) % 2 == 0:
                        cr.set_source_rgb(1, 1, 1)
                    else:
                        cr.set_source_rgb(0, 0, 1)
                elif self.board_num == 2:
                    if (i+j) % 2 == 0:
                        cr.set_source_rgb(0.5, 0, 0)
                    else:
                        cr.set_source_rgb(1, 1, 1)
                elif self.board_num == 3:
                    if (i+j) % 2 == 0:
                        cr.set_source_rgb(1, 1, 1)
                    else:
                        cr.set_source_rgb(0, 0.6, 0)
                elif self.board_num == 4:
                    if (i+j) % 2 == 0:
                        cr.set_source_rgb(1, 1, 1)
                    else:
                        cr.set_source_rgb(0, 0.3, 0.5)
                elif self.board_num == 5:
                    if (i+j) % 2 == 0:
                        cr.set_source_rgb(1, 1, 1)
                    else:
                        cr.set_source_rgb(0.7, 0, 0.5)
    
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
    
        line_sets = [
            
            [(460+(10 * self.diff), 170+(4 *self.diff )), (460+ (10* self.diff) , 260+(6 *self.diff))],
            [(210+(5 * self.diff), 160+(4 *self.diff)), (370+ (8 * self.diff), 420+( 10 * self.diff))],
            [(205+(5 * self.diff) , 369+(7 * self.diff)), (260+(6* self.diff) , 480+ (10* self.diff))],
            [(210+ (5* self.diff), 20+ (1* self.diff)), (160+(4*self.diff), 160+(3* self.diff))],
            [(10+(1 *self.diff),380+(6 *self.diff)), (60+ (2* self.diff), 210+ (5* self.diff))],
            [(365+(8 * self.diff), 165+(4 * self.diff)), (255+ (6 * self.diff), 70+(2 *self.diff))],
            [(10+(1 * self.diff),120+(3 * self.diff)), (115+(3 * self.diff),30+ (1*self.diff))]
            
        ]
    
        
        for line_set in line_sets :
            
            line1_start_x, line1_start_y = line_set[0]
            line1_end_x, line1_end_y = line_set[1]
    
            line2_start_x, line2_start_y = line1_start_x + 30, line1_start_y + 5
            line2_end_x, line2_end_y = line1_end_x + 30, line1_end_y + 5
    
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

       
 
        radius = 15 +self.diff // 3
        rad_eye = 2 + self.diff //5 
        body_width =10 +self.diff //5 
        width = 75
        height = 30
        cr.set_source_rgb(1, 0.0, 0.0)
        #radius = 15
        center_x =  75+(2*self.diff)
        center_y = 30+(1*self.diff)
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.set_source_rgb(1.0, 0.0, 0.0) 
        cr.move_to(center_x , center_y)  #snakebody
        cr.curve_to(190,50,100,210,180+(4 *self.diff), 320+(7*self.diff))
        cr.stroke()
        
        
        width = center_x #eye1
        height = center_y
        cr.set_source_rgb(0.0, 0.0, 0.0)
        #radius = 2
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, rad_eye, 0, 2 * 3.14)
        cr.fill()
        
        width = 75 #eye2
        height = 20
        cr.set_source_rgb(0.0, 0.0, 0.0)
        #radius = 2
        center_x = 75 +(2*self.diff)
        center_y = 20+(1*self.diff)
        cr.arc(center_x, center_y, rad_eye, 0, 2 * 3.14)
        cr.fill()
        
        cr.set_source_rgb(1, 0.5, 0.0)
        #radius = 15
        cr.arc(120 + (3 *self.diff),370 + (8 *self.diff), radius, 0, 2 * 3.14)
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.set_source_rgb(1.0, 0.5, 0.0) 
        cr.move_to(125 + (3 *self.diff), 380 + (8 *self.diff))  #snakebody
        cr.curve_to(180 + (4 *self.diff), 450 + (10*self.diff),  150 + (4 *self.diff), 450 +(10 *self.diff), 220 + (5 *self.diff), 480 + (10 *self.diff))  
        cr.stroke()
        
        
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(110 + (3 *self.diff),370 +(8 *self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        cr.arc(125 + (3 *self.diff),370 + (8 *self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        
        cr.set_source_rgb(0.0, 0.5, 0.0)
        #radius = 15
        cr.arc(420 + (9 *self.diff),70 + (2 * self.diff), radius, 0, 2 * 3.14)
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.set_source_rgb(0.0, 0.5, 0.0) 
        cr.move_to(420 + ( 9 * self.diff), 70 + (2 *self.diff))  #snakebody
        cr.curve_to(290+ ( 6 * self.diff),100+ ( 2 * self.diff),300+ ( 6 * self.diff),100 + ( 2 * self.diff),280 + ( 6 * self.diff), 220 + ( 5 * self.diff))  
        cr.stroke()
        
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(430+ ( 9 * self.diff),70+ ( 2 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        cr.arc(420+ ( 9 * self.diff),70+ ( 2* self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        
        cr.move_to(260+ ( 6 * self.diff), 240+ ( 6* self.diff))#tail
        cr.line_to(275+ ( 6 * self.diff), 220+ ( 6* self.diff))
        cr.line_to(280+ ( 6 * self.diff), 220+ ( 6 * self.diff))
        cr.close_path()
        cr.set_line_width(3)
        cr.set_source_rgb(0.0, 0.5, 0.0)
        cr.stroke()
        
        cr.move_to(190+ ( 4 * self.diff), 340+ ( 7 * self.diff))#tail
        cr.line_to(175+ ( 4 * self.diff), 320+ ( 7 * self.diff))
        cr.line_to(185+ ( 4 * self.diff), 315+ ( 7 * self.diff))
        cr.close_path()
        cr.set_line_width(3)
        cr.set_source_rgb(1, 0.0, 0.0)
        cr.fill()
        cr.stroke()
        
        cr.move_to(210+ ( 5 * self.diff), 480+ ( 10 * self.diff))#tail
        cr.line_to(230+ ( 5 * self.diff), 500+ ( 10 * self.diff))
        cr.line_to(215+ ( 5 * self.diff), 470+ ( 10 * self.diff))
        cr.close_path()
        cr.set_line_width(3)
        cr.set_source_rgb(1, 0.5, 0.0)
        cr.fill()
        cr.stroke()
        
        
        width = 420+ ( 9 * self.diff)
        height = 270+ ( 6 * self.diff)
        cr.set_source_rgb(0, 1.0, 1.0)
        #radius = 15
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.set_source_rgb(0, 1.0, 1.0) 
        cr.move_to(420+ ( 9 * self.diff), 270+ ( 6 * self.diff))  #snakebody
        cr.curve_to(440+ ( 9 * self.diff),288+ ( 6 * self.diff),410+ ( 9 * self.diff),490+ ( 10 * self.diff),440+ ( 9 * self.diff), 420+ ( 9 * self.diff))  
        cr.stroke()
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(410+ ( 9 * self.diff),270+ ( 6 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        cr.arc(425+ ( 9 * self.diff),260+ ( 6 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        
        width = 270+( 6 * self.diff)
        height = 320+( 7 * self.diff)
        cr.set_source_rgb(1, 1.0, 0)
        #radius = 15
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.set_source_rgb(1, 1.0, 0.0) 
        cr.move_to(270+( 6 * self.diff), 320+( 7 * self.diff))  #snakebody
        cr.curve_to(230+ (5 * self.diff),340+( 7 * self.diff),330+( 7 * self.diff),430+( 9 * self.diff),340+( 7 * self.diff), 470+( 10 * self.diff))  
        cr.stroke()
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(265+( 6 * self.diff),320+( 7 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        cr.arc(275+( 6 * self.diff),320+( 7 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        
       
        
        
        width = 220+( 5 * self.diff)
        height = 220+( 5* self.diff)
        cr.set_source_rgb(0, 0.5, 1.0)
        #radius = 15
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.move_to(220+( 5 * self.diff), 220+( 5 * self.diff))  #snakebody
        cr.curve_to(410+( 9 * self.diff),280+( 6 * self.diff),150+( 4 * self.diff),340+( 7 * self.diff),170+( 4 * self.diff), 360+( 8 * self.diff))  
        cr.stroke()
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(220+( 5 * self.diff),210+( 5 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        cr.arc(220+( 5 * self.diff),225+( 5 * self.diff),rad_eye,0, 2 * 3.14)
        cr.fill()
        
        width = 70+( 2 * self.diff)
        height = 120+( 3 * self.diff)
        cr.set_source_rgb(0, 1, 0.5)
        radius = 15+self.diff // 3
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(body_width)
        cr.move_to(70+( 2 * self.diff), 120+( 3 * self.diff))  #snakebody
        cr.curve_to(30+( 1 * self.diff),150+( 3 * self.diff),110+( 3 * self.diff),340+( 7 * self.diff),30+( 1 * self.diff), 230+( 5 * self.diff))  
        cr.stroke()
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(70+( 2 * self.diff),110+( 3 * self.diff),2 +self.diff // 4,0, 2 * 3.14)
        cr.fill()
        cr.arc(70+( 2 * self.diff),125+( 3 * self.diff),2+ self.diff //4,0, 2 * 3.14)
        cr.fill()
        
        width = 330+( 7 * self.diff) 
        height = 30+( 1 * self.diff)
        cr.set_source_rgb(0.9, 0.5, 0.5)
        radius = 15 + self.diff // 3
        center_x = width 
        center_y = height 
        cr.arc(center_x, center_y, radius, 0, 2 * 3.14)#circle
        cr.fill()
        
        cr.set_line_width(10+self.diff // 3)
        cr.move_to(328+( 7 * self.diff), 30+( 1 * self.diff))  #snakebody
        cr.curve_to(490+( 10 * self.diff),90+( 1 * self.diff),350+( 8 * self.diff),200+( 5* self.diff),430+( 9 * self.diff), 230+( 5 * self.diff))  
        cr.stroke()
        cr.set_source_rgb(0.0, 0.0, 0.0)#eyes
        cr.arc(330+( 7 * self.diff),20+( 1 * self.diff),2 + self.diff //4 ,0, 2 * 3.14)
        cr.fill()
        cr.arc(320+( 7 * self.diff),30+( 1 * self.diff),2+ self.diff //4,0, 2 * 3.14)
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
            
            #cr.set_source_rgb(1, 0, 0)  
            #cr.select_font_face("Arial", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
            #cr.set_font_size(18)
            #cr.move_to(x + square_size /2 - 8, y + square_size/2 + 8) 
            #cr.show_text(player.name) 
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
        y = row *  self.square_size
        return x, y

    def roll_dice(self):
        self.typed_value = 0
        self.correct_answer=0
        self.wrong_count = 1
        if self.check_game_over():
            return
        self.play_file('dice_sound.wav')
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
            
        player.position[0],player.position[1] = [current_row, new_col]
        if self.dice_number != 6:
            self.count += 1 
        self.queue_draw() 
        time.sleep(1)
        self.speak_number(current_row, new_col,player) 
        
                
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
            
        player.position[0],player.position[1] = [current_row, new_col]
        
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
            #self.notify_cancel()
            self.notify(player.name+" in position "+str(number))
        else :
            number = (9 - row) * 10 +(9 - col) + 1
            #self.notify_cancel()
            self.notify(player.name+" in position "+str(number))
        
        snakes = [ 23 , 35 , 49 , 56 , 79 , 89 , 94 , 99]
        ladders = [ 6 , 13 , 21 ,  50 , 64 , 68 , 80]
        if number in ladders:
            self.notify("great !! You have found a ladder!")
            
            #time.sleep(0.5)
            self.move_player(player,number) 
    
        elif number in snakes:
            
            self.notify("oops !! you are on a snake ")
           
           
            #time.sleep(0.5)
            self.move_player(player,number) 
        else :
            
            for snake in snakes:
                if ( snake - number) <=6 and (snake -number) > 0 :
                    pos = snake -number
                    self.notify("watch out !there is a snake at " + str(snake) +" and it is " +str(pos)+" position away from you")
            for ladder in ladders :
                if (ladder - number) <= 6 and (ladder - number) > 0:
                    pos = ladder - number
                    self.notify(" there is a ladder at " + str(ladder) +" it is " +str(pos)+" position away from you")
            
         
                
            if self.check_game_over():
                winner = self.get_winner()
                self.play_file('got_promotion.ogg')
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
            #self.notify_cancel()
            return cell_val
        else :
            cell_val = (9 - row) * 10 +(9 - col) + 1
            #self.notify_cancel()
            return cell_val 
            
    def move_player(self, player, number):
        #time.sleep(3)
        
        #if number in [6, 13, 21, 50, 64, 68, 80, 23, 35, 49, 56, 79, 89,94 , 99]:
        end_pos = self.get_end_position(number)
        if end_pos[0] < player.position[0]:
            thread = threading.Thread(target=self.climb_up, args=(player, end_pos))
        else:
            thread = threading.Thread(target=self.descend, args=(player, end_pos))

        thread.start()
        
    '''else:
        player.position = self.get_end_position(number)
        self.queue_draw()
        self.speak_number(player.position[0], player.position[1], player,callback)'''
    
    def climb_up(self, player, end_pos):
        start_pos = player.position
        time.sleep(3)
        self.play_file('next_level_6.ogg')
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
                
                
            self.play_file('wrong_pressed.ogg')
            # Delay between each step
            time.sleep(0.2)
    
           
        player.position = end_pos
        self.speak_number(player.position[0], player.position[1], player)
        self.queue_draw()
        
    
    def get_end_position(self, number):
        ladder_positions = {
            6: [7, 4],
            13: [3, 4],
            21: [4, 1],
            50: [3, 9],
            64: [0, 4],
            68: [1, 5],
            80: [0, 2],
            23: [9, 4],
            35: [9, 6],
            49: [8, 8],
            56: [7, 3],
            79: [4, 0],
            89: [4, 5],
            94: [4, 8],
            99: [6, 3]
        }
        
        return ladder_positions[number]


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
            self.check_ans()
        elif keyval == Gdk.KEY_BackSpace:
            key_value_str = str(self.typed_value)
            if len(key_value_str) > 1:
                self.typed_value = (key_value_str[:-1])
            #self.check_ans()
        self.queue_draw()
    
    def check_ans(self):
        time.sleep(2)
        print("Correct answer:", self.correct_answer)
    
        if (self.typed_value) == str(self.correct_answer):
            #self.notify("your answer "+str(self.typed_value))
            self.notify("You are correct!")
            self.move_pos(self.dice_number)
        else:
            if self.wrong_count == 3:
                self.notify("you are wrong")
                self.notify("the correct position is "+str(int(self.correct_answer)));
                self.move_pos(self.dice_number)
            else:
                self.notify("your answer "+str(int(self.typed_value)))
                self.notify("You are wrong.")
                self.notify(str(self.current_pos)+" plus "+str(self.dice_number)+" equals to ")
                self.wrong_count+=1
                
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
        snakes = [ 23 , 35 , 49 , 56 , 79 , 89 , 91 , 99]
        ladders = [ 6 , 13 , 21 ,  50 , 64 , 68 , 80]
        if num in snakes :
            self.notify("its a snake")
        elif num in ladders:
            self.notify("its a ladder")
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
            for start, end in self.snakes:
                if start == i:
                    position_text += f" Snake at position  {start} takes you to position {end}. "
            for start, end in self.ladders:
                if start == i:
                    position_text += f" Ladder at position  {start} takes you to osition {end}. "
            if position_text:
                self.notify(position_text)
                        

    def notify(self, text):
	    #self.speech.speak(text)
	    
	    
	    thread2 = threading.Thread(target=self.status_bar.set_text, args=(text, self.i))
	    print("Notification: " + text)
	    thread2.start()
	    self.i=self.i+1
	    #self.status_bar.set_text(text)

    def notify_cancel(self):
	    self.speech.cancel()
	    #self.status_bar.set_text("")

                
    #method to play music            
    def play_file(self, filename):
        file_path_and_name = 'file:///usr/share/SnakeAndLadder/sounds/' + filename
        self.player1.set_state(Gst.State.READY)
        self.player1.set_property('uri', file_path_and_name)
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
		print("delay"+str(delay))
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
