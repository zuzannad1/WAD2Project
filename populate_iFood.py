import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'project.settings')
import django
django.setup()
from iFood.models import Restaurant, Dishes


def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories. 
# This might seem a little bit confusing, but it allows us to iterate 
# through each data structure, and add the data to our models.

#Indian cuisines
    curry_pot_dishes = [
        {"name": "Chicken Pakora",
         "cuisine":"Indian", "description": "Deep fried pieces of chicken with tikka masala paste.", "price": 3.40 },
        {"name":"Prawn Puri",
         "cuisine":"Indian", "description": "Prawns topped with masala & wrapped in puri bread.", "price": 4.25 },
        {"name":"Mumbai Spicy Wings",
         "cuisine":"Indian", "description": "Spicy wings with slight curry flavor", "price": 6.45} ]
         
    indian_orchard_dishes = [
        {"name":"Chicken Tikka",
         "cuisine":"Indian", "description":"Traditional curry in a medium sauce with fresh herbs, spices & coriander", "price": 7.25 },
        {"name":"Vegetable Saag",
         "cuisine":"Indian", "description": "Saag with methi, spinach & a touch of ginger", "price": 6.50},
        {"name":"Lamb Biryani",
         "cuisine":"Indian", "description": "Cooked with rice, Punjabi spices & herbs & served with curry sauce", "price":9.50 } ]
         
    bollywood_spice_dishes = [
        {"name":"Tandoori Mix Grill",
         "cuisine":"Indian", "description": "Assortment of chicken tandoori, chicken tikka, lamb tikka, chicken chaat, donner meat & naan bread", "price":9.50},
        {"name":"Tarka Daal",
         "cuisine":"indian", "description": "Lentils cooked with garlic & ginger fried in butter", "price":4.90 },
         {"name":"Malaidar King Prawn",
         "cuisine":"Indian", "description": "King Prawns & Spinach puree simmered with lashings of green chilli & garlic with a dash of fresh cream", "price":8.00}  ]
	
#Asian cuisines
    station_wok_dishes = [
		{"name": "Kung Po Chicken",
         "cuisine":"Chinese", "description": "Spicy, stir-fried dish made with chicken, peanuts, vegetables, and chili peppers.", "price": 7.20 },
        {"name":"Beef with Green Pepper in Black Bean Sauce",
         "cuisine":"Chinese", "description": "Prawns topped with masala & wrapped in puri bread.", "price": 7.20 },
        {"name":"Sweet & Sour King Prawn",
         "cuisine":"Chinese", "description": "Sweet and Sour curry with King Prawns", "price": 7.70} ]
         
    temaki_dishes = [
		{"name": "Futomaki Sushi Burrito",
         "cuisine":"Japanese", "description": "Sushi with tofu, avocado, cucumber & wrapped in a burrito.", "price": 9.00 },
        {"name":"Beef with Green Pepper in Black Bean Sauce",
         "cuisine":"Japanese", "description": "Prawns topped with masala & wrapped in puri bread.", "price": 7.20 },
        {"name":"Agadashi Tofu Starter",
         "cuisine":"Japanese", "description": "Tofu flash fried and served with bonito flakes, spring onions and dashi sauce.", "price": 7.70} ]
	
    feng_huang_dishes = [
		{"name": "Squid Thai Red Curry",
         "cuisine":"Thai", "description": "Squid with curry sauce made from many mixed spices, coconut oil & coconut milk.", "price": 6.50 },
        {"name":"King Prawn with Thai Sweet Chilli",
         "cuisine":"Thai", "description": " fried in a thin light batter then tossed in a sweet chilli sauce with onions, green pepper, carrots & pineapple.", "price": 7.00 },
        {"name":"Hot & Sour Soup",
         "cuisine":"Thai", "description": "Soup with hot and sour spices", "price": 3.00} ]
         
