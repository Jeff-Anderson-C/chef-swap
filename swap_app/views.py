from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Recipe, Suggestion, Image, Category, TestRec, Post, Group, Invite
import bcrypt
from .forms import ImageForm, ContactForm
import random 
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def index(request):
    return render(request, 'intro.html')

def log_reg(request):
    return render(request, 'log_reg.html')

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

# Recipes

def new_rec(request):
    user = User.objects.get(id=request.session['userid'])
    cats = Category.objects.all()
    groups = Group.objects.filter(member=user)
    context = {
        'user':user, 
        'cats':cats,
        'groups':groups,
    }
    return render(request, 'newRecipe.html', context)

def create_new(request):
    user = User.objects.get(id=request.session['userid'])
    rec_cat = Category.objects.get(name = request.POST ['category'])
    rec_group = Group.objects.get(name = request.POST ['group_rec'])
    new_recipe = Recipe.objects.create(
        rec_name = request.POST ['rec_name'],
        prep_time = request.POST ['prep_time'],
        procedure = request.POST ['procedure'],
        ingredients = request.POST ['ingredients'],
        notes = request.POST ['notes'],
        creator = user,
        category = rec_cat, 
        group_rec = rec_group,
    )
    request.session['rec_id'] = new_recipe.id
    return redirect('/my_recipes')

def change_pic(request, rec_id):
    user = User.objects.get(id= request.session ['userid'])
    recipe = Recipe.objects.get(id=rec_id)
    x=recipe.images.all()
    x.delete()
    request.session['rec_id'] = recipe.id
    return redirect('/photo_up')

def photo_up(request):
    user = User.objects.get(id=request.session ['userid'])
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            img_obj = form.instance
            recipe = Recipe.objects.get(id=request.session['rec_id']) 
            this_pic = Image.objects.get(pk=img_obj.pk)
            this_pic.for_recipe = recipe
            user = User.objects.get(id=request.session['userid'])
            user.save()
            this_pic.save()
            m = request.session.pop('rec_id')
            return redirect('/my_recipes')
    else:
        form = ImageForm()
    return render(request, 'recPic.html', {'form': form, 'user': user})

