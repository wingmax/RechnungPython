from pathlib import Path


# PART 1     ##################
path = Path("pi.txt")
#path = Path('C:\Users\PC\Desktop\Python\Lpython\LPython\src\File Operations\pi.txt')
#contents = path.read_text()
#contents = contents.rstrip()

contents = path.read_text()
lines = contents.splitlines()
pi_string = ''
for line in lines:
    pi_string += line
print(pi_string)
print(len(pi_string))


# PART 2####################################

# birtday = input("Enter your Birthday:")
# if birtday in pi_string:
#     print("Your birthday appears in PI Number")
# else:
#     print("Du hast Pech gehabt")

# PART 3 ####### WRITING TO A FILE ##########
path = Path("write.txt")
path.write_text("I will write hear in Python")

new_content = input("New Content")
path.write_text(new_content)
