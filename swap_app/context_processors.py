import random
from .models import Image, Recipe



def categories_processor(request):
    categories = ['Breakfast', 'Salad', 'Shares', 'Pasta', 'Sandwich', 'Meat', 'Fish', 'Sauce', 'Dessert', 'Pizza']
    return {'categories': categories
    }

def image_processor(request):
    items = list(Image.objects.all())
    food_rand_imgs = random.sample(items, 3)
    return {'food_rand_imgs':food_rand_imgs}
