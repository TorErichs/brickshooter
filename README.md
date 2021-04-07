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

Let's get started!

## TODOs

+ brick counter / time counter / total ball counter to print exit message
+ friction with the slider  
+ use the `.font` to write some simple instructions on the background
    * ```python # Display some text
        font = pygame.font.Font(None, 36)
        text = font.render("Hello There", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)```
    * use this to first explain game and then start at key like `K_SPACE`
+ add the loading errors and so on also to packages
+ refactor complex functions

### Ideas

+ `surfarray` to make bricks explode?
+ special bricks
    + moving brick
    + double hit brick?
+ nice colors
+ 90° Ball?
+ add music
+ highscore (exclude pause time)
+ use certain keys to trigger modes (developer flag?)
+ `def reinit` for a new round
+ lookup dirty rect and partial refresh
+ Multiple sliders?
+ Use real pause key

## Personal progress documentation

### Day 0 (half a day)

1. Imported the starting structure from "Eric Matthes: Python 3 Crashkurs".
1. Imported the key handling from https://realpython.com/pygame-a-primer/
1. Create the "ball" as a black square and blit on surface
   1. Creating random starting position for the ball in the upper center
1. Create the slider in `brickshooter.py` 
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

***End of day 0***

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
1. created git repository to make sure I'm able to revert 
1. after very long thought process:
   * found a simple solution (logic) to determine the brick reflection condition
   * remove the brick afterwards
1. implemented random brick position generation:
    * new position is generated until it doesn't collide with any object
    * generate many bricks at the beginning (`start_bricks`)
    * generate bricks if few (`min_bricks`)
1. read into the further modules of pygame
    + possible candidates:
        * midi / sound
        * pixelarray
        * eventlist
1. first very quick test with clock and fps printing

***End of real day 1***
    
### Real Day 2

1. Improved the brick collision again (2px tolerance and including ball radius)
1. debug flag for more focus on game mechanics:
    * activates auto reflection at bottom
1. `settings.max_fps` works but either makes game very slow or won't work on slow PCs
    * read that it might also be costly in the processor
    * changed to pure `self.clock.tick()` from `self.clock.tick_busy_loop()`
    * must have made a mistake at first try, because I remember to have tried before
1. Used the proper function for pause `pygame.time.wait`:
   * send the processor into sleep 
   * before just used `continue` and restarted the loop :see_no_evil:
1. `sprite.move_ip` is `int` based so that 0.5 vertical speed is equal to no vertical speed
    * prevents mechanics like percentage-wise (slow) ball speed up or subtle effects like slider friction1
1. gave brick collisions a speed dependent component:
    * works with higher speeds
    * allows the fps to set lower (needs higher speed, because otherwise :snail:)
1. Some refactoring of `Ball.update()`
1. Resize the collision rect of ball to make it less 'rectanglish'
1. prevent runaway loop in `Brick.__init__()`
1. Added background change on user close or loss
1. Established float handling for speed:
    * starting direction can now be set to random
        - boring though
    * game starts at 45° for nicest gameplay
    * would allow to speed the ball up over time
1. ball speed up factor implemented `Settings.speed_increase`
1. Implemented two special bricks
    * the duplicator brick:
        - adds another ball
    * the teleporter brick:
        - adds a special ball
        - has another skin (basket ball)
        - flies through the walls
        - starts with a much slower speed, because otherwise no chance to react to it
1. needed to rewrite the reflection functions:
   * problems when introducing the small new ball showed some special cases
1. changed the duplicator and teleporter so they wouldn't just start upwards
    * inherit the original speed of the ball
1. rewrote the `calculate_speed` function so that I could hand over the speed of original ball
    * allows to create new ball with same direction
    * but starting speed as in settings specified