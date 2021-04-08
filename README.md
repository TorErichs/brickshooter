# The non-ultimate brick shooter ***(TNUPS)***

## General description

This game was started to practice my skills in object-oriented programming.
It still is not fully finished, but a game probably never really is.
It should be fully functioning, though. And, if you run, I hope you get some joy out of it.

*Please note that I used some public domain content. See the credits and disclosure.*

### Basic Game Design

To summarize the main objectives of the game:

The goal of the game is to keep the ball in bounds:
+ The ball starts at the initial position of the slider at a random 45° degree angle.
+ The player has to protect the bottom of the screen with a slider,
which can only be moved left and right.
+ The ball is reflected by all sides, but the bottom, and the slider.
+ The player cannot move off the screen.
+ The game ends when the last ball is of the screen 

Let's get started!

#### Gameplay

The game starts automatically after a short time to give the user an overview
+ ***'Left'*** and ***'right'*** cursor move the slider
+ ***'p'*** can be used to pause the game and restart it
+ ***'Esc'*** ends the game normally
+ ***Close window*** can be used to shut the game done immediately

### Special functions

* Additional to the normal functions some special balls can be triggered by hitting bricks that create them:
   + An additional ball can be triggered by a blue brick (soccer ball)
      - the new ball continues in the previous direction of the hitting ball
      - the speed is reduced to the starting speed of normal balls
   + By hitting a red brick a *teleporter* is created (basketball)
      - *teleporters* start with much lower speed and tunnel through the walls
      - they get deleted only if they move downwards through the bottom
      - they react with bricks in the normal way
   * A *beach ball* can be triggered by hitting a yellow brick (beach ball)
      - *beach balls* are reflected at 90° at walls and on the slider
      - they also start with slower speeds 
      - they reflect normally from bricks
* Each time a normal ball hits the slider:
   + speed is added to the ball
   + it can react to slider movement
      - friction allows to slow the ball down or speed it up horizontally
      - this changes the angle of the ball
      - allows some active control by the user

## TODOs

+ brick counter / time counter / total ball counter to print exit message
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
+ highscore (exclude pause time)
+ screenshots for documentation
+ concept for presentation
+ determine useful starting values

### Ideas

+ Background music?
   + decided against it for the moment
+ special bricks
    + moving brick
    + special bricks that disappear after a while?  
    + double hit brick?
+ nicer colors
+ replace the slider with nicer skin
+ `def reinit` for a new round
+ lookup dirty rect and partial refresh
+ Multiple sliders?
+ Use real pause key
+ special bricks only after a certain time

### Known glitches
+ reflections of ball on the long side of the brick can behave like reflections on the inner side of the shorts sides of the brick. This is only observed when the collisions happen very close to the edge. 
+ at high speeds balls can get lost at the bottom despite debug flag that should reflect

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

***End of day zero***

### Day 1

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

***End of day one***

    
### Day 2

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
   
***End of day two***
    
### Day 3

1. Repaired a glitch in `Ball.calculate_speed()`
1. Refactoring of Brick
   * also needed to fix the chance calculation
1. Implemented first version of beach ball (`Ball.special = "Beach"`)
1. Introduced a friction interaction with the slider to give the player more control
   + Strength (if at all) can be set in `Settings.friction`
   + if the slider moves in different horizontal direction as ball it gives something like a spin causing the ball to bounce of flatter
   + gives the chance to give very vertical balls some more angle by moving the slider in contact
1. "Beach" ball only reflects at right angle at wall and slide
   + would otherwise be just too much
1. tried to suppress double reflections by a `Ball.last_collision`
   + doesn't work well
   + better implementation is just checking the speed and meant-to-be speed
1. tried to make the "teleporter" only move straight when hitting bricks
   * works easily by addition if in brick collision
   * boring, because if it hits a special ball one gets a line of balls
   * also if it starts with upward speed the game will never end =)
1. Established sound effects
   * downloaded sounds from www.opengameart.org
   * some manual tests
   * created a function to play the sounds (`play_sound`)
      - sounds can be assigned via a dictionary to make double usage and changes easier
      - included a flag `Settings.sound` that allows turning off the sound
      
***End day three***

## Credits & disclosure

### Sound files
downloaded from www.opengameart.org

+ "short alarm" by "yd"  
+ "Glass bell sounds" by "Varkalander"  
+ "5 break, crunch impacts" by "Independent.nu"  
+ "Interface Sounds Starter Pack" by "p0ss"  
+ "Collision Nutfall (Yo Frankie!)" by "Blender Foundation"  
+ "Cute cartoon jump sound effect" by cfork and qubodup (Boing Raw Copyright 2005 cfork <http://freesound.org/people/cfork/> Boing Jump Copyright 2012 Iwan Gabovitch <http://qubodup.net>)  
+ "Laser shot" by "Mobeyee Sounds"  

### Images
downloaded for wikimedia commons