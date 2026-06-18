RATE_PER_KM=12

DISTANCES={
    "Chennai->Coimbatore":450,
    "Chennai->Bangalore":590,
    "Chennai->Dhanushkodi":600,
    "Chennai->America":13000
}

class FareCache:
    def __init__(self):
        self._cache={}
        self._frequency={}

    def compute_fare(self,route:str)->int:
        km=DISTANCES[route]
        return km * RATE_PER_KM
    
    def search(self,route:str)->str:
        if route not in DISTANCES:
            return "Route not found"
        
        self._frequency[route]=self._frequency.get(route,0)+1

        if route in self.cache:
            fare=self.cache[route]
            return f"Cache Hit -- Rs.{fare:,}"
        
        fare=self.compute_fare(route)
        self._cache[route]=fare

        return f"Cache Miss --Rs.{fare:,}"
    
    def top_routes(self,n:int=3)->list:
        ranked=sorted(self._frequency.items(),key=lambda x:x[1],reverse=True)

        return ranked[:n]
    
    def clear_cache(self)->None:
        self._cache.clear()


MENU = """
Commands:
  s <route>  - search fare  (e.g. s Pune->Mumbai)
  t          - show top 3 routes
  c          - clear cache
  l          - list available routes
  x          - exit
"""

if __name__ == "__main__":
    fc = FareCache()
    print(MENU)
 
    while True:
        raw = input(">> ").strip()
        if not raw:
            continue
 
        parts = raw.split(maxsplit=1)
        cmd   = parts[0].lower()
 
        if cmd == "s" and len(parts) == 2:
            print(fc.search(parts[1].strip()))
 
        elif cmd == "t":
            top = fc.top_routes()
            if not top:
                print("No searches yet.")
            else:
                print("\nTop routes:")
                for rank, (route, count) in enumerate(top, 1):
                    print(f"  {rank}. {route} — {count} search{'es' if count != 1 else ''}")
                print()
 
        elif cmd == "c":
            fc.clear_cache()
            print("Cache cleared. Frequency data preserved.")
 
        elif cmd == "l":
            print("\nAvailable routes:")
            for route, km in DISTANCES.items():
                print(f"{route:<30} {km} km  Rs.{km * RATE_PER_KM:,}")
            print()
 
        elif cmd == "x":
            break
        else:
            print(MENU)
 