def my_recipes(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.all()
    my_recs = Recipe.objects.filter(creator=user)
    cats = Category.objects.all()
    groups = Group.objects.filter(member=user).exclude(name='All Recipes')
    member_list = []
    for group in groups:
        for member in group.member.all().exclude(id=user.id):
            if member not in member_list:
                member_list.append(member)    
    context = {
        'recipes': recipes,
        'user': user,
        'user_recipes': my_recs.order_by('category', 'rec_name'),
        'cats':cats,
        'groups':groups,
        'member_list':member_list,
    }
    return render(request, 'myRecipes.html', context)

def all_rec(request):
    user = User.objects.get(id=request.session['userid'])
    allrec = Group.objects.get(name='All Recipes')
    recipes = Recipe.objects.filter(group_rec=allrec).order_by('category', 'rec_name')
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
    groups = Group.objects.filter(member=user)
    recipe = Recipe.objects.get(id=rec_id)
    context = {
        'recipe':recipe,
        'user':user,
        'groups':groups,
    }
    return render(request, 'editRecipe.html', context)

def save_edit(request, rec_id):
    cat = Category.objects.get(name=request.POST['category'])
    rec_group = Group.objects.get(name = request.POST ['group_rec'])
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.rec_name = request.POST['rec_name']
    this_recipe.category = cat
    this_recipe.prep_time = request.POST['prep_time']
    this_recipe.procedure = request.POST['procedure']
    this_recipe.ingredients = request.POST['ingredients']
    this_recipe.notes = request.POST['notes']
    rec_group.group_recs.add(this_recipe)
    rec_group.save()
    this_recipe.save() 
    return redirect('/my_recipes')


# Suggestions


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

def delete_sugg(request, sugg_id):
    sugg = Suggestion.objects.get(id=sugg_id)
    sugg.delete()
    return redirect('/my_suggs')


# Favorite Recipes


def fav_recipes(request):
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipe.objects.all()
    cats = Category.objects.all()
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
    return redirect('/fav_recipes')

def group_recs(request):
    user = User.objects.get(id=request.session ['userid'])
    groups = Group.objects.filter(member=user).exclude(name="All Recipes")
    return render(request, 'groupRecs.html', {'groups':groups, 'user':user})

def search_recipes(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        user = User.objects.get(id=request.session['userid'])
        recipes = Recipe.objects.filter(rec_name__contains=searched).filter(group_rec=2)
        my_recipes = Recipe.objects.filter(rec_name__contains=searched).filter(creator=user)
        context = {
            'searched':searched,
            'recipes':recipes,
            'user':user,
            'my_recipes':my_recipes
        }
        return render(request, 'searchRecRes.html', context)
    else:
        return render(request, 'searchRecRes.html')

def remove_rec(request, rec_id):
    this_recipe = Recipe.objects.get(id=rec_id)
    this_recipe.delete()
    return redirect('/my_recipes')


# Test Kitchen


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
    return redirect('/test_kit')

def save_test_rec_edit(request, rec_id):
    cat = Category.objects.get(name=request.POST['category'])
    this_recipe = TestRec.objects.get(id=rec_id)
    this_recipe.rec_name = request.POST['rec_name']
    this_recipe.category = cat
    this_recipe.prep_time = request.POST['prep_time']
    this_recipe.procedure = request.POST['procedure']
    this_recipe.ingredients = request.POST['ingredients']
    this_recipe.notes = request.POST['notes']
    this_recipe.save()
    return redirect('/test_kit')

def save_to_main(request, test_id):
    test_rec = TestRec.objects.get(id=test_id)
    all_rec = Group.objects.get(name='All Recipes')
    new_rec = Recipe.objects.create(
        rec_name = test_rec.rec_name,
        category = test_rec.category,
        prep_time = test_rec.prep_time,
        procedure = test_rec.procedure,
        ingredients = test_rec.ingredients, 
        creator = test_rec.creator,
        notes = test_rec.notes,
        group_rec = all_rec
    )
    test_rec.delete()
    return redirect('/my_recipes')


# Knife roll/Profile


def prof_dash(request):
    user = User.objects.get(id=request.session['userid'])
    posts = Post.objects.filter(poster=request.session['userid']).order_by('-created_at')
    groups = Group.objects.filter(member=user).exclude(name='All Recipes')
    member_list = []
    for group in groups:
        for member in group.member.all().exclude(id=user.id):
            if member not in member_list:
                member_list.append(member)            
    if user.profile_pics.exists():
        prof_pic = user.profile_pics.last()
    else:
        prof_pic = None
    context = {
        'user':user,
        'prof_pic':prof_pic,
        'posts':posts,
        'member_list':member_list,
        'groups':groups,
    }
    return render(request, 'profDash.html', context)

def my_profile(request):
    user = User.objects.get(id = request.session ['userid'])
    context = {
        'user':user
    }
    return render(request, 'myProfile.html', context)

def profile_edit_save(request):
    user = User.objects.get(id = request.session ['userid'])
    user.first_name = request.POST ['first_name']
    user.last_name = request.POST ['last_name']
    # user.email = request.POST ['email']
    user.save()
    return redirect('/my_profile')

def pr_photo_up(request):
    user = User.objects.get(id = request.session ['userid'])
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            img_obj = form.instance
            user = User.objects.get(id = request.session ['userid'])
            this_pic = Image.objects.get(title=img_obj.title)
            this_pic.profile_pic = user
            user.save()
            this_pic.save()
            return redirect('/prof_dash')
    else:
        form = ImageForm()
    return render(request, 'profPic.html', {'form': form, 'user': user})

def other_prof(request, chef_id):
    user = User.objects.get(id=chef_id)
    posts = Post.objects.filter(poster=chef_id).order_by('-created_at')
    groups = Group.objects.filter(member=user).exclude(name='All Recipes').exclude(active_group='off')
    member_list = []
    for group in groups:
        for member in group.member.all().exclude(id=user.id):
            if member not in member_list:
                member_list.append(member)            
    if user.profile_pics.exists():
        prof_pic = user.profile_pics.last()
    else:
        prof_pic = None
    context = {
        'user':user,
        'prof_pic':prof_pic,
        'posts':posts,
        'member_list':member_list,
        'groups':groups,
    }
    
    return render(request, 'otherProf.html', context)

# def messages(request):
#     return render(request, 'message.html')

def roll_manage(request):
    return render(request, 'knifeRoll.html')

def kr_photo_up(request):
    user = User.objects.get(id=request.session ['userid'])
    # if user.kn_ro_pics:
    images = Image.objects.filter(knife_roll_pic = user)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            this_pic = img_obj
            print(this_pic)
            user = User.objects.get(id = request.session ['userid'])
            this_pic.knife_roll_pic = user
            this_pic.save()
            return render(request, 'knifeRoll.html', {'form':form, 'img_obj':img_obj, 'images':images, 'user':user})
    else:
        form = ImageForm()
    return render(request, 'knifeRoll.html', {'form': form, 'images':images, 'user':user})

def view_image(request, img_id):
    image = Image.objects.get(id=img_id)
    user = User.objects.get(id=request.session ['userid'])
    return render(request, 'imageView.html', {'image':image, 'user':user})

def destroy_image(request, img_id):
    destroy = Image.objects.get(id=img_id)
    destroy.delete()
    return redirect('/kr_photo_up')




def add_post(request):
    user = User.objects.get(id=request.session ['userid'])
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            user = User.objects.get(id = request.session ['userid'])
            if img_obj.id:
                request.session['imageid'] = img_obj.id
                return render(request, 'addPost.html', {'form':form, 'img_obj':img_obj, 'user':user})
            else:
                return render(request, 'addPost.html', {'form': form, 'user':user})

    else:
        form = ImageForm()
    return render(request, 'addPost.html', {'form': form, 'user':user})

def add_text_post(request):
    user = User.objects.get(id=request.session ['userid'])
    return render(request, 'addPost.html', {'user':user})

def post_content(request):
    user = User.objects.get(id=request.session ['userid'])
    # this_image = Image.objects.get(id=request.session ['imageid'])
    this_post = Post.objects.create (
        post_title = request.POST ['title'],
        content = request.POST ['content'],
        # post_image = this_image,
        poster = user,
    )
    # key_pop = request.session.pop ('imageid')
    return redirect('/prof_dash')

def destroy_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(id=request.session ['userid'])
    if post.poster == user:
        destroy = Post.objects.get(pk=post_id)
        destroy.delete()
        return redirect('/prof_dash')
    else:
        return redirect('/dash')

def destroy_acct(request, user_id):
    user = User.objects.get (id=request.session ['userid'])
    if user.id == user_id:
        user.delete()
        return redirect('/')
    else:
        return redirect('/')


# Groups

def groups(request):
    user = User.objects.get(id=request.session ['userid'])
    owned_groups = Group.objects.filter(creator=user)
    join_reqs=[]
    for group in owned_groups:
        if group.requests.all():
            x=group.requests.all()
            for req in x:
                join_reqs.append(req)
    groups = Group.objects.filter(member=user).exclude(name='All Recipes').exclude(active_group='off')
    context = {
        'user':user,
        'groups':groups,
        'join_reqs':join_reqs
    }
    return render(request, 'groups.html', context)

def create_group(request):
    user = User.objects.get(id=request.session ['userid'])
    new_group = Group.objects.create (
    name = request.POST ['group_name'],
    desc = request.POST ['desc'],
    active_group = request.POST ['true_switch'],
    creator = user, 
    )
    new_group.member.add(user)
    if request.POST ['admin']:
        ad_user = User.objects.get(email = request.POST ['admin'])
        new_group.gr_admin.set(ad_user)
    return redirect('/groups')

def view_group(request, group_id):
    user = User.objects.get(id=request.session ['userid'])
    group = Group.objects.get(id=group_id)
    return render(request, 'viewGroup.html', {'group':group, 'user':user})

def group_edit(request, group_id):
    pass

def join_request(request, group_id):
    user = User.objects.get(id=request.session ['userid'])
    group = Group.objects.get(id=group_id)
    if group.member.filter(id=user.id):
        return redirect('/prof_dash')
    new_join = Invite.objects.create (
        sender = user,
        for_group = group, 
        msg_txt = request.POST ['msg_txt']
    )
    return redirect('/prof_dash')

def accept_member(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    group = invite.for_group
    new_member = invite.sender
    group.member.add(new_member)
    invite.delete()
    group.save()
    return redirect ('/groups')

def reject_member(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.delete()
    return redirect ('/groups')

def search_chefs(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        user = User.objects.get(id=request.session['userid'])
        chefs = User.objects.filter(first_name__contains=searched)
        return render(request, 'searchChefRes.html', {'searched':searched, 'user':user, 'chefs':chefs})
    else:
        return render(request, 'searchChefRes.html', {})



def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("/dash")

	form = ContactForm()
	return render(request, "contact.html", {'form':form})

def terms_conditions(request):
    return render(request, 'termsAndConditions.html')

def privacy_policy(request):
    return render(request, 'privacyPolicy.html')

def logout(request):
    request.session.clear()
    return redirect('/')



