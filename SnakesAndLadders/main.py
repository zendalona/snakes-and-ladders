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
import gi 
import webbrowser
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk 
from SnakesAndLadders.board import GameBoard
import pygame

class SelectPlay(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Select Player")

		pygame.mixer.init()

		# Load and play the background music
		pygame.mixer.music.load('/usr/share/SnakesAndLadders/sounds/bgmusic.ogg')
		pygame.mixer.music.set_volume(0.2)
		pygame.mixer.music.play(-1)

		self.set_default_size(500, 500)
		self.user_guide_file_path="https://www.google.com/"

		#We will fix this later 
		#self.connect("destroy", Gtk.main_quit)
		#sets background colour for the window
		self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
		

		#creates an alignment container and add to the window 
		alignment = Gtk.Alignment()
		alignment.set(0.5, 0.5, 0.5, 0)
		self.add(alignment)
		
		#create vertical box container and add it to the alignment container
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		alignment.add(vbox)
		hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
		vbox.add(hbox1)
		
		hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=110)
		vbox.add(hbox3)
		hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		vbox.add(hbox2)
		hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
		hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		#creates a label and set its text and font color
		label1 = Gtk.Label()
		label1.set_text("Choose gameboard  :")
		label1.set_use_underline(True)
		label1.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0, 1.0))
		hbox1.pack_start(label1, False, False, 30) # add label to the vertical box container
		
		board_combo=Gtk.ComboBoxText()
		board_combo.connect("changed", self.on_board_selected)
		board_combo.append_text("Board1")
		board_combo.append_text("Board2")
		board_combo.append_text("Board3")
		board_combo.append_text("Board4")
		board_combo.append_text("Board5")
		board_combo.set_active(0)
		label1.set_mnemonic_widget(board_combo)
		hbox1.pack_start(board_combo, False, False, 20)
		
		label3 = Gtk.Label()
		label3.set_text("Choose game mode  :")
		label3.set_use_underline(True)
		label3.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0, 1.0))
		hbox3.pack_start(label3, False, False, 30)
		
		game_mode_combo = Gtk.ComboBoxText()
		game_mode_combo.connect("changed", self.on_game_mode_changed)
		#adding values to combobox
		game_mode_combo.append_text("Normal  mode")
		game_mode_combo.append_text("Education mode")
		hbox3.pack_start(game_mode_combo, False, False, 0)
		label3.set_mnemonic_widget(game_mode_combo)
		label2 = Gtk.Label()
		label2.set_text("Choose the number of players:")
		label2.set_use_underline(True)
		label2.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0, 1.0))
		hbox2.pack_start(label2, False, False, 30)
		
		player_count_combo = Gtk.ComboBoxText()
		player_count_combo.connect("changed", self.on_player_count_changed)
		#adding values to combobox
		player_count_combo.append_text("1")
		player_count_combo.append_text("2")
		player_count_combo.append_text("3")
		player_count_combo.append_text("4")
		player_count_combo.append_text("5")
		label2.set_mnemonic_widget(player_count_combo)

		player_count_combo.set_size_request(100, 30)
		#adding combobox to vbox
		hbox2.pack_start(player_count_combo, False, False, 50)

		#creating entry for adding player names
		self.player_name_entries_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		hbox5.pack_start(self.player_name_entries_vbox, False, False, 170)
		vbox.add(hbox5)
		
		
		#creating start button
		start_button = Gtk.Button(label="Start")
		#connect the clicked signal to the on_submit_clicked method
		start_button.connect("clicked", self.on_submit_clicked)
		start_button.set_size_request(100, 30)
		hbox4.pack_start(start_button, False, False, 200)
		vbox.add(hbox4)
		
		
		#creating about button
		about_button=Gtk.Button(label="About")
		about_button.connect("clicked",self.on_about_clicked)
		about_button.set_size_request(20, 30)
		
		#creating help button
		user_button=Gtk.Button(label="User-Guide")
		user_button.connect("clicked",self.on_user_clicked)
		user_button.set_size_request(20, 30)
		
		submit_vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		submit_vbox.pack_start(about_button, False, False, 100)
		submit_vbox.pack_start(user_button, False, False, 0)
		vbox.pack_start(submit_vbox, False, False, 80)
		

		 
		#empty list is created to hold player names
		self.player_name_entries = []
		self.set_resizable(False)

		game_mode_combo.set_active(0)
		player_count_combo.set_active(0)

		self.show_all()
		
		self.connect("destroy", self.quit)

		Gtk.main()
		
		
	def on_player_count_changed(self, combo):
		#select the active text from combobox
		player_count = combo.get_active_text()
		self.count=int(player_count)
		#clears previously added player name entry fields
		self.clear_player_names()
		#creates entry fields based on the player_count
		if player_count:
			for i in range(int(player_count)):
				entry = Gtk.Entry()
				entry.set_placeholder_text(f"Player {i+1} name")
				entry.set_size_request(100, 30)  
				entry.show()
				#adds the entry to player_name_entries_vbox
				self.player_name_entries_vbox.pack_start(entry, False, False, 0)
				#append player names to list player_name_entries
				self.player_name_entries.append(entry)
            
	#cleares previously added player name entry fields
	def clear_player_names(self):
		for entry in self.player_name_entries:
			self.player_name_entries_vbox.remove(entry)
		self.player_name_entries.clear()
		
	def on_game_mode_changed(self,combo):
		self.mode=combo.get_active()
		
	def on_board_selected(self,combo):
		self.board_num = combo.get_active() + 1
		
	def on_submit_clicked(self, button):
		#gets the text from each player name entry field and stores them in the player_names
		player_names = [entry.get_text() for entry in self.player_name_entries]


		#if all player names are provided, a GameBoard instance is created with the count and player names
		if all(player_names):
			pygame.mixer.music.stop()
			#destroy the window
			self.destroy()

			game_board = GameBoard(self.board_num,self.count, player_names,self.mode)
			game_board.connect("destroy", Gtk.main_quit)
			
	def on_user_clicked(self,widget,data=None):
		url = self.user_guide_file_path
		try:
			webbrowser.get("firefox").open(url, new=2)
		except webbrowser.Error:
			webbrowser.open(url, new=2)
	def show_about_dialog(self):
		about_dialog = Gtk.AboutDialog()

		 # Set the relevant properties of the about dialog
		about_dialog.set_program_name("SNAKE AND LADDER GAME\n 0.1 \n\nSnake and Ladder is an ancient Indian board game\n which is regarded as a world wide classic.\n This game offers an inclusive and enjoyable experience to everyone.  \n\n   Copyright(C) 2022-2023 ARCHANA V S <archanavs1211@gmail.com>\n\n   Supervised by  Zendalona(2022-2023)\n\n This program is free software you can redistribute it and or modify \nit under the terms of GNU General Public License as published by the free software foundation \n either gpl3 of the license.This program is distributed in the hope that it will be useful,\n but without any warranty without even the implied warranty of merchantability or fitness for a particular purpose.\n see the GNU General Public License for more details") 
        
        #self.set_version("")
        
		about_dialog.set_website_label("GNU General Public License,version 0.1\n\n" "Visit SNAKE AND LADDER GAME Home page")
        
		about_dialog.set_website("http://wwww,zendalona.com//SNAKE AND LADDER")
		about_dialog.set_authors(["Archana V S"])
		about_dialog.set_documenters(["Archana V S"])
		about_dialog.set_artists(["Nalin Sathyan" ,"Dr.Saritha Namboodiri", "Subha I N", "Bhavya P V", "K.Sathyaseelan"])
		
		about_dialog.run()
		about_dialog.destroy()
		
	def on_about_clicked(self,button):
		 self.show_about_dialog()

	def quit(self,widget, data=None):
		self.destroy()
		Gtk.main_quit()
