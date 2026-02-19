
#for i in range(5):
#    print(i)


#i = 0
#while i < 5:
#    print(i)
#    i += 1

# response = ""
# while response != "quit":
#     response = input("Enter command:")
#     print(f"You said: (response)")

    # username = "admin"
    # password = "password123"
    # logged_in = False

    # while not logged_in:
    #     user_input = input("Enter username: ")
    #     pass_input = input("Enter password: ")
        
    #     if user_input == username and pass_input == password:
    #         print("Login successful!")
    #         logged_in = True
    #     else:
    #         print("Invalid credentials. Try again.")

# break - exit the loop immediately
# words = ["hello", "world", "target", "python"]
# for w in words:
#     print('checking:',w)
#     if w == "target":
#         print("Found it!")
#         break


# words = ["hello", "world", "target", "python"]
# for w in words:
#     print('checking:',w)
#     if w == "target":
#         print("Found it!")
#         continue
#     print("Not the target\n")

#continue   skip to the next iteration
# for num in range(10):
#     if num % 2 == 0:
#         continue
#     print(num)  #print odd numbers only


# def f(n):
#     for num in range(n):
#         if num % 2 == 0:
#             continue
#     return num

# print(f(10))

for line in open("data/words.txt"):
    print(line)