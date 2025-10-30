# task 7

user = input("enter a word: ").lower()

user = "".join(i for i in user if i.isalnum() )

l,r = 0, len(user)-1
while l <= r:
    if user[l] != user[r]:
        print(f"{user} is not a palindrome")
        break
    l+=1
    r-=1
else:
    print(f"{user} is a palindrome")