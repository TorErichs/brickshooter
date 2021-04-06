# The not-ultimate brick shooter ***(TNUPS)***

### Disclosure
***images taken from wiki commons***

## General description

### Basic Game Design

To summarize the main objectives of the game:

The goal of the game is to keep the ball in bounds:
+ The ball starts at the center with a random direction.
+ The player has to protect the bottom of the screen with a slider,
which can be moved left and right.
+ The ball is reflected by all sides, but the bottom, and the slider.
+ The player cannot move off the screen.
+ The game ends when the ball hits the bottom of the screen 

Let’s get started!

## TODOs

+ Move the main app to the main folder?
+ Move ball to list and use class method to check for the amount of balls  
+ transition the image input to `handling.load_png()`
+ programm collision and removal
+ fixed frame rate for more control?
+ only reflect while v downwards
+ fix reflection: maybe use collision
+ use the `.time` for example to make pause more efficient
+ use the `.font` to write some simple instructions on the background
    * ```# Display some text
        font = pygame.font.Font(None, 36)
        text = font.render("Hello There", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)```
    * use this to first explain game and then start at key like `K_SPACE`
+ add the loading errors and so on also to packages


### Ideas

+ `surfarray` to make bricks explode?
+ special bricks
    + extra ball
    + moving brick
    + double hit brick?
+ nice colors
+ changing speed of game
+ 0.95 rect for collision?
+ 90° Ball?
+ Use real pause key
+ while time < ...:
+ lookup dirty rect and partial refresh
+ Object tunnel through the walls
+ Multiple sliders?
+ add music
+ use certain keys to trigger modes (developer flag?)
+ `def reinit` for a new round



## Personal progress documentation

### Day 1/2

1. Imported the starting structure from "Eric Matthes: Python 3 Crashkurs".
1. Imported the key handling from https://realpython.com/pygame-a-primer/
1. Create the "ball" as a black square and blit on surface
   1. Creating random starting position for the ball in the upper center
1. Create the slider in brickshooter.py 
    1. Create left / right movement
    1. Move the slider into app.py, because of dependency conflicts
1. Start moving the ball
    1. generate reflection conditions for all walls
    1. remove bottom reflection:
        1. program reflection on slider
        1. problem: multiple reflections if same as wall with smaller or larger
           + solved by comparison in int() (round() better?)
        1. adapt boundaries for hits near the edge
1. Moved some classes into different files
1. Imported first brick

***End of day 1***

### Real day 1

1. Applied `.convert()` and `.convert_alpha()` to the objects ball and brick
1. `pygame.transform.scale()` to get the brick into a good size   
1. Implemented a pause mode with the key `p`
1. Reading pygame.org tutorial on game making:
    + implemented the image loading function as `load_png()`
1. Rethinking the game mechanics because of `collide` and `sprite.Group`
   1. Changing the graphics update to `self.all_sprites` 
   1. updating the ball via the `self.balls` sprite group
   1. stopping if the list is empty and no ball left





