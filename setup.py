###########################################################################
#    
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

from distutils.core import setup
from glob import glob
setup(name='SnakeAndLadder',
      version='1.0',
      description='Accessible snake and ladder game',
      author='Archana V S',
      author_email='archanavs1211@gmail.com',
      url='https://github.com/VSarchana/Snake-and-ladder.git',
      license = 'GPL-3',
      packages=['SnakeAndLadder'],
      data_files=[('share/SnakeAndLadder/',['data/icon.png' ]),
      ('share/SnakeAndLadder/sounds/',['data/sounds/dice_sound.wav', 'data/sounds/got_promotion.ogg', 'data/sounds/next_level_6.ogg' ,  'data/sounds/start.ogg' ,  'data/sounds/start.wav' , 'data/sounds/warning.ogg' ,  'data/sounds/wrong_pressed.ogg']),
      ('share/applications/',['snake-and-ladder.desktop']),
      ('bin/',['snake-and-ladder'])]
      )
# sudo python3 setup.py install --install-data=/usr
