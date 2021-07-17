from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Recipe, Suggestion, Image, Category, TestRec, TestImg
import bcrypt
from .forms import ImageForm
import random 

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST ['first_name'],
            last_name = request.POST ['last_name'],
            email = request.POST ['email'],
            password = pw_hash,
        )
        request.session['userid'] = new_user.id 
        return redirect('/dash')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:    
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/dash')
            else:
                messages.error(request, 'Invalid password')
            return redirect('/')
        return redirect('/')

def dash(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
    }
    return render(request, 'dash.html', context)

def new_rec(request):
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user':user
    }
    return render(request, 'newRecipe.html', context)

def create_new(request):
    user = User.objects.get(id=request.session['userid'])
    rec_cat = Category.objects.get(name = request.POST ['category'])
    new_recipe = Recipe.objects.create(
        rec_name = request.POST ['rec_name'],
        prep_time = request.POST ['prep_time'],
        procedure = request.POST ['procedure'],
        ingredients = request.POST ['ingredients'],
        creator = user,
        category = rec_cat,
    )
    rec_cat.save()
    user.save()
    request.session['rec_id'] = new_recipe.id
    return redirect('/photo_up')

def rec_pic(request, rec_id):
    pass

def photo_up(request):
# """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            recipe = Recipe.objects.get(id=request.session['rec_id']) 
            this_pic = Image.objects.get(title=img_obj.title)
            this_pic.for_recipe = recipe
            user = User.objects.get(id=request.session['userid'])
            x = recipe.creator.id
            y = recipe.ingredients.split('\n')
            ing_list = [x.replace('\r',' ') for x in y]
            context = {
                'recipe': recipe,
                'user': user,
                'ing_list': ing_list,
                'form': form,
                'img_obj': img_obj,
            }
            recipe.save()
            user.save()
            this_pic.save()
            return render(request, 'addNotes.html', context)
    else:
        form = ImageForm()
    return render(request, 'recPic.html', {'form': form})

def add_notes(request):
    recipe = Recipe.objects.get(id=request.session['rec_id'])
    recipe.notes = request.POST['notes']
    recipe.save()
    m = request.session.pop('rec_id')
    return redirect('/my_recipes')


