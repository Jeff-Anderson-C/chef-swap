import random
from .models import Image, Recipe, User



def categories_processor(request):
    categories = ['Breakfast', 'Salad', 'Shares', 'Pasta', 'Sandwich', 'Meat', 'Fish', 'Sauce', 'Dessert', 'Pizza']
    return {'categories': categories
    }

def image_processor(request):
    items = list(Image.objects.filter(for_recipe__pk__isnull=False))
    food_rand_imgs = random.sample(items, 0)
    return {'food_rand_imgs':food_rand_imgs}
