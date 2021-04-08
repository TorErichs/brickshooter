import pygame

pygame.mixer.init()

sound_bounce = pygame.mixer.Sound("../sounds/qubodup-cfork-ccby3-jump.ogg")
sound_hit = pygame.mixer.Sound("../sounds/nutfall.flac")
sound_crunch = pygame.mixer.Sound("../sounds/impactcrunch01.mp3.flac")
sound_bell = pygame.mixer.Sound("../sounds/hjm-glass_bell_1.wav")
sound_dropped_ball = pygame.mixer.Sound("../sounds/alarm.ogg")
sound_teleport = pygame.mixer.Sound("../sounds/laser_shot.wav")
# TODO: find sounds for this
# sound_lost
# sound_esc: horn?

sound_dict = {
    "bounce": sound_bounce,
    "wall_hit": sound_hit,
    "hit_teleport": sound_teleport,
    "hit_beach": sound_hit,
    "brick_normal": sound_crunch,
    "brick_duplicator": sound_bell,
    "brick_teleporter": sound_bell,
    "brick_beach": sound_bell,
    "dropped_ball": sound_dropped_ball,
}


def play_sound(string, sound_on=True):
    if not sound_on:
        pass
    else:
        sound = sound_dict.get(string, None)
        if sound:
            sound.play()
        else:
            print(f"Sound {string} couldn't be played.")


if __name__ == "__main__":
    pygame.mixer.init()
    # sound_bounce.play()
    # sound_dropped_ball.play()
    # sound_teleport.play()
    # sound_hit_normal.play(-1)
    play_sound("hit_normal")
    # pygame.mixer.music.load("../sounds/nutfall.flac")
    # load_sound("hjm-glass_bell_1.wav")
    # pygame.mixer.music.play(3)

    pygame.time.wait(1000)
    print("Waited to keep program alive to play sounds for a while. Over now...")

    pygame.mixer.music.stop()
    pygame.quit()
