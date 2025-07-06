from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene

from .compositions.topbar import print_top_bar
from .compositions.screensize import print_screen_size, MIN_WIDTH, MIN_HEIGHT


class WarrantyEffect(Print):
    """The Game's Warranty Information"""

    def __init__(self, screen, game_state):
        warranty = """THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

For more information, please consult the LICENSE file found in the root of this project."""

        self.game = game_state
        super().__init__(
            screen=screen,
            renderer=SpeechBubble(warranty),
            y=5,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("b") or event.key_code == ord(
                "B"
            ):  # Press 'b' to go back
                raise NextScene("Start")
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None
        return event

    def _update(self, frame_no):
        if self.screen.width < MIN_WIDTH or self.screen.height < MIN_HEIGHT:
            print_screen_size(self)
        else:
            print_top_bar(self, "Warranty Information")

            # Draw the instructions to go back to the Main Menu
            instruction = "[B]ack to the Main Menu"
            colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
            colour_map += [(7, 1, 0)] * (len(instruction) - 3)
            self._screen.paint(
                text=instruction,
                x=(self._screen.width - len(instruction)) // 2,
                y=self._screen.height - 2,
                colour_map=colour_map,
            )

            return super()._update(frame_no)
