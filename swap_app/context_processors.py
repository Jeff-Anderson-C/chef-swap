import random
from .models import Image



def categories_processor(request):
    categories = ['Breakfast', 'Salads', 'Shares', 'Pastas', 'Sandwiches', 'Meat/Poultry', 'Fish/Shell', 'Soup/Sauce', 'Dessert', 'Pizza', 'Sides']
    return {'categories': categories}

def image_processor(request):
    items = list(Image.objects.all())
    food_rand_imgs = random.sample(items, 3)
    return {'food_rand_imgs':food_rand_imgs}
