import string

paragraph=input("Enter a paragraph: ")
paragraph=paragraph.lower()

for char in string.punctuation:
    paragraph=paragraph.replace(char,"")

words=paragraph.split()
word_count={}

for word in words:
    if word in word_count:
        word_count[word]+=1
    else:
        word_count[word]=1

sorted_words=sorted(word_count.items(),key=lambda value:value[1],reverse=True)

print(f"\nTop 5 Most Frequent Words:")
for word,count in sorted_words[:5]:
    print(f"{word}:{count}")

    