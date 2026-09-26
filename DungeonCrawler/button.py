
from socketserver import DatagramRequestHandler
import pygame
import colors
import os
import Cards
import SettingHelp

scale = SettingHelp.get_scale()

font = pygame.font.SysFont("Arial", int(24*scale))
small_font = pygame.font.SysFont("Arial", int(16*scale))

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.mode = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, colors.GREEN, self.rect, 2, border_radius=10)

        text_surface = font.render(self.text, True, colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

    def is_Rclicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            return self.rect.collidepoint(pos)
        return False

    def setText(self, text):
        self.text = text

    def setPosition(self, x, y):
        self.rect.topleft = (x, y)

    def setSize(self, width, height):
        self.rect.size = (width, height)
        #resize the font based on the new size

    def changeMode(self, newMode):
        self.mode=newMode




import SettingHelp

class CardButton(Button):
    def __init__(self, x, y, name, color, hover_color, card, card_type="default"):
        self.selected = False
        self.Rselected = False
        # Define base dimensions (unscaled)
        base_width = 54
        base_height = 72

        # Scale dimensions
        width = int(base_width * scale)
        height = int(base_height * scale)

        # Initialize Button with scaled dimensions
        super().__init__(x, y, width, height, "", color, hover_color)

        # Card properties
        self.name = name
        self.card_type = card_type
        self.card=card #store card
        self.stats = self._load_stats()  # Load stats for the card
        self.image = self._load_image()  # Load the card image
        self.DescText = [
            f"{card.name}",
            f"weight {card.weight}",
            f"type {card.card_type}",
            f"attack {card.Aval}",
            f"Light def {card.Dval}",
            f"Heavy def {card.D2val}",
            f"Heal {card.Hval}",
            f"Trick {card.desc}"
        ]





        # Scale the image
        if self.image:
            self.image = pygame.transform.scale(
                self.image,
                (width, height)
            )

        # Set up font for stats
        self.font = pygame.font.SysFont("Arial", int(24 * scale))
        self.small_font = pygame.font.SysFont("Arial", int(16 * scale))

    def check_hover(self, pos, screen):
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered:
            self.drawDesc2

    def _load_image(self):
        """Load the card image from assets/{name}.png"""
        image_path = os.path.join("assets", f"{self.name}.png")
        if os.path.exists(image_path):
            return pygame.image.load(image_path).convert_alpha()
        else:
            print(f"Warning: Image not found at {image_path}")
            return None

    def _load_stats(self):
        """Load stats for the card (example: replace with your logic)"""
        # Example stats, replace with actual logic
        return {
            self.card.desc,
        }

    def drawDesc(self, surface):
        """Draw the card description as multiple lines."""
        # Draw the card name
        name_surface = self.font.render(self.name, True, colors.WHITE)
        name_rect = name_surface.get_rect(
            centerx=scale * 150,
            top=scale * 10
        )
        surface.blit(name_surface, name_rect)

        # Starting y position for stats
        y_offset = scale * 40

        # Draw each line manually using card attributes
        line_surface = self.small_font.render(f"weight - {self.card.weight}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"type - {self.card.card_type}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"attack - {self.card.Aval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Light def - {self.card.Dval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Heavy def - {self.card.D2val}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Heal - {self.card.Hval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Trick - {self.card.desc}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 10, y_offset))

        # Draw the border
        self.drawBorder(surface)



    def drawDesc2(self, surface):
        """Draw the card description as multiple lines at a different screen position."""
        # Draw the card name
        name_surface = self.font.render(self.name, True, colors.WHITE)
        name_rect = name_surface.get_rect(
            centerx=scale * 800,
            top=scale * 250
        )
        surface.blit(name_surface, name_rect)

        # Starting y position for stats (relative to the name position)
        y_offset = scale * 300

        # Draw each line of the description manually
        line_surface = self.small_font.render(f"weight - {self.card.weight}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"type - {self.card.card_type}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"attack - {self.card.Aval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Light def - {self.card.Dval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Heavy def - {self.card.D2val}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Heal - {self.card.Hval}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))
        y_offset += line_surface.get_height()

        line_surface = self.small_font.render(f"Trick - {self.card.desc}", True, colors.WHITE)
        surface.blit(line_surface, (scale * 800 - line_surface.get_width() // 2, y_offset))

        # Draw the border
        self.drawBorder(surface)

    def draw(self, surface):
        # Draw the card background
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, colors.GREEN, self.rect, 2, border_radius=10)

        if self.image:
            surface.blit(self.image, self.rect)

        self.drawBorder(surface)

    def check_hover2(self, pos, surface):
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered or self.mode:
            self.drawDesc(surface)
        return self.is_hovered

    def check_hover3(self, pos, surface):
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered:
            self.drawDesc2(surface)
        return self.is_hovered

    def setText(self, text):
        # Override if you want to set custom text
        self.name = text

    def set_card(self, card):
        """Swap out the card this button represents, refreshing name/type/stats/image."""
        scale = SettingHelp.get_scale()
        self.card = card
        self.name = card.name
        self.card_type = card.card_type
        self.stats = self._load_stats()

        raw_image = self._load_image()
        if raw_image:
            self.image = pygame.transform.scale(
                raw_image, (self.rect.width, self.rect.height)
            )
        else:
            self.image = None

        self.DescText = small_font.render(card.name+" "+card.desc, True, (255, 255, 255))

    def drawBorder(self, screen):
        if self.Rselected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, width=4) 
        elif self.selected:
            pygame.draw.rect(screen, (255, 215, 0), self.rect, width=4)  # gold border
        elif self.mode:
            pygame.draw.rect(screen, colors.BLUE, self.rect, 2, border_radius=10)
        else:
            pygame.draw.rect(screen, colors.GREEN, self.rect, 2, border_radius=10)


class EntityCards(CardButton):
    def __init__(self, x, y, name, color, hover_color, card):
        # Entity cards are 3x wider than default cards
        base_width = 468//2
        base_height = 458//2

        # Scale dimensions
        width = int(base_width * scale)
        height = int(base_height * scale)

        # Initialize with scaled dimensions
        super().__init__(x, y, name, color, hover_color, card,card_type="entity")

        # Override rect with new dimensions
        self.rect = pygame.Rect(x, y, width, height)

        # Scale the image
        if self.image:
            self.image = pygame.transform.scale(
                self.image,
                (width, height)
            )

class WeaponCards(CardButton):
    def __init__(self, x, y, name, color, hover_color):
        # Weapon cards are the default size
        base_width = 174//2
        base_height = 347//2

        self.Lclicked = False
        self.Rclicked = False

        # Scale dimensions
        width = int(base_width * scale)
        height = int(base_height * scale)
        super().__init__(x, y, name, color, hover_color, card_type="weapon")

                # Override rect with new dimensions
        self.rect = pygame.Rect(x, y, width, height)
        
                # Scale the image
        if self.image:
            self.image = pygame.transform.scale(
                self.image,
                (width, height)
            )
        

class PlayerDeck():
    #a set of 12 buttons and 1 trinket slot for a player
    def __init__(self, x, y):
        self.buttons = []
        self.trinket_slot = None
        self.x = x
        self.y = y
        self.create_buttons()