from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import modelform_factory
from forms import UserCreateForm
from countries.models import Country, Build, Army, Tech, Resource
from military.models import Military
from techs.models import Tech as Techs
from buildings.models import Building
from governments.models import effects
from decimal import Decimal

title = "King of the World"
css = 'kotw.css'

def home(request):
	content = """<p>Welcome to King of the World, a Massive Multiplayer Online Real-Time Strategy game you can play from anywhere.</p>
			<p>	It is the year 2015, the world is in complete chaos at the moment. Just last year the world witnessed the third great war.
			Large populations were wiped out in an instant as countries decided to use weapons of mass destruction. Six months after the
			start of the war, the waring countries decided to attempt to stop the fighting by unleashing their nuclear arsenal. Nuclear
			strikes bombarded the entire planet annhilating two-thirds of the world's population. The third world war came to an end that
			day after the end of the bombardment. For the past 6 months, survivors fought like savages to survive. Small groups formed,
			trying to rebuild civiliazation.</p>
			<p>You have been chosen to be the leader of a small group. As their leader you are to lead them to conquer the world and unite
			all the survivors under one banner to avoid another repeat of the third great war. <a href="/kotw/register/">Register</a> now and become the King of the World.</p>
			<p><a href="/kotw/login/">Login</a></p>"""
	return render_to_response('base.html', {'page_title': title, 'page_css':css, 'page_content':content})

def register(request):
	if request.method=='POST':
		form=UserCreateForm(request.POST)
		if form.is_valid():
			u=form.save()
			c=Country.objects.get(user=u)
			b=Build(country=c)
			b.save()
			a=Army(country=c)
			a.save()
			t=Tech(country=c)
			t.save()
			r=Resource(country=c)
			r.save()
			return HttpResponseRedirect('/kotw/')
	else:
		form=UserCreateForm()
	return render_to_response('form.html', {'page_title': title, 'page_css':css, 'register_form':form}, context_instance=RequestContext(request))

def signin(request):
	msg=""
	if request.method=='POST':
		form=AuthenticationForm(request.POST)
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				#redirect to a success page
				msg="login successful"
				return HttpResponseRedirect('/kotw/hq/')
			else:
				#return account has been disabled
				msg="disabled account"
		else:
			#return invalid login
			msg="invalid login"
	else:
		form=AuthenticationForm()
	return render_to_response('form.html', {'page_title': title, 'page_css':css, 'login_form':form, 'page_content':msg}, context_instance=RequestContext(request))

def signout(request):
	logout(request)
	return HttpResponseRedirect('/kotw/')

def calcArmyPower(c):	#calculate [mod_off,mod_def]
	b = Build.objects.get(country=c)
	a = Army.objects.get(country=c)
	t = Tech.objects.get(country=c)
	r = Resource.objects.get(country=c)
	turret = Military.objects.get(unit="Turrets")
	tank = Military.objects.get(unit="Tanks")
	jet = Military.objects.get(unit="Jets")
	troop = Military.objects.get(unit="Troops")
	raw_off=a.troops*troop.offense+a.jets*jet.offense+a.tanks*tank.offense
	raw_def = a.troops*troop.defense + a.jets*jet.defense + a.tanks*tank.defense + a.turrets*turret.defense
	weap_tech=(Techs.objects.get(type="Weapons").effect_val)
	armyBase_mod=Building.objects.get(type="military_base").effect_val
	build_mod=1+float((b.army/r.land)*armyBase_mod)
	gov_mod=1
	tech_mod=1+float((t.weapons/r.land)/100*weap_tech)
	if c.government=='DI':
		gov_mod=effects.objects.get(effect_name="increase military effectiveness").effect_val
	elif c.government=='T':
		tech_mod=1+(tech_mod-1)*float(effects.objects.get(effect_name="decrease technology effectiveness").effect_val)
	elif c.government=='R':
		gov_mod=effects.objects.get(effect_name="decrease military effectiveness").effect_val
	elif c.government=='DE':
		tech_mod=1+(tech_mod-1)*float(effects.objects.get(effect_name="increase technology effectiveness").effect_val)
	mod_off=raw_off*build_mod*gov_mod*tech_mod
	mod_def=raw_def*build_mod*gov_mod*tech_mod
	return [int(mod_off), int(mod_def)]

def calcModOff(c, troops, jets, tanks):
	b = Build.objects.get(country=c)
	a = Army.objects.get(country=c)
	t = Tech.objects.get(country=c)
	r = Resource.objects.get(country=c)
	tank = Military.objects.get(unit="Tanks")
	jet = Military.objects.get(unit="Jets")
	troop = Military.objects.get(unit="Troops")
	raw_off=a.troops*troop.offense+a.jets*jet.offense+a.tanks*tank.offense
	weap_tech=Techs.objects.get(type="Weapons").effect_val
	armyBase_mod=Building.objects.get(type="military_base").effect_val
	build_mod=1+float((b.army/r.land)*armyBase_mod)
	gov_mod=1
	tech_mod=1+float((t.weapons/r.land)/100*weap_tech)
	if c.government=='DI':
		gov_mod=effects.objects.get(effect_name="increase military effectiveness").effect_val
	elif c.government=='T':
		tech_mod=1+(tech_mod-1)*float(effects.objects.get(effect_name="decrease technology effectiveness").effect_val)
	elif c.government=='R':
		gov_mod=effects.objects.get(effect_name="decrease military effectiveness").effect_val
	elif c.government=='DE':
		tech_mod=1+(tech_mod-1)*float(effects.objects.get(effect_name="increase technology effectiveness").effect_val)
	mod_off=raw_off*build_mod*gov_mod*tech_mod
	return int(mod_off)

def calcNetworth(c):
	b = Build.objects.get(country=c)
	a = Army.objects.get(country=c)
	r = Resource.objects.get(country=c)
	t = Tech.objects.get(country=c)
	armyPower=calcArmyPower(c)
	nw = b.unused*20 + (b.farm+b.enterprise+b.residence+b.industry+b.army+b.labs+b.oil)*75 +r.pop+a.troops*2+a.jets*3+a.turrets*3+a.tanks*8+r.gold*1/1000+r.food*0+(t.military + t.medical+t.economics+t.residential+t.geography+t.weapons)*1/100 
	return nw

@login_required()
def main(request):
	u = request.user
	c = Country.objects.get(user=u)
	b = Build.objects.get(country=c)
	a = Army.objects.get(country=c)
	r = Resource.objects.get(country=c)
	data = {'page_title': title, 'page_css':css}
	data.update(country_name=c.name, country_user=u.username)
	data.update(country_land=r.land, country_pop=r.pop, country_money=r.gold, country_food=r.food, country_oil=r.oil)
	data.update(country_troops=a.troops, country_jets=a.jets, country_turrets=a.turrets, country_tanks=a.tanks)
	armyPower=calcArmyPower(c)
	data.update(country_offense=armyPower[0], country_defense=armyPower[1])
	revForm=modelform_factory(Country, fields=('government',))
	data.update(RevolutionForm=revForm(instance=c))
	if request.method=='POST':
		newGov=request.POST['government']
		c.government=newGov
		c.save()
		return HttpResponseRedirect('/kotw/hq/')
	return render_to_response('game.html', data, context_instance=RequestContext(request))

@login_required()
def attack(request):
	u = request.user
	c = Country.objects.get(user=u)
	b = Build.objects.get(country=c)
	a = Army.objects.get(country=c)
	r = Resource.objects.get(country=c)
	t = Tech.objects.get(country=c)
	troop = Military.objects.get(unit="Troops")
	jet = Military.objects.get(unit="Jets")
	tank = Military.objects.get(unit="Tanks")
	data = {'page_title': title, 'page_css':css}
	data.update(country_name=c.name, country_user=u.username)
	data.update(country_land=r.land, country_pop=r.pop, country_money=r.gold, country_food=r.food, country_oil=r.oil)
	data.update(country_troops=a.troops, country_jets=a.jets, country_tanks=a.tanks)
	max_troops=a.troops
	max_jets=min(a.jets, r.oil/jet.fuel)
	max_tanks=min(a.tanks, r.oil/tank.fuel)
	data.update(troops_off=troop.offense, troops_def=troop.defense, troop_fuel=troop.fuel, max_troop=max_troops)
	data.update(jets_off=jet.offense, jets_def=jet.defense, jet_fuel=jet.fuel, max_jet=max_jets)
	data.update(tanks_off=tank.offense, tanks_def=tank.defense, tank_fuel=tank.fuel, max_tank=max_tanks)
	allCountries=Country.objects.all().exclude(user=u)
	country_list=[]
	for country in allCountries:
		armyPower=calcArmyPower(country)
		country_list.append([country.user.id, country.name, armyPower[0], armyPower[1]])
	data.update(targets=country_list)
	msg=""
	if request.method=='POST':
		target=request.POST['target']
		att_type=request.POST['attack']
		armySent=request.POST.getlist('army')
		armySent=map(int,armySent)
		mod_off=calcModOff(c, armySent[0], armySent[1], armySent[2])
		target=User.objects.get(id=target)
		targetCountry=Country.objects.get(user=target)
		targetBuild=Build.objects.get(country=targetCountry)
		targetResource=Resource.objects.get(country=targetCountry)
		targetArmy=Army.objects.get(country=targetCountry)
		armyPower=calcArmyPower(targetCountry)
		mod_def=armyPower[1]
		gains = Decimal(mod_off)/Decimal(mod_def)
		if gains < 1: #failed attack, army sent is destroyed, defender loses units = 50% of attacking army
			if int(0.5*armySent[0]) < targetArmy.troops:
				targetArmy.troops=targetArmy.troops-int(0.5*armySent[0])
			else:
				targetArmy.troops=0
			if int(0.5*armySent[1]) < targetArmy.turrets: 
				targetArmy.turrets=targetArmy.turrets-int(0.5*armySent[1])
			else:
				targetArmy.turrets=0
			if int(0.5*armySent[2]) < targetArmy.tanks:
				targetArmy.tanks=targetArmy.tanks-int(0.5*armySent[2])
			else:
				targetArmy.tanks=0
			if armySent[0] < a.troops:
				a.troops=a.troops-armySent[0]
			else:
				a.troops=0
			if armySent[1] < a.jets:
				a.jets=a.jets-armySent[1]
			else:
				a.jets=0
			if armySent[2] < a.tanks:
				a.tanks=a.tanks-armySent[2]
			else:
				a.tanks=0
			targetArmy.save()
			a.save()
			msg="Your Army was Destroyed"
		else: # steal 50% of resources and destroy 10% of all buildings + steal 50% of unused land, 50% army sent is destroyed, defender loses units = 50% of attacking army
			if int(0.5*armySent[0]) < targetArmy.troops:
				targetArmy.troops=targetArmy.troops-int(0.5*armySent[0])
			else:
				targetArmy.troops=0
			if int(0.5*armySent[1]) < targetArmy.turrets: 
				targetArmy.turrets=targetArmy.turrets-int(0.5*armySent[1])
			else:
				targetArmy.turrets=0
			if int(0.5*armySent[2]) < targetArmy.tanks:
				targetArmy.tanks=targetArmy.tanks-int(0.5*armySent[2])
			else:
				targetArmy.tanks=0
			if armySent[0] < a.troops:
				a.troops=a.troops-int(0.5*armySent[0])
			else:
				a.troops=0
			if armySent[1] < a.jets:
				a.jets=a.jets-int(0.5*armySent[1])
			else:
				a.jets=0
			if armySent[2] < a.tanks:
				a.tanks=a.tanks-int(0.5*armySent[2])
			else:
				a.tanks=0
			targetArmy.save()
			a.save()

			targetBuild.farm=targetBuild.farm*0.9
			targetBuild.enterprise=targetBuild.enterprise*0.9
			targetBuild.residence=targetBuild.residence*0.9
			targetBuild.industry=targetBuild.industry*0.9
			targetBuild.army=targetBuild.army*0.9
			targetBuild.labs=targetBuild.labs*0.9
			targetBuild.oil=targetBuild.oil*0.9
			targetBuild.unused=targetResource.land-(targetBuild.farm+targetBuild.enterprise+targetBuild.residence+targetBuild.industry+targetBuild.army+targetBuild.labs+targetBuild.oil)
			targetBuild.save()

			land_lost=int(round(targetBuild.unused*0.5))
			if land_lost < targetBuild.unused:
				targetBuild.unused=targetBuild.unused-land_lost
			else:
				targetBuild.unused=0
			targetBuild.save()
			r.land=r.land+land_lost
			b.unused=b.unused+land_lost
			b.save()

			gold_lost = int(targetResource.gold*0.5)
			food_lost = int(targetResource.food*0.5)
			oil_lost = int(targetResource.oil*0.5)

			if gold_lost < targetResource.gold:
				targetResource.gold=targetResource.gold-gold_lost
			else:
				targetResource.gold=0
			if food_lost < targetResource.food:
				targetResource.food=targetResource.food-food_lost
			else:
				targetResource.food=0
			if oil_lost < targetResource.oil:
				targetResource.oil=targetResource.oil-oil_lost
			else:
				targetResource.oil=0
			r.gold=r.gold+gold_lost
			r.food=r.food+food_lost
			fuel_consume=armySent[0]*troop.fuel+armySent[1]*jet.fuel+armySent[2]*tank.fuel
			r.oil=r.oil+oil_lost-fuel_consume
			r.save()
			msg="Your army was successful in capturing land and resources"
	return render_to_response('attack.html', data, context_instance=RequestContext(request))

def ranks(request):
	rank_list = []
	country = Country.objects.all()
	for c in country:
		b = Build.objects.get(country=c)
		a = Army.objects.get(country=c)
		r = Resource.objects.get(country=c)
		t = Tech.objects.get(country=c)
		armyPower=calcArmyPower(c)
		nw = calcNetworth(c)
		rank_list.append([c.user.username, c.name, r.land, nw, armyPower[0], armyPower[1]]) # add offense and defense here
	return render_to_response('rank.html', {'page_title': title, 'page_css':css, 'rank_list': rank_list})
