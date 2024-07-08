import os
import pygame

class DialogueBlock:
    
    def __init__(self, id, is_choice=False):
        self.id = id
        self.is_choice = is_choice
        self.lines = []
        # Either a next will not be none or choices will be populated?
        self.choices = []
        self.next = None
        
    def add_line(self, line):
        self.lines.append(line)

    def __str__(self):
        return f"DialogueBlock <ID: {self.id}, lines: {self.lines}, next: {self.next}, choices: {self.choices}>"

    def __repr__(self):
        return f"DialogueBlock <ID: {self.id}, lines: {self.lines}, next: {self.next}, choices: {self.choices}>"
    
class DialogueHandler:
    
    font_size = 25
    
    def __init__(self, dialogue_file: str, font: pygame.font.Font | None = None):
        
        self.font = None
        if pygame.font.get_init():
            if font is None:
                self.font = pygame.font.SysFont(None, DialogueHandler.font_size)
        
        assert dialogue_file is not None
        self.parse_dialogue_file(dialogue_file)

        self.current_block_id = 0
        assert self.dialogue_blocks.get(self.current_block_id) is not None

        self.current_text_idx = 0
        assert len(self.dialogue_blocks.get(self.current_block_id).lines) > 0

    def parse_dialogue_file(self, fname: str):
        self.dialogue_blocks = {}
        current_block = None
        with open(fname) as f:
            # Assume the first line is the start of a new block    
            while (line := f.readline()) != '':
                # print(repr(line))
                if line.startswith('[start]'):
                    block_id = line.removeprefix('[start] ')
                    block_id_int = int(block_id)
                    if (current_block := self.dialogue_blocks.get(block_id_int)) is None:
                        current_block = DialogueBlock(block_id_int)
                        self.dialogue_blocks[block_id_int] = current_block

                    print(f"Starting block {block_id_int}")

                elif line.startswith('[choice]'):
                    data = line.removeprefix('[choice] ')
                    new_id, text = data.split(',', 1)
                    new_id_int = int(new_id)
                    if (next_block := self.dialogue_blocks.get(new_id_int)) is None: # This should always be true, when would we add another line to as a choice to a block?
                        next_block = DialogueBlock(new_id_int, True)
                        next_block.add_line(text)

                    current_block.choices.append(new_id_int)

                elif line.startswith('[next]'):
                    data = line.removeprefix('[next] ')
                    current_block.next = int(data)

                elif line.startswith('[end]'):
                    pass

                elif line in ['\n', '\r\n']:
                    pass

                else:
                    current_block.add_line(line.strip())
    
        print(self.dialogue_blocks)

    
    def update(self, delta: float):
        pass
    
    def draw_text(self, surface: pygame.Surface, text_rect: pygame.Rect):
        """Draws the current dialogue block"""
        pygame.draw.rect(surface, (255, 0, 0), text_rect, 2)

        current_text = self.current_block.lines[self.current_block_id]
        rendered_text = self.font.render(current_text, True, (255, 255, 255))
        surface.blit(rendered_text, text_rect)
    
    @property
    def current_block(self) -> DialogueBlock:
        return self.dialogue_blocks[self.current_block_id]

if __name__ == "__main__":
    dh = DialogueHandler("dialogue.txt")