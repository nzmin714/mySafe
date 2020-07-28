import sqlite3

password = "Password123"

def convertToBinData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def convertToImage(filename, bin_data):
    with open(filename, 'wb') as file:
        imageData = file.write(bin_data)
        print("File Opened\n")
    return imageData


connect = input("Type password for MySafe: ")

while connect != password:
    connect = input("Type password for MySafe: ")
    if connect == "quit":
        break

if connect == password:
    conn = sqlite3.connect('mySafe.db')
    c = conn.cursor()
    # c.execute("""DELETE TABLE mysafe""")
    # conn.commit()
    # c.close()
    # conn.close()
    try:
        
        c.execute("""CREATE TABLE mysafe
                    (file_name TEXT,
                    extension TEXT,
                    bin_file BLOB,
                    PRIMARY KEY ("file_name"));
                    """)
        conn.commit()

        print("Safe has been create!\nWhat would you like to do?")
    except:
        print("Safe exists.\nWhat would you like to do?")    

    while True:
        print("q = quit program")
        print("s = store file")
        print("o = open file")
        print("d = delete file")
        print("v = view files")
        option = input("Please select an option: ")

        if option == "q":
            break
        if option == "s":
            path = input("File location: ")
            file_name = path.split("\\")
            file_name = file_name[len(file_name)-1]
            bin_data = convertToBinData(path)
            extension = file_name.split(".")[1]
            try:
                c.execute("INSERT INTO mysafe VALUES (:name, :ext, :binfile)", {"name":file_name, "ext":extension, "binfile":bin_data})
                conn.commit()
                print(file_name + "Uploaded file\n")
            except:
                print("Invalid Entry")



        if option == "o":
            file = input("What is the file name?: ")
            try:
                result = c.execute("SELECT * FROM mysafe WHERE file_name=" + '"' + file + '"')
                bin_data =''
                for row in result:
                    bin_data = row[2]
                convertToImage(file, bin_data)
            except:
                print("File does not exist")

        if option == "d":
            c.execute("SELECT file_name FROM mysafe")
            print("\n" + str(c.fetchall()))
            file = input("What is the file name: ")
            try:
                c.execute("DELETE FROM mysafe WHERE file_name=" + '"' + file + '"')
                conn.commit()
                print(file + " has been deleted.\n")
            except:
                print("File does not exist")

        if option == "v":
            c.execute("SELECT file_name FROM mysafe")
            print(str(c.fetchall()) + "\n")
        
        else:
            print("Please select one of the options above.")
            