def my_recipes(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.all()
    my_recs = Recipe.objects.filter(creator=user)
    cats = Category.objects.all()
    context = {
        'recipes': recipes,
        'user': user,
        'user_recipes': my_recs.order_by('category', 'rec_name'),
        'cats':cats,
    }
    return render(request, 'myRecipes.html', context)

def all_rec(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.order_by('category', 'rec_name')
    cats = Category.objects.all()
    context = {
        'recipes':recipes,
        'cats':cats,
        'user':user,
    }
    return render(request, 'allRecipes.html', context)



def recipe(request, rec_id):
    recipe = Recipe.objects.get(id=rec_id)
    user = User.objects.get(id=request.session['userid'])
    x = recipe.creator.id
    if recipe.images.exists():
        pic = recipe.images.get()
    else:
        pic = None
    y = recipe.ingredients.split('\n')
    ing_list = [x.replace('\r',' ') for x in y]
    context = {
        'recipe': recipe,
        'user': user,
        'ing_list': ing_list,
        'pic':pic,
    }
    if x == user.id:
        return render(request, 'viewMyRec.html', context)
    else:
        return render(request, 'viewOthRec.html', context)


def edit_rec(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    context = {
        'recipe':recipe,
        'user':user,
    }
    return render(request, 'editRecipe.html', context)

def save_edit(request, rec_id):
    cat = Category.objects.filter(name=request.POST['category'])
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.rec_name = request.POST['rec_name']
    this_recipe.category = cat
    this_recipe.prep_time = request.POST['prep_time']
    this_recipe.procedure = request.POST['procedure']
    this_recipe.ingredients = request.POST['ingredients']
    this_recipe.save() 
    return redirect('/my_recipes')

def suggest(request, rec_id):
    recipe = Recipe.objects.get(id=rec_id)
    y = recipe.ingredients.split('\n')
    ing_list = [x.replace('\r',' ') for x in y]
    context = {
        'recipe':recipe,
        'ing_list': ing_list,
    }
    return render(request, 'suggRec.html', context)

def create_sugg(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    new_sugg = Suggestion.objects.create(
        rec_name = request.POST ['rec_name'],
        category = request.POST ['category'],
        prep_time = request.POST ['prep_time'],
        procedure = request.POST ['procedure'],
        ingredients = request.POST ['ingredients'],
        helper = user,
        link = recipe,
    )
    return redirect('/all_rec')

def my_suggs(request):
    user = User.objects.get(id=request.session['userid'])
    my_recs = Recipe.objects.filter(creator=user)
    context = {
        'my_recs':my_recs,
        'user':user
    }
    return render(request, 'mySuggs.html', context)

def sugg_for_me(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    sugg = Suggestion.objects.filter(link=recipe)
    this_sugg=sugg[0]
    y = recipe.ingredients.split('\n')
    ingy_list = [x.replace('\r',' ') for x in y]
    z = this_sugg.ingredients.split('\n')
    ingz_list = [x.replace('\r',' ') for x in z]
    context = {
        'recipe':recipe,
        'this_sugg':this_sugg,
        'ingy_list':ingy_list,
        'ingz_list':ingz_list,
        'user':user,
    }
    return render(request, 'suggForMyRec.html', context)

def fav_recipes(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.all()
    cats = Category.objects.all()
    print(recipes)
    context = {
        'recipes': recipes,
        'user': user,
        'fav_recipes': recipes.filter(favorite=user),
        'cats': cats,
    }
    return render(request, 'favRecipes.html', context)

def make_fav(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    user.fav_recipes.add(recipe)
    return redirect('/favRecipes')

def test_kit(request):
    user = User.objects.get(id=request.session['userid'])
    test_recs = TestRec.objects.filter(creator=user)
    context = {
        'user':user, 
        'test_recs':test_recs,
    }
    return render(request, 'testKit.html', context)
def new_test_rec(request):
    user = User.objects.get(id=request.session['userid'])
    return render(request, 'newTestRec.html')

def view_test_rec(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = TestRec.objects.get(id=rec_id)
    y = recipe.ingredients.split('\n')
    ing_list = [x.replace('\r',' ') for x in y]
    context = {
        'recipe': recipe,
        'user': user,
        'ing_list': ing_list,
    }
    return render(request, 'viewMyTestRec.html', context)

def save_test_rec(request):
    user = User.objects.get(id=request.session['userid'])
    rec_cat = Category.objects.get(name = request.POST ['category'])
    new_recipe = TestRec.objects.create(
        rec_name = request.POST ['rec_name'],
        prep_time = request.POST ['prep_time'],
        procedure = request.POST ['procedure'],
        ingredients = request.POST ['ingredients'],
        notes = request.POST ['notes'],
        creator = user,
        category = rec_cat,
    )
    rec_cat.save()
    user.save()
    request.session['rec_id'] = new_recipe.id
    return redirect('/test_kit')

def save_test_rec_edit(request, rec_id):
    cat = Category.objects.get(name=request.POST['category'])
    this_recipe = TestRec.objects.get(id=rec_id)
    this_recipe.rec_name = request.POST['rec_name']
    this_recipe.category.name = request.POST['category']
    this_recipe.prep_time = request.POST['prep_time']
    this_recipe.procedure = request.POST['procedure']
    this_recipe.ingredients = request.POST['ingredients']
    this_recipe.notes = request.POST['notes']
    this_recipe.save() 
    this_recipe.category.save()
    return redirect('/test_kit')

def test_photo_up(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            recipe = TestRec.objects.get(id=request.session['rec_id']) 
            this_pic = TestImg.objects.get(title=img_obj.title)
            this_pic.for_recipe = recipe
            user = User.objects.get(id=request.session['userid'])
            recipe.save()
            user.save()
            this_pic.save()
            return render(request, 'testKit.html', context)
    else:
        form = ImageForm()
    return render(request, 'recPicTest.html', {'form': form})

def search_recipes(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        user = User.objects.get(id=request.session['userid'])
        recipes = Recipe.objects.filter(rec_name__contains=searched)
        return render(request, 'searchResult.html', {'searched':searched, 'recipes':recipes, 'user':user})
    else:
        return render(request, 'searchResult.html', {})

def remove_rec(request, rec_id):
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.delete()
    return redirect('/my_recipes')

def delete_sugg(request, sugg_id):
    sugg = Suggestion.objects.get(id=sugg_id)
    sugg.delete()
    return redirect('/my_suggs')


def logout(request):
    request.session.clear()
    return redirect('/')



def knife_roll(request):
    return render(request, 'knifeRoll.html')