class Book():
    
    def __init__(self, title, author, pages):
        self.title  = title
        self.author = author
        self.pages  = pages
        
    def __str__(self):
        return "Title : {}\nAuthor : {}\nPages {}".format(self.title, self.author, self.pages)

    def __len__(self):
        return self.pages
    
    
class book1(Book):
    def __init__(self):
        Book.__init__(self)
        print("Inhertinse success")

        
#book = Book("Tale of tow cities", "badr", 200)        
print(book1)
#print(len(book))
                