#Italian cuisines
    grillicious_mediterranean_dishes = [
		{"name": "Margherita Pizza",
         "cuisine":"Italian", "description": "Home roast tomato sauce, mozzarella cheese & fresh basil leaves, 14 inches.", "price": 7.80 },
        {"name":"Calzone",
         "cuisine":"Italian", "description": "Caramelised onions, grilled chicken, fresh basil & cheese, 10 inches.", "price": 8.00 },
        {"name":"Gamberoni Portofino",
         "cuisine":"Italian", "description": "King prawns in truffle oil, sliced shallots, peppers, fresh coriander leaves & sliced chillies served with garlic bread", "price": 6.80} ]
         
    pastaios_dishes = [
		{"name": "Pepperoni Pizza",
         "cuisine":"Italian", "description": "Tomato sauce, mozzarella & pepperoni, 12 inches.", "price": 8.50 },
        {"name":"Penne Arrabiata",
         "cuisine":"Italian", "description": "Penne pasta with spicy tomato sauce, cherry tomato & fresh parsley.", "price": 6.50 },
        {"name":"Focaccia Pomodoro",
         "cuisine":"Italian", "description": "Traditional italian bread topped with cherry tomato & fresh basil.", "price": 5.00} ]
	
    tony_macaroni_dishes = [
		{"name": "Spaghetti Carbonara",
         "cuisine":"Italian", "description": "A sauce with fresh garlic, crispy bacon, egg cream parmesan cheese sauce.", "price": 6.55 },
        {"name":"Vegetariana Pizza",
         "cuisine":"Italian", "description": " Tomato sauce, mozarella & fresh seasonal mixed vegetables.", "price": 6.80 },
        {"name":"Polpetta Scacciata Classica Burger",
         "cuisine":"Italian", "description": "Homemade chargrilled burger with grilled onion, crispy bacon, sliced tomato on a bap bun served with french fries.", "price": 6.40} ]

#Western Cuisine
    number_sixteen_dishes = [
		{"name": "Roasted beetroot",
         "cuisine":"Scottish", "description": "Golden beetroot marmalade, gorgonzola, figs, puffed buckwheat, mizuna.", "price": 7.95 },
        {"name":"Lamb belly",
         "cuisine":"Scottish", "description": " Lamb with pearl barley, green sauce, crispy shallots .", "price": 8.50 },
        {"name":"Crispy salt cod brandade",
         "cuisine":"Scottish", "description": "Cod with roast garlic and parsley sauce, caviar, samphire.", "price": 8.45} ]
	
    cote_brasserie_dishes = [
		{"name": "Spinach and Mushroom Crêpes",
         "cuisine":"French", "description": "Baked crêpes with wild mushrooms, spinach and Gruyère cheese.", "price": 10.95 },
        {"name":"Prawn Gratinée",
         "cuisine":"French", "description": "King prawns in a white wine, garlic, chilli and tomato sauce with toasted garlic and parsley croutons .", "price": 7.95 },
        {"name":"Chicken Liver Parfait",
         "cuisine":"French", "description": "Chicken liver pâté with toasted brioche and spiced apple chutney.", "price": 6.50} ]
	
    steak_and_cherry_dishes = [
		{"name": "Philly Cheese Steak Baguette",
         "cuisine":"American", "description": "Fillet steak strips with caramelized onions & cheese, with homemade chips.", "price": 9.95 },
        {"name":"Ribeye Steak",
         "cuisine":"American", "description": "Steak served with rocket, caramelized onion, balsamic cherry tomato with vine .", "price": 14.95 },
        {"name":"Oklahoma Chicken Burger",
         "cuisine":"American", "description": "Chicken burger served with salad leaves, tomato, caramelized onions & homemade chips.", "price": 9.95} ]
	
	
	
		         
    cats = {"Indian": {"Curry Pot": {"dishes": curry_pot_dishes},
                       "Indian Orchard": {"dishes": indian_orchard_dishes},
                       "Bollywood Spice": {"dishes": bollywood_spice_dishes}}, 
            "Asian":{"Station Wok": {"dishes": station_wok_dishes},
                     "Temaki": {"dishes": temaki_dishes},
                     "Feng Huang": {"dishes": feng_huang_dishes}},
            "Italian":{"Grillicious Mediterranean Dishes" : {"dishes": grillicious_mediterranean_dishes},
                       "Pastaios": {"dishes": pastaios_dishes},
                       "Tony Macaroni": {"dishes": tony_macaroni_dishes}}, 
            "Western":{"Number Sixteen": {"dishes": number_sixteen_dishes},
                       "Cote Brasserie": {"dishes": cote_brasserie_dishes},
                       "Steak and Cherry": {"dishes": steak_and_cherry_dishes}} }
   
   
    for cuisine, cat in cats.items():
        for ca,cat_data in cat.items():   
            c = add_restaurant(ca, cuisine, rating=0)
            for p in cat_data["dishes"]:
                add_dishes(c, p["name"], p["cuisine"], p["description"], p["price"])
    # Print out the categories we have added.
    for c in Restaurant.objects.all():
        for p in Dishes.objects.filter(restaurant=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_dishes(cat, name, cuisine, description, price):
    p = Dishes.objects.get_or_create(restaurant=cat, name=name)[0] 
    p.cuisine = cuisine
    p.description = description
    p.price = price
    p.save()
    return p

def add_restaurant(name, type, rating=0):
    c = Restaurant.objects.get_or_create(name=name)[0] 
    c.type = type
    c.rating = rating
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting iFood population script...") 
    populate()
