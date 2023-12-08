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
setup(name='SnakesAndLadders',
      version='1.0',
      description='Accessible snakes and ladders game',
      author='Archana V S',
      author_email='archanavs1211@gmail.com',
      url='https://github.com/VSarchana/Snake-and-ladder.git',
      license = 'GPL-3',
      packages=['SnakesAndLadders'],
      data_files=[('share/SnakesAndLadders/',['data/icon.png' ]),
      ('share/SnakesAndLadders/sounds/',['data/sounds/bgmusic.ogg','data/sounds/dice_sound.ogg',
       'data/sounds/win.ogg', 'data/sounds/climb-1.ogg' ,'data/sounds/climb-2.ogg',
        'data/sounds/climb-3.ogg','data/sounds/fall-1.ogg','data/sounds/fall-2.ogg',
        'data/sounds/fall-3.ogg','data/sounds/correct-1.ogg','data/sounds/correct-2.ogg',
         'data/sounds/start.ogg' ,'data/sounds/wrong-anwser-1.ogg','data/sounds/wrong-anwser-2.ogg',
         'data/sounds/wrong-anwser-3.ogg' ]),
      ('share/applications/',['snakes-and-ladders.desktop']),
      ('bin/',['snakes-and-ladders'])]
      )
# sudo python3 setup.py install --install-data=/usr
