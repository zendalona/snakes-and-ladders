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
      ('share/SnakeAndLadder/sounds/',['share/SnakeAndLadder/sounds/dice_sound.wav', 'share/SnakeAndLadder/sounds/win.wav', ' share/SnakeAndLadder/sounds/climb-1.ogg' ,'share/SnakeAndLadder/sounds/climb-2.ogg', 'share/SnakeAndLadder/sounds/climb-3.ogg','share/SnakeAndLadder/sounds/fall-1.ogg','share/SnakeAndLadder/sounds/fall-2.ogg','share/SnakeAndLadder/sounds/fall-3.ogg','share/SnakeAndLadder/sounds/correct-1.ogg','share/SnakeAndLadder/sounds/correct-2.ogg', 'share/SnakeAndLadder/sounds/start.wav' ,'share/SnakeAndLadder/sounds/wrong-anwser-1.ogg','share/SnakeAndLadder/sounds/wrong-anwser-2.ogg','share/SnakeAndLadder/sounds/wrong-anwser-3.ogg' ]),
      ('share/applications/',['snake-and-ladder.desktop']),
      ('bin/',['snake-and-ladder'])]
      )
# sudo python3 setup.py install --install-data=/usr
