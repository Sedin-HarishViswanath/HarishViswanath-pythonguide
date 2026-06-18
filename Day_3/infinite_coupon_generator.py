# Custom iterator class implementing __iter__ and __next__. Generates unique PREFIX-XXXX 
# coupon codes up to a maximum total. Supports redeem(code) to mark codes as used and 
# remaining() to track inventory. Raises StopIteration at the limit. Shows exactly what Python does 
# internally for every for loop.


import random

class CouponIterator:
    def __init__(self,prefix:str,total:int,discount:int):
        self.prefix = prefix
        self.total = total
        self.discount = discount
        self._codes = self.generate_codes()
        self._redeemed = set()
        self._index = 0
    
    def generate_codes(self) -> list:
        seen,codes=set(),[] 
        while len(codes)<self.total:
            code=f"{self.prefix}-{random.randint(0,9999):04d}"
            if code not in seen:
                seen.add(code)
                codes.append(code)
        return codes
    
    def __iter__(self):
        self._index=0
        return self
    
  
    def __next__(self)->str:
        if self._index >= self.total:
            raise StopIteration
        
        code=self._codes[self._index]
        self._index+=1

        return f"{code} ({self.discount}%off)"
    
    def redeem(self,code:str)->bool:
        if code in self._codes and code not in self._redeemed:
            self._redeemed.add(code)
            print(f"Redeemed: {code} -- {self.discount}% discount applied!")
            return True
        
        print(f"Invalid: {code} -- code not found")
        return False
    
    def used(self)->int:
        return len(self._redeemed)
    
    def remaining(self)->int:
        return self.total - self.used()

if __name__=="__main__":
    prefix=input("Prefix of Coupon code: ").strip().upper() or "SALE"

    try:
        total=int(input("Total no.of coupons: ").strip() or "5")
        discount=int(input("Discount %: ").strip() or "20")
        

    except ValueError:
        print("Invalid input.")
        total,discount=5,20

    coupons=CouponIterator(prefix,total,discount)


    print(f"Generated {total} coupons:")

    for code in coupons:
        print(code)

    while True:
        code=input("Enter code to redeem,(Enter q to quit):").strip()

        if code.upper()=="Q":
            break

        coupons.redeem(code)


    print(f"Used Coupons:{coupons.used()}")
    print(f"Remaining:{coupons.remaining()}")