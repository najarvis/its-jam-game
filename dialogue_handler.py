import os
import pygame

class DialogueHandler:
    
    font_size = 12
    
    def __init__(self, dialogue_file: str, font: pygame.font.Font | None = None):
        
        if pygame.font.get_init():
            if font is None:
                self.font = pygame.font.SysFont(None, DialogueHandler.font_size)
        
        assert dialogue_file is not None
        self.parse_dialogue_file(dialogue_file)
    
    def update(self, delta: float):
        pass
    
    def parse_dialogue_file(self, fname: str):
        self.dialogue_blocks = {}
        with open(fname) as f:
            # Assume the first line is the start of a new block    
            while (line := f.readline()) != '':
                print(repr(line))
                if line.startswith('[start]'):
                    block_id = int(line[8:])
                    self.dialogue_blocks[block_id] = DialogueBlock(block_id)
                    print(f"Starting block {block_id}")
    
    def write_text(self):
        pass
    
    
class DialogueBlock:
    
    def __init__(self, id, is_choice=False):
        self.id = id
        self.is_choice = is_choice
        self.lines = []
        
    def add_line(self, line):
        self.lines.append(line)
        
if __name__ == "__main__":
    dh = DialogueHandler("dialogue.txt")