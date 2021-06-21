from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Recipe, Suggestion
import bcrypt

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
    new_recipe = Recipe.objects.create(
        rec_name = request.POST ['rec_name'],
        category = request.POST ['category'],
        prep_time = request.POST ['prep_time'],
        procedure = request.POST ['procedure'],
        ingredients = request.POST ['ingredients'],
        creator = user,
    )
    return redirect('/myRecipes')


def myRecipes(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
        'user': user,
        'user_recipes': Recipe.objects.filter(creator=user),
    }
    return render(request, 'myRecipes.html', context)

def all_rec(request):
    recipes = Recipe.objects.order_by('category', 'rec_name')
    context = {
        'recipes':recipes
    }
    return render(request, 'allRecipes.html', context)



def recipe(request, rec_id):
    recipe = Recipe.objects.get(id=rec_id)
    user = User.objects.get(id=request.session['userid'])
    x = recipe.creator.id
    y = recipe.ingredients.split('\n')
    ing_list = [x.replace('\r',' ') for x in y]
    context = {
        'recipe': recipe,
        'user': user,
        'ing_list': ing_list,
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
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.rec_name = request.POST['rec_name']
    this_recipe.category = request.POST['category']
    this_recipe.prep_time = request.POST['prep_time']
    this_recipe.procedure = request.POST['procedure']
    this_recipe.ingredients = request.POST['ingredients']
    this_recipe.save() 
    return redirect('/myRecipes')

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
    context = {
        'recipes': recipes,
        'user': user,
        'fav_recipes': Recipe.objects.filter(favorite=user),
    }
    return render(request, 'favRecipes.html', context)

def make_fav(request, rec_id):
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    user.fav_recipes.add(recipe)
    return redirect('/favRecipes')


def remove_rec(request, rec_id):
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.delete()
    return redirect('/myRecipes')

def delete_sugg(request, sugg_id):
    sugg = Suggestion.objects.get(id=sugg_id)
    sugg.delete()
    return redirect('/my_suggs')


def logout(request):
    request.session.clear()
    return redirect('/')

def test_kit(request):
    return render(request, 'testKit.html')

def knife_roll(request):
    return render(request, 'knifeRoll.html')