books =[
  {
    "title": "User-centric upward-trending frame",
    "author": "Penny Franco",
    "rating": "2006",
    "year_published": "2020",
    "id": 101
  },
  {
    "id": 102,
    "title": "eaque voluptatibus",
    "author": "Talia Schultz",
    "rating": 0.15,
    "year_published": 1702
  },
  {
    "id" : 111,
    "title" : "eaque voluptatibus",
    "author" : "Talia Schultz",
    "rating" : 0.15,
    "year_published" : 1702
  },
{
    "title": "User-centric upward-trending frame",
    "author": "Penny Franco",
    "rating": "2006",
    "year_published": "2020",
    "id": 122
  },
{
    "title": "fghgfhgfhyh",
    "author": "Penny Franco",
    "rating": "2006",
    "year_published": "2020",
    "id": 125
  },
{
    "title": "fghgfhgfhyh",
    "author": "Penny Franco",
    "rating": "2006",
    "year_published": "2020",
    "id": 14444
  },

]

temp =[]
duplicates = []
for d in books:
    if d.get("title") not in temp:
        temp.append(d.get("title"))
    else:
      duplicates.append(d.get("id"))
print(duplicates)