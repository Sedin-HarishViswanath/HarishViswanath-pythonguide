import random 

class SongNode:
    def __init__(self,name:str,artist:str,duration:int):
        self.name=name
        self.artist=artist
        self.duration=duration
        self.prev=None
        self.next=None

    def formatted_duration(self)->str:
        return f"{self.duration//60}:{self.duration%60:02d}"
    
    def __str__(self)->str:
        return f"{self.name}-{self.artist} ({self.formatted_duration()})"
    
class Playlist:
    def __init__(self):
        self.head=None
        self.tail=None
        self.current=None

def add_song(self,name:str,artist:str,duration:int)->None:
    node=SongNode(name,artist,duration)
    if self.tail is None:
        self.head=self.tail=self.current=node

    else:
        node.prev=self.tail
        self.tail.next=node
        self.tail=node

def remove_current(self)->None:
    if self.current is None:
        print("Playlist is empty")
        return
    
    removed=self.current

    if removed.prev:
        removed.prev.next=removed.next
    else:
        self.head=removed.next

    if removed.next:
        removed.next.prev=removed.prev
    else:
        self.tail=removed.prev

    self.current=removed.next or removed.prev
    print(f"Removed :{removed}")

def next_track(self)->None:
    if self.current is None or self.current.next is None:
        print("End of playlist")
        return
    
    self.current=self.current.next
    print(f"Now playing:{self.current}")

def prev_track(self)->None:
    if self.current is None or self.current.prev is None:
        print("Already at beginning of playlist")
        return
    
    self.current=self.current.prev
    print(f"Now playing:{self.current}")

def show_queue(self)->None:
    if self.head is None:
        print("Queue is empty")
        return
    
    node=self.head
    while node:
          marker="playing" if self.current else ""
          print(f"{node} {marker}")
          node=node.next

def shuffle(self)->None:
    nodes=[]
    node=self.head

    while node:
        nodes.append(node)
        node=node.next

    random.shuffle(nodes)

    for i,n in enumerate(nodes):
        n.prev=nodes[i-1] if i>0 else None
        n.next=nodes[i+1] if i<len(nodes)-1 else None

    self.head=nodes[0]
    self.tail=nodes[-1]
    self.current=self.head

    print("Playlist shuffled")

SONGS = [
    ("Hawa Hawa",         "Hadiqa Kiani",  245),
    ("Blinding Lights",   "The Weeknd",    200),
    ("Aaluma Doluma",      "Vedalam",  270),
    ("GBU Mame",           "Good Bad Ugly",203),
    ("Karuppa Kooda va",   "Karuppu (Sai Abhyankkar)", 310),
    ("Shape of You",      "Ed Sheeran",    234),
]

MENU = """
Commands:
  n   - next track       p   - prev track
  r   - remove current   q   - show queue
  s   - shuffle          a   - add song
  x   - exit
"""

if __name__=="main":
    pl=Playlist()
    for name,artist,dur in SONGS:
        pl.add_song(name,artist,dur)

    print("Playlist loaded.")
    print(f"Now playing: {pl.current}")
    print(MENU)


    while True:
        cmd = input(">> ").strip().lower()
 
        if cmd == "n":
            pl.next_track()
        elif cmd == "p":
            pl.prev_track()
        elif cmd == "r":
            pl.remove_current()
        elif cmd == "q":
            print()
            pl.show_queue()
            print()
        elif cmd == "s":
            pl.shuffle()
            print(f"Now playing: {pl.current}")
        elif cmd == "a":
            name   = input("  Song name:   ").strip()
            artist = input("  Artist:      ").strip()
            raw    = input("  Duration (seconds): ").strip()
            dur    = int(raw) if raw.isdigit() else 180
            pl.add_song(name, artist, dur)
            print(f"  Added: {name}")
        elif cmd == "x":
            break
        else:
            print(MENU)
 