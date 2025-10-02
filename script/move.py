import sys
import time

def moveon():
    lirik = [
        ("how can i move on", 0.1),
        ("when i'm still in love with you", 0.05),
        ("'cause if one day you wake up", 0.07),
        ("and find that you're missing me", 0.07),
        ("and your heart starts to wonder", 0.07),
        ("where on this earth i could be" ,0.06),
        ("thinkin' maybe you'll comeback", 0.08),
        ("here to the place that we'd meet", 0.06),
        ("and you'll see me waiting for you", 0.06),
        ("on the corner of the street", 0.09),
        ("so i'm not moving..", 0.08),
        ("i'm not moving...", 0.08)
    ]
    
    delay = [0.4, 0.3, 0.4, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.9, 0.9]
    time.sleep(2)
    
    for i, (lagu, delayk) in enumerate(lirik):
        for karakter in lagu:
            print(karakter, end='')
            sys.stdout.flush()
            time.sleep(delayk)
        time.sleep(delay[i])
        print('')
        
moveon